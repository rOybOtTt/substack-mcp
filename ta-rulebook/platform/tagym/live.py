"""Apply the rulebook to live TradingView OHLCV.

Input: JSON saved from `mcp-tv-get-ohlcv(..., format="columns")` for the stock
and for AMEX:SPY (either the raw tool response or just its "bars" object).
Usage:
    python -m tagym.live stock.json spy.json [--symbol NASDAQ:XYZ] [--drop-last] [--next-earnings YYYY-MM-DD]
(--next-earnings: next report date from mcp-tv-get-earnings-calendar; enables flag E1)
Prints the rulebook JSON verdict (Section 9 of RULEBOOK.md).
"""
from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd


def load_tv(path):
    d = json.load(open(path))
    b = d.get("bars", d)
    df = pd.DataFrame({"o": b["o"], "h": b["h"], "l": b["l"], "c": b["c"], "v": b["v"]},
                      index=pd.to_datetime(b["t"], unit="s").normalize())
    return df.sort_index()


def wilder(x, n):
    return x.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()


def rsi(c, n):
    d = c.diff()
    up, dn = wilder(d.clip(lower=0), n), wilder((-d).clip(lower=0), n)
    return 100 - 100 / (1 + up / dn)


def atr(df, n=14):
    pc = df.c.shift(1)
    tr = np.maximum(df.h - df.l, np.maximum((df.h - pc).abs(), (df.l - pc).abs()))
    return wilder(tr, n)


def regime(spy: pd.DataFrame):
    c = spy.c
    m = c.resample("ME").last()
    # use only COMPLETED months: if the last bar is not month-end, the current month is excluded
    if c.index[-1] != m.index[-1] and c.index[-1].to_period("M") == m.index[-1].to_period("M"):
        m = m.iloc[:-1]
    ten = bool(m.iloc[-1] > m.iloc[-10:].mean())
    cross = bool(c.rolling(50).mean().iloc[-1] > c.rolling(200).mean().iloc[-1])
    lab = "RISK_ON" if ten and cross else ("RISK_OFF" if not ten and not cross else "MIXED")
    return lab, {"spy_above_10m_sma": ten, "spy_sma50_gt_sma200": cross}


RULEBOOK_VERSION = "2.2"

# P(>=10% drop within 10 trading days), mean of 6 samples (dev + holdout + 2020-26 test)
EARN_CAL = {("BULLISH", True): 0.096, ("BULLISH", False): 0.039,
            ("NO_SIGNAL", True): 0.132, ("NO_SIGNAL", False): 0.071,
            ("BEARISH", True): 0.178, ("BEARISH", False): 0.126}


def trading_days_until(as_of, date_str):
    """Business days from as_of (exclusive) to date (inclusive); None if unknown/past."""
    if not date_str:
        return None
    d = np.datetime64(str(date_str)[:10])
    a = np.datetime64(str(as_of)[:10])
    if d <= a:
        return None
    return int(np.busday_count(a + np.timedelta64(1, "D"), d + np.timedelta64(1, "D")))


