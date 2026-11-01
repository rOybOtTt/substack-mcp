"""Fast 'market shock' overlays for the regime layer (designed on 2000-2019 only).

Each candidate returns a boolean Series (known at the close of t): True = SHOCK.
Under SHOCK the rulebook treats the regime as RISK_OFF (no BULLISH). A shock
persists for `hold` trading days after the last trigger.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def _hold(trig: pd.Series, hold: int) -> pd.Series:
    return trig.astype(float).rolling(hold, min_periods=1).max().astype(bool)


def candidates(spy: pd.Series, vix: pd.Series, hold=10):
    spy = spy.dropna(); vix = vix.reindex(spy.index).ffill()
    r = spy.pct_change()
    rv20 = r.rolling(20).std() * np.sqrt(252)
    dd20 = spy / spy.rolling(20).max() - 1
    c = {
        "vix_ge_30": vix >= 30,
        "vix_spike_50pct_5d": (vix / vix.shift(5) - 1 >= 0.5) & (vix >= 20),
        "spy_dd_7pct_20d": dd20 <= -0.07,
        "spy_dd_10pct_20d": dd20 <= -0.10,
        "rv20_ge_30": rv20 >= 0.30,
        "vix_spike_or_dd7": ((vix / vix.shift(5) - 1 >= 0.5) & (vix >= 20)) | (dd20 <= -0.07),
    }
    return {k: _hold(v.fillna(False), hold) for k, v in c.items()}
