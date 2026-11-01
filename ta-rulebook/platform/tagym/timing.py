"""Index / ETF market-timing tests (no survivorship bias: indices & ETFs)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .data import DATA_DIR, load
from .evaluate import perf_stats, COST_PER_SIDE


def long_index():
    c = pd.read_parquet(DATA_DIR / "long_Close.parquet")
    irx = pd.read_parquet(DATA_DIR / "irx.parquet").iloc[:, 0].reindex(c.index).ffill()
    rf = (irx / 100 / 252).fillna(0.0)  # T-bill daily yield (0 before 1960 -> conservative)
    return c, rf


def run_state(close: pd.Series, pos: pd.Series, rf: pd.Series, lag=1, cost=COST_PER_SIDE, start=None, end=None):
    r = close.pct_change(fill_method=None).fillna(0)
    p = pos.astype(float).shift(lag).fillna(0)
    turn = p.diff().abs().fillna(0)
    strat = p * r + (1 - p) * rf - turn * cost
    sl = slice(start, end)
    s, b = strat.loc[sl], r.loc[sl]
    out = {**perf_stats(s, "timing"), **perf_stats(b, "buyhold"),
           "exposure": float(p.loc[sl].mean()), "switches_per_yr": float(turn.loc[sl].sum() / (len(s) / 252))}
    # crash avoidance: worst 1% of buy-and-hold days — fraction spent in the market
    worst = b <= b.quantile(0.01)
    out["in_mkt_on_worst1pct_days"] = float(p.loc[sl][worst].mean())
    return out


def monthly_sma_pos(close: pd.Series, n=10):
    m = close.resample("ME").last()
    sig = (m > m.rolling(n).mean()).astype(float)
    # decided at month-end close, effective from next trading day
    return sig.reindex(close.index, method="ffill").fillna(0)


def daily_sma_pos(close, n=200, band=0.0):
    s = close.rolling(n).mean()
    return (close > s * (1 + band)).astype(float)


def cross_pos(close, f=50, s=200):
    return (close.rolling(f).mean() > close.rolling(s).mean()).astype(float)


def tsmom_pos(close, n=252):
    return (close / close.shift(n) - 1 > 0).astype(float)
