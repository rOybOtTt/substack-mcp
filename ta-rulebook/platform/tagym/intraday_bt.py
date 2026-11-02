"""Intraday backtest for the hourly 20-minute trading windows (pre-registered rules).

    python -m tagym.intraday_bt [raw5m.pkl] [raw1h.pkl]

Design (fixed before looking at results):
  * Universe: paper/watchlist.csv (98 large caps) + SPY, QQQ. Regular-hours 5-minute bars (yfinance, ~60 days).
  * Windows: one per hour, xx:35-xx:55 New York time, hours 9..15 (the live trader's schedule).
    Decisions at xx:35, xx:40, xx:45 use only bars completed by then. Entry = open of the next bar,
    exit = open of the xx:55 bar (hold 10-20 minutes). At most one entry per symbol per window.
  * Cost 2.5 bps per side (5 bps round trip). Results reported gross and net.
  * Statistics: per-trade returns averaged by day; t = mean / (sd / sqrt(days)) (date-clustered).
  * Verdicts (pre-registered): PASS if net t >= 2.6 and net mean > 0 in both halves (first 60% /
    last 40% of days); CANDIDATE if gross t >= 2 and full-sample net mean > 0; otherwise REJECT.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from .paper import watchlist

NY = "America/New_York"
COST_BPS = 2.5
HOURS = range(9, 16)
DECISIONS = (35, 40, 45)
RULES = {
    "R1_vwap_trend": "Close above VWAP, EMA9 > EMA21, 30-min return > 0, SPY above its VWAP -> long (mirror short)",
    "R2_reversal": "15-min return vs SPY beyond 2.5 sigma -> fade it (liquidity provision)",
    "R3_orb": "Fresh break of the 9:30-10:00 opening range with relative volume > 1.2 -> trade the break",
    "R4_mkt_momentum": "SPY/QQQ 15:35-15:55 in the direction of the prior-close -> 10:00 move (Gao et al. 2018)",
    "R5_xs_momentum": "At xx:35 long the 5 strongest / short the 5 weakest stocks since the open (vs SPY)",
    "R6_periodicity": "At xx:35 long top / short bottom quintile of the same window's average return over the past 10 days (Heston-Korajczyk-Sadka)",
    "R7_lead_lag": "SPY moved > 0.25% in 10 min and the stock lagged (< 30% of SPY's move) -> catch-up trade",
    "R8_rsi": "RSI(14) on 5-min bars < 25 -> long, > 75 -> short (retail TA)",
    "R9_ema_cross": "EMA9 crosses EMA21 on the last 5-min bar -> trade the cross (retail TA)",
    "C0_spy_long": "Control: always long SPY in every window",
}


def clean(raw, tickers):
    out = {}
    for t in tickers:
        try:
            x = raw[t][["Open", "High", "Low", "Close", "Volume"]].dropna()
        except KeyError:
            continue
        x.columns = list("ohlcv")
        idx = x.index.tz_convert(NY) if x.index.tz is not None else x.index.tz_localize("UTC").tz_convert(NY)
        x.index = idx.tz_localize(None)
        x = x.between_time("09:30", "15:55")
        if len(x) > 500:
            out[t] = x
    return out


def rsi(c, n=14):
    d = c.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))


def features(x):
    f = x.copy()
    day = f.index.normalize()
    f["day"] = day
    f["tod"] = f.index.hour * 60 + f.index.minute
    g = f.groupby("day")
    first = g.cumcount() == 0
    f["r5"] = np.log(f.c).diff()
    f.loc[first, "r5"] = np.nan
    tp = (f.h + f.l + f.c) / 3
    f["vwap"] = (tp * f.v).groupby(day).cumsum() / f.v.groupby(day).cumsum()
    f["day_open"] = g.o.transform("first")
    f["ret_open"] = f.c / f.day_open - 1
    for k, n in (("ret10", 2), ("ret15", 3), ("ret30", 6)):
        f[k] = f.c / g.c.shift(n) - 1
    orb = f[f.tod < 600].groupby("day").agg(orh=("h", "max"), orl=("l", "min"))
    f = f.join(orb, on="day")
    f["ema9"] = f.c.ewm(span=9, adjust=False).mean()
    f["ema21"] = f.c.ewm(span=21, adjust=False).mean()
    f["rsi"] = rsi(f.c)
    sd = f.groupby("day").r5.std()
    f["sig5"] = f.day.map(sd.rolling(10, min_periods=5).mean().shift(1))
    cv = f.v.groupby(day).cumsum()
    f["cumv"] = cv
    piv = cv.groupby([day, f.tod]).first().unstack()
    avg = piv.rolling(10, min_periods=5).mean().shift(1)
    f["relvol"] = cv.values / np.array([avg.at[d, t] if d in avg.index and t in avg.columns else np.nan
                                        for d, t in zip(day, f.tod)])
    f["prev_close"] = f.day.map(g.c.last().shift(1))
    return f


def window_returns(f):
    """For each (day, hour): open at each decision bar and the exit open at xx:55."""
    o = f.set_index(["day", "tod"]).o
    return o


def bar_signals(sym, t, b, sb, pb):
    """Pre-registered single-stock rules on the last completed 5-minute bar.
    t = decision time (minutes after midnight), b = the stock's bar ending at t, sb = SPY's bar ending at t,
    pb = the stock's bar before b (or None). Returns {rule: side}. Used by the backtest AND the live trader."""
    sig = {}
    if sb is not None:
        if b.c > b.vwap and b.ema9 > b.ema21 and b.ret30 > 0 and sb.c > sb.vwap:
            sig["R1_vwap_trend"] = 1
        elif b.c < b.vwap and b.ema9 < b.ema21 and b.ret30 < 0 and sb.c < sb.vwap:
            sig["R1_vwap_trend"] = -1
        if np.isfinite(b.sig5) and np.isfinite(b.ret15) and np.isfinite(sb.ret15):
            z = (b.ret15 - sb.ret15) / (b.sig5 * np.sqrt(3))
            if z < -2.5:
                sig["R2_reversal"] = 1
            elif z > 2.5:
                sig["R2_reversal"] = -1
        if np.isfinite(sb.ret10) and np.isfinite(b.ret10) and abs(sb.ret10) > 0.0025 and sym not in ("SPY", "QQQ"):
            if b.ret10 / sb.ret10 < 0.3:
                sig["R7_lead_lag"] = int(np.sign(sb.ret10))
    if t >= 600 + 30 and np.isfinite(b.orh) and pb is not None and b.relvol > 1.2:
        if b.c > b.orh and pb.c <= b.orh:
            sig["R3_orb"] = 1
        elif b.c < b.orl and pb.c >= b.orl:
            sig["R3_orb"] = -1
    if b.rsi < 25:
        sig["R8_rsi"] = 1
    elif b.rsi > 75:
        sig["R8_rsi"] = -1
    if pb is not None:
        if pb.ema9 <= pb.ema21 and b.ema9 > b.ema21:
            sig["R9_ema_cross"] = 1
        elif pb.ema9 >= pb.ema21 and b.ema9 < b.ema21:
            sig["R9_ema_cross"] = -1
    return sig


