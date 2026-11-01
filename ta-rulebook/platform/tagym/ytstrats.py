"""Backtests of the specific 'claimed win-rate' strategies from top YouTube creators.

Each strategy is run twice on the same dates:
  * SIGNAL  : entries where the creator's trigger fires
  * CONTROL : same number of random entries on the same dates among stocks that
              pass the SAME trend filter (so only the trigger's value is measured)
with identical exit logic. Costs: 10 bps per side.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .indicators import rsi, ema, bollinger, macd, stochastic

COST = 0.001


def sim(x, events, *, stop=None, target_r=None, exit_sig=None, trail_atr=None, max_hold=20,
        limit=None, limit_bars=1, mask=None, max_trades=40000, seed=0):
    O, H, L, C = (x.p[k].values for k in ["Open", "High", "Low", "Close"])
    A = x.atr(20).values
    ev = (events & x.tradeable)
    if mask is not None:
        ev &= mask
    ti, ki = np.nonzero(ev.fillna(False).values)
    rng = np.random.default_rng(seed)
    if len(ti) > max_trades:
        s = rng.choice(len(ti), max_trades, replace=False); ti, ki = ti[s], ki[s]
    S = stop.values if stop is not None else None
    X = exit_sig.values if exit_sig is not None else None
    LM = limit.values if limit is not None else None
    T = len(O)
    out = []
    for t, k in zip(ti, ki):
        if t + max_hold + limit_bars + 2 >= T:
            continue
        # ---- entry
        if LM is not None:
            lv = LM[t, k]; e = np.nan; j0 = None
            for j in range(t + 1, t + 1 + limit_bars):
                if O[j, k] <= lv:
                    e, j0 = O[j, k], j; break
                if L[j, k] <= lv:
                    e, j0 = lv, j; break
            if j0 is None or not np.isfinite(e):
                continue
        else:
            j0 = t + 1; e = O[j0, k]
        if not np.isfinite(e) or e <= 0:
            continue
        st = S[t, k] if S is not None else -np.inf
        if S is not None and (not np.isfinite(st) or st >= e):
            continue
        risk = e - st if S is not None else np.nan
        tg = e + target_r * risk if (target_r and S is not None) else np.inf
        hc = e
        px = np.nan
        end = j0 + max_hold
        j = j0
        while j <= end:
            o, h, l, c = O[j, k], H[j, k], L[j, k], C[j, k]
            if not np.isfinite(c):
                break
            if j > j0 and (o <= st or o >= tg):
                px = o; break
            if l <= st:
                px = st; break
            if h >= tg:
                px = tg; break
            if trail_atr is not None:
                hc = max(hc, c)
                st = max(st, hc - trail_atr * A[j, k]) if np.isfinite(A[j, k]) else st
            if X is not None and X[j, k] and j < end:
                px = O[j + 1, k]; j += 1; break
            j += 1
        if not np.isfinite(px):
            px = C[min(end, T - 1), k]
            j = min(end, T - 1)
        if not np.isfinite(px):
            continue
        ret = px / e - 1 - 2 * COST
        out.append((ret, (px - e) / risk if np.isfinite(risk) and risk > 0 else np.nan, j - j0 + 1))
    a = np.array(out)
    if len(a) < 30:
        return {"trades": len(a)}
    r = a[:, 0]
    wins, losses = r[r > 0], r[r <= 0]
    return {"trades": len(a), "win_rate": float((r > 0).mean()), "avg_ret": float(r.mean()),
            "med_ret": float(np.median(r)), "avg_win": float(wins.mean()) if len(wins) else np.nan,
            "avg_loss": float(losses.mean()) if len(losses) else np.nan,
            "profit_factor": float(wins.sum() / max(1e-9, -losses.sum())),
            "avg_R": float(np.nanmean(a[:, 1])) if np.isfinite(a[:, 1]).any() else np.nan,
            "avg_days": float(a[:, 2].mean()), "ret_per_day": float(r.mean() / a[:, 2].mean())}


def control_events(x, events, filt, seed=1):
    """Same count per date, random stocks from those passing the filter."""
    rng = np.random.default_rng(seed)
    ev = (events & x.tradeable).fillna(False).values
    f = (filt & x.tradeable).fillna(False).values
    out = np.zeros_like(ev)
    for t in np.nonzero(ev.sum(axis=1))[0]:
        cand = np.nonzero(f[t])[0]
        if len(cand):
            out[t, rng.choice(cand, min(len(cand), ev[t].sum()), replace=False)] = True
    return pd.DataFrame(out, index=events.index, columns=events.columns)


def strategies(x):
    c, h, l, o = x.c, x.h, x.l, x.o
    F1 = c > x.sma(200)
    e50, e200 = ema(c, 50), ema(c, 200)
    F2 = (c > e200) & (e50 > e200)
    r10 = rsi(c, 10); r2 = x.rsi(2)
    mid, up, lo, pb, bw = bollinger(c, 20, 2.5)
    ml, ms, mh = x.macd()
    k, d = x.stoch()
    a = x.atr(20)
    low10 = l.rolling(10).min()
    S = {}
    S["YT2_rayner_rsi10_pullback"] = dict(ev=F1 & (r10 < 30) & ~((r10 < 30).shift(1, fill_value=False)), filt=F1,
        kw=dict(exit_sig=r10 > 40, max_hold=10), claim="88% win rate (SPY), 12.29%/yr stocks")
    S["YT3_rayner_bb25_reversion"] = dict(ev=F1 & (c < lo), filt=F1,
        kw=dict(limit=c * 0.97, limit_bars=1, exit_sig=r2 > 50, max_hold=10), claim="66-94% win rate, 15.56%/yr")
    hi200 = c.shift(1).rolling(200).max()
    S["YT4_rayner_200d_breakout_6atr"] = dict(ev=(c > hi200) & ~((c > hi200).shift(1, fill_value=False)), filt=F1,
        kw=dict(stop=c - 6 * a, trail_atr=6, max_hold=250), claim="win 35-50%, payoff>2, 14.51%/yr (futures)")
    S["YT6_tradinglab_macd_200ema"] = dict(ev=(c > e200) & (ml > ms) & (ml.shift(1) <= ms.shift(1)) & (ml < 0) & (ms < 0), filt=c > e200,
        kw=dict(stop=low10, target_r=1.5, max_hold=30), claim="86% win rate")
    k20 = ((k < 20) & (d < 20)).rolling(6).max().astype(bool)
    trig = k20 & (x.rsi(14) > 50) & (ml > ms)
    S["YT7_datatrader_stoch_rsi_macd"] = dict(ev=trig & ~trig.shift(1, fill_value=False), filt=pd.DataFrame(True, index=c.index, columns=c.columns),
        kw=dict(stop=low10, target_r=1.5, max_hold=30), claim="'Proven 100x'")
    body = (c - o).abs()
    mid_bull = (c.shift(1) > o.shift(1)) & (body.shift(1) >= a.shift(1)) & (((c.shift(1) - l.shift(1)) / (h.shift(1) - l.shift(1))) >= 0.75)
    fvg = (l > h.shift(2)) & mid_bull & ((l - h.shift(2)) >= 0.25 * a) & (c > x.sma(50))
    S["YT17_ict_fvg_retrace"] = dict(ev=fvg, filt=c > x.sma(50),
        kw=dict(limit=(l + h.shift(2)) / 2, limit_bars=10, stop=l.shift(1) - 0.1 * a, target_r=2, max_hold=30),
        claim="ICT FVG: popular, no published stats")
    low20 = l.shift(1).rolling(20).min()
    sweep = (l < low20 - 0.1 * a) & (c > low20) & (c > o) & F2
    S["YT20_ict_liquidity_sweep"] = dict(ev=sweep, filt=F2, kw=dict(stop=l - 0.1 * a, target_r=2, max_hold=30),
        claim="ICT/TJR sweep reversal; Silver Bullet 55-65% at 1:3 (unofficial)")
    s50 = x.sma(50)
    pb50 = (s50 > x.sma(200)) & (l <= s50) & (c > s50) & (c.shift(5) > s50.shift(5) * 1.03)
    S["YT14_50ma_pullback"] = dict(ev=pb50 & ~pb50.shift(1, fill_value=False), filt=s50 > x.sma(200),
        kw=dict(stop=c - 2 * x.atr(14), exit_sig=c < s50 * 0.97, max_hold=60), claim="'catch the wave' pullback")
    return S
