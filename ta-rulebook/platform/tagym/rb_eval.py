"""Evaluate the rulebook classifier: outcomes by class (sampled weekly)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .evaluate import forward_returns, universe_benchmark, group_benchmark
from .diagnose import fwd_min_return
from .rulebook_engine import classify_panel
from .run import period_mask


def outcomes(ctx, cls, period, h=60, unlock=False):
    mask = period_mask(ctx, period, unlock=unlock) & ctx.tradeable
    key = ("rb_labels", h)
    if key not in ctx._cache:
        fr = forward_returns(ctx.p, h)
        grp = np.floor(ctx.xs_rank(ctx.natr(14)).clip(0, 0.9999) * 3)
        ctx._cache[key] = (fr, fr.sub(universe_benchmark(fr, ctx.tradeable), axis=0),
                           fr - group_benchmark(fr, ctx.tradeable, grp), fwd_min_return(ctx.p, h))
    fr, exc, vm, fm = ctx._cache[key]
    samp = pd.Series(np.arange(len(ctx.c)) % 5 == 0, index=ctx.c.index)
    sm = ctx.bcast(samp.astype(float)).astype(bool)
    rows = []
    for lab in ["BULLISH", "NO_SIGNAL", "BEARISH"]:
        m = (cls[lab] & mask & sm).values
        per_date = pd.DataFrame(exc.values * np.where(m, 1, np.nan), index=ctx.c.index).mean(axis=1).dropna()
        rows.append({"class": lab, "obs": int(m.sum()), "share": float(m.sum() / max(1, (mask & sm).values.sum())),
                     "raw_ret": float(np.nanmean(np.clip(fr.values[m], -0.9, 3))),
                     "excess": float(np.nanmean(np.clip(exc.values[m], -0.9, 3))),
                     "vm_excess": float(np.nanmean(np.clip(vm.values[m], -0.9, 3))),
                     "excess_t": float(per_date.mean() / per_date.std() * np.sqrt(len(per_date) / (h / 5))),
                     "p_dd20": float(np.nanmean(fm.values[m] <= -0.2)),
                     "worst5pct": float(np.nanquantile(fr.values[m][np.isfinite(fr.values[m])], 0.05))})
    return pd.DataFrame(rows)
