"""Forward test of the intraday rules by nightly replay (30-day program, from 2026-11-04).

    python -m tagym.intraday_fwd update [--start 2026-11-04]   # add every finished day not yet in the ledger
    python -m tagym.intraday_fwd report                        # rebuild intraday/FORWARD_REPORT.md

Why a replay and not a live process: the live trader (tagym.intraday) and the backtest share the same signal
code, and replaying a live window through it gave 126 of 126 identical trades. A nightly replay on 5-minute bars
therefore measures the same thing as a live window but cannot miss one (the live run lost 2 of 10 windows to a
worker restart). It uses the backtest's fill convention (open of the bar after the decision, exit at the xx:55
open); live fills one minute later averaged +0.3 bps worse (+-5.4 per trade), so the replay is not optimistic.

Pre-registered protocol: ../PLAN_30D.md. Rules are frozen at RULEBOOK v2.3 (the 10 original rules) plus one
forward-only hypothesis, R2L (the long side of R2, suggested by the 60-day backtest). Forward days are days never
used to design anything. Verdicts only use the thresholds in PLAN_30D.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from .intraday_bt import COST_BPS, RULES, clean, events, features
from .paper import watchlist

ROOT = Path(__file__).resolve().parents[2]
IDIR = ROOT / "intraday"
LEDGER = IDIR / "forward_events.csv.gz"
REPORT = IDIR / "FORWARD_REPORT.md"
FWD_START = "2026-11-04"
UNIT = 1000.0
KEY = ["rule", "sym", "day", "hour", "minute"]
RULES_FWD = dict(RULES, R2L_reversal_long="R2 restricted to its long side (buy sharp drops vs SPY): forward-only hypothesis from the backtest")

# pre-registered thresholds (PLAN_30D.md)
MIN_DAYS_CANDIDATE = 20
MIN_DAYS_PASS = 40
T_CANDIDATE = 2.0   # gross, date-clustered
T_PASS = 3.0        # net, date-clustered, both halves positive


def now_ny():
    return pd.Timestamp.now(tz="America/New_York").tz_localize(None)


def finished_days(spy_days, now):
    """A day is finished once it is before today, or after 16:15 New York time today."""
    out = []
    for d in spy_days:
        if d < now.normalize() or (d == now.normalize() and now.hour * 60 + now.minute >= 16 * 60 + 15):
            out.append(d)
    return out


def download():
    import time
    import yfinance as yf
    tick = list(watchlist().ticker) + ["SPY", "QQQ"]
    for i in range(3):
        try:
            raw = yf.download(tick, period="60d", interval="5m", auto_adjust=False, prepost=False,
                              progress=False, group_by="ticker", threads=True)
            if len(raw):
                return raw, tick
        except Exception:
            pass
        time.sleep(5 * (i + 1))
    raise RuntimeError("yfinance 5m download failed")


def update(start=FWD_START, raw=None, now=None):
    now = now or now_ny()
    start = pd.Timestamp(start)
    if raw is None:
        raw, tick = download()
    else:
        tick = list(watchlist().ticker) + ["SPY", "QQQ"]
    X = clean(raw, tick)
    F = {s: features(x) for s, x in X.items()}
    have = pd.read_csv(LEDGER, parse_dates=["day"]) if LEDGER.exists() else pd.DataFrame(columns=KEY + ["side", "gross_bps"])
    done = set(have.day.dt.normalize()) if len(have) else set()
    spy_days = sorted(set(F["SPY"].day.unique()))
    new_days = [d for d in finished_days(spy_days, now) if d >= start and d not in done]
    if not new_days:
        print("forward ledger already up to date")
        return have
    ev = events(F, F["SPY"], min_day=min(new_days))
    ev = ev[ev.day.isin(new_days)]
    r2l = ev[(ev.rule == "R2_reversal") & (ev.side == 1)].assign(rule="R2L_reversal_long")
    ev = pd.concat([ev, r2l], ignore_index=True)
    # a day with no bar at 15:55 is a half day: its late windows simply have no events
    out = pd.concat([have, ev], ignore_index=True)
    out["day"] = pd.to_datetime(out.day)
    out = out.drop_duplicates(KEY)
    IDIR.mkdir(exist_ok=True)
    out.sort_values(["day", "hour", "minute", "rule", "sym"]).to_csv(LEDGER, index=False)
    print(f"forward ledger: +{len(ev)} events for {len(new_days)} day(s) "
          f"({str(new_days[0].date())} -> {str(new_days[-1].date())}); total {len(out)} events over {out.day.nunique()} days")
    return out


def tstat(x):
    x = pd.Series(x).dropna()
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) >= 3 and x.std() > 0 else float("nan")


def summarize(ev, cost=COST_BPS):
    ev = ev.copy()
    ev["net_bps"] = ev.gross_bps - 2 * cost
    rows = []
    for rule, g in ev.groupby("rule"):
        days = sorted(g.day.unique())
        dg, dn = g.groupby("day").gross_bps.mean(), g.groupby("day").net_bps.mean()
        half = len(days) // 2
        a, b = g[g.day.isin(days[:half])], g[g.day.isin(days[half:])]
        tg, tn = tstat(dg), tstat(dn)
        nd = len(days)
        if nd >= MIN_DAYS_PASS and tn >= T_PASS and a.net_bps.mean() > 0 and b.net_bps.mean() > 0:
            v = "PASS"
        elif nd >= MIN_DAYS_CANDIDATE and tg >= T_CANDIDATE and g.net_bps.mean() > 0:
            v = "CANDIDATE"
        elif nd >= MIN_DAYS_CANDIDATE:
            v = "NO EDGE"
        else:
            v = "TOO EARLY"
        rows.append({"rule": rule, "days": nd, "trades": len(g), "gross_bps": g.gross_bps.mean(),
                     "net_bps": g.net_bps.mean(), "t_gross": tg, "t_net": tn, "hit_rate_net": float((g.net_bps > 0).mean()),
                     "pnl": float((UNIT * g.net_bps / 1e4).sum()), "verdict": v})
    return pd.DataFrame(rows).sort_values("t_gross", ascending=False)


def report():
    if not LEDGER.exists():
        return
    ev = pd.read_csv(LEDGER, parse_dates=["day"])
    s = summarize(ev)
    bt = pd.read_csv(ROOT / "experiments" / "results" / "intraday_backtest.csv").set_index("rule")
    d0, d1 = ev.day.min(), ev.day.max()
    L = [f"# Intraday forward test (replay) - {ev.day.nunique()} trading days ({d0:%Y-%m-%d} to {d1:%Y-%m-%d})", "",
         "Rules frozen at RULEBOOK v2.3 plus the forward-only hypothesis R2L. $1,000 per trade, 2.5 bps per side, windows xx:35-xx:55",
         "(hours 9-15). Verdict bars (PLAN_30D.md): CANDIDATE = >= 20 days, gross t >= 2 and net mean > 0; PASS = >= 40 days, net t >= 3",
         "and both halves positive. Fewer than 20 days is TOO EARLY, whatever the numbers look like.", "",
         "| Rule | Days | Trades | Gross bps | Net bps | t gross | t net | Hit rate | P&L | 60-day backtest net | Verdict |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in s.itertuples():
        b = f"{bt.loc[r.rule].net_bps:+.2f}" if r.rule in bt.index else "n/a"
        L.append(f"| {r.rule} | {r.days} | {r.trades:,} | {r.gross_bps:+.2f} | {r.net_bps:+.2f} | {r.t_gross:+.2f} | {r.t_net:+.2f} | "
                 f"{r.hit_rate_net:.0%} | {r.pnl:+,.0f} | {b} | {r.verdict} |")
    day = ev.assign(net=ev.gross_bps - 2 * COST_BPS).groupby("day").agg(trades=("net", "size"), net_bps=("net", "mean"))
    day["pnl"] = UNIT * ev.assign(net=ev.gross_bps - 2 * COST_BPS).groupby("day").net.sum() / 1e4
    L += ["", "## By day", "", "| Day | Trades | Mean net bps | P&L |", "|---|---|---|---|"]
    for d, r in day.iterrows():
        L.append(f"| {d:%Y-%m-%d} | {int(r.trades)} | {r.net_bps:+.2f} | {r.pnl:+,.0f} |")
    L += ["", "## Rules", ""] + [f"- **{k}**: {v}" for k, v in RULES_FWD.items()]
    REPORT.write_text("\n".join(L) + "\n")
    print(f"report written: {len(s)} rules, {ev.day.nunique()} days")


if __name__ == "__main__":
    a = sys.argv[1:]
    cmd = a[0] if a else "update"
    if cmd == "update":
        update(start=a[a.index("--start") + 1] if "--start" in a else FWD_START)
        report()
    elif cmd == "report":
        report()
