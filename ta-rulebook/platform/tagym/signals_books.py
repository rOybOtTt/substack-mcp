"""Rules operationalised from the books (Livermore/Lefevre, Selden, Dow, Wyckoff)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .data import DATA_DIR
from .signals import R, Rule, cross_up, cross_dn, first_in


def reg(name, fn, d, h, fam, src):
    R[name] = Rule(name, fn, d, h, fam, src)


def _sector(x):
    def f():
        u = pd.read_csv(DATA_DIR / "universe.csv").set_index("ticker")["sector"]
        return u.reindex(x.c.columns).fillna("Unknown")
    return x.get("sector", f)


def _group_ret(x, n=63):
    """Equal-weight sector return over n days, broadcast to each stock."""
    def f():
        sec = _sector(x)
        r = x.roc(n).where(x.tradeable)
        out = pd.DataFrame(np.nan, index=r.index, columns=r.columns)
        for s in sec.unique():
            cols = sec.index[sec == s]
            mu = r[cols].mean(axis=1)
            out[cols] = np.repeat(mu.values[:, None], len(cols), axis=1)
        return out
    return x.get(("grp_ret", n), f)


def _mkt_up200(x):
    return x.mkt_up(200)


# H-LIV-1: tight 60-day range (<=15%) then close beyond it, with market trend
def liv_range_breakout(x):
    hh, ll = x.hi(60), x.lo(60)
    tight = (hh / ll - 1) <= 0.15
    return first_in(tight & (x.c > hh) & _mkt_up200(x), 20)


reg("liv_range_breakout", liv_range_breakout, 1, 60, "books", "Livermore H-LIV-1: 60d range<=15% breakout, market up")
reg("liv_range_breakout_nomkt", lambda x: first_in(((x.hi(60) / x.lo(60) - 1) <= 0.15) & (x.c > x.hi(60)), 20),
    1, 60, "books", "H-LIV-1 without market filter (ablation)")


# H-LIV-3: new highs vs 'bargains' in an up market
reg("liv_new_high_upmkt", lambda x: first_in((x.c >= x.c.rolling(252).max()) & _mkt_up200(x), 20), 1, 60, "books",
    "H-LIV-3a: close at 252d high while market up")


def liv_bargain(x):
    d = x.c / x.c.rolling(252).max() - 1
    return first_in((d <= -0.15) & (d >= -0.25) & (x.c > x.sma(200)) & _mkt_up200(x), 20)


reg("liv_bargain_upmkt", liv_bargain, 1, 60, "books", "H-LIV-3b: 15-25% off high but above SMA200 ('looks cheap')")


# H-LIV-5: failed follow-through after a range breakout (bearish)
def liv_failed_follow(x):
    brk = (((x.hi(60) / x.lo(60) - 1) <= 0.15) & (x.c > x.hi(60)))
    lvl = x.c.where(brk)
    a = x.atr(14)
    fired = []
    out = pd.DataFrame(False, index=x.c.index, columns=x.c.columns)
    for k in range(1, 4):
        b = brk.shift(k, fill_value=False)
        L = lvl.shift(k)
        tgt = L + np.maximum(0.03 * L, a.shift(k))
        no_follow = (x.h.rolling(k).max() < tgt)
        back = x.c <= L * 1.003
        if k == 3:
            out |= b & no_follow & back
    return first_in(out, 20)


reg("liv_failed_followthrough", liv_failed_follow, -1, 20, "books", "H-LIV-5: breakout fails to follow through in 3 days")


# H-LIV-7: fallen leaders while the market is near highs (bearish)
def liv_fallen_leader(x):
    leader = x.xs_rank(x.roc(126)).shift(20) >= 0.9
    off = x.c <= x.c.rolling(60).max() * 0.94
    no_new = x.c.rolling(20).max() < x.c.rolling(60).max().shift(20)
    spy = x.mkt("SPY")
    near = x.bcast((spy >= spy.rolling(252).max() * 0.97).astype(float)).astype(bool)
    return first_in(leader & off & no_new & near, 40)


reg("liv_fallen_leader", liv_fallen_leader, -1, 60, "books", "H-LIV-7: former RS leader fails while index near highs")


# H-LIV-8b: laggard in a strong group (bearish); H-LIV-8a leader in strong group (bullish)
def liv_laggard(x):
    g = _group_ret(x, 63)
    gr = x.xs_rank(g)
    return first_in((gr >= 0.67) & (x.roc(63) <= 0) & (x.c <= x.clo(20)), 40)


reg("liv_laggard_strong_group", liv_laggard, -1, 60, "books", "H-LIV-8b: 'Chester' laggard in a top-tercile group")


def leader_strong_group(x):
    g = _group_ret(x, 63)
    gr = x.xs_rank(g)
    within = x.roc(63) - g
    return (gr >= 0.67) & (x.xs_rank(within) >= 0.8) & (x.c > x.sma(50)) & _month_end_(x)


reg("leader_in_strong_group", leader_strong_group, 1, 21, "books", "Livermore/O'Neil: leader of a leading group, monthly")


# H-LIV-11: climax after big advance (bearish)
def liv_climax_top(x):
    big = x.roc(126) >= 0.5
    return first_in(big & (x.volr() >= 3) & (x.clv() >= 0.75) & (x.ret1() > 0), 20)


reg("liv_climax_top", liv_climax_top, -1, 20, "books", "H-LIV-11: buying climax after +50% in 6 months")


# Selden: up-volume vs down-volume
def _updown_vol(x, n=20):
    def f():
        up = x.v.where(x.c > x.c.shift(1)).rolling(n, min_periods=5).mean()
        dn = x.v.where(x.c < x.c.shift(1)).rolling(n, min_periods=5).mean()
        return up / dn
    return x.get(("udv", n), f)


reg("selden_updown_vol_strong", lambda x: first_in(cross_up(_updown_vol(x), 0 * x.c + 1.5) & (x.c > x.sma(50)), 20),
    1, 20, "books", "Selden: up-day volume >= 1.5x down-day volume (accumulation)")


def selden_distribution(x):
    near_hi = x.c >= x.c.rolling(252).max() * 0.95
    return first_in(cross_dn(_updown_vol(x), 0 * x.c + 0.7) & near_hi, 20)


reg("selden_distribution_near_high", selden_distribution, -1, 20, "books",
    "Selden: near highs, down-day volume dominates (distribution)")


def _month_end_(x):
    from .signals import _month_end
    return _month_end(x)


# ============================== WYCKOFF (Studies in Tape Reading, 1910) =====
def _rng_pct(x, n=20):
    return x.get(("rngpct", n), lambda: (x.h.rolling(n).max() - x.l.rolling(n).min()) / x.c)


def wyc_dull_breakout(x):
    rp = _rng_pct(x, 20).shift(1)
    low_rng = rp <= rp.rolling(250, min_periods=200).quantile(0.2)
    dry = (x.v.shift(1).rolling(20).mean() <= 0.8 * x.v.shift(21).rolling(50).mean())
    return first_in(low_rng & dry & (x.c > x.hi(20)) & (x.volr() >= 1.5), 20)


reg("wyc_dull_range_breakout", wyc_dull_breakout, 1, 20, "books",
    "H-WYC-1: narrow 20d range (bottom 20%) on drying volume, close > 20d high on vol>=1.5x")


def wyc_effort_no_result(x):
    a = x.atr(20)
    tr = x.h - x.l
    cond = (x.roc(40) >= 0.15) & (x.c >= 0.97 * x.c.rolling(60).max()) & (x.volr() >= 2.5) & \
           (tr <= 0.75 * a) & ((x.c - x.c.shift(1)).abs() <= 0.3 * a)
    return first_in(cond, 20)


reg("wyc_effort_without_result", wyc_effort_no_result, -1, 20, "books",
    "H-WYC-2: huge volume, tiny range, near highs after +15% (distribution/churning)")


def wyc_selling_climax(x):
    a = x.atr(20)
    tr = x.h - x.l
    return first_in((x.roc(40) <= -0.20) & (tr >= 2.5 * a.shift(1)) & (x.volr() >= 3) & (x.ret1() < 0), 20)


reg("wyc_selling_climax", wyc_selling_climax, 1, 20, "books", "H-WYC-3: wide-range high-volume down day after -20% in 40d")


def wyc_buying_climax(x):
    a = x.atr(20)
    tr = x.h - x.l
    return first_in((x.roc(40) >= 0.25) & (tr >= 2.5 * a.shift(1)) & (x.volr() >= 3) & (x.ret1() > 0), 20)


reg("wyc_buying_climax", wyc_buying_climax, -1, 20, "books", "H-WYC-3: wide-range high-volume up day after +25% in 40d")


def wyc_resilience(x):
    spy = x.mkt("SPY")
    shock = (spy.pct_change(fill_method=None) <= -0.02)
    sh = x.bcast(shock.astype(float)).astype(bool)
    rel = x.ret1().sub(spy.pct_change(fill_method=None), axis=0)
    return sh & (x.xs_rank(rel) >= 0.9)


reg("wyc_resilience_on_shock", wyc_resilience, 1, 20, "books", "H-WYC-6: top-decile relative return on a SPY -2% day")
reg("wyc_weakest_on_shock", lambda x: x.bcast((x.mkt("SPY").pct_change(fill_method=None) <= -0.02).astype(float)).astype(bool)
    & (x.xs_rank(x.ret1().sub(x.mkt("SPY").pct_change(fill_method=None), axis=0)) <= 0.1), -1, 20, "books",
    "H-WYC-6 mirror: bottom decile on a SPY -2% day")


def _eff_ratio(x, n=20):
    return x.get(("er", n), lambda: (x.c - x.c.shift(n)).abs() / x.c.diff().abs().rolling(n).sum())


reg("donchian20_trending_only", lambda x: first_in((x.c > x.hi(20)) & (_eff_ratio(x).shift(1) >= 0.3), 10), 1, 20, "books",
    "H-WYC-9: 20d breakout only when efficiency ratio(20) >= 0.3 (not chop)")
reg("donchian20_chop_only", lambda x: first_in((x.c > x.hi(20)) & (_eff_ratio(x).shift(1) < 0.2), 10), 1, 20, "books",
    "H-WYC-9: 20d breakout during chop (ER < 0.2) - claimed to fail")


def wyc_streak_up(x):
    u = x.c > x.c.shift(1)
    s = u & u.shift(1, fill_value=False) & u.shift(2, fill_value=False) & u.shift(3, fill_value=False) & u.shift(4, fill_value=False)
    return first_in(s, 5)


def wyc_streak_dn(x):
    d = x.c < x.c.shift(1)
    s = d & d.shift(1, fill_value=False) & d.shift(2, fill_value=False) & d.shift(3, fill_value=False) & d.shift(4, fill_value=False)
    return first_in(s, 5)


reg("wyc_streak_5up", wyc_streak_up, -1, 5, "books", "H-WYC-10: 5 consecutive up closes -> exhaustion")
reg("wyc_streak_5down", wyc_streak_dn, 1, 5, "books", "H-WYC-10: 5 consecutive down closes -> bounce")


def wyc_low_vol_retest(x):
    dd = x.c / x.c.rolling(60).max() - 1
    newlow = x.l <= x.lo(20)
    vol_at_prior_low = x.v.where(x.l <= x.l.rolling(20).min()).shift(5).rolling(40, min_periods=1).max()
    return first_in((dd <= -0.15) & newlow & (x.v <= 0.7 * vol_at_prior_low) & (x.clv() >= 0.5), 20)


reg("wyc_low_volume_retest", wyc_low_vol_retest, 1, 20, "books", "H-WYC-11: new low on much lower volume, closes in upper half")


def wyc_small_giveback(x):
    spy = x.mkt("SPY")
    corr = (spy <= 0.90 * spy.rolling(252).max())
    adv = x.c.rolling(252).max() / x.c.rolling(252).min() - 1
    give = (1 - x.c / x.c.rolling(252).max()) / adv.replace(0, np.nan)
    from .signals import _month_end
    return x.bcast(corr.astype(float)).astype(bool) & (x.xs_rank(-give) >= 0.8) & _month_end(x)


reg("wyc_small_giveback_in_correction", wyc_small_giveback, 1, 60, "books",
    "H-WYC-12: in a >=10% market correction, stocks giving back least of their advance (monthly)")

# ============================ SCHABACKER (Stock Market Theory & Practice, 1930)
def sch_shakeout(x):
    a = x.atr(20)
    zone = x.l.shift(1).rolling(40).min()
    return first_in((x.l < zone - 0.5 * a) & (x.c >= zone) & (x.volr() >= 1.5) & (x.c > x.sma(200)), 20)


reg("sch_shakeout_spring", sch_shakeout, 1, 20, "books", "H-SCH-5 / Wyckoff spring: undercut 40d low, close back above on vol")


def sch_breakaway_gap(x):
    gap = x.o > x.h.shift(1)
    hh, ll = x.hi(20), x.lo(20)
    cons = (hh / ll - 1) <= 0.15
    return first_in(gap & cons & (x.c > hh), 20)


reg("sch_breakaway_gap", sch_breakaway_gap, 1, 20, "books", "H-SCH-6: gap up out of a tight 20d range to a new high")


def sch_exhaustion_gap(x):
    gap = x.o > x.h.shift(1) * 1.01
    run = x.roc(30) >= 0.25
    return first_in(gap & run, 20)


reg("sch_exhaustion_gap", sch_exhaustion_gap, -1, 20, "books", "H-SCH-6: gap up after +25% in 30d (exhaustion)")


def sch_reversal_day(x):
    newhi = x.h > x.hi(20)
    return first_in(newhi & (x.clv() <= 0.25) & (x.volr() >= 2) & (x.c > x.sma(50)), 10)


reg("sch_key_reversal_top", sch_reversal_day, -1, 10, "books", "H-SCH-8: new 20d high intraday, closes in bottom 25%, vol>=2x")


def sch_quiet_pullback(x):
    dd = x.c / x.c.rolling(60).max() - 1
    quiet = x.v.rolling(10).mean() <= 0.7 * x.v.shift(10).rolling(50).mean()
    near_low = x.c <= x.c.rolling(10).min() * 1.03
    return first_in((dd <= -0.07) & (dd >= -0.15) & quiet & near_low & x.mkt_up(200), 20)


reg("sch_quiet_pullback_bull", sch_quiet_pullback, 1, 20, "books", "H-SCH-10: 7-15% pullback on dry volume in a bull market")


def sch_loud_pullback(x):
    dd = x.c / x.c.rolling(60).max() - 1
    loud = x.v.rolling(10).mean() >= 1.2 * x.v.shift(10).rolling(50).mean()
    near_low = x.c <= x.c.rolling(10).min() * 1.03
    return first_in((dd <= -0.07) & (dd >= -0.15) & loud & near_low & x.mkt_up(200), 20)


reg("sch_loud_pullback_bull", sch_loud_pullback, -1, 20, "books", "H-SCH-10 control: same pullback on heavy volume ('not over')")


def sch_thrust(x):
    a = x.atr(20)
    thrust = ((x.h - x.l) >= 2 * a.shift(1)) & (x.clv() >= 0.75) & (x.h > x.hi(20))
    t3 = thrust.shift(3, fill_value=False)
    hh = (x.h > x.h.shift(1)) & (x.l > x.l.shift(1))
    seq = hh & hh.shift(1, fill_value=False) & hh.shift(2, fill_value=False)
    return first_in(t3 & seq, 20)


reg("sch_thrust_followthrough", sch_thrust, 1, 10, "books", "H-SCH-11: wide-range thrust to 20d high + 3 higher-high/low days")
