"""Experiment runner + ledger.

Pre-registered verdict rules (fixed BEFORE any test was run):
  signed_t = direction * t  (direction=-1 for rules claimed bearish)
  SIGNAL    : signed net excess > 0 and min(event t, calendar t) >= 3.0
  WEAK      : min(...) >= 2.0
  NO_EDGE   : |t| < 2
  REVERSED  : signed t <= -2  (works OPPOSITE to the popular claim)
A train SIGNAL must then hold its sign with t >= 2 on VALID to be 'confirmed';
the locked TEST (2020-2026 + holdout ticker group B) is scored once at the end.
"""
from __future__ import annotations

import datetime as _dt
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

from .data import load, clean
from .evaluate import (PERIODS, ticker_group, event_study, calendar_portfolio, simulate_trades,
                       COST_PER_SIDE)
from .features import Ctx
from .signals import R
from . import signals_books, signals_regime  # noqa: F401  (register extra rules)

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "experiments" / "results" / "ledger.jsonl"
TEST_LOG = ROOT / "experiments" / "test_access_log.md"
EMBARGO_DAYS = 90  # drop events in the last 90 days of a period (their labels leak into the next)

_PANELS = {}


def get_ctx(group="A", unlock=False):
    if group != "A" and not unlock:
        raise PermissionError("Holdout ticker group is locked")
    key = group
    if key in _PANELS:
        return _PANELS[key]
    p = load("stocks")
    cols = [c for c in p["Close"].columns if group == "AB" or ticker_group(c) == group]
    sub = {k: v[cols] for k, v in p.items()}
    sub = clean(sub)
    mk = load("etf")["Close"]
    ctx = Ctx(sub, market=mk)
    _PANELS[key] = ctx
    return ctx


def period_mask(ctx, period, unlock=False, note=""):
    if period in ("test", "all") and not unlock:
        raise PermissionError("TEST period is locked")
    if unlock:
        TEST_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(TEST_LOG, "a") as f:
            f.write(f"- {_dt.datetime.now().isoformat(timespec='seconds')} | period={period} | {note}\n")
    a, b = PERIODS[period]
    b = pd.Timestamp(b) - pd.Timedelta(days=EMBARGO_DAYS)
    idx = ctx.c.index
    rows = (idx >= pd.Timestamp(a)) & (idx <= b)
    return pd.DataFrame(np.repeat(rows[:, None], ctx.c.shape[1], axis=1), index=idx, columns=ctx.c.columns)


def verdict(direction, m, h):
    t_ev = m.get(f"t{h}", np.nan)
    t_cal = m.get("cal_t", np.nan)
    exc = m.get(f"exc{h}_mean", np.nan)
    if not np.isfinite(t_ev):
        return "INSUFFICIENT"
    s_ev = direction * t_ev
    s_cal = direction * t_cal if np.isfinite(t_cal) else s_ev
    s_min = min(s_ev, s_cal)
    net_ok = (direction * exc - (2 * COST_PER_SIDE if direction > 0 else 0)) > 0
    # beta/vol confound check: if vol-matched excess flips sign, demote
    vm = m.get(f"vm{h}_t", np.nan)
    if np.isfinite(vm) and direction * vm < 1.0 and s_min >= 2.0:
        return "VOL_ARTIFACT"
    if s_min >= 3.0 and net_ok:
        return "SIGNAL"
    if s_min >= 2.0 and net_ok:
        return "WEAK"
    if max(s_ev, s_cal) <= -2.0:
        return "REVERSED"
    return "NO_EDGE"


_FR = {}


def vol_groups(ctx):
    """Volatility tercile (ATR%, known at t) used for the vol-matched benchmark."""
    return ctx.get("volgrp", lambda: np.floor(ctx.xs_rank(ctx.natr(14)).clip(0, 0.9999) * 3))


