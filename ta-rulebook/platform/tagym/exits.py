"""Exit / stop-loss rules tested on RANDOM entries (isolates exit effect from entry skill)."""
from __future__ import annotations

import numpy as np
import pandas as pd


def simulate_exits(x, mask, n=40000, max_hold=60, seed=0):
    rng = np.random.default_rng(seed)
    ok = (mask & x.tradeable & x.sma(50).notna()).values.copy()
    ok[-max_hold - 2:, :] = False
    cand = np.argwhere(ok)
    pick = cand[rng.choice(len(cand), min(n, len(cand)), replace=False)]
    O, H, L, C = (x.p[k].values for k in ["Open", "High", "Low", "Close"])
    A = x.atr(14).values
    S50 = x.sma(50).values
    LL20 = x.l.shift(1).rolling(20).min().values
    rules = ["hold60", "stop8pct", "stop2atr", "trail3atr", "close_below_sma50", "close_below_20d_low", "stop8_or_sma50"]
    res = {r: [] for r in rules}
    for t, k in pick:
        e = O[t + 1, k]
        if not np.isfinite(e):
            continue
        a = A[t, k]
        path_c = C[t + 1:t + 1 + max_hold, k]
        path_l = L[t + 1:t + 1 + max_hold, k]
        path_h = H[t + 1:t + 1 + max_hold, k]
        path_o = O[t + 1:t + 1 + max_hold, k]
        if not np.isfinite(path_c).all():
            continue
        def done(r, px): res[r].append(px / e - 1 - 0.002)
        done("hold60", path_c[-1])
        # fixed % stop
        for nm, stop in [("stop8pct", e * 0.92), ("stop2atr", e - 2 * a)]:
            hit = np.nonzero(path_l <= stop)[0]
            if len(hit):
                j = hit[0]; px = min(stop, path_o[j]) if j > 0 else stop
                done(nm, px)
            else:
                done(nm, path_c[-1])
        # 3ATR chandelier trail
        hh = np.maximum.accumulate(path_h)
        trail = hh - 3 * a
        hit = np.nonzero(path_l[1:] <= trail[:-1])[0]
        if len(hit):
            j = hit[0] + 1; done("trail3atr", min(trail[j - 1], path_o[j]))
        else:
            done("trail3atr", path_c[-1])
        for nm, lvl in [("close_below_sma50", S50[t + 1:t + 1 + max_hold, k]), ("close_below_20d_low", LL20[t + 1:t + 1 + max_hold, k])]:
            hit = np.nonzero(path_c[:-1] < lvl[:-1])[0]
            if len(hit):
                j = hit[0]; done(nm, path_o[j + 1])
            else:
                done(nm, path_c[-1])
        hit1 = np.nonzero(path_l <= e * 0.92)[0]; hit2 = np.nonzero(path_c[:-1] < S50[t + 1:t + max_hold, k])[0]
        j1 = hit1[0] if len(hit1) else 10**9; j2 = hit2[0] + 1 if len(hit2) else 10**9
        if j1 == 10**9 and j2 == 10**9:
            done("stop8_or_sma50", path_c[-1])
        elif j1 <= j2:
            done("stop8_or_sma50", min(e * 0.92, path_o[j1]) if j1 > 0 else e * 0.92)
        else:
            done("stop8_or_sma50", path_o[j2])
    rows = []
    for r in rules:
        v = np.array(res[r])
        rows.append({"exit_rule": r, "n": len(v), "mean": v.mean(), "median": np.median(v), "std": v.std(),
                     "worst1pct": np.quantile(v, 0.01), "p_loss_gt20": (v < -0.20).mean(), "win_rate": (v > 0).mean(),
                     "mean_over_std": v.mean() / v.std()})
    return pd.DataFrame(rows)
