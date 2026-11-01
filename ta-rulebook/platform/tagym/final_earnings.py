"""ONE-TIME locked test of the earnings additions (flag + 4 drift rules), frozen as specified
in experiments/ITERATION_LOG.md #63-#64 before unlocking."""
import sys
import numpy as np
import pandas as pd
from .run import get_ctx, period_mask, evaluate, fmt, ROOT
from .earnings import upcoming_flag
from .earn_rules import RULES, events
from .rulebook_engine import classify_panel, V21
from .diagnose import fwd_min_return

KEY = ["earn_gap_up_vol", "earn_gap_down_vol", "earn_ear_bottom_decile", "earn_surprise_pos10"]
group = sys.argv[1]
x = get_ctx(group, unlock=True)
periods = ["test"] if group == "A" else ["train", "valid", "test"]
fm10 = fwd_min_return(x.p, 10); up = upcoming_flag(x, 10); cls = classify_panel(x, V21)
samp = x.bcast(pd.Series(np.arange(len(x.c)) % 5 == 0, index=x.c.index).astype(float)).astype(bool)
rows = []
for p in periods:
    m = (period_mask(x, p, unlock=True, note=f"FINAL earnings flag {group}") & x.tradeable & samp).values
    for lab in ["BULLISH", "NO_SIGNAL", "BEARISH"]:
        for fl, cond in [("earnings_in_next_10d", up.values), ("no_earnings_next_10d", ~up.values)]:
            mm = m & cls[lab].values & cond
            rows.append(dict(group=group, period=p, cls=lab, flag=fl, obs=int(mm.sum()),
                             p_drop10_10d=float(np.nanmean(fm10.values[mm] <= -0.10))))
pd.DataFrame(rows).to_csv(ROOT / "experiments" / "results" / f"final_earnings_flag_{group}.csv", index=False)
print(pd.DataFrame(rows).pivot_table(index=["cls", "flag"], columns="period", values="p_drop10_10d").round(4).to_string())
for p in periods:
    for nm in KEY:
        dr, h, _ = RULES[nm]
        print(fmt(evaluate(nm, p, group=group, events=events(x, nm), direction=dr, horizon=h, unlock=True, note=f"FINAL earnings {group}"))[:250], flush=True)
