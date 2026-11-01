"""Rule library: every popular TA claim, encoded as an event detector.

Each Rule: fn(ctx) -> bool DataFrame (True on the bar the signal fires),
direction (+1 = claimed bullish, -1 = claimed bearish), the horizon the
source implies, the family, and where the belief comes from.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np
import pandas as pd


def cross_up(a, b):
    return (a > b) & (a.shift(1) <= b.shift(1))


def cross_dn(a, b):
    return (a < b) & (a.shift(1) >= b.shift(1))


def first_in(x: pd.DataFrame, cooldown=20):
    """Keep only the first True per `cooldown` bars (de-duplicate clustered fires)."""
    x = x.fillna(False).astype(bool)
    prior = x.shift(1).rolling(cooldown, min_periods=1).max().fillna(0).astype(bool)
    return x & ~prior


@dataclass
class Rule:
    name: str
    fn: Callable
    direction: int = 1
    horizon: int = 20
    family: str = ""
    source: str = ""
    params: dict = field(default_factory=dict)


R: dict[str, Rule] = {}


def rule(name, direction=1, horizon=20, family="", source=""):
    def deco(fn):
        R[name] = Rule(name, fn, direction, horizon, family, source)
        return fn
    return deco


# ------------------------------------------------------------ TREND / MA
@rule("golden_cross", 1, 60, "trend", "Popular YouTube/Investopedia: SMA50 crosses above SMA200")
def _(x): return cross_up(x.sma(50), x.sma(200))

@rule("death_cross", -1, 60, "trend", "SMA50 crosses below SMA200 = bearish")
def _(x): return cross_dn(x.sma(50), x.sma(200))

@rule("price_cross_above_sma200", 1, 60, "trend", "Close crosses above 200-day SMA (Granville/Faber)")
def _(x): return first_in(cross_up(x.c, x.sma(200)), 20)

@rule("price_cross_below_sma200", -1, 60, "trend", "Close crosses below 200-day SMA = sell")
def _(x): return first_in(cross_dn(x.c, x.sma(200)), 20)

@rule("ma_stack_bull", 1, 60, "trend", "C>SMA50>SMA150>SMA200 & SMA200 rising (Minervini partial), monthly sample")
def _(x):
    s50, s150, s200 = x.sma(50), x.sma(150), x.sma(200)
    st = (x.c > s50) & (s50 > s150) & (s150 > s200) & (s200 > s200.shift(21))
    return st & _month_end(x)

@rule("trend_template", 1, 60, "trend", "Minervini Trend Template (all 8 criteria), monthly sample")
def _(x): return trend_template(x) & _month_end(x)

@rule("ema_9_21_cross", 1, 20, "trend", "YouTube day/swing traders: EMA9 crosses above EMA21")
def _(x): return cross_up(x.ema(9), x.ema(21))

@rule("ema_20_50_cross", 1, 40, "trend", "EMA20 crosses above EMA50")
def _(x): return cross_up(x.ema(20), x.ema(50))

@rule("weinstein_stage2_breakout", 1, 60, "trend", "Weinstein: close crosses above rising 30-wk(150d) SMA, vol>=2x, RS>0")
def _(x):
    s = x.sma(150)
    return first_in(cross_up(x.c, s) & (s >= s.shift(10)) & (x.volr() >= 2.0) & (x.rs(126) > 0), 40)

@rule("stage4_breakdown", -1, 60, "trend", "Weinstein: close crosses below falling 150d SMA on volume")
def _(x):
    s = x.sma(150)
    return first_in(cross_dn(x.c, s) & (s <= s.shift(10)) & (x.volr() >= 1.5), 40)

# ------------------------------------------------------------- BREAKOUT
@rule("high_52w_breakout", 1, 60, "breakout", "Close above prior 252-day high (Livermore/O'Neil/Darvas)")
def _(x): return first_in(x.c > x.hi(252), 20)

@rule("high_52w_breakout_vol", 1, 60, "breakout", "52-wk high breakout on volume >=1.5x 50d avg (O'Neil)")
def _(x): return first_in((x.c > x.hi(252)) & (x.volr() >= 1.5), 20)

@rule("low_52w_breakdown", -1, 60, "breakout", "Close below prior 252-day low = bearish")
def _(x): return first_in(x.c < x.lo(252), 20)

@rule("donchian20_breakout", 1, 20, "breakout", "Turtle System 1: close above 20-day high")
def _(x): return first_in(x.c > x.hi(20), 10)

@rule("donchian55_breakout", 1, 40, "breakout", "Turtle System 2: close above 55-day high")
def _(x): return first_in(x.c > x.hi(55), 20)

@rule("base_breakout", 1, 40, "breakout", "Tight 30-day base (range<=15%) then close>base high on vol>=1.5x, above SMA200")
def _(x):
    hh, ll = x.hi(30), x.lo(30)
    tight = (hh / ll - 1) <= 0.15
    return first_in(tight & (x.c > hh) & (x.volr() >= 1.5) & (x.c > x.sma(200)), 30)

@rule("near_52w_high", 1, 60, "breakout", "George-Hwang: within 5% of 52-wk high, monthly sample")
def _(x):
    return (x.c >= 0.95 * x.c.rolling(252).max()) & _month_end(x)

@rule("far_from_52w_high", -1, 60, "breakout", ">=40% below 52-wk high, monthly sample (anchoring loser)")
def _(x):
    return (x.c <= 0.60 * x.c.rolling(252).max()) & _month_end(x)

@rule("bb_squeeze_breakout", 1, 20, "volatility", "Bollinger squeeze: bandwidth at 6-mo low within 5d, then close > upper band")
def _(x):
    mid, up, lo, pb, bw = x.bb()
    sq = (bw <= bw.rolling(126).min() * 1.05).rolling(5).max().astype(bool)
    return first_in(sq & (x.c > up), 20)

@rule("gap_up_volume", 1, 20, "breakout", "Gap up >=4% on volume >=2x and holds (close>open) - 'gap and go'/earnings gap")
def _(x):
    gap = x.o / x.c.shift(1) - 1
    return (gap >= 0.04) & (x.volr() >= 2.0) & (x.c > x.o)

@rule("gap_down_volume", -1, 20, "breakout", "Gap down >=4% on volume >=2x and closes weak")
def _(x):
    gap = x.o / x.c.shift(1) - 1
    return (gap <= -0.04) & (x.volr() >= 2.0) & (x.c < x.o)

# ------------------------------------------------------------- MOMENTUM
@rule("mom_12_1_top_decile", 1, 21, "momentum", "Jegadeesh-Titman: top decile 12-1 month return, monthly")
def _(x): return (x.xs_rank(x.mom121()) >= 0.9) & _month_end(x)

@rule("mom_12_1_bottom_decile", -1, 21, "momentum", "Bottom decile 12-1 month return, monthly")
def _(x): return (x.xs_rank(x.mom121()) <= 0.1) & _month_end(x)

@rule("rs_top_decile_6m", 1, 21, "momentum", "IBD-style RS: top decile 6-month return vs universe, monthly")
def _(x): return (x.xs_rank(x.roc(126)) >= 0.9) & _month_end(x)

@rule("macd_bull_cross", 1, 20, "momentum", "MACD line crosses above signal line")
def _(x): l, s, hist = x.macd(); return cross_up(l, s)

@rule("macd_bull_cross_below0", 1, 20, "momentum", "MACD bullish cross while MACD<0 (popular 'stronger' variant)")
def _(x): l, s, hist = x.macd(); return cross_up(l, s) & (l < 0)

@rule("macd_bear_cross", -1, 20, "momentum", "MACD line crosses below signal")
def _(x): l, s, hist = x.macd(); return cross_dn(l, s)

@rule("macd_zero_cross", 1, 40, "momentum", "MACD crosses above zero")
def _(x): l, s, hist = x.macd(); return cross_up(l, 0 * l)

@rule("adx_trend_up", 1, 20, "momentum", "Wilder: ADX crosses above 25 with +DI>-DI")
def _(x):
    a, p, n = x.adx()
    return first_in(cross_up(a, 0 * a + 25) & (p > n), 20)

@rule("rsi_cross_50_up", 1, 20, "momentum", "RSI(14) crosses above 50 (momentum regime shift)")
def _(x): r = x.rsi(14); return first_in(cross_up(r, 0 * r + 50), 10)

# ------------------------------------------------------ MEAN REVERSION
@rule("rsi14_oversold", 1, 10, "oscillator", "Classic: RSI(14) crosses below 30 = oversold buy")
def _(x): r = x.rsi(14); return first_in(cross_dn(r, 0 * r + 30), 10)

@rule("rsi14_oversold_exit", 1, 10, "oscillator", "RSI(14) crosses back above 30 from below")
def _(x): r = x.rsi(14); return first_in(cross_up(r, 0 * r + 30), 10)

@rule("rsi14_overbought", -1, 10, "oscillator", "Classic: RSI(14) crosses above 70 = overbought sell")
def _(x): r = x.rsi(14); return first_in(cross_up(r, 0 * r + 70), 10)

@rule("rsi2_connors", 1, 5, "oscillator", "Connors: C>SMA200 and RSI(2)<10")
def _(x): return first_in((x.c > x.sma(200)) & (x.rsi(2) < 10), 5)

@rule("rsi2_connors_nofilter", 1, 5, "oscillator", "RSI(2)<10 without trend filter")
def _(x): return first_in(x.rsi(2) < 10, 5)

@rule("bb_lower_close", 1, 10, "oscillator", "Close below lower Bollinger band = buy (band 'bounce')")
def _(x): mid, up, lo, pb, bw = x.bb(); return first_in(x.c < lo, 10)

@rule("bb_upper_close", -1, 10, "oscillator", "Close above upper Bollinger band = overbought/sell")
def _(x): mid, up, lo, pb, bw = x.bb(); return first_in(x.c > up, 10)

@rule("stoch_oversold_cross", 1, 10, "oscillator", "Lane: %K crosses above %D while both < 20")
def _(x): k, d = x.stoch(); return first_in(cross_up(k, d) & (d < 20), 10)

@rule("stoch_overbought_cross", -1, 10, "oscillator", "%K crosses below %D while both > 80")
def _(x): k, d = x.stoch(); return first_in(cross_dn(k, d) & (d > 80), 10)

@rule("short_term_loser", 1, 5, "reversal", "Bottom decile 5-day return (short-term reversal)")
def _(x): return (x.xs_rank(x.roc(5)) <= 0.1) & _week_end(x)

@rule("short_term_winner", -1, 5, "reversal", "Top decile 5-day return (short-term reversal)")
def _(x): return (x.xs_rank(x.roc(5)) >= 0.9) & _week_end(x)

@rule("pullback_in_uptrend", 1, 10, "reversal", "Uptrend (C>SMA200, SMA50>SMA200) and 3 consecutive down closes")
def _(x):
    d = x.c < x.c.shift(1)
    three = d & d.shift(1, fill_value=False) & d.shift(2, fill_value=False)
    return first_in((x.c > x.sma(200)) & (x.sma(50) > x.sma(200)) & three, 5)

@rule("pullback_to_sma50", 1, 20, "reversal", "Uptrend and low touches SMA50 then closes above it")
def _(x):
    s = x.sma(50)
    return first_in((x.sma(50) > x.sma(200)) & (x.l <= s) & (x.c > s) & (x.c.shift(5) > s.shift(5) * 1.03), 10)

@rule("capitulation_volume", 1, 20, "volume", "Selling climax: down>=4%, vol>=3x, after >=25% drop from 60d high")
def _(x):
    dd = x.c / x.c.rolling(60).max() - 1
    return first_in((x.ret1() <= -0.04) & (x.volr() >= 3) & (dd <= -0.25), 20)

# --------------------------------------------------------------- VOLUME
@rule("volume_thrust_up", 1, 20, "volume", "Up >=4% on vol >=3x, close in top 25% of range (institutional buying)")
def _(x): return first_in((x.ret1() >= 0.04) & (x.volr() >= 3) & (x.clv() >= 0.75), 10)

@rule("volume_thrust_down", -1, 20, "volume", "Down >=4% on vol >=3x, close in bottom 25% (distribution)")
def _(x): return first_in((x.ret1() <= -0.04) & (x.volr() >= 3) & (x.clv() <= 0.25), 10)

@rule("obv_new_high_lead", 1, 20, "volume", "OBV at 60-day high while price is NOT (accumulation divergence)")
def _(x):
    ob = x.obv()
    return first_in((ob >= ob.rolling(60).max()) & (x.c < x.c.rolling(60).max() * 0.97), 20)

@rule("cmf_strong", 1, 20, "volume", "Chaikin Money Flow crosses above +0.20")
def _(x): m = x.cmf(); return first_in(cross_up(m, 0 * m + 0.2), 20)

@rule("breakout_low_volume", 1, 40, "volume", "52w-high breakout on BELOW-average volume (claimed to fail)")
def _(x): return first_in((x.c > x.hi(252)) & (x.volr() < 0.9), 20)

# ----------------------------------------------------------- DIVERGENCE
@rule("rsi_bull_divergence", 1, 20, "divergence", "Price lower 20d low than 20d ago, RSI higher low, RSI<40")
def _(x):
    r = x.rsi(14)
    ll_now = x.c <= x.c.rolling(20).min()
    prev_low = x.c.shift(20).rolling(20).min()
    prev_rsi = r.shift(20).rolling(20).min()
    return first_in(ll_now & (x.c < prev_low) & (r > prev_rsi + 5) & (r < 40), 20)

@rule("rsi_bear_divergence", -1, 20, "divergence", "Price higher 20d high, RSI lower high, RSI>60")
def _(x):
    r = x.rsi(14)
    hh_now = x.c >= x.c.rolling(20).max()
    prev_hi = x.c.shift(20).rolling(20).max()
    prev_rsi = r.shift(20).rolling(20).max()
    return first_in(hh_now & (x.c > prev_hi) & (r < prev_rsi - 5) & (r > 60), 20)

# ------------------------------------------------------- SUPPORT/RESIST
@rule("support_bounce", 1, 20, "sr", "Low within 1.5% of prior 60-120d swing low, close up from it (bounce)")
def _(x):
    sup = x.l.shift(60).rolling(60).min()  # support formed 60-120 bars ago
    touch = (x.l <= sup * 1.015) & (x.l >= sup * 0.985)
    return first_in(touch & (x.c > x.o) & (x.clv() > 0.6), 20)

@rule("support_break", -1, 20, "sr", "Close breaks >2% below prior 60-120d swing low")
def _(x):
    sup = x.l.shift(60).rolling(60).min()
    return first_in(cross_dn(x.c, sup * 0.98), 20)

@rule("resistance_reject", -1, 20, "sr", "High tags prior 60-120d high (within 1.5%) and closes in bottom 30%")
def _(x):
    res = x.h.shift(60).rolling(60).max()
    tag = (x.h >= res * 0.985) & (x.h <= res * 1.015)
    return first_in(tag & (x.clv() < 0.3), 20)

@rule("round_number_breakout", 1, 20, "sr", "Close crosses above a round number (10/25/50/100/...) for the first time in 60d")
def _(x):
    c = x.c
    step = pd.DataFrame(np.where(c < 20, 5, np.where(c < 100, 10, np.where(c < 500, 50, 100))), index=c.index, columns=c.columns)
    lvl = (np.floor(c / step) * step)
    crossed = (c >= lvl) & (c.shift(1) < lvl) & (x.chi(60) < lvl)
    return first_in(crossed, 20)

@rule("fib_618_bounce", 1, 20, "sr", "Uptrend leg >=20% in 60d, pullback to 61.8% retrace (+-2%), bullish close")
def _(x):
    hh = x.h.rolling(40).max()
    ll = x.l.shift(20).rolling(60).min()
    leg = hh / ll - 1
    lvl = hh - 0.618 * (hh - ll)
    near = (x.l <= lvl * 1.02) & (x.l >= lvl * 0.98)
    return first_in((leg >= 0.2) & near & (x.c > x.o) & (x.c > lvl), 20)

# ----------------------------------------------------------- CANDLESTICK
for _nm, _dir in [("bull_engulfing", 1), ("bear_engulfing", -1), ("hammer", 1), ("shooting_star", -1),
                  ("doji_after_down", 1), ("doji_after_up", -1), ("piercing", 1), ("dark_cloud", -1),
                  ("morning_star", 1), ("evening_star", -1), ("three_white_soldiers", 1),
                  ("three_black_crows", -1)]:
    def _mk(nm):
        return lambda x: x.candles()[nm]
    R["cdl_" + _nm] = Rule("cdl_" + _nm, _mk(_nm), _dir, 10, "candlestick", "Nison candlestick pattern (with prior-trend context)")


# --------------------------------------------------------------- helpers
def _month_end(x):
    def f():
        idx = x.c.index
        me = pd.Series(idx.to_period("M"), index=idx)
        last = me != me.shift(-1)
        return x.bcast(last.astype(float)).astype(bool)
    return x.get("month_end", f)


def _week_end(x):
    def f():
        idx = x.c.index
        wk = pd.Series(idx.to_period("W"), index=idx)
        last = wk != wk.shift(-1)
        return x.bcast(last.astype(float)).astype(bool)
    return x.get("week_end", f)


def trend_template(x):
    """Minervini's 8 Trend Template criteria (RS rating approximated by
    cross-sectional percentile of a weighted 3/6/9/12-month return)."""
    def f():
        c = x.c
        s50, s150, s200 = x.sma(50), x.sma(150), x.sma(200)
        hi52 = c.rolling(252).max()
        lo52 = c.rolling(252).min()
        rs_raw = 0.4 * x.roc(63) + 0.2 * x.roc(126) + 0.2 * x.roc(189) + 0.2 * x.roc(252)
        rs_rank = x.xs_rank(rs_raw)
        return ((c > s150) & (c > s200) & (s150 > s200) & (s200 > s200.shift(21)) &
                (s50 > s150) & (s50 > s200) & (c > s50) & (c >= 1.30 * lo52) &
                (c >= 0.75 * hi52) & (rs_rank >= 0.70))
    return x.get("trend_template", f)


# ---------------------------------------------------------- CHART PATTERNS
_PAT_SRC = {
    "pat_double_bottom": (1, 40, "Edwards&Magee/Bulkowski double bottom: close above middle peak"),
    "pat_double_top": (-1, 40, "Double top: close below middle trough"),
    "pat_inv_head_shoulders": (1, 40, "Inverse head & shoulders: close above neckline"),
    "pat_head_shoulders": (-1, 40, "Head & shoulders top: close below neckline"),
    "pat_bull_flag": (1, 20, "Bull flag: >=20% pole in <=15 bars, <=50% retrace, break above pole high"),
    "pat_asc_triangle": (1, 40, "Ascending triangle: flat tops, rising lows, upside breakout"),
    "pat_desc_triangle": (-1, 40, "Descending triangle: flat bottoms, falling highs, downside break"),
    "pat_cup_handle": (1, 60, "O'Neil cup-with-handle: 12-35% cup, handle in upper half, breakout on vol>=1.4x"),
    "pat_vcp": (1, 40, "Minervini VCP: 3 contracting pullbacks, last <=10%, breakout on vol>=1.5x"),
}


def _patterns(x):
    def f():
        from .patterns import detect_all
        return detect_all(x.p, x.natr(14), x.volr(50))
    return x.get("patterns", f)


for _nm, (_d, _h, _src) in _PAT_SRC.items():
    def _mkp(nm):
        return lambda x: _patterns(x)[nm]
    R[_nm] = Rule(_nm, _mkp(_nm), _d, _h, "chart_pattern", _src)
