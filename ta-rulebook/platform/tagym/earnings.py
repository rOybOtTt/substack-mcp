"""Earnings-aware tests (EODHD earnings calendar 2000-2026).

* load_events(ctx): per-stock earnings events mapped to the trading calendar.
  Reaction window = trading days [d-1, d+1] around the report date d (covers both
  before-open and after-close releases). EAR = C(d+1)/C(d-2) - 1, and its excess
  over the equal-weight universe. Signal known at the close of d+1; trading starts
  at the next open (d+2), so nothing uses future data.
* upcoming_flag(ctx, k): True on day t if a report date falls in (t, t+k] trading
  days. Report dates are scheduled weeks ahead, so this is known in practice
  (TradingView's earnings calendar supplies the next date live).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .data import DATA_DIR

EARN_CSV = DATA_DIR.parent / "earnings_raw" / "us_earnings.csv"


def raw():
    d = pd.read_csv(EARN_CSV, parse_dates=["report_date"])
    return d.dropna(subset=["report_date"]).drop_duplicates(["ticker", "report_date"])


def _positions(ctx, d):
    idx = ctx.c.index
    cols = {c: i for i, c in enumerate(ctx.c.columns)}
    d = d[d.ticker.isin(cols)].copy()
    d["k"] = d.ticker.map(cols)
    d["t"] = idx.searchsorted(d.report_date.values)  # first trading day >= report date
    d = d[(d.t >= 2) & (d.t < len(idx) - 2)]
    return d


def load_events(ctx):
    def f():
        d = _positions(ctx, raw())
        C, V = ctx.c.values, ctx.v.values
        t, k = d.t.values, d.k.values
        ear = C[t + 1, k] / C[t - 2, k] - 1
        bench = np.nanmean(np.where(ctx.tradeable.values[t], C[t + 1] / C[t - 2] - 1, np.nan), axis=1)
        vr = ctx.volr(50).values
        d["ear"] = ear
        d["ear_exc"] = ear - bench
        d["vol_ratio"] = np.nanmax(np.stack([vr[t, k], vr[t + 1, k]]), axis=0)
        d["surprise"] = pd.to_numeric(d.surprise_pct, errors="coerce")
        d["signal_t"] = t + 1  # known at close of d+1
        return d.reset_index(drop=True)
    return ctx.get("earn_events", f)


def event_panel(ctx, mask_rows: np.ndarray):
    d = load_events(ctx)
    d = d[mask_rows]
    out = np.zeros(ctx.c.shape, bool)
    out[d.signal_t.values, d.k.values] = True
    return pd.DataFrame(out, index=ctx.c.index, columns=ctx.c.columns)


def upcoming_flag(ctx, k=10):
    def f():
        d = _positions(ctx, raw())
        hit = np.zeros(ctx.c.shape, bool)
        hit[d.t.values, d.k.values] = True
        h = pd.DataFrame(hit, index=ctx.c.index, columns=ctx.c.columns).astype(float)
        # earnings within (t, t+k]: rolling sum over the NEXT k days
        fut = h[::-1].rolling(k, min_periods=1).sum()[::-1].shift(-1).fillna(0)
        return fut > 0
    return ctx.get(("earn_upcoming", k), f)