def classify(df: pd.DataFrame, spy: pd.DataFrame, symbol="?", healthy_max_from_high=-0.10, broken_from_high=-0.40,
             next_earnings=None):
    out = {"symbol": symbol, "as_of": str(df.index[-1].date()), "rulebook_version": RULEBOOK_VERSION}
    c = df.c
    if len(df) < 260:
        return {**out, "signal": "NO_SIGNAL", "decision_row": "D1", "reason": f"only {len(df)} bars (<260)"}
    dollar_vol = (c * df.v).iloc[-20:].median()
    if c.iloc[-1] < 5 or dollar_vol < 5e6:
        return {**out, "signal": "NO_SIGNAL", "decision_row": "D1", "reason": "untradeable (price<$5 or $vol<$5M)"}
    s50, s200 = c.rolling(50).mean(), c.rolling(200).mean()
    rising = s200.iloc[-1] > s200.iloc[-22]
    falling = s200.iloc[-1] < s200.iloc[-22]
    d52 = c.iloc[-1] / c.iloc[-252:].max() - 1
    r14, r10 = rsi(c, 14), rsi(c, 10)
    mid = c.rolling(20).mean(); sd = c.rolling(20).std(ddof=0)
    upper = mid + 2 * sd
    a = atr(df, 14); atrp = a.iloc[-1] / c.iloc[-1]
    ret5 = c.iloc[-1] / c.iloc[-6] - 1
    ups = (c.diff() > 0).iloc[-5:].all()
    ret5_extreme = ret5 > 2.2 * atrp * np.sqrt(5)
    healthy = (c.iloc[-1] > s200.iloc[-1]) and rising and (s50.iloc[-1] > s200.iloc[-1]) and d52 >= healthy_max_from_high
    broken = (((c.iloc[-1] < s200.iloc[-1]) and falling) or d52 <= broken_from_high
              or ((c.iloc[-1] < s200.iloc[-1]) and (s50.iloc[-1] < s200.iloc[-1]) and d52 <= -0.25))
    health = "HEALTHY" if healthy else ("BROKEN" if broken else "NEUTRAL")
    rsi_cross70 = r14.iloc[-1] >= 70 and r14.iloc[-2] < 70
    extended = bool(r14.iloc[-1] >= 70 or c.iloc[-1] > upper.iloc[-1] or ret5_extreme or ups)
    dd60_close = c.iloc[-1] / c.iloc[-60:].max() - 1
    dd60 = c.iloc[-1] / c.iloc[-60:].max() - 1
    quiet = df.v.iloc[-10:].mean() <= 0.7 * df.v.iloc[-60:-10].mean()
    pullback = healthy and (r10.iloc[-1] < 30 or (-0.15 <= dd60 <= -0.07 and quiet))
    timing = "EXTENDED" if extended else ("PULLBACK" if pullback else "NORMAL")
    reg, reg_detail = regime(spy)
    rs6 = c.iloc[-1] / c.iloc[-127] - 1
    spy6 = spy.c.iloc[-1] / spy.c.iloc[-127] - 1
    warnings = []
    if not reg_detail["spy_above_10m_sma"] and rs6 - spy6 > 0.25:
        warnings.append("A1: strong relative-strength leader while the index is below its 10-month SMA - momentum-crash risk; never BULLISH")
    if healthy and extended and reg != "RISK_ON":
        warnings.append("D4 in an unhealthy market: healthy but extended AND regime is not RISK_ON")
    if health == "BROKEN":
        row, sig = "D2", "BEARISH"
    elif healthy and reg == "RISK_ON" and not extended:
        row, sig = "D3", "BULLISH"
    elif healthy and extended:
        row, sig = "D4", "NO_SIGNAL"
    elif healthy:
        row, sig = "D5", "NO_SIGNAL"
    else:
        row, sig = "D6", "NO_SIGNAL"
    # calibrated P(>=20% drawdown within 60 trading days), mean of 2000-14 and 2015-19
    # (experiments/results/risk_calibration_by_row.csv)
    CAL = {("D2", "RISK_ON"): 0.156, ("D2", "MIXED"): 0.169, ("D2", "RISK_OFF"): 0.208,
           ("D3", "RISK_ON"): 0.060,
           ("D4", "RISK_ON"): 0.068, ("D4", "MIXED"): 0.121, ("D4", "RISK_OFF"): 0.111,
           ("D5", "MIXED"): 0.098, ("D5", "RISK_OFF"): 0.123,
           ("D6", "RISK_ON"): 0.111, ("D6", "MIXED"): 0.145, ("D6", "RISK_OFF"): 0.167}
    p_dd = CAL.get((row, reg), 0.12)
    if row == "D3" and d52 >= 0:
        warnings.append("A3: close is the 52-week closing high - prefer a pullback entry over buying the breakout bar")
    high_vol = atrp >= 0.03  # ~ top tercile of US stocks' ATR% (2000-2019 median cut-off 2.9%)
    days_to_earn = trading_days_until(out["as_of"], next_earnings)
    earn_due = days_to_earn is not None and days_to_earn <= 10
    if earn_due:
        warnings.append(f"E1: earnings in {days_to_earn} trading days - short-term crash risk ~2-3x higher "
                        "(P(>=10% drop in 10d) {:.0%} vs {:.0%} without)".format(EARN_CAL[(sig, True)], EARN_CAL[(sig, False)]))
    if health == "BROKEN" or (high_vol and reg == "RISK_OFF"):
        risk_flag = "HIGH"
    elif row == "D3" and not high_vol and not earn_due:
        risk_flag = "LOW"
    else:
        risk_flag = "NORMAL"
    near = []  # inputs within a hair of a threshold -> downgrade confidence
    if abs(d52 - healthy_max_from_high) < 0.01 or abs(d52 - broken_from_high) < 0.01:
        near.append("pct_from_52w_high")
    if abs(c.iloc[-1] / s200.iloc[-1] - 1) < 0.01:
        near.append("close_vs_sma200")
    if abs(s200.iloc[-1] / s200.iloc[-22] - 1) < 0.001:
        near.append("sma200_slope")
    if abs(r14.iloc[-1] - 70) < 1:
        near.append("rsi14")
    out.update({
        "signal": sig, "decision_row": row,
        "layers": {"regime": reg, "health": health, "timing": timing},
        "risk": {"p_drawdown20_60d_est": p_dd,
                 # observed in the locked 2020-2026 test (includes the COVID crash): harsher, use for conservative views
                 "p_drawdown20_60d_2020_26_observed": {"BULLISH": 0.125, "NO_SIGNAL": 0.155, "BEARISH": 0.192}[sig],
                 "p_drop10_10d_est": EARN_CAL[(sig, earn_due)],
                 "earnings_in_next_10d": (None if next_earnings is None else bool(earn_due)),
                 "next_earnings": next_earnings,
                 "risk_flag": risk_flag, "atr_pct": round(atrp * 100, 2)},
        "confidence": "low" if near else "medium",
        "near_threshold": near,
        "horizon_days": 60,
        "features": {"close": round(float(c.iloc[-1]), 2), "pct_from_52w_high": round(d52 * 100, 1),
                     "pct_from_60d_high": round(dd60_close * 100, 1),
                     "volume_10d_vs_prior_50d": round(float(df.v.iloc[-10:].mean() / df.v.iloc[-60:-10].mean()), 2),
                     "close_vs_sma200_pct": round((c.iloc[-1] / s200.iloc[-1] - 1) * 100, 1),
                     "sma200_rising": bool(rising), "sma50_gt_sma200": bool(s50.iloc[-1] > s200.iloc[-1]),
                     "rsi14": round(float(r14.iloc[-1]), 1), "rsi10": round(float(r10.iloc[-1]), 1),
                     "rsi14_crossed_above_70_today": bool(rsi_cross70),
                     "close_above_upper_bb": bool(c.iloc[-1] > upper.iloc[-1]), "ret5_pct": round(ret5 * 100, 1),
                     "rs_6m_vs_spy_pct": round((rs6 - spy6) * 100, 1), **reg_detail},
        "warnings": warnings,
        "invalidation": {"D2": "health recovers: close back above a rising SMA200 and within 40% of the 52w high",
                         "D3": "close below SMA200, SMA200 rolls over, >10% off the 52w high, or regime leaves RISK_ON"}.get(row, "n/a"),
    })
    return out


if __name__ == "__main__":
    flag_vals = {sys.argv[i + 1] for i, a in enumerate(sys.argv[:-1]) if a in ("--symbol", "--next-earnings")}
    args = [a for a in sys.argv[1:] if not a.startswith("--") and a not in flag_vals]
    sym = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--symbol"), "?")
    nxt = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--next-earnings"), None)
    df, spy = load_tv(args[0]), load_tv(args[1])
    if "--drop-last" in sys.argv:
        df, spy = df.iloc[:-1], spy.iloc[:-1]
    print(json.dumps(classify(df, spy, sym, next_earnings=nxt), indent=1))
