"""Evaluation engine for TA Gym.

Three ways to score a rule:

1. event_study(events, ...)      -- signal fires at close t, we buy at OPEN t+1,
   measure return to CLOSE t+h for h in horizons, minus the equal-weight
   universe return over the same window (excess). Stats are clustered by
   date (per-date mean, Newey-West t over dates) because many stocks fire on
   the same day and are not independent observations.

2. calendar_portfolio(events, h) -- every day hold equal weights in all
   stocks that fired within the last h days (entered at the next open).
   Daily excess return vs the EW universe -> annualised excess, IR, NW t-stat,
   after costs. This is the gold-standard for overlapping event windows.

3. simulate_trades(events, ...)  -- per-trade simulation with an ATR stop,
   optional profit target, optional trailing exit, and a time stop.
   Returns expectancy in R-multiples and %.

Splits: tickers are hashed into group A (discovery, 60%) and B (holdout, 40%).
Periods: TRAIN 2000-2014, VALID 2015-2019, TEST 2020-2026. The TEST period and
group B are LOCKED: they can only be scored with unlock=True, and every
access is appended to experiments/test_access_log.md.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
TEST_LOG = ROOT / "experiments" / "test_access_log.md"

PERIODS = {
    "train": ("2000-01-01", "2014-12-31"),
    "valid": ("2015-01-01", "2019-12-31"),
    "test": ("2020-01-01", "2026-12-31"),
    "all": ("2000-01-01", "2026-12-31"),
}
COST_PER_SIDE = 0.0010  # 10 bps per side (commission+spread+slippage, liquid US stocks)


def ticker_group(t: str) -> str:
    hv = int(hashlib.md5(t.encode()).hexdigest()[:8], 16) % 100
    return "A" if hv < 60 else "B"


def split_mask(index: pd.DatetimeIndex, columns, period: str, group: str | None,
               unlock: bool = False, note: str = "") -> pd.DataFrame:
    if (period in ("test", "all") or group in ("B", "AB", None)) and not unlock:
        raise PermissionError("TEST period / group B is locked. Pass unlock=True (logged).")
    if unlock:
        TEST_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(TEST_LOG, "a") as f:
            f.write(f"- {_dt.datetime.now().isoformat(timespec='seconds')} | period={period} group={group} | {note}\n")
    a, b = PERIODS[period]
    rows = (index >= pd.Timestamp(a)) & (index <= pd.Timestamp(b))
    if group in ("A", "B"):
        cols = np.array([ticker_group(c) == group for c in columns])
    else:
        cols = np.ones(len(columns), bool)
    return pd.DataFrame(np.outer(rows, cols), index=index, columns=columns)


# ---------------------------------------------------------------- helpers
def nw_tstat(x: np.ndarray, lags: int) -> float:
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 20:
        return np.nan
    mu = x.mean()
    e = x - mu
    g0 = e @ e / n
    s = g0
    for L in range(1, min(lags, n - 1) + 1):
        w = 1 - L / (lags + 1)
        s += 2 * w * (e[L:] @ e[:-L]) / n
    se = np.sqrt(max(s, 1e-18) / n)
    return mu / se


def forward_returns(panel, h: int) -> pd.DataFrame:
    """Return from OPEN t+1 to CLOSE t+h (known only in the future; label only)."""
    o, c = panel["Open"], panel["Close"]
    return c.shift(-h) / o.shift(-1) - 1.0


def universe_benchmark(fr: pd.DataFrame, tradeable: pd.DataFrame) -> pd.Series:
    return fr.where(tradeable).mean(axis=1)


def group_benchmark(fr: pd.DataFrame, tradeable: pd.DataFrame, groups: pd.DataFrame) -> pd.DataFrame:
    """Per-stock benchmark = EW mean of tradeable stocks in the same group (e.g. volatility
    tercile known at t). Removes beta/volatility tilts from 'excess' returns."""
    out = pd.DataFrame(np.nan, index=fr.index, columns=fr.columns)
    f = fr.where(tradeable)
    for g in np.unique(groups.values[np.isfinite(groups.values)]):
        m = groups == g
        mu = f.where(m).mean(axis=1)
        out = out.mask(m, np.repeat(mu.values[:, None], fr.shape[1], axis=1))
    return out


# ----------------------------------------------------------- event study
def event_study(events: pd.DataFrame, panel, horizons=(5, 20, 60), mask=None,
                winsor=0.01, fr_cache: dict | None = None, groups: pd.DataFrame | None = None) -> dict:
    tradeable = panel["tradeable"]
    ev = events.reindex_like(tradeable).fillna(False).astype(bool) & tradeable
    if mask is not None:
        ev &= mask.reindex_like(ev).fillna(False)
    out = {"n_events": int(ev.values.sum()), "n_dates": int(ev.any(axis=1).sum()),
           "n_tickers": int(ev.any(axis=0).sum())}
    for h in horizons:
        if fr_cache is not None and h in fr_cache:
            fr, bench = fr_cache[h]
        else:
            fr = forward_returns(panel, h)
            bench = universe_benchmark(fr, tradeable)
            if fr_cache is not None:
                fr_cache[h] = (fr, bench)
        exc = fr.sub(bench, axis=0).where(ev)
        if groups is not None:
            key = ("vm", h)
            if fr_cache is not None and key in fr_cache:
                gb = fr_cache[key]
            else:
                gb = group_benchmark(fr, tradeable, groups)
                if fr_cache is not None:
                    fr_cache[key] = gb
            exc_vm = (fr - gb).where(ev)
            vv = exc_vm.values[ev.values]; vv = vv[~np.isnan(vv)]
            if len(vv) >= 30:
                lo2, hi2 = np.quantile(vv, [winsor, 1 - winsor])
                out[f"vm{h}_mean"] = float(np.clip(vv, lo2, hi2).mean())
                out[f"vm{h}_t"] = float(nw_tstat(exc_vm.clip(lo2, hi2).mean(axis=1).dropna().values, lags=max(5, h)))
        vals = exc.values[ev.values]
        vals = vals[~np.isnan(vals)]
        if len(vals) < 30:
            out.update({f"exc{h}_mean": np.nan, f"exc{h}_med": np.nan, f"hit{h}": np.nan,
                        f"t{h}": np.nan, f"raw{h}_mean": np.nan})
            continue
        lo, hi = np.quantile(vals, [winsor, 1 - winsor])
        v = np.clip(vals, lo, hi)
        per_date = exc.clip(lo, hi).mean(axis=1).dropna()
        raw = fr.where(ev).values[ev.values]
        raw = raw[~np.isnan(raw)]
        out[f"exc{h}_mean"] = float(v.mean())
        out[f"exc{h}_med"] = float(np.median(v))
        out[f"hit{h}"] = float((v > 0).mean())
        out[f"raw{h}_mean"] = float(np.clip(raw, *np.quantile(raw, [winsor, 1 - winsor])).mean())
        # per-date clustering; NW lag = h (overlapping windows across dates)
        out[f"t{h}"] = float(nw_tstat(per_date.values, lags=max(5, h)))
        # net of round-trip cost
        out[f"exc{h}_net"] = out[f"exc{h}_mean"] - 2 * COST_PER_SIDE
    return out


# ---------------------------------------------------- calendar portfolio
def calendar_portfolio(events: pd.DataFrame, panel, h=20, mask=None, cost=COST_PER_SIDE) -> dict:
    tradeable = panel["tradeable"]
    o, c = panel["Open"], panel["Close"]
    ev = events.reindex_like(tradeable).fillna(False).astype(bool) & tradeable
    if mask is not None:
        ev &= mask.reindex_like(ev).fillna(False)
    evf = ev.astype(float)
    r_oc = (c / o - 1).fillna(0.0)
    r_cc = (c / c.shift(1) - 1).fillna(0.0)
    entry = evf.shift(1).fillna(0.0)
    hold = sum(evf.shift(j).fillna(0.0) for j in range(1, h + 1))
    cont = hold - entry
    n_act = hold.sum(axis=1)
    gross = ((entry * r_oc).sum(axis=1) + (cont * r_cc).sum(axis=1)) / n_act.replace(0, np.nan)
    exits = evf.shift(h).fillna(0.0).sum(axis=1)
    turn = (entry.sum(axis=1) + exits) / n_act.replace(0, np.nan)
    net = gross - turn * cost
    bench = r_cc.where(tradeable.shift(1, fill_value=False)).mean(axis=1)
    exc_g = (gross - bench).where(n_act > 0).dropna()
    exc = (net - bench).where(n_act > 0).dropna()
    if len(exc) < 60:
        return {"cal_days": len(exc)}
    # t-stat and IR on GROSS excess (cost drag would bias bearish claims toward 'confirmed');
    # net annual excess reported separately and used for the bullish profitability check.
    return {"cal_days": int(len(exc)), "cal_exc_ann": float(exc_g.mean() * 252),
            "cal_exc_ann_net": float(exc.mean() * 252),
            "cal_ir": float(exc_g.mean() / exc_g.std() * np.sqrt(252)),
            "cal_t": float(nw_tstat(exc_g.values, lags=10)),
            "cal_avg_names": float(n_act[n_act > 0].mean())}


# --------------------------------------------------------- state strategy
def state_strategy(position: pd.DataFrame | pd.Series, close: pd.DataFrame | pd.Series,
                   lag=1, cost=COST_PER_SIDE, rf_daily=0.0) -> dict:
    """position decided at close t (0..1) earns close-to-close return of t+lag..
    lag=1: trade at the close of the signal day; lag=2: one extra day of delay."""
    pos = position.shift(lag).fillna(0.0)
    r = close.pct_change(fill_method=None).fillna(0.0)
    turn = pos.diff().abs().fillna(0.0)
    strat = pos * r + (1 - pos) * rf_daily - turn * cost
    if isinstance(strat, pd.DataFrame):
        strat = strat.mean(axis=1)
        bh = r.mean(axis=1)
        expo = pos.mean(axis=1).mean()
        trades = turn.sum().sum() / 2 / max(1, position.shape[1])
    else:
        bh = r
        expo = pos.mean()
        trades = turn.sum() / 2
    return {**perf_stats(strat, "strat"), **perf_stats(bh, "bh"), "exposure": float(expo),
            "trades_per_year": float(trades / (len(strat) / 252))}


def perf_stats(r: pd.Series, p: str) -> dict:
    r = r.dropna()
    if len(r) < 50:
        return {}
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    cagr = eq.iloc[-1] ** (1 / yrs) - 1
    vol = r.std() * np.sqrt(252)
    dd = (eq / eq.cummax() - 1).min()
    sh = r.mean() / r.std() * np.sqrt(252) if r.std() > 0 else np.nan
    return {f"{p}_cagr": float(cagr), f"{p}_vol": float(vol), f"{p}_sharpe": float(sh),
            f"{p}_maxdd": float(dd)}


# ------------------------------------------------------------ trade sim
def simulate_trades(events: pd.DataFrame, panel, atr_df: pd.DataFrame, stop_atr=2.0,
                    target_r: float | None = None, max_hold=20, trail_low: pd.DataFrame | None = None,
                    mask=None, cost=COST_PER_SIDE, max_trades=200000, seed=0) -> dict:
    """Long trades: enter OPEN t+1. Stop = entry - stop_atr*ATR_t (checked on
    lows, filled at stop or at the open if gapped through). Optional target at
    entry + target_r*risk. Optional trailing exit when close < trail_low (a
    DataFrame of levels known at each close; exit next open). Time exit at
    close of day max_hold. Returns R-multiple and % stats."""
    o, h, l, c = (panel[k].values for k in ["Open", "High", "Low", "Close"])
    tradeable = panel["tradeable"]
    ev = events.reindex_like(tradeable).fillna(False).astype(bool) & tradeable
    if mask is not None:
        ev &= mask.reindex_like(ev).fillna(False)
    ti, ki = np.nonzero(ev.values)
    if len(ti) > max_trades:
        rng = np.random.default_rng(seed)
        sel = rng.choice(len(ti), max_trades, replace=False)
        ti, ki = ti[sel], ki[sel]
    A = atr_df.reindex_like(tradeable).values
    TL = trail_low.reindex_like(tradeable).values if trail_low is not None else None
    T = len(o)
    Rs, pcts, holds = [], [], []
    for t, k in zip(ti, ki):
        if t + 1 >= T:
            continue
        e = o[t + 1, k]
        a = A[t, k]
        if not np.isfinite(e) or not np.isfinite(a) or a <= 0:
            continue
        risk = stop_atr * a
        stop = e - risk
        tgt = e + target_r * risk if target_r else np.inf
        exit_p = np.nan
        end = min(T - 1, t + max_hold)
        j = t + 1
        while j <= end:
            if j > t + 1 and np.isfinite(o[j, k]) and (o[j, k] <= stop or o[j, k] >= tgt):
                exit_p = o[j, k]; break
            if np.isfinite(l[j, k]) and l[j, k] <= stop:
                exit_p = stop; break
            if np.isfinite(h[j, k]) and h[j, k] >= tgt:
                exit_p = tgt; break
            if TL is not None and np.isfinite(TL[j, k]) and c[j, k] < TL[j, k] and j < end:
                nxt = o[j + 1, k]
                exit_p = nxt if np.isfinite(nxt) else c[j, k]; j += 1; break
            j += 1
        if not np.isfinite(exit_p):
            j = end
            exit_p = c[end, k]
            if not np.isfinite(exit_p):
                continue
        pct = exit_p / e - 1 - 2 * cost
        Rs.append((exit_p - e - 2 * cost * e) / risk)
        pcts.append(pct)
        holds.append(j - t)
    Rs, pcts = np.array(Rs), np.array(pcts)
    if len(Rs) < 30:
        return {"trades": len(Rs)}
    wins = Rs[Rs > 0]
    losses = Rs[Rs <= 0]
    pf = wins.sum() / max(1e-9, -losses.sum())
    return {"trades": int(len(Rs)), "win_rate": float((Rs > 0).mean()), "avg_R": float(Rs.mean()),
            "med_R": float(np.median(Rs)), "avg_pct": float(pcts.mean()), "profit_factor": float(pf),
            "avg_win_R": float(wins.mean()) if len(wins) else np.nan,
            "avg_loss_R": float(losses.mean()) if len(losses) else np.nan,
            "avg_hold": float(np.mean(holds))}


def random_same_date(events: pd.DataFrame, tradeable: pd.DataFrame, seed=0) -> pd.DataFrame:
    """Placebo: for every real event (t, k) pick a random tradeable stock on the same date t.
    Preserves the market-timing of the rule; removes its stock selection."""
    rng = np.random.default_rng(seed)
    ev = events.reindex_like(tradeable).fillna(False).astype(bool).values & tradeable.values
    tv = tradeable.values
    out = np.zeros_like(ev)
    counts = ev.sum(axis=1)
    for t in np.nonzero(counts)[0]:
        cand = np.nonzero(tv[t])[0]
        if len(cand) == 0:
            continue
        pick = rng.choice(cand, size=min(counts[t], len(cand)), replace=False)
        out[t, pick] = True
    return pd.DataFrame(out, index=tradeable.index, columns=tradeable.columns)
