"""Turn the experiment ledger into markdown tables."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .run import ledger


def pct(x):
    return "" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x*100:+.2f}%"


def num(x, f="{:+.2f}"):
    return "" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f.format(x)


def compare_table(note=None, periods=("train", "valid"), rules=None):
    d = ledger()
    if note is not None:
        d = d[d.note == note]
    if rules is not None:
        d = d[d.rule.isin(rules)]
    d = d.drop_duplicates(["rule", "period"], keep="last")
    rows = []
    for rule, g in d.groupby("rule", sort=False):
        r = {"rule": rule}
        first = g.iloc[0]
        h = int(first.horizon)
        r["family"] = first.family
        r["dir"] = "bull" if first.direction > 0 else "bear"
        r["h"] = h
        for p in periods:
            gp = g[g.period == p]
            if gp.empty:
                continue
            x = gp.iloc[-1]
            r[f"{p}_N"] = int(x.n_events) if pd.notna(x.n_events) else 0
            r[f"{p}_exc"] = x.get(f"exc{h}_mean")
            r[f"{p}_t"] = x.get(f"t{h}")
            r[f"{p}_calT"] = x.get("cal_t")
            r[f"{p}_vmT"] = x.get(f"vm{h}_t")
            r[f"{p}_hit"] = x.get(f"hit{h}")
            r[f"{p}_v"] = x.verdict
        rows.append(r)
    return pd.DataFrame(rows)


def to_md(df, periods=("train", "valid")):
    hdr = ["Rule", "Family", "Claim", "h"]
    for p in periods:
        hdr += [f"{p} N", f"{p} excess", f"{p} t (event/cal/vol-matched)", f"{p} hit", f"{p} verdict"]
    lines = ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
    for _, r in df.iterrows():
        cells = [f"`{r['rule']}`", r["family"], r["dir"], str(r["h"])]
        for p in periods:
            if f"{p}_v" not in r or pd.isna(r.get(f"{p}_v")):
                cells += [""] * 5
                continue
            cells += [str(r[f"{p}_N"]), pct(r[f"{p}_exc"]),
                      f"{num(r[f'{p}_t'])} / {num(r[f'{p}_calT'])} / {num(r[f'{p}_vmT'])}",
                      "" if pd.isna(r[f"{p}_hit"]) else f"{r[f'{p}_hit']*100:.1f}%", f"**{r[f'{p}_v']}**"]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)
