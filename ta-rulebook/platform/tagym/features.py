"""Cached feature store over a price panel."""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import indicators as ind


class Ctx:
    def __init__(self, panel: dict, market: pd.DataFrame | None = None):
        self.p = panel
        self.o, self.h, self.l, self.c, self.v = (panel[k] for k in ["Open", "High", "Low", "Close", "Volume"])
        self.tradeable = panel["tradeable"]
        self._cache = {}
        self.market = market  # ETF/index panel Close (dates x symbols)

    def get(self, key, fn):
        if key not in self._cache:
            self._cache[key] = fn()
        return self._cache[key]

    # --- common features
    def sma(self, n): return self.get(("sma", n), lambda: ind.sma(self.c, n))
    def ema(self, n): return self.get(("ema", n), lambda: ind.ema(self.c, n))
    def rsi(self, n=14): return self.get(("rsi", n), lambda: ind.rsi(self.c, n))
    def atr(self, n=14): return self.get(("atr", n), lambda: ind.atr(self.h, self.l, self.c, n))
    def natr(self, n=14): return self.get(("natr", n), lambda: self.atr(n) / self.c)
    def adx(self, n=14): return self.get(("adx", n), lambda: ind.adx(self.h, self.l, self.c, n))
    def macd(self): return self.get("macd", lambda: ind.macd(self.c))
    def bb(self, n=20, k=2.0): return self.get(("bb", n, k), lambda: ind.bollinger(self.c, n, k))
    def stoch(self): return self.get("stoch", lambda: ind.stochastic(self.h, self.l, self.c))
    def volr(self, n=50): return self.get(("volr", n), lambda: ind.vol_ratio(self.v, n))
    def hi(self, n): return self.get(("hi", n), lambda: ind.donchian_prior(self.h, self.l, n)[0])
    def lo(self, n): return self.get(("lo", n), lambda: ind.donchian_prior(self.h, self.l, n)[1])
    def chi(self, n): return self.get(("chi", n), lambda: self.c.shift(1).rolling(n, min_periods=n).max())
    def clo(self, n): return self.get(("clo", n), lambda: self.c.shift(1).rolling(n, min_periods=n).min())
    def roc(self, n): return self.get(("roc", n), lambda: ind.roc(self.c, n))
    def ret1(self): return self.get("ret1", lambda: self.c.pct_change(fill_method=None))
    def candles(self): return self.get("candles", lambda: ind.candles(self.o, self.h, self.l, self.c))
    def rvol(self, n=20): return self.get(("rvol", n), lambda: ind.realized_vol(self.c, n))
    def clv(self): return self.get("clv", lambda: ind.close_location(self.h, self.l, self.c))
    def obv(self): return self.get("obv", lambda: ind.obv(self.c, self.v))
    def cmf(self, n=20): return self.get(("cmf", n), lambda: ind.cmf(self.h, self.l, self.c, self.v, n))
    def mom121(self): return self.get("mom121", lambda: ind.mom_12_1(self.c))
    def swings(self, k=5): return self.get(("swings", k), lambda: ind.swing_points(self.h, self.l, k))

    def xs_rank(self, df):
        """Cross-sectional percentile rank among tradeable names (0..1)."""
        return df.where(self.tradeable).rank(axis=1, pct=True)

    # --- market regime (broadcast to the stock panel)
    def mkt(self, sym="SPY"):
        return self.market[sym].reindex(self.c.index).ffill()

    def bcast(self, s: pd.Series):
        return pd.DataFrame(np.repeat(s.values[:, None], self.c.shape[1], axis=1),
                            index=self.c.index, columns=self.c.columns)

    def mkt_up(self, n=200, sym="SPY"):
        def f():
            m = self.mkt(sym)
            return self.bcast((m > m.rolling(n).mean()).astype(float)).astype(bool)
        return self.get(("mkt_up", n, sym), f)

    def vix(self):
        return self.get("vix", lambda: self.bcast(self.mkt("^VIX")))

    def breadth(self, n=200):
        return self.get(("breadth", n), lambda: self.bcast(ind.breadth_above(self.c, n, self.tradeable)))

    def rs(self, n=126, sym="SPY"):
        return self.get(("rs", n, sym), lambda: ind.relative_strength(self.c, self.mkt(sym), n))