def evaluate(name, period="train", group="A", events=None, direction=None, horizon=None,
             it=None, note="", unlock=False, trades=False, log=True, extra_mask=None):
    ctx = get_ctx(group, unlock=unlock)
    r = R.get(name)
    direction = direction if direction is not None else (r.direction if r else 1)
    horizon = horizon if horizon is not None else (r.horizon if r else 20)
    t0 = time.time()
    ev = events if events is not None else r.fn(ctx)
    ev = ev.fillna(False).astype(bool)
    mask = period_mask(ctx, period, unlock=unlock, note=f"{name} {note}")
    if extra_mask is not None:
        mask &= extra_mask.reindex_like(mask).fillna(False).astype(bool)
    hz = sorted(set([5, 20, 60, horizon]))
    cache = _FR.setdefault(group, {})
    m = event_study(ev, ctx.p, horizons=hz, mask=mask, fr_cache=cache, groups=vol_groups(ctx))
    m.update(calendar_portfolio(ev, ctx.p, h=horizon, mask=mask))
    if trades:
        m.update({f"tr_{k}": v for k, v in simulate_trades(ev, ctx.p, ctx.atr(14), stop_atr=2.0,
                                                            max_hold=horizon, mask=mask).items()})
    m["verdict"] = verdict(direction, m, horizon)
    row = {"time": _dt.datetime.now().isoformat(timespec="seconds"), "iter": it, "rule": name,
           "period": period, "group": group, "direction": direction, "horizon": horizon,
           "family": r.family if r else "", "note": note, **m, "secs": round(time.time() - t0, 1)}
    if log:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        with open(LEDGER, "a") as f:
            f.write(json.dumps({k: (None if isinstance(v, float) and not np.isfinite(v) else v)
                                for k, v in row.items()}, default=str) + "\n")
    return row


def fmt(row, h=None):
    h = h or row["horizon"]
    g = lambda k: row.get(k, np.nan)
    return (f"{row['rule']:<28} {row['period']:<5} dir={row['direction']:+d} h={h:<3} N={g('n_events'):>7} "
            f"exc{h}={g(f'exc{h}_mean')*100:+6.2f}% med={g(f'exc{h}_med')*100:+6.2f}% hit={g(f'hit{h}')*100:5.1f}% "
            f"t={g(f't{h}'):+5.2f} | cal_ann={g('cal_exc_ann')*100 if np.isfinite(g('cal_exc_ann')) else np.nan:+6.2f}% "
            f"calIR={g('cal_ir'):+5.2f} calT={g('cal_t'):+5.2f} vmT={g(f'vm{h}_t'):+5.2f} | e5={g('exc5_mean')*100:+5.2f}% e60={g('exc60_mean')*100:+5.2f}% -> {row['verdict']}")


KEEP = {"sma", "natr", "atr", "volr", "volgrp", "month_end", "week_end", "mkt_up", "rsi", "roc",
        "candles", "patterns", "hi", "lo", "chi", "trend_template", "rs", "ret1", "clv", "macd", "bb"}


def prune(ctx):
    for k in list(ctx._cache):
        name = k[0] if isinstance(k, tuple) else k
        if name not in KEEP:
            del ctx._cache[k]


if __name__ == "__main__":
    period = sys.argv[1] if len(sys.argv) > 1 else "train"
    note = sys.argv[2] if len(sys.argv) > 2 else "batch"
    names = sys.argv[3:] or list(R)
    for n in names:
        try:
            row = evaluate(n, period=period, note=note)
            print(fmt(row), flush=True)
        except Exception as e:
            print(n, "ERROR", e, flush=True)
        prune(get_ctx("A"))


def ledger(rule=None, period=None):
    rows = [json.loads(x) for x in open(LEDGER)] if LEDGER.exists() else []
    df = pd.DataFrame(rows)
    if rule is not None:
        df = df[df.rule == rule]
    if period is not None:
        df = df[df.period == period]
    return df
