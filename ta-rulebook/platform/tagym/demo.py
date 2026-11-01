"""Demo week: a simulated $100k long-only portfolio run mechanically by the rulebook.

    python -m tagym.demo auto        # picks the mode from the current New York time
    python -m tagym.demo preopen|midday|preclose|close [--earnings ../paper/next_earnings.json]

Rules (fixed before the week starts; RULEBOOK v2.2):
  * Universe: paper/watchlist.csv (98 S&P 500 names). Benchmark: SPY bought at the first open.
  * Entry: verdict BULLISH (D3: healthy + RISK_ON + not extended), no earnings within 10 trading
    days (E1), not already held. Ranked: PULLBACK timing first, then 6-month RS vs SPY.
  * Size: risk 0.5% of equity per position with a stop 2.5 x ATR14 below entry; max 8% of equity
    per position; max 15 positions; never more than available cash.
  * Orders are decided on COMPLETED daily bars (after-close run) and filled at the NEXT open
    (market-on-open), 10 bps cost per side.
  * Exits: initial stop (resting order: fills at the stop, or at the open if it gaps through);
    verdict turns BEARISH -> sell all at next open; earnings within 2 trading days -> sell half
    at next open (RULEBOOK section 8, rule 5).
  * Mid-day and pre-close runs never trade on signals. They record what the rule would say on the
    unfinished bar, and the after-close run compares those reads with the final verdict.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from .live import classify, atr as _atr, trading_days_until, RULEBOOK_VERSION
from .paper import fetch, watchlist, _completed

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "demo"
STATE = DEMO / "state.json"
TRADES = DEMO / "trades.csv"
EQUITY = DEMO / "equity.csv"
FLIPS = DEMO / "flips.csv"
LOG = DEMO / "decision_log.csv"
REPORT = DEMO / "DEMO_REPORT.md"
COST = 0.001
RISK_PER_POS = 0.005
STOP_ATR = 2.5
MAX_POS_PCT = 0.08
MAX_POSITIONS = 15
WEEK = ("2026-11-02", "2026-11-06")


def ny_now():
    return pd.Timestamp.now(tz="America/New_York")


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"initial_capital": 100000.0, "cash": 100000.0, "positions": {}, "pending": [],
            "spy_base": None, "week": list(WEEK), "rulebook_version": RULEBOOK_VERSION}


def save_state(s):
    DEMO.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(s, indent=1, default=str))


def append(path, rows):
    if not rows:
        return
    DEMO.mkdir(exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(path, mode="a", header=not path.exists(), index=False)


def log(rows, mode, when, symbol, action, rule, detail):
    rows.append({"time_ny": when, "mode": mode, "symbol": symbol, "action": action, "rule": rule, "detail": detail})


def today_bar(df, day):
    return df.loc[df.index.normalize() == day] if df is not None else None


# ------------------------------------------------------------------ fills & stops
def process_fills_and_stops(s, bars, mode, when, logs, full_day=False):
    """Fill pending market-on-open orders at today's open, then check resting stops against
    today's low so far (full day in the after-close run)."""
    trades = []
    day = when.tz_localize(None).normalize()
    keep = []
    for o in s["pending"]:
        df = bars.get(o["ticker"])
        tb = today_bar(df, day)
        if tb is None or tb.empty or pd.Timestamp(o["created"]) >= day:
            keep.append(o)
            continue
        px = float(tb.o.iloc[0])
        if o["side"] == "BUY":
            cost_ps = px * (1 + COST)
            shares = int(min(o["shares"], s["cash"] // cost_ps))
            if shares <= 0:
                log(logs, mode, when, o["symbol"], "BUY_SKIPPED", "cash", "no cash at fill")
                continue
            s["cash"] -= shares * cost_ps
            s["positions"][o["symbol"]] = {"ticker": o["ticker"], "shares": shares, "entry_date": str(day.date()),
                                           "entry_price": px, "stop": o["stop"], "atr_at_entry": o["atr"],
                                           "trimmed": False}
            trades.append({"date": str(day.date()), "symbol": o["symbol"], "side": "BUY", "shares": shares, "price": px,
                           "value": shares * px, "rule": o["rule"], "reason": o["reason"],
                           "prev_close": o.get("ref_close"), "gap_pct": (px / o["ref_close"] - 1) * 100 if o.get("ref_close") else None})
        else:
            p = s["positions"].get(o["symbol"])
            if not p:
                continue
            shares = min(o["shares"], p["shares"])
            s["cash"] += shares * px * (1 - COST)
            p["shares"] -= shares
            if o.get("trim"):
                p["trimmed"] = True
            trades.append({"date": str(day.date()), "symbol": o["symbol"], "side": "SELL", "shares": shares, "price": px,
                           "value": shares * px, "rule": o["rule"], "reason": o["reason"],
                           "pnl": shares * (px - p["entry_price"]), "prev_close": o.get("ref_close"),
                           "gap_pct": (px / o["ref_close"] - 1) * 100 if o.get("ref_close") else None})
            if p["shares"] <= 0:
                del s["positions"][o["symbol"]]
    s["pending"] = keep
    # resting stops
    if s.get("spy_base") is None and bars.get("SPY") is not None and str(day.date()) >= WEEK[0]:
        tb = today_bar(bars["SPY"], day)
        if tb is not None and not tb.empty:  # benchmark = SPY bought at the week's first open
            s["spy_base"] = {"date": str(day.date()), "open": float(tb.o.iloc[0])}
    for sym, p in list(s["positions"].items()):
        tb = today_bar(bars.get(p["ticker"]), day)
        if tb is None or tb.empty or p["entry_date"] > str(day.date()):
            continue
        lo, op = float(tb.l.iloc[0]), float(tb.o.iloc[0])
        if lo <= p["stop"]:
            px = min(op, p["stop"])  # a sell-stop fills at the stop, or at the open if the open is already below it
            s["cash"] += p["shares"] * px * (1 - COST)
            trades.append({"date": str(day.date()), "symbol": sym, "side": "SELL", "shares": p["shares"], "price": px,
                           "value": p["shares"] * px, "rule": "STOP", "reason": f"low {lo:.2f} <= stop {p['stop']:.2f}"
                           + (" (gapped through at open)" if px == op else ""),
                           "pnl": p["shares"] * (px - p["entry_price"])})
            log(logs, mode, when, sym, "STOP_FILLED", "§8.1 stop", f"{p['shares']} @ {px:.2f}")
            del s["positions"][sym]
    append(TRADES, trades)
    for t in trades:
        log(logs, mode, when, t["symbol"], f"FILL_{t['side']}", t["rule"], f"{t['shares']} @ {t['price']:.2f}")
    return trades


# ------------------------------------------------------------------ verdicts
def verdicts(bars, earn, partial):
    spy = bars["SPY"] if partial else _completed(bars["SPY"])
    out = {}
    for _, w in watchlist().iterrows():
        df = bars.get(w.ticker)
        if df is None or len(df) < 50:
            continue
        if not partial:
            df = _completed(df)
        df = df.loc[:spy.index[-1]]
        out[w.symbol_tv] = (w.ticker, classify(df, spy, w.symbol_tv, next_earnings=earn.get(w.symbol_tv)), df)
    return out


def mode_preopen(s, bars, earn, when, logs):
    day = when.tz_localize(None).normalize()
    for sym, p in s["positions"].items():
        nd = earn.get(sym)
        if nd and pd.Timestamp(nd) <= day:
            log(logs, "preopen", when, sym, "RISK_NOTE", "§8.5 earnings", f"earnings reported {nd}; gap risk at open")
        log(logs, "preopen", when, sym, "HOLD_CHECK", "§8.1", f"stop {p['stop']:.2f}")
    for o in s["pending"]:
        nd = earn.get(o["symbol"])
        if o["side"] == "BUY" and nd and trading_days_until(str((day - pd.Timedelta(days=1)).date()), nd) is not None \
                and trading_days_until(str((day - pd.Timedelta(days=1)).date()), nd) <= 1:
            o["cancel"] = True
            log(logs, "preopen", when, o["symbol"], "CANCEL_BUY", "E1", f"earnings {nd}")
    s["pending"] = [o for o in s["pending"] if not o.get("cancel")]
    log(logs, "preopen", when, "-", "SUMMARY", "-", f"{len(s['pending'])} orders queued for the open, {len(s['positions'])} positions")


def record_flips(bars, earn, mode, when):
    v = verdicts(bars, earn, partial=True)
    day = str(when.tz_localize(None).normalize().date())
    rows = [{"date": day, "mode": mode, "time_ny": str(when)[:19], "symbol": k, "partial_signal": x[1].get("signal"),
             "partial_row": x[1].get("decision_row")} for k, x in v.items()
            if str(x[2].index[-1].date()) == day]  # only if today's unfinished bar is really in the data
    append(FLIPS, rows)
    return len(rows)


def mode_close(s, bars, earn, when, logs):
    v = verdicts(bars, earn, partial=False)
    if not v:
        return
    as_of = max(str(x[2].index[-1].date()) for x in v.values())
    held = set(s["positions"])
    pending_syms = {o["symbol"] for o in s["pending"]}
    # exits
    for sym in held:
        p = s["positions"][sym]
        tk, vv, df = v.get(sym, (p["ticker"], None, None))
        if vv is None:
            continue
        ref = float(df.c.iloc[-1])
        if vv["signal"] == "BEARISH" and sym not in pending_syms:
            s["pending"].append({"symbol": sym, "ticker": tk, "side": "SELL", "shares": p["shares"], "created": as_of,
                                 "rule": "D2", "reason": "verdict turned BEARISH", "ref_close": ref})
            log(logs, "close", when, sym, "QUEUE_SELL", "D2", "BEARISH -> sell all at next open")
        nd = earn.get(sym)
        dte = trading_days_until(as_of, nd)
        if dte is not None and dte <= 2 and not p["trimmed"] and sym not in pending_syms and vv["signal"] != "BEARISH":
            s["pending"].append({"symbol": sym, "ticker": tk, "side": "SELL", "shares": p["shares"] // 2, "created": as_of,
                                 "rule": "§8.5", "reason": f"earnings {nd} within 2 trading days: trim half",
                                 "trim": True, "ref_close": ref})
            log(logs, "close", when, sym, "QUEUE_TRIM", "§8.5", f"earnings {nd}")
    # mark to market
    mv = sum(p["shares"] * float(v[sym][2].c.iloc[-1]) for sym, p in s["positions"].items() if sym in v)
    equity = s["cash"] + mv
    # entries
    cands = []
    for sym, (tk, vv, df) in v.items():
        if vv.get("signal") != "BULLISH" or sym in s["positions"] or sym in pending_syms:
            continue
        if vv["risk"].get("earnings_in_next_10d"):
            log(logs, "close", when, sym, "SKIP_ENTRY", "E1", "BULLISH but earnings within 10 trading days")
            continue
        a = float(_atr(df, 14).iloc[-1])
        cands.append((vv["layers"]["timing"] == "PULLBACK", vv["features"]["rs_6m_vs_spy_pct"], sym, tk, a, float(df.c.iloc[-1])))
    cands.sort(key=lambda z: (not z[0], -z[1]))
    slots = MAX_POSITIONS - len(s["positions"]) - sum(1 for o in s["pending"] if o["side"] == "BUY")
    budget = s["cash"] - sum(o["shares"] * o["ref_close"] for o in s["pending"] if o["side"] == "BUY")
    for pull, rs, sym, tk, a, close in cands[:max(0, slots)]:
        risk_ps = STOP_ATR * a
        shares = int(min(RISK_PER_POS * equity / risk_ps, MAX_POS_PCT * equity / close, budget / (close * (1 + COST))))
        if shares <= 0:
            log(logs, "close", when, sym, "SKIP_ENTRY", "cash", "no budget left")
            continue
        budget -= shares * close * (1 + COST)
        s["pending"].append({"symbol": sym, "ticker": tk, "side": "BUY", "shares": shares, "created": as_of, "rule": "D3",
                             "reason": ("PULLBACK " if pull else "") + f"BULLISH, RS6 {rs:+.1f}", "stop": close - risk_ps,
                             "atr": a, "ref_close": close})
        log(logs, "close", when, sym, "QUEUE_BUY", "D3", f"{shares} sh, stop {close - risk_ps:.2f} (2.5xATR)")
    for c in cands[max(0, slots):]:
        log(logs, "close", when, c[2], "SKIP_ENTRY", "max_positions", "no free slot")
    # equity curve
    spy_c = float(_completed(bars["SPY"]).c.iloc[-1])
    spy_eq = s["initial_capital"] * spy_c / s["spy_base"]["open"] if s.get("spy_base") else s["initial_capital"]
    eq_rows = [{"date": as_of, "equity": round(equity, 2), "cash": round(s["cash"], 2), "positions": len(s["positions"]),
                "spy_benchmark": round(spy_eq, 2), "pending_orders": len(s["pending"])}]
    if EQUITY.exists() and as_of in set(pd.read_csv(EQUITY).date.astype(str)):
        e = pd.read_csv(EQUITY)
        e = e[e.date.astype(str) != as_of]
        e = pd.concat([e, pd.DataFrame(eq_rows)])
        e.to_csv(EQUITY, index=False)
    else:
        append(EQUITY, eq_rows)
    # flips: compare today's partial reads with the final verdict
    if FLIPS.exists():
        f = pd.read_csv(FLIPS)
        final = {k: x[1].get("signal") for k, x in v.items()}
        f["final_signal"] = [final.get(sym) if str(d) == as_of else fs for sym, d, fs in
                             zip(f.symbol, f.date, f.get("final_signal", pd.Series([None] * len(f))))]
        f.to_csv(FLIPS, index=False)
    s["last_close_run"] = as_of
    return as_of, v


def report(s):
    eq = pd.read_csv(EQUITY) if EQUITY.exists() else pd.DataFrame()
    tr = pd.read_csv(TRADES) if TRADES.exists() else pd.DataFrame()
    fl = pd.read_csv(FLIPS) if FLIPS.exists() else pd.DataFrame()
    lg = pd.read_csv(LOG) if LOG.exists() else pd.DataFrame()
    L = [f"# Demo week {WEEK[0]} → {WEEK[1]}: rulebook v{RULEBOOK_VERSION} on a simulated $100k account", "",
         "Mechanical rules (see `platform/tagym/demo.py`). Decisions are made on completed daily bars, filled at the next open, 10 bps cost per side.",
         "**One week is far too short to judge the method.** These numbers test the process (execution, discipline, data), not the edge.", ""]
    if len(eq):
        last = eq.iloc[-1]
        r = last.equity / s["initial_capital"] - 1
        rb = last.spy_benchmark / s["initial_capital"] - 1
        L += [f"**Equity {last.equity:,.0f}** ({r:+.2%}) vs SPY benchmark {last.spy_benchmark:,.0f} ({rb:+.2%}). "
              f"Cash {last.cash:,.0f}, {int(last.positions)} positions, {int(last.pending_orders)} orders queued for the next open.", "",
              "| Date | Equity | SPY benchmark | Cash | Positions |", "|---|---|---|---|---|"]
        for _, e in eq.iterrows():
            L.append(f"| {e.date} | {e.equity:,.0f} | {e.spy_benchmark:,.0f} | {e.cash:,.0f} | {int(e.positions)} |")
        L.append("")
    L += ["## Open positions", "", "| Symbol | Shares | Entry | Entry price | Stop | Trimmed |", "|---|---|---|---|---|---|"]
    for sym, p in sorted(s["positions"].items()):
        L.append(f"| {sym} | {p['shares']} | {p['entry_date']} | {p['entry_price']:.2f} | {p['stop']:.2f} | {p['trimmed']} |")
    L += ["", "## Orders queued for the next open", "", "| Symbol | Side | Shares | Rule | Reason |", "|---|---|---|---|---|"]
    for o in s["pending"]:
        L.append(f"| {o['symbol']} | {o['side']} | {o['shares']} | {o['rule']} | {o['reason']} |")
    if len(tr):
        L += ["", "## Fills", "", "| Date | Symbol | Side | Shares | Price | Rule | Gap vs prior close | P&L |", "|---|---|---|---|---|---|---|---|"]
        for _, t in tr.iterrows():
            gap = f"{t.gap_pct:+.2f}%" if "gap_pct" in t and pd.notna(t.get("gap_pct")) else ""
            pnl = f"{t.pnl:+,.0f}" if "pnl" in t and pd.notna(t.get("pnl")) else ""
            L.append(f"| {t.date} | {t.symbol} | {t.side} | {int(t.shares)} | {t.price:.2f} | {t.rule} | {gap} | {pnl} |")
        if "gap_pct" in tr:
            g = tr.gap_pct.dropna()
            if len(g):
                L += ["", f"Execution: {len(g)} market-on-open fills, mean |gap| vs prior close {g.abs().mean():.2f}% "
                      f"(the backtests charged 0.10% per side and did not assume a favourable gap)."]
    if len(fl) and "final_signal" in fl:
        done = fl.dropna(subset=["final_signal"])
        if len(done):
            L += ["", "## How often an unfinished-bar read disagreed with the evening verdict", "",
                  "| Run | Reads | Disagreed | Rate |", "|---|---|---|---|"]
            for m, g in done.groupby("mode"):
                k = int((g.partial_signal != g.final_signal).sum())
                L.append(f"| {m} | {len(g)} | {k} | {k/len(g):.1%} |")
    if len(lg):
        L += ["", "## Decision log (latest 40)", "", "| Time (NY) | Run | Symbol | Action | Rule | Detail |", "|---|---|---|---|---|---|"]
        for _, x in lg.tail(40).iterrows():
            L.append(f"| {str(x.time_ny)[:16]} | {x['mode']} | {x.symbol} | {x.action} | {x.rule} | {x.detail} |")
    REPORT.write_text("\n".join(L) + "\n")


def run(mode, earnings_file):
    s = load_state()
    earn = json.loads(Path(earnings_file).read_text()) if earnings_file and Path(earnings_file).exists() else {}
    earn = {k: v for k, v in earn.items() if not k.startswith("_")}
    when = ny_now()
    logs = []
    tickers = list(watchlist().ticker) + ["SPY"]
    bars = fetch(tickers, period="2y")
    if when.dayofweek >= 5 and mode != "close":
        print("weekend - nothing to do"); return
    if mode == "preopen":
        mode_preopen(s, bars, earn, when, logs)
    elif mode in ("midday", "preclose"):
        process_fills_and_stops(s, bars, mode, when, logs)
        n = record_flips(bars, earn, mode, when)
        log(logs, mode, when, "-", "FLIP_LOG", "-", f"recorded {n} unfinished-bar reads")
    elif mode == "close":
        process_fills_and_stops(s, bars, mode, when, logs, full_day=True)
        mode_close(s, bars, earn, when, logs)
    append(LOG, [{**r, "time_ny": str(r["time_ny"])[:19]} for r in logs])
    save_state(s)
    report(s)
    print(f"{mode} done at {str(when)[:16]} NY: {len(logs)} decisions logged, {len(s['positions'])} positions, "
          f"{len(s['pending'])} queued orders, cash {s['cash']:,.0f}")


def auto_mode(now=None):
    now = now or ny_now()
    hm = now.hour * 60 + now.minute
    if hm < 9 * 60 + 30:
        return "preopen"
    if hm < 15 * 60:
        return "midday"
    if hm < 16 * 60 + 15:
        return "preclose"
    return "close"


if __name__ == "__main__":
    m = sys.argv[1]
    ef = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--earnings"), str(ROOT / "paper" / "next_earnings.json"))
    run(auto_mode() if m == "auto" else m, ef)
