"""ONE-TIME locked out-of-sample test of the frozen rulebook (v2) and key findings.

Run:  python -m tagym.final_test A     (discovery tickers, TEST period 2020-2026)
      python -m tagym.final_test B     (unseen holdout tickers: train/valid/test periods)
      python -m tagym.final_test index (S&P 500 + 22 ETFs timing 2020-2026)
Every access is logged in experiments/test_access_log.md.
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from .run import get_ctx, evaluate, fmt, ROOT
from .rulebook_engine import classify_panel, V21 as V2  # frozen v2.1
from .rb_eval import outcomes

OUT = ROOT / "experiments" / "results"
KEY_RULES = ["rsi14_overbought", "short_term_winner", "bb_upper_close", "rs_leaders_bear_mkt", "wyc_resilience_on_shock",
             "leader_in_strong_group", "donchian20_breakout", "golden_cross", "high_52w_breakout", "macd_bull_cross",
             "cdl_bull_engulfing", "cdl_hammer", "pat_double_bottom", "pat_inv_head_shoulders", "fib_618_bounce",
             "support_bounce", "yt_rsi10_pullback", "sch_quiet_pullback_bull", "rs_leaders_bull_mkt", "trend_template"]


def run_group(group):
    x = get_ctx(group, unlock=True)
    cls = classify_panel(x, V2)
    periods = ["test"] if group == "A" else ["train", "valid", "test"]
    res = []
    for p in periods:
        d = outcomes(x, cls, p, 60, unlock=True)
        d.insert(0, "period", p); d.insert(0, "group", group)
        res.append(d)
        print(d.round(4).to_string(index=False), flush=True)
    pd.concat(res).to_csv(OUT / f"final_rulebook_{group}.csv", index=False)
    rows = []
    for p in periods:
        for r in KEY_RULES:
            row = evaluate(r, period=p, group=group, unlock=True, note=f"FINAL {group}")
            print(fmt(row), flush=True)
            rows.append(row)
    pd.DataFrame(rows).to_csv(OUT / f"final_rules_{group}.csv", index=False)


def run_index():
    from .timing import long_index, run_state, monthly_sma_pos, cross_pos, daily_sma_pos
    from .data import load
    with open(ROOT / "experiments" / "test_access_log.md", "a") as f:
        f.write(f"- {pd.Timestamp.now().isoformat(timespec='seconds')} | period=test | index/ETF timing FINAL\n")
    c, rf = long_index()
    e = load("etf")["Close"]
    rows = []
    syms = ["^GSPC"] + ["SPY", "QQQ", "DIA", "MDY", "IWM", "XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB",
                        "EFA", "EEM", "EWJ", "EWZ", "TLT", "GLD", "VNQ", "SMH"]
    for s in syms:
        px = (c[s] if s in c else e[s]).dropna()
        rr = rf.reindex(px.index).ffill().fillna(0)
        both = ((monthly_sma_pos(px, 10) == 1) & (cross_pos(px) == 1)).astype(float)
        for nm, pos in [("faber_10m", monthly_sma_pos(px, 10)), ("sma50_gt_200", cross_pos(px)),
                        ("regime_both", both), ("sma200_daily", daily_sma_pos(px, 200))]:
            o = run_state(px, pos, rr, lag=1, start="2020-01-01", end="2026-10-30"); o.update(sym=s, rule=nm); rows.append(o)
    d = pd.DataFrame(rows)
    d["dSharpe"] = d.timing_sharpe - d.buyhold_sharpe
    d["dMaxDD"] = d.timing_maxdd - d.buyhold_maxdd
    d["dCAGR"] = d.timing_cagr - d.buyhold_cagr
    d.to_csv(OUT / "final_index_timing.csv", index=False)
    print(d[d.sym == "^GSPC"][["rule", "timing_cagr", "buyhold_cagr", "timing_sharpe", "buyhold_sharpe", "timing_maxdd", "buyhold_maxdd"]].round(3).to_string(index=False))
    e2 = d[d.sym != "^GSPC"]
    print(e2.groupby("rule")[["dCAGR", "dSharpe", "dMaxDD"]].median().round(3).to_string())
    print(e2.assign(dd=e2.dMaxDD > 0, sh=e2.dSharpe > 0).groupby("rule")[["dd", "sh"]].mean().round(2).to_string())


if __name__ == "__main__":
    what = sys.argv[1]
    run_index() if what == "index" else run_group(what)