def events(F, spyF):
    """Build all pre-registered events. Returns DataFrame(rule, sym, day, hour, side, ret_gross_bps)."""
    rows = []
    spy_o = spyF.set_index(["day", "tod"])
    spy_by = spyF.set_index(["day", "tod"])
    for sym, f in F.items():
        fi = f.set_index(["day", "tod"])
        o = fi.o
        days = fi.index.get_level_values(0).unique()
        for d in days:
            for h in HOURS:
                exit_key = (d, h * 60 + 55)
                if exit_key not in o.index:
                    continue
                px_exit = o.loc[exit_key]
                taken = set()
                for m in DECISIONS:
                    t = h * 60 + m
                    prev, ent = (d, t - 5), (d, t)
                    if prev not in fi.index or ent not in o.index:
                        continue
                    b = fi.loc[prev]
                    sb = spy_by.loc[prev] if prev in spy_by.index else None
                    px = o.loc[ent]
                    pb = fi.loc[(d, t - 10)] if (d, t - 10) in fi.index else None
                    sig = bar_signals(sym, t, b, sb, pb)
                    for rule, side in sig.items():
                        if rule in taken:
                            continue
                        taken.add(rule)
                        rows.append((rule, sym, d, h, m, side, side * (px_exit / px - 1) * 1e4))
                    if sym == "SPY" and m == 35:
                        rows.append(("C0_spy_long", sym, d, h, m, 1, (px_exit / px - 1) * 1e4))
    ev = pd.DataFrame(rows, columns=["rule", "sym", "day", "hour", "minute", "side", "gross_bps"])
    return pd.concat([ev, cross_sectional(F, spyF), mkt_momentum(F)], ignore_index=True)


