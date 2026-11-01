"""Vectorised indicators. Every function takes/returns DataFrames shaped
(dates x tickers) and uses ONLY information available at the close of each
bar (no look-ahead). Swing-pivot detectors are explicitly lagged by their
confirmation window.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


# ---------------------------------------------------------------- basics
def sma(x, n):
    return x.rolling(n, min_periods=n).mean()


def ema(x, n):
    return x.ewm(span=n, adjust=False, min_periods=n).mean()


def wilder(x, n):
    return x.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()


def roc(c, n):
    return c / c.shift(n) - 1.0


def true_range(h, l, c):
    pc = c.shift(1)
    return np.maximum(h - l, np.maximum((h - pc).abs(), (l - pc).abs()))


def atr(h, l, c, n=14):
    return wilder(true_range(h, l, c), n)


def rsi(c, n=14):
    d = c.diff()
    up = wilder(d.clip(lower=0), n)
    dn = wilder((-d).clip(lower=0), n)
    rs = up / dn.replace(0, np.nan)
    out = 100 - 100 / (1 + rs)
    return out.where(dn != 0, 100.0).where(up.notna())


def macd(c, fast=12, slow=26, signal=9):
    line = ema(c, fast) - ema(c, slow)
    sig = line.ewm(span=signal, adjust=False, min_periods=signal).mean()
    return line, sig, line - sig


def bollinger(c, n=20, k=2.0):
    mid = sma(c, n)
    sd = c.rolling(n, min_periods=n).std(ddof=0)
    up, lo = mid + k * sd, mid - k * sd
    pctb = (c - lo) / (up - lo)
    bw = (up - lo) / mid
    return mid, up, lo, pctb, bw


def stochastic(h, l, c, n=14, smooth=3):
    hh = h.rolling(n, min_periods=n).max()
    ll = l.rolling(n, min_periods=n).min()
    k = 100 * (c - ll) / (hh - ll).replace(0, np.nan)
    k = k.rolling(smooth).mean()
    d = k.rolling(3).mean()
    return k, d


def adx(h, l, c, n=14):
    up = h.diff()
    dn = -l.diff()
    pdm = up.where((up > dn) & (up > 0), 0.0)
    ndm = dn.where((dn > up) & (dn > 0), 0.0)
    tr = wilder(true_range(h, l, c), n)
    pdi = 100 * wilder(pdm, n) / tr
    ndi = 100 * wilder(ndm, n) / tr
    dx = 100 * (pdi - ndi).abs() / (pdi + ndi).replace(0, np.nan)
    return wilder(dx, n), pdi, ndi


def obv(c, v):
    return (np.sign(c.diff()).fillna(0) * v).cumsum()


def donchian_prior(h, l, n):
    """Highest high / lowest low of the PRIOR n bars (excludes today)."""
    return h.shift(1).rolling(n, min_periods=n).max(), l.shift(1).rolling(n, min_periods=n).min()


def vol_ratio(v, n=50):
    return v / v.shift(1).rolling(n, min_periods=n).mean()


def realized_vol(c, n=20):
    return np.log(c).diff().rolling(n, min_periods=n).std() * np.sqrt(252)


def pct_from_high(c, n=252):
    return c / c.rolling(n, min_periods=n).max() - 1.0


def mom_12_1(c):
    return c.shift(21) / c.shift(252) - 1.0


def mfi(h, l, c, v, n=14):
    tp = (h + l + c) / 3
    mf = tp * v
    pos = mf.where(tp > tp.shift(1), 0.0).rolling(n).sum()
    neg = mf.where(tp < tp.shift(1), 0.0).rolling(n).sum()
    return 100 - 100 / (1 + pos / neg.replace(0, np.nan))


def cmf(h, l, c, v, n=20):
    mfm = ((c - l) - (h - c)) / (h - l).replace(0, np.nan)
    return (mfm * v).rolling(n).sum() / v.rolling(n).sum()


def close_location(h, l, c):
    """0 = closed on the low, 1 = closed on the high."""
    return (c - l) / (h - l).replace(0, np.nan)


# ------------------------------------------------------------ candlesticks
def candles(o, h, l, c, trend_n=10):
    """Classic Nison patterns. Returns dict name -> bool DataFrame.
    'Context' (prior trend) is required, per Nison: a reversal pattern only
    counts after a decline (bullish) / advance (bearish) over trend_n bars.
    """
    body = (c - o).abs()
    rng = (h - l).replace(0, np.nan)
    upper = h - np.maximum(o, c)
    lower = np.minimum(o, c) - l
    bull = c > o
    bear = c < o
    avg_body = body.rolling(20).mean()
    down_ctx = c.shift(1) < c.shift(trend_n + 1) * 0.97
    up_ctx = c.shift(1) > c.shift(trend_n + 1) * 1.03
    po, pc, ph, pl = o.shift(1), c.shift(1), h.shift(1), l.shift(1)
    pbody = body.shift(1)
    out = {}
    out["bull_engulfing"] = down_ctx & bull & (pc < po) & (c >= po) & (o <= pc) & (body > pbody)
    out["bear_engulfing"] = up_ctx & bear & (pc > po) & (o >= pc) & (c <= po) & (body > pbody)
    out["hammer"] = down_ctx & (lower >= 2 * body) & (upper <= 0.3 * body + 0.1 * rng) & (body > 0.05 * rng)
    out["shooting_star"] = up_ctx & (upper >= 2 * body) & (lower <= 0.3 * body + 0.1 * rng) & (body > 0.05 * rng)
    out["doji_after_down"] = down_ctx & (body <= 0.1 * rng)
    out["doji_after_up"] = up_ctx & (body <= 0.1 * rng)
    mid_prev = (po + pc) / 2
    out["piercing"] = down_ctx & (pc < po) & (pbody > avg_body) & bull & (o < pl) & (c > mid_prev) & (c < po)
    out["dark_cloud"] = up_ctx & (pc > po) & (pbody > avg_body) & bear & (o > ph) & (c < mid_prev) & (c > po)
    # three-bar stars
    b2 = body.shift(1)
    o3, c3 = o.shift(2), c.shift(2)
    big3_down = (c3 < o3) & (body.shift(2) > avg_body.shift(2))
    big3_up = (c3 > o3) & (body.shift(2) > avg_body.shift(2))
    small2 = b2 < 0.5 * avg_body.shift(1)
    out["morning_star"] = down_ctx.shift(2, fill_value=False) & big3_down & small2 & bull & (c > (o3 + c3) / 2)
    out["evening_star"] = up_ctx.shift(2, fill_value=False) & big3_up & small2 & bear & (c < (o3 + c3) / 2)
    w = bull & (body > 0.6 * rng)
    out["three_white_soldiers"] = w & w.shift(1, fill_value=False) & w.shift(2, fill_value=False) & (c > pc) & (pc > c.shift(2)) & down_ctx.shift(2, fill_value=False)
    k = bear & (body > 0.6 * rng)
    out["three_black_crows"] = k & k.shift(1, fill_value=False) & k.shift(2, fill_value=False) & (c < pc) & (pc < c.shift(2)) & up_ctx.shift(2, fill_value=False)
    return {n: x.fillna(False).astype(bool) for n, x in out.items()}


# ------------------------------------------------------------ swing pivots
def swing_points(h, l, k=5):
    """Fractal pivots: a swing high at t-k is CONFIRMED at t (k bars later).
    Returns (sh_conf, sl_conf): DataFrames that, at confirmation date t, hold
    the pivot price (else NaN). Using confirmation dates avoids look-ahead.
    """
    win = 2 * k + 1
    hmax = h.rolling(win, min_periods=win).max()
    lmin = l.rolling(win, min_periods=win).min()
    cand_h = h.shift(k)
    cand_l = l.shift(k)
    sh = cand_h.where(cand_h >= hmax)
    sl = cand_l.where(cand_l <= lmin)
    return sh, sl


def last_n_pivots(piv: pd.DataFrame, n=3):
    """For each date, the values of the last n confirmed pivots (most recent first)."""
    out = []
    cur = piv.ffill()
    out.append(cur)
    mask = piv.notna()
    # value before the latest pivot: shift the pivot series by one event
    vals = piv.copy()
    for i in range(1, n):
        # previous pivot = forward-filled value as of the day before the latest pivot event
        prev = cur.shift(1).where(mask)  # at a pivot day, the prior pivot value
        prev = prev.ffill()
        out.append(prev)
        cur = prev
        mask = mask  # same event days
    return out


# --------------------------------------------------------- regime features
def breadth_above(c, n=200, tradeable=None):
    above = (c > sma(c, n))
    valid = sma(c, n).notna()
    if tradeable is not None:
        valid &= tradeable
    return (above & valid).sum(axis=1) / valid.sum(axis=1).replace(0, np.nan)


def relative_strength(c, bench: pd.Series, n=126):
    rel = c.div(bench, axis=0)
    return rel / rel.shift(n) - 1.0
