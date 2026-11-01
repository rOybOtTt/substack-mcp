"""ML ceiling test: how much can ALL common TA features predict, combined?

Walk-forward: train a gradient-boosted model on the prior 5 years of
(stock, date) samples, predict the next calendar year, roll forward. Target =
next-20-day vol-matched excess return. Reports yearly rank-IC and the
top-minus-bottom decile spread (before/after cost), plus permutation feature
importance. If even this can't find edge, discretionary rules won't either.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .evaluate import forward_returns, group_benchmark
from .signals import trend_template


def feature_panel(x):
    c = x.c
    f = {}
    for n in (20, 50, 200):
        f[f"c_vs_sma{n}"] = c / x.sma(n) - 1
    f["sma200_slope"] = x.sma(200) / x.sma(200).shift(21) - 1
    f["sma50_vs_200"] = x.sma(50) / x.sma(200) - 1
    for n in (5, 21, 63, 126, 252):
        f[f"ret_{n}"] = x.roc(n)
    f["mom_12_1"] = x.mom121()
    f["from_52w_high"] = c / c.rolling(252).max() - 1
    f["from_52w_low"] = c / c.rolling(252).min() - 1
    f["rsi14"] = x.rsi(14)
    f["rsi2"] = x.rsi(2)
    l, s, hst = x.macd()
    f["macd_hist_norm"] = hst / c
    a, p, n = x.adx()
    f["adx"] = a; f["di_spread"] = p - n
    mid, up, lo, pb, bw = x.bb()
    f["bb_pctb"] = pb; f["bb_bw"] = bw
    k, d = x.stoch(); f["stoch_k"] = k
    f["natr14"] = x.natr(14)
    f["volr50"] = x.volr(50)
    f["vol5_vs_50"] = x.v.rolling(5).mean() / x.v.shift(5).rolling(50).mean()
    f["clv"] = x.clv()
    f["cmf20"] = x.cmf(20)
    f["range60"] = x.hi(60) / x.lo(60) - 1
    f["rs6_rank"] = x.xs_rank(x.roc(126))
    f["trend_template"] = trend_template(x).astype(float)
    spy = x.mkt("SPY")
    f["mkt_vs_sma200"] = x.bcast(spy / spy.rolling(200).mean() - 1)
    f["mkt_ret_63"] = x.bcast(spy / spy.shift(63) - 1)
    f["breadth200"] = x.breadth(200)
    return f


def build_dataset(x, step=5, h=20):
    f = feature_panel(x)
    fr = forward_returns(x.p, h)
    grp = np.floor(x.xs_rank(x.natr(14)).clip(0, 0.9999) * 3)
    y = fr - group_benchmark(fr, x.tradeable, grp)
    idx = x.c.index
    rows = np.arange(len(idx)) % step == 0
    keep = x.tradeable.values & rows[:, None]
    ti, ki = np.nonzero(keep)
    X = np.column_stack([f[nm].values[ti, ki] for nm in f])
    Y = y.values[ti, ki]
    D = idx[ti]
    ok = np.isfinite(X).all(axis=1) & np.isfinite(Y)
    return pd.DataFrame(X[ok], columns=list(f)), Y[ok], D[ok], ki[ok]


def walk_forward(X, Y, D, first_test_year=2005, last_test_year=2019, train_years=5, embargo_days=30, seed=0):
    from sklearn.ensemble import HistGradientBoostingRegressor
    yrs = pd.DatetimeIndex(D).year
    res, preds = [], []
    Yc = np.clip(Y, np.quantile(Y, 0.01), np.quantile(Y, 0.99))
    for ty in range(first_test_year, last_test_year + 1):
        tr = (yrs >= ty - train_years) & (yrs < ty) & (pd.DatetimeIndex(D) < pd.Timestamp(f"{ty}-01-01") - pd.Timedelta(days=embargo_days))
        te = yrs == ty
        m = HistGradientBoostingRegressor(max_iter=200, learning_rate=0.05, max_leaf_nodes=31,
                                          min_samples_leaf=500, l2_regularization=1.0, random_state=seed)
        m.fit(X[tr], Yc[tr])
        p = m.predict(X[te])
        df = pd.DataFrame({"d": np.asarray(D)[te], "p": p, "y": Y[te]})
        ic = df.groupby("d").apply(lambda g: g.p.rank().corr(g.y.rank()), include_groups=False)
        df["dec"] = df.groupby("d").p.transform(lambda s: np.floor(s.rank(pct=True).clip(0, 0.9999) * 10))
        spread = df.groupby("d").apply(lambda g: g.y[g.dec == 9].mean() - g.y[g.dec == 0].mean(), include_groups=False)
        top = df.groupby("d").apply(lambda g: g.y[g.dec == 9].mean(), include_groups=False)
        res.append({"year": ty, "ic": ic.mean(), "ic_t": ic.mean() / ic.std() * np.sqrt(len(ic) / 4),
                    "top_minus_bottom_20d": spread.mean(), "top_decile_20d": top.mean(), "n": int(te.sum())})
        preds.append(df)
        if ty == last_test_year:
            last_model = m
    return pd.DataFrame(res), pd.concat(preds), last_model
