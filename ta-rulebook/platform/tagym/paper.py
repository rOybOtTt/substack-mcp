"""Forward paper-trading journal + automatic scoring for the rulebook.

    python -m tagym.paper run   [--earnings ../paper/next_earnings.json]   # today's verdicts
    python -m tagym.paper score                                           # grade matured calls
    python -m tagym.paper xcheck SYMBOL=CLOSE [...]                       # log TradingView cross-check
    python -m tagym.paper earnings-yf                                     # fallback next-earnings dates

* Verdicts come from tagym.live.classify (the same engine the agent uses).
* Bars: yfinance (split+dividend adjusted, same as the backtests).
  The daily job cross-checks a few symbols against TradingView.
* Scoring: each call is graded once its 10/20/60-trading-day windows have passed:
  max drawdown from the next open, return vs SPY, and whether the rulebook's
  stated odds were right (binomial 95% test of realized vs expected rates).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from .live import classify, RULEBOOK_VERSION

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper"
JOURNAL = PAPER / "journal.csv"
SCORE = PAPER / "SCOREBOARD.md"
XCHECK = PAPER / "integrity_log.csv"


def watchlist():
    return pd.read_csv(PAPER / "watchlist.csv")


def fetch(tickers, period="2y"):
    import yfinance as yf
    d = yf.download(list(tickers), period=period, auto_adjust=True, progress=False, group_by="ticker", threads=True)
    out = {}
    for t in tickers:
        try:
            x = d[t][["Open", "High", "Low", "Close", "Volume"]].dropna()
        except KeyError:
            continue
        x.columns = ["o", "h", "l", "c", "v"]
        x.index = pd.to_datetime(x.index).tz_localize(None)
        out[t] = x
    return out


def _completed(df):
    """Drop today's bar if the US session has not closed yet (before 16:15 New York time)."""
    now = pd.Timestamp.now(tz="America/New_York")
    if len(df) and df.index[-1].date() == now.date() and (now.hour, now.minute) < (16, 15):
        return df.iloc[:-1]
    return df


def run(earnings_file=None):
    wl = watchlist()
    earn = json.loads(Path(earnings_file).read_text()) if earnings_file and Path(earnings_file).exists() else {}
    bars = fetch(list(wl.ticker) + ["SPY"])
    spy = _completed(bars["SPY"])
    rows = []
    for _, w in wl.iterrows():
        df = bars.get(w.ticker)
        if df is None or len(df) < 50:
            continue
        df = _completed(df).loc[:spy.index[-1]]
        v = classify(df, spy, w.symbol_tv, next_earnings=earn.get(w.symbol_tv))
        rows.append({"as_of": v["as_of"], "symbol": w.symbol_tv, "ticker": w.ticker, "sector": w.sector,
                     "rulebook_version": RULEBOOK_VERSION, "signal": v["signal"], "row": v["decision_row"],
                     "regime": v.get("layers", {}).get("regime"), "health": v.get("layers", {}).get("health"),
                     "timing": v.get("layers", {}).get("timing"), "risk_flag": v.get("risk", {}).get("risk_flag"),
                     "p_dd20_60d_est": v.get("risk", {}).get("p_drawdown20_60d_est"),
                     "p_drop10_10d_est": v.get("risk", {}).get("p_drop10_10d_est"),
                     "earnings_due_10d": v.get("risk", {}).get("earnings_in_next_10d"),
                     "close": v.get("features", {}).get("close"), "confidence": v.get("confidence"),
                     "warnings": " | ".join(v.get("warnings", []))})
    new = pd.DataFrame(rows)
    PAPER.mkdir(exist_ok=True)
    if JOURNAL.exists():
        old = pd.read_csv(JOURNAL)
        new = new[~new.set_index(["as_of", "symbol"]).index.isin(old.set_index(["as_of", "symbol"]).index)]
        allj = pd.concat([old, new], ignore_index=True)
    else:
        allj = new
    allj.to_csv(JOURNAL, index=False)
    print(f"as_of {new.as_of.max() if len(new) else '-'}: appended {len(new)} verdicts; journal {len(allj)} rows")
    print(new.groupby("signal").size().to_string() if len(new) else "nothing new (already journaled)")
    return new


def _binom_ok(k, n, p):
    """True if k successes out of n are inside a two-sided 95% normal-approx band around p."""
    if n == 0 or p is None or not np.isfinite(p):
        return None
    sd = math.sqrt(max(p * (1 - p) / n, 1e-12))
    return abs(k / n - p) <= 1.96 * sd + 0.5 / n


