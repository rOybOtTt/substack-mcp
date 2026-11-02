"""Export the demo-week and paper-trading results as JSON row files for the tracker dashboard.

    python -m tagym.dashboard [--mode auto|preopen|midday|preclose|close] [--no-prices]

Writes ta-rulebook/demo/dashboard/{equity,book,trades,journal,activity,flips}.json (arrays of row
objects) and appends one mark-to-market row per run to demo/marks.csv, so the dashboard's equity
curve has a point for every scheduled run (pre-open, mid-day, pre-close, after close).
Nothing here trades or changes the demo state; it only reads it (and prices, via yfinance).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pandas as pd

from . import demo as d
from .paper import JOURNAL, PAPER, fetch

OUT = d.DEMO / "dashboard"
MARKS = d.DEMO / "marks.csv"
ACTIVITY_ROWS = 400


def _clean(v):
    if v is None:
        return None
    if isinstance(v, float) and not math.isfinite(v):
        return None
    if hasattr(v, "item"):  # numpy scalar
        v = v.item()
        if isinstance(v, float) and not math.isfinite(v):
            return None
    return v


def _rows(df, cols=None):
    if df is None or not len(df):
        return []
    if cols:
        df = df.reindex(columns=cols)
    return [{k: _clean(v) for k, v in r.items()} for r in df.to_dict("records")]


def _read(path):
    return pd.read_csv(path) if Path(path).exists() and Path(path).stat().st_size else pd.DataFrame()


def last_prices(tickers):
    if not tickers:
        return {}
    bars = fetch(sorted(set(tickers)), period="5d")
    return {t: float(df.c.iloc[-1]) for t, df in bars.items() if len(df)}


def mark(s, prices, mode, when):
    """Mark the book to market now and append it to marks.csv (one row per run; a re-run replaces it)."""
    invested = sum(p["shares"] * prices.get(p["ticker"], p["entry_price"]) for p in s["positions"].values())
    equity = s["cash"] + invested
    base = s.get("spy_base")
    spy_eq = s["initial_capital"] * prices["SPY"] / base["open"] if base and "SPY" in prices else s["initial_capital"]
    row = {"time_ny": str(when)[:19], "date": str(when.date()), "mode": mode, "broker": s.get("broker", "simulated"),
           "equity": round(equity, 2), "spy_benchmark": round(spy_eq, 2), "cash": round(s["cash"], 2),
           "invested": round(invested, 2), "positions": len(s["positions"]), "pending_orders": len(s["pending"])}
    m = _read(MARKS)
    if not len(m):  # seed with the official daily closes recorded before the first mark
        eq = _read(d.EQUITY)
        m = pd.DataFrame([{"time_ny": f"{e.date} 16:00:00", "date": e.date, "mode": "close", "broker": "simulated",
                           "equity": e.equity, "spy_benchmark": e.spy_benchmark, "cash": e.cash,
                           "invested": round(e.equity - e.cash, 2), "positions": int(e.positions),
                           "pending_orders": int(e.pending_orders)} for e in eq.itertuples()])
    if len(m):
        m = m[~((m.date.astype(str) == row["date"]) & (m["mode"] == mode))]
    m = pd.concat([m, pd.DataFrame([row])], ignore_index=True).sort_values("time_ny")
    d.DEMO.mkdir(exist_ok=True)
    m.to_csv(MARKS, index=False)
    return m


def book_rows(s, prices, trades):
    buy_reason = {}
    if len(trades):
        for t in trades[trades.side == "BUY"].itertuples():
            buy_reason[t.symbol] = (t.rule, t.reason)
    rows = []
    for sym, p in sorted(s["positions"].items()):
        last = prices.get(p["ticker"])
        rule, reason = buy_reason.get(sym, ("D3", ""))
        rows.append({"symbol": sym, "status": "Held", "shares": p["shares"], "entry_date": p["entry_date"],
                     "entry_price": round(p["entry_price"], 2), "last": round(last, 2) if last else None,
                     "stop": round(p["stop"], 2),
                     "value": round(p["shares"] * last, 2) if last else None,
                     "pnl": round(p["shares"] * (last - p["entry_price"]), 2) if last else None,
                     "pnl_pct": round((last / p["entry_price"] - 1) * 100, 2) if last else None,
                     "to_stop_pct": round((last / p["stop"] - 1) * 100, 2) if last else None,
                     "rule": rule, "reason": reason + (" · trimmed" if p.get("trimmed") else "")})
    for o in s["pending"]:
        last = prices.get(o["ticker"])
        status = ("Trim at next open" if o.get("trim") else "Sell at next open") if o["side"] == "SELL" else "Buy at next open"
        if o.get("broker_id"):
            status += " (sent to Alpaca)"
        stop = o.get("stop")
        rows.append({"symbol": o["symbol"], "status": status, "shares": o["shares"], "entry_date": None,
                     "entry_price": None, "last": round(last, 2) if last else None,
                     "stop": round(stop, 2) if stop else None,
                     "value": round(o["shares"] * last, 2) if last else None, "pnl": None, "pnl_pct": None,
                     "to_stop_pct": round((last / stop - 1) * 100, 2) if last and stop else None,
                     "rule": o["rule"], "reason": o["reason"]})
    return rows


def journal_rows():
    j = _read(PAPER / "scored.csv")
    if not len(j):
        j = _read(JOURNAL)
    cols = ["as_of", "symbol", "sector", "signal", "row", "regime", "health", "timing", "risk_flag",
            "p_dd20_60d_est", "p_drop10_10d_est", "earnings_due_10d", "close", "mdd10", "mdd60", "exc20"]
    if len(j):
        j["earnings_due_10d"] = j.earnings_due_10d.astype(str).str.lower().eq("true")
        j["as_of"] = j.as_of.astype(str)
    return _rows(j, cols)


def export(mode=None, prices=True, when=None):
    when = when or d.ny_now()
    mode = mode or d.auto_mode(when)
    s = d.load_state()
    trades = _read(d.TRADES)
    tick = [p["ticker"] for p in s["positions"].values()] + [o["ticker"] for o in s["pending"]] + ["SPY"]
    px = last_prices(tick) if prices else {}
    m = mark(s, px, mode, when)
    OUT.mkdir(parents=True, exist_ok=True)
    tr = trades.reset_index(drop=True)
    if len(tr):
        tr.insert(0, "fill", range(1, len(tr) + 1))
    lg = _read(d.LOG)
    if len(lg):
        lg = lg.reset_index(drop=True)
        lg.insert(0, "n", range(1, len(lg) + 1))
        lg = lg.iloc[::-1].head(ACTIVITY_ROWS)
    fl = _read(d.FLIPS)
    files = {
        "equity": _rows(m, ["time_ny", "date", "mode", "broker", "equity", "spy_benchmark", "cash", "invested",
                            "positions", "pending_orders"]),
        "book": book_rows(s, px, trades),
        "trades": _rows(tr, ["fill", "date", "symbol", "side", "shares", "price", "value", "rule", "reason",
                             "pnl", "gap_pct", "slippage_bps_vs_open"]) if len(tr) else [],
        "journal": journal_rows(),
        "activity": _rows(lg, ["n", "time_ny", "mode", "symbol", "action", "rule", "detail"]),
        "flips": _rows(fl, ["date", "mode", "symbol", "partial_signal", "final_signal"]),
    }
    for name, rows in files.items():
        (OUT / f"{name}.json").write_text(json.dumps(rows, allow_nan=False, default=str))
    print(f"dashboard export ({mode} @ {str(when)[:16]} NY): "
          + ", ".join(f"{k} {len(v)}" for k, v in files.items()) + f" -> {OUT}")
    return files


if __name__ == "__main__":
    a = sys.argv[1:]
    md = next((a[i + 1] for i, x in enumerate(a) if x == "--mode"), "auto")
    export(None if md == "auto" else md, prices="--no-prices" not in a)
