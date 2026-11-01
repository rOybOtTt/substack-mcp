"""TA-RL: an online reinforcement-learning agent that learns WHEN a technical
state deserves a long signal, purely from feedback.

Because a small trader's action does not move the price, the MDP collapses to
a contextual bandit (gamma = 0): state = discretised technical context of a
stock on a decision date; action in {LONG, FLAT}; reward = next-H-day excess
return over the equal-weight universe minus round-trip cost if LONG, 0 if FLAT.

Learning: Bayesian (Normal-Inverse-Gamma style) posterior per state, Thompson
sampling for exploration. The agent walks FORWARD in time: at each decision
date it acts with current beliefs, the reward is revealed H days later, and only
then is the posterior updated (no peeking). Reports cumulative realised reward
and the learned policy table (which states it trusts / avoids).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .evaluate import forward_returns, universe_benchmark, COST_PER_SIDE

FEATURES = {
    "trend": "C vs SMA200 & slope: 0=below&falling,1=mixed,2=above&rising",
    "rs6": "6-month return cross-sectional tercile (0 low..2 high)",
    "rsi": "RSI14 bucket: 0:<30 1:30-50 2:50-70 3:>70",
    "hi52": "distance from 52w high: 0:>25% below 1:10-25% 2:<10%",
    "volr": "volume vs 50d avg (5d mean): 0:<0.8 1:0.8-1.3 2:>1.3",
    "natr": "ATR% tercile (0 calm..2 volatile)",
    "st5": "5-day return tercile (0 losers..2 winners)",
    "mkt": "SPY above 10-month SMA (1) or not (0)",
}


def build_states(ctx):
    c = ctx.c
    s200 = ctx.sma(200)
    above = c > s200
    rising = s200 > s200.shift(21)
    trend = pd.DataFrame(1, index=c.index, columns=c.columns)
    trend = trend.mask(above & rising, 2).mask(~above & ~rising, 0)
    tert = lambda df: np.floor(ctx.xs_rank(df).clip(0, 0.9999) * 3)
    rs6 = tert(ctx.roc(126))
    r = ctx.rsi(14)
    rsi = pd.DataFrame(np.select([r < 30, r < 50, r < 70], [0, 1, 2], 3), index=c.index, columns=c.columns)
    d52 = c / c.rolling(252).max() - 1
    hi52 = pd.DataFrame(np.select([d52 < -0.25, d52 < -0.10], [0, 1], 2), index=c.index, columns=c.columns)
    vr = ctx.v.rolling(5).mean() / ctx.v.shift(5).rolling(50).mean()
    volr = pd.DataFrame(np.select([vr < 0.8, vr < 1.3], [0, 1], 2), index=c.index, columns=c.columns)
    natr = tert(ctx.natr(14))
    st5 = tert(ctx.roc(5))
    spy = ctx.mkt("SPY")
    m = spy.resample("ME").last()
    mk = (m > m.rolling(10).mean()).astype(float).reindex(c.index, method="ffill")
    mkt = ctx.bcast(mk.shift(1).fillna(0))
    feats = [trend, rs6, rsi, hi52, volr, natr, st5, mkt]
    valid = s200.notna() & r.notna() & d52.notna() & vr.notna() & ctx.natr(14).notna() & ctx.tradeable
    sizes = [3, 3, 4, 3, 3, 3, 3, 2]
    code = pd.DataFrame(0, index=c.index, columns=c.columns, dtype=np.int64)
    mult = 1
    for f, s in zip(feats, sizes):
        code = code + f.fillna(0).astype(np.int64) * mult
        mult *= s
    return code.where(valid, -1).astype(np.int64), sizes


def decode(code, sizes):
    out = []
    for s in sizes:
        out.append(code % s)
        code //= s
    return dict(zip(FEATURES, out))


class ThompsonAgent:
    def __init__(self, n_states, prior_mean=0.0, prior_n=20.0, prior_var=0.01, seed=0):
        self.n = np.full(n_states, prior_n)
        self.mean = np.full(n_states, prior_mean)
        self.m2 = np.full(n_states, prior_var * prior_n)
        self.rng = np.random.default_rng(seed)

    def sample(self, s):
        var = self.m2[s] / self.n[s]
        return self.mean[s] + self.rng.standard_normal(len(s)) * np.sqrt(var / self.n[s])

    def act(self, s, threshold=0.0):
        return self.sample(s) > threshold

    def update(self, s, r):
        # Welford per state (vectorised over a batch with possible repeats)
        for si, ri in zip(s, r):
            self.n[si] += 1
            d = ri - self.mean[si]
            self.mean[si] += d / self.n[si]
            self.m2[si] += d * (ri - self.mean[si])


def run_online(ctx, start, end, h=20, step=5, cost=COST_PER_SIDE, seed=0, agent=None, sizes_out=None):
    """Walk forward: decide every `step` days; reward revealed after h days."""
    codes, sizes = build_states(ctx)
    if sizes_out is not None:
        sizes_out.extend(sizes)
    n_states = int(np.prod(sizes))
    agent = agent or ThompsonAgent(n_states, seed=seed)
    fr = forward_returns(ctx.p, h)
    exc = fr.sub(universe_benchmark(fr, ctx.tradeable), axis=0)
    idx = ctx.c.index
    dates = np.nonzero((idx >= pd.Timestamp(start)) & (idx <= pd.Timestamp(end)))[0][::step]
    pending = []  # (reveal_t, states, rewards)
    log = []
    C, E = codes.values, exc.values
    for t in dates:
        # reveal matured rewards (only those whose window has closed by t)
        still = []
        for (rt, s, r) in pending:
            if rt <= t:
                agent.update(s, r)
            else:
                still.append((rt, s, r))
        pending = still
        s = C[t]
        ok = (s >= 0) & np.isfinite(E[t])
        s, e = s[ok], E[t][ok]
        if len(s) == 0:
            continue
        a = agent.act(s)
        r_long = e - 2 * cost
        realised = np.where(a, r_long, 0.0)
        log.append((idx[t], a.mean(), realised[a].mean() if a.any() else 0.0, e.mean(), len(s)))
        # the agent learns from ALL states' outcomes (it observes the market, it just doesn't trade all)
        pending.append((t + h + 1, s, r_long))
    lg = pd.DataFrame(log, columns=["date", "frac_long", "avg_reward_long", "avg_exc_all", "n"]).set_index("date")
    return agent, lg, sizes


def policy_table(agent, sizes, min_n=300):
    rows = []
    prior_n = 20.0
    for s in range(len(agent.n)):
        obs = agent.n[s] - prior_n
        if obs < min_n:
            continue
        sd = np.sqrt(agent.m2[s] / agent.n[s])
        se = sd / np.sqrt(agent.n[s])
        d = decode(s, sizes)
        rows.append({"state": s, **d, "n_obs": int(obs), "mean_reward": agent.mean[s], "t": agent.mean[s] / se})
    return pd.DataFrame(rows).sort_values("t", ascending=False)


# ------------------------------------------------------------------ RL v2
class LinearTS:
    """Bayesian linear-regression contextual bandit with Thompson sampling."""

    def __init__(self, d, lam=50.0, noise=0.08, seed=0):
        self.A = np.eye(d) * lam
        self.b = np.zeros(d)
        self.noise = noise
        self.rng = np.random.default_rng(seed)

    def coef(self):
        return np.linalg.solve(self.A, self.b)

    def sample_w(self):
        mu = self.coef()
        cov = self.noise ** 2 * np.linalg.inv(self.A)
        return self.rng.multivariate_normal(mu, (cov + cov.T) / 2)

    def update(self, X, r):
        self.A += X.T @ X
        self.b += X.T @ r


def onehot_design(codes_row, sizes):
    """codes_row: int array of joint state codes -> one-hot of each feature, plus
    the same one-hots interacted with the market-regime flag (last feature)."""
    feats = decode(codes_row.copy(), sizes)
    cols = []
    for (nm, vals), s in zip(feats.items(), sizes):
        oh = np.eye(s)[vals]
        cols.append(oh)
    X = np.concatenate(cols, axis=1)
    mkt = feats["mkt"][:, None].astype(float)
    return np.concatenate([np.ones((len(codes_row), 1)), X, X * mkt], axis=1)


def run_online_v2(ctx, start, end, h=20, step=5, cost=COST_PER_SIDE, seed=0, vol_matched=True):
    codes, sizes = build_states(ctx)
    fr = forward_returns(ctx.p, h)
    if vol_matched:
        from .evaluate import group_benchmark
        grp = np.floor(ctx.xs_rank(ctx.natr(14)).clip(0, 0.9999) * 3)
        exc = fr - group_benchmark(fr, ctx.tradeable, grp)
    else:
        exc = fr.sub(universe_benchmark(fr, ctx.tradeable), axis=0)
    idx = ctx.c.index
    dates = np.nonzero((idx >= pd.Timestamp(start)) & (idx <= pd.Timestamp(end)))[0][::step]
    C, E = codes.values, exc.values
    d = 1 + 2 * sum(sizes)
    agent = LinearTS(d, seed=seed)
    pending, log = [], []
    for t in dates:
        still = []
        for (rt, X, r) in pending:
            if rt <= t:
                agent.update(X, r)
            else:
                still.append((rt, X, r))
        pending = still
        s = C[t]
        ok = (s >= 0) & np.isfinite(E[t])
        if ok.sum() == 0:
            continue
        X = onehot_design(s[ok], sizes)
        e = E[t][ok]
        w = agent.sample_w()
        score = X @ w
        a = score > 2 * cost  # go long only if sampled expected excess beats round-trip cost
        r_long = e - 2 * cost
        log.append((idx[t], a.mean(), r_long[a].mean() if a.any() else 0.0, a.sum(),
                    np.corrcoef(X @ agent.coef(), e)[0, 1] if len(e) > 10 else np.nan))
        pending.append((t + h + 1, X, e - 2 * cost))
    lg = pd.DataFrame(log, columns=["date", "frac_long", "avg_reward_long", "n_long", "ic"]).set_index("date")
    names = ["bias"] + [f"{nm}={v}" for nm, s in zip(FEATURES, sizes) for v in range(s)]
    names += [f"{n}|mkt_up" for n in names[1:]]
    coef = pd.Series(agent.coef(), index=names)
    return agent, lg, coef