def score():
    j = pd.read_csv(JOURNAL)
    tick = sorted(set(j.ticker)) + ["SPY"]
    bars = fetch(tick, period="5y")
    spy = bars["SPY"]
    res = []
    for _, r in j.iterrows():
        df = bars.get(r.ticker)
        if df is None:
            continue
        t0 = pd.Timestamp(r.as_of)
        fut = df.loc[df.index > t0]
        sfut = spy.loc[spy.index > t0]
        rec = r.to_dict()
        for h in (10, 20, 60):
            if len(fut) >= h and len(sfut) >= h:
                e = fut.o.iloc[0]
                path = fut.c.iloc[:h]
                rec[f"ret{h}"] = path.iloc[-1] / e - 1
                rec[f"spy{h}"] = sfut.c.iloc[h - 1] / sfut.o.iloc[0] - 1
                rec[f"exc{h}"] = rec[f"ret{h}"] - rec[f"spy{h}"]
                rec[f"mdd{h}"] = path.min() / e - 1
        res.append(rec)
    s = pd.DataFrame(res)
    lines = [f"# Paper-trading scoreboard (rulebook v{RULEBOOK_VERSION})", "",
             f"Journal: {len(j)} verdicts, {j.as_of.nunique()} trading days ({j.as_of.min()} → {j.as_of.max()}), "
             f"{j.symbol.nunique()} symbols. Updated {pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC.", "",
             "Each call is graded once its window has passed (entry = next open). 'Expected' is the rulebook's",
             "stated probability; 'calibrated?' tests realized vs expected at 95% (binomial).", ""]
    for h, col, thr, pcol, lab in [(60, "mdd60", -0.20, "p_dd20_60d_est", "≥20% drawdown within 60 days"),
                                   (10, "mdd10", -0.10, "p_drop10_10d_est", "≥10% drop within 10 days")]:
        m = s[s.get(col).notna()] if col in s else s.iloc[0:0]
        lines += [f"## {lab}", "", "| Class | matured calls | realized | expected | calibrated? | mean excess vs SPY |",
                  "|---|---|---|---|---|---|"]
        for c in ["BULLISH", "NO_SIGNAL", "BEARISH"]:
            g = m[m.signal == c]
            n = len(g)
            if n == 0:
                lines.append(f"| {c} | 0 | – | – | – | – |")
                continue
            k = int((g[col] <= thr).sum())
            p = float(g[pcol].mean())
            ok = _binom_ok(k, n, p)
            lines.append(f"| {c} | {n} | {k/n:.1%} | {p:.1%} | {'yes' if ok else 'NO'} | {g[f'exc{h}'].mean():+.2%} |")
        lines.append("")
    s20 = s[s.get("exc20").notna()] if "exc20" in s else s.iloc[0:0]
    if len(s20):
        lines += ["## 20-day excess return vs SPY by class (expected ≈ 0: the rulebook claims risk, not alpha)", "",
                  "| Class | n | mean | median | share beating SPY |", "|---|---|---|---|---|"]
        for c in ["BULLISH", "NO_SIGNAL", "BEARISH"]:
            g = s20[s20.signal == c]
            if len(g):
                lines.append(f"| {c} | {len(g)} | {g.exc20.mean():+.2%} | {g.exc20.median():+.2%} | {(g.exc20 > 0).mean():.0%} |")
        lines.append("")
    last = j[j.as_of == j.as_of.max()]
    lines += [f"## Latest verdicts ({j.as_of.max()})", "", "| Symbol | Signal | Row | Health | Timing | Risk | Earnings ≤10d | Warnings |",
              "|---|---|---|---|---|---|---|---|"]
    for _, r in last.sort_values(["signal", "symbol"]).iterrows():
        lines.append(f"| {r.symbol} | {r.signal} | {r.row} | {r.health} | {r.timing} | {r.risk_flag} | "
                     f"{r.earnings_due_10d} | {str(r.warnings)[:90] if isinstance(r.warnings, str) else ''} |")
    if XCHECK.exists():
        x = pd.read_csv(XCHECK)
        lines += ["", f"## Data integrity (TradingView cross-checks): {len(x)} checks, "
                  f"max |diff| {x.abs_diff_pct.max():.3f}%, last {x.date.max()}"]
    SCORE.write_text("\n".join(lines) + "\n")
    s.to_csv(PAPER / "scored.csv", index=False)
    print("\n".join(lines[:30]))


def earnings_yf(out=None):
    """Fallback when the TradingView MCP is not available: next report dates from yfinance
    (agreed with TradingView on every symbol checked on 2026-11-01)."""
    import yfinance as yf
    out = Path(out) if out else PAPER / "next_earnings.json"
    res = {"_source": f"yfinance calendar {pd.Timestamp.now():%Y-%m-%d}"}
    today = pd.Timestamp.now().normalize()
    for _, w in watchlist().iterrows():
        try:
            cal = yf.Ticker(w.ticker).calendar
            ds = cal.get("Earnings Date") if isinstance(cal, dict) else None
            ds = [pd.Timestamp(d) for d in (ds or []) if pd.Timestamp(d) >= today]
            if ds:
                res[w.symbol_tv] = str(min(ds).date())
        except Exception:
            continue
    out.write_text(json.dumps(res, indent=0))
    print(f"wrote {len(res) - 1} next-earnings dates to {out}")


def xcheck(pairs):
    """pairs: ["NASDAQ:AAPL=344.63", ...] closes reported by TradingView for the latest journal date."""
    j = pd.read_csv(JOURNAL)
    d = j.as_of.max()
    last = j[j.as_of == d].set_index("symbol")
    rows = []
    for p in pairs:
        sym, val = p.split("=")
        if sym in last.index:
            ours = float(last.loc[sym, "close"])
            tv = float(val)
            rows.append({"date": d, "symbol": sym, "ours": ours, "tradingview": tv,
                         "abs_diff_pct": abs(ours / tv - 1) * 100})
    x = pd.DataFrame(rows)
    x.to_csv(XCHECK, mode="a", header=not XCHECK.exists(), index=False)
    print(x.to_string(index=False))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "run":
        ef = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--earnings"), None)
        run(ef)
    elif cmd == "score":
        score()
    elif cmd == "earnings-yf":
        earnings_yf()
    elif cmd == "xcheck":
        xcheck(sys.argv[2:])