def cross_sectional(F, spyF):
    """R5 and R6 at xx:35 across the universe."""
    stocks = {s: f.set_index(["day", "tod"]) for s, f in F.items() if s not in ("SPY", "QQQ")}
    spy = spyF.set_index(["day", "tod"])
    # window returns for periodicity: open xx:35 -> open xx:55
    wret = {}
    for s, fi in stocks.items():
        o = fi.o.unstack()
        for h in HOURS:
            a, b = h * 60 + 35, h * 60 + 55
            if a in o.columns and b in o.columns:
                wret[(s, h)] = o[b] / o[a] - 1
    rows = []
    days = spy.index.get_level_values(0).unique()
    for d in days:
        for h in HOURS:
            t = h * 60 + 35
            if (d, t - 5) not in spy.index:
                continue
            s_ret = spy.loc[(d, t - 5)].ret_open
            mom, per, fwd = {}, {}, {}
            for s, fi in stocks.items():
                k = (d, t - 5)
                if k not in fi.index or (s, h) not in wret:
                    continue
                w = wret[(s, h)]
                if d not in w.index or not np.isfinite(w.loc[d]):
                    continue
                fwd[s] = w.loc[d]
                mom[s] = fi.loc[k].ret_open - s_ret
                past = w.loc[:d].iloc[:-1].tail(10)
                if len(past) >= 5:
                    per[s] = past.mean()
            for rule, sc, k in (("R5_xs_momentum", mom, 5), ("R6_periodicity", per, None)):
                sc = pd.Series(sc).dropna()
                if len(sc) < 30:
                    continue
                n = k or max(1, len(sc) // 5)
                srt = sc.sort_values()
                for s in srt.index[-n:]:
                    rows.append((rule, s, d, h, 35, 1, fwd[s] * 1e4))
                for s in srt.index[:n]:
                    rows.append((rule, s, d, h, 35, -1, -fwd[s] * 1e4))
    return pd.DataFrame(rows, columns=["rule", "sym", "day", "hour", "minute", "side", "gross_bps"])


def mkt_momentum(F):
    rows = []
    for s in ("SPY", "QQQ"):
        if s not in F:
            continue
        fi = F[s].set_index(["day", "tod"])
        for d in fi.index.get_level_values(0).unique():
            k10, a, b = (d, 595), (d, 15 * 60 + 35), (d, 15 * 60 + 55)
            if not all(k in fi.index for k in (k10, a, b)):
                continue
            pc = fi.loc[k10].prev_close
            if not np.isfinite(pc):
                continue
            side = int(np.sign(fi.loc[k10].c / pc - 1))
            if side:
                rows.append(("R4_mkt_momentum", s, d, 15, 35, side, side * (fi.loc[b].o / fi.loc[a].o - 1) * 1e4))
    return pd.DataFrame(rows, columns=["rule", "sym", "day", "hour", "minute", "side", "gross_bps"])


def tstat(daily):
    daily = daily.dropna()
    if len(daily) < 3 or daily.std() == 0:
        return np.nan
    return daily.mean() / (daily.std(ddof=1) / np.sqrt(len(daily)))


def summarize(ev, cost=COST_BPS):
    ev = ev.copy()
    ev["net_bps"] = ev.gross_bps - 2 * cost
    out = []
    for rule, g in ev.groupby("rule"):
        days = sorted(g.day.unique())
        cut = days[int(len(days) * 0.6)]
        dg = g.groupby("day").gross_bps.mean()
        dn = g.groupby("day").net_bps.mean()
        a, b = g[g.day < cut], g[g.day >= cut]
        tn, tg = tstat(dn), tstat(dg)
        na, nb = a.net_bps.mean(), b.net_bps.mean()
        if np.isfinite(tn) and tn >= 2.6 and na > 0 and nb > 0:
            v = "PASS"
        elif np.isfinite(tg) and tg >= 2 and g.net_bps.mean() > 0:
            v = "CANDIDATE"
        else:
            v = "REJECT"
        out.append({"rule": rule, "trades": len(g), "days": g.day.nunique(), "gross_bps": g.gross_bps.mean(),
                    "net_bps": g.net_bps.mean(), "t_gross": tg, "t_net": tn, "hit_rate_net": (g.net_bps > 0).mean(),
                    "net_first60": na, "net_last40": nb, "net_at_1bp_side": g.gross_bps.mean() - 2, "verdict": v})
    return pd.DataFrame(out).sort_values("t_gross", ascending=False)


def long_history_mkt_momentum(raw1h):
    """R4 on two years of hourly bars: prior close -> 10:30 sign predicts the 15:30-16:00 bar."""
    rows = []
    for s in ("SPY", "QQQ"):
        x = clean(raw1h, [s]).get(s)
        if x is None:
            continue
        x["day"] = x.index.normalize()
        pc = x.groupby("day").c.last().shift(1)
        for d, g in x.groupby("day"):
            a = g[g.index.hour == 9]
            z = g[(g.index.hour == 15) & (g.index.minute == 30)]
            if a.empty or z.empty or not np.isfinite(pc.get(d, np.nan)):
                continue
            side = int(np.sign(a.c.iloc[0] / pc[d] - 1))
            if side:
                rows.append(("R4_mkt_momentum_2y_1h", s, d, 15, 30, side, side * (z.c.iloc[0] / z.o.iloc[0] - 1) * 1e4))
    return pd.DataFrame(rows, columns=["rule", "sym", "day", "hour", "minute", "side", "gross_bps"])


def main(p5, p1h, out_dir, reuse=False):
    if reuse and (out_dir / "intraday_events.csv.gz").exists():
        ev = pd.read_csv(out_dir / "intraday_events.csv.gz", parse_dates=["day"])
        s = summarize(ev)
        s.to_csv(out_dir / "intraday_backtest.csv", index=False)
        with pd.option_context("display.width", 220, "display.max_columns", 20):
            print(s.round(2).to_string(index=False))
        return s
    raw = pd.read_pickle(p5)
    tick = list(watchlist().ticker) + ["SPY", "QQQ"]
    X = clean(raw, tick)
    F = {s: features(x) for s, x in X.items()}
    ev = events(F, F["SPY"])
    if p1h and Path(p1h).exists():
        ev = pd.concat([ev, long_history_mkt_momentum(pd.read_pickle(p1h))], ignore_index=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    ev.to_csv(out_dir / "intraday_events.csv.gz", index=False)
    s = summarize(ev)
    s.to_csv(out_dir / "intraday_backtest.csv", index=False)
    by_hour = ev.assign(net_bps=ev.gross_bps - 2 * COST_BPS).pivot_table(index="rule", columns="hour", values="net_bps", aggfunc="mean")
    by_hour.to_csv(out_dir / "intraday_by_hour.csv")
    d0, d1 = min(ev.day), max(ev.day)
    print(f"{len(X)} symbols, {ev.day.nunique()} days ({str(d0)[:10]} -> {str(d1)[:10]}), {len(ev)} events")
    with pd.option_context("display.width", 200, "display.max_columns", 20):
        print(s.round(2).to_string(index=False))
        print(by_hour.round(1).to_string())
    return s


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1] if len(a) > 1 and not a[1].startswith("--") else None,
         Path(__file__).resolve().parents[2] / "experiments" / "results", reuse="--reuse" in a)
