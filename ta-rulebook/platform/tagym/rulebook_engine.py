"""Deterministic implementation of the rulebook's decision procedure.

classify_panel(ctx, params) -> dict of boolean panels:
    BULLISH, BEARISH, NO_SIGNAL plus the intermediate layers
    (regime, health, extension) so each layer can be tested separately.
Parameters are versioned so every fine-tuning iteration is reproducible.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

V1 = dict(
    name="v1",
    healthy_max_from_high=-0.15,   # within 15% of 52w high
    broken_from_high=-0.40,        # >=40% below 52w high
    require_mkt_on_for_bull=True,
    ext_rsi=70, ext_bb=True, ext_st_rank=0.9,
    bear_requires_mkt_off=False,
)


def market_regime(ctx):
    """+1 RISK_ON (10m SMA & 50>200 both up), -1 RISK_OFF (both down), 0 MIXED. Known at t."""
    def f():
        spy = ctx.mkt("SPY")
        m = spy.resample("ME").last()
        ten = (m > m.rolling(10).mean()).astype(float).reindex(spy.index, method="ffill")
        cross = (spy.rolling(50).mean() > spy.rolling(200).mean()).astype(float)
        reg = pd.Series(0.0, index=spy.index)
        reg[(ten == 1) & (cross == 1)] = 1
        reg[(ten == 0) & (cross == 0)] = -1
        return ctx.bcast(reg)
    return ctx.get("mkt_regime", f)


def health(ctx, p):
    c, s50, s200 = ctx.c, ctx.sma(50), ctx.sma(200)
    rising = s200 > s200.shift(21)
    falling = s200 < s200.shift(21)
    d52 = c / c.rolling(252).max() - 1
    healthy = (c > s200) & rising & (s50 > s200) & (d52 >= p["healthy_max_from_high"])
    broken = ((c < s200) & falling) | (d52 <= p["broken_from_high"])
    if p.get("broken_b3"):
        # v2.1 (blind-test feedback): fresh breakdown under a still-rising SMA200
        broken |= (c < s200) & (s50 < s200) & (d52 <= -0.25)
    h = pd.DataFrame(0, index=c.index, columns=c.columns)
    return h.mask(healthy, 1).mask(broken, -1)


def extension(ctx, p):
    r = ctx.rsi(14)
    ext = (r >= p["ext_rsi"])
    if p.get("ext_bb"):
        ext |= ctx.c > ctx.bb()[1]
    if p.get("ext_mode") == "live":
        # single-stock computable: 5-day move > 2.2*ATR%*sqrt(5)  or 5 straight up closes
        ext |= ctx.roc(5) > 2.2 * ctx.natr(14) * np.sqrt(5)
        u = ctx.c > ctx.c.shift(1)
        ext |= u & u.shift(1, fill_value=False) & u.shift(2, fill_value=False) & u.shift(3, fill_value=False) & u.shift(4, fill_value=False)
    elif p.get("ext_st_rank"):
        ext |= ctx.xs_rank(ctx.roc(5)) >= p["ext_st_rank"]
    return ext


def classify_panel(ctx, p=V1):
    reg = market_regime(ctx)
    hl = health(ctx, p)
    ext = extension(ctx, p)
    bull = (hl == 1) & ~ext
    if p["require_mkt_on_for_bull"]:
        bull &= reg == 1
    bear = hl == -1
    if p["bear_requires_mkt_off"]:
        bear &= reg == -1
    valid = ctx.sma(200).notna() & ctx.tradeable
    bull &= valid; bear &= valid
    nos = valid & ~bull & ~bear
    return {"BULLISH": bull, "BEARISH": bear, "NO_SIGNAL": nos, "regime": reg, "health": hl, "extended": ext}


# v2 = fine-tuned on TRAIN only (grid of 18 settings, iteration log #60-#77):
# healthy = within 10% of 52w high maximised risk separation (3.97x train, 3.21x valid).
V2 = dict(V1, name="v2", healthy_max_from_high=-0.10, broken_from_high=-0.40, ext_mode="live")

# v2.1 = v2 + clause B3 (iteration #47, adopted: small improvement in BOTH periods)
V21 = dict(V2, name="v2.1", broken_b3=True)
