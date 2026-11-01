"""Diagnostics: break a rule's edge down by sub-period, market regime, and
measure left-tail risk (probability of a >=20% drawdown within 60 days)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .evaluate import forward_returns, universe_benchmark, nw_tstat
from .run import get_ctx, period_mask
from .signals import R


def fwd_min_return(panel, h=60):
    """Worst close over the next h days relative to next open (label only)."""
    c, o = panel["Close"], panel["Open"]
    fut_min = c[::-1].rolling(h, min_periods=1).min()[::-1].shift(-1)
    return fut_min / o.shift(-1) - 1


def breakdown(name=None, events=None, period="train", group="A", h=None, unlock=False):
    ctx = get_ctx(group, unlock=unlock)
    r = R.get(name)
    h = h or (r.horizon if r else 20)
    ev = (events if events is not None else r.fn(ctx)).fillna(False).astype(bool) & ctx.tradeable
    ev &= period_mask(ctx, period, unlock=unlock)
    fr = forward_returns(ctx.p, h)
    exc = fr.sub(universe_benchmark(fr, ctx.tradeable), axis=0).where(ev)
    lo, hi = np.nanquantile(exc.values[ev.values], [0.01, 0.99])
    exc = exc.clip(lo, hi)
    per_date = exc.mean(axis=1)
    cnt = ev.sum(axis=1)
    df = pd.DataFrame({"exc": per_date, "n": cnt})
    df = df[df.n > 0]
    spy = ctx.mkt("SPY")
    up = (spy > spy.rolling(200).mean()).reindex(df.index)
    out = {}
    df["yr"] = df.index.year
    w = lambda g: np.average(g.exc, weights=g.n)
    out["by_year"] = df.groupby("yr").apply(w, include_groups=False).round(4).to_dict()
    out["bull_regime"] = float(w(df[up])) if up.any() else np.nan
    out["bear_regime"] = float(w(df[~up])) if (~up).any() else np.nan
    out["n_bull"] = int(df.n[up].sum()); out["n_bear"] = int(df.n[~up].sum())
    # left tail
    fm = fwd_min_return(ctx.p, 60)
    base = (fm <= -0.20).where(ctx.tradeable & period_mask(ctx, period, unlock=unlock))
    out["p_dd20_event"] = float(np.nanmean((fm <= -0.20).values[ev.values]))
    out["p_dd20_base"] = float(np.nanmean(base.values))
    return out


def state_risk(ctx, states: dict, period="train", h=60, unlock=False):
    """For boolean state panels, compare next-h-day outcomes: mean raw return,
    mean excess, P(max drawdown from entry >= 20%), forward realised vol."""
    mask = period_mask(ctx, period, unlock=unlock) & ctx.tradeable
    fr = forward_returns(ctx.p, h)
    bench = universe_benchmark(fr, ctx.tradeable)
    exc = fr.sub(bench, axis=0)
    fm = fwd_min_return(ctx.p, h)
    lr = np.log(ctx.c).diff()
    fvol = lr[::-1].rolling(h, min_periods=h // 2).std()[::-1].shift(-1) * np.sqrt(252)
    rows = []
    # sample every 5th day to limit overlap
    samp = pd.Series(np.arange(len(ctx.c.index)) % 5 == 0, index=ctx.c.index)
    sm = ctx.bcast(samp.astype(float)).astype(bool)
    for name, st in states.items():
        st = st.reindex_like(mask).fillna(False).astype(bool)
        for lab, m in [(name, st & mask & sm), ("NOT " + name, ~st & mask & sm)]:
            v = m.values
            rows.append({"state": lab, "obs": int(v.sum()),
                         "raw_ret": float(np.nanmean(np.clip(fr.values[v], -0.9, 3))),
                         "excess": float(np.nanmean(np.clip(exc.values[v], -0.9, 3))),
                         "p_dd20": float(np.nanmean(fm.values[v] <= -0.20)),
                         "p_dd30": float(np.nanmean(fm.values[v] <= -0.30)),
                         "fwd_vol": float(np.nanmean(fvol.values[v]))})
    return pd.DataFrame(rows)
