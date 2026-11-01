"""Dow Theory (Hamilton 1922 / Nelson 1903) as a state machine on two averages."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .patterns import zigzag


def index_trend(close: pd.Series, thr=0.06):
    """Per-average trend from swing structure: +1 after (higher low & close > prior swing high),
    -1 after (lower high & close < prior swing low); holds otherwise. Pivots are causal (confirmed)."""
    c = close.values
    piv = zigzag(c, c, c, np.full(len(c), thr))
    state = np.zeros(len(c))
    cur = 0
    highs, lows = [], []
    pi = 0
    for t in range(len(c)):
        while pi < len(piv) and piv[pi][1] <= t:
            (highs if piv[pi][3] == 1 else lows).append(piv[pi][2]); pi += 1
        if len(highs) >= 1 and len(lows) >= 2:
            if lows[-1] > lows[-2] and c[t] > highs[-1]:
                cur = 1
        if len(lows) >= 1 and len(highs) >= 2:
            if highs[-1] < highs[-2] and c[t] < lows[-1]:
                cur = -1
        state[t] = cur
    return pd.Series(state, index=close.index)


def dow_state(a: pd.Series, b: pd.Series, thr=0.06):
    sa, sb = index_trend(a, thr), index_trend(b, thr)
    st = np.zeros(len(sa)); cur = 0
    for t in range(len(sa)):
        if sa.iat[t] == 1 and sb.iat[t] == 1:
            cur = 1
        elif sa.iat[t] == -1 and sb.iat[t] == -1:
            cur = -1
        st[t] = cur
    return pd.Series(st, index=a.index), sa, sb
