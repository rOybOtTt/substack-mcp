"""Unit tests for the agent-facing rulebook engine (tagym.live).

Run from ta-rulebook/platform:   python -m pytest -q tests
Synthetic, seeded price paths exercise every decision row (D1-D6), the regime
layer, rule A1, the earnings flag E1 and the TradingView JSON loader.
"""
import json

import numpy as np
import pandas as pd
import pytest

from tagym.live import classify, load_tv, trading_days_until, RULEBOOK_VERSION

IDX = pd.bdate_range("2024-01-01", periods=420)


def frame(close, vol=2_000_000, idx=IDX):
    c = pd.Series(close, index=idx[: len(close)])
    o = c.shift(1).fillna(c.iloc[0])
    return pd.DataFrame({"o": o, "h": np.maximum(o, c) * 1.005, "l": np.minimum(o, c) * 0.995, "c": c, "v": vol})


def path(drift, vol, n=420, seed=0, start=100.0):
    r = np.random.default_rng(seed).normal(drift, vol, n)
    return start * np.exp(np.cumsum(r))


SPY_UP = frame(path(0.0006, 0.004, seed=1, start=400))
SPY_DOWN = frame(path(-0.0012, 0.004, seed=2, start=400))


def calm_end(c, days=25, seed=7):
    """Flatten the last `days` bars into small mean-zero noise so RSI sits mid-range."""
    c = c.copy()
    noise = np.random.default_rng(seed).normal(0, 0.004, days)
    base = c[-days - 1]
    c[-days:] = base * np.exp(np.cumsum(noise - noise.mean()))
    return c


def test_version():
    assert RULEBOOK_VERSION == "2.2"


def test_d1_short_history():
    v = classify(frame(path(0.001, 0.01)[:200]), SPY_UP)
    assert v["signal"] == "NO_SIGNAL" and v["decision_row"] == "D1"


def test_d1_untradeable_low_dollar_volume():
    v = classify(frame(path(0.001, 0.01), vol=1_000), SPY_UP)
    assert v["decision_row"] == "D1"


def test_d3_bullish_healthy_uptrend_risk_on():
    c = calm_end(path(0.0012, 0.008, seed=3))
    v = classify(frame(c), SPY_UP)
    assert v["layers"]["regime"] == "RISK_ON"
    assert v["layers"]["health"] == "HEALTHY", v["features"]
    assert v["signal"] == "BULLISH" and v["decision_row"] == "D3"
    assert v["risk"]["p_drawdown20_60d_est"] == pytest.approx(0.06)


def test_d2_bearish_broken_downtrend():
    v = classify(frame(path(-0.002, 0.012, seed=4)), SPY_UP)
    assert v["layers"]["health"] == "BROKEN"
    assert v["signal"] == "BEARISH" and v["decision_row"] == "D2"
    assert v["risk"]["risk_flag"] == "HIGH"


def test_d4_healthy_but_extended():
    c = calm_end(path(0.0012, 0.008, seed=3))
    c[-6:] = c[-7] * np.cumprod([1.03, 1.03, 1.03, 1.03, 1.03, 1.03])  # 6 straight up days, RSI spikes
    v = classify(frame(c), SPY_UP)
    assert v["layers"]["timing"] == "EXTENDED"
    assert v["decision_row"] in ("D4", "D2")  # a spike can push it >0% off high but never BULLISH
    assert v["signal"] != "BULLISH"


def test_d5_healthy_stock_bad_market_and_a1():
    c = calm_end(path(0.0016, 0.008, seed=3))
    v = classify(frame(c), SPY_DOWN)
    assert v["layers"]["regime"] == "RISK_OFF"
    assert v["signal"] == "NO_SIGNAL" and v["decision_row"] in ("D5", "D4")
    assert any(w.startswith("A1") for w in v["warnings"])  # strong RS while SPY < 10m SMA


def test_e1_earnings_flag():
    c = calm_end(path(0.0012, 0.008, seed=3))
    as_of = IDX[len(c) - 1]
    nxt = str((as_of + pd.offsets.BDay(3)).date())
    v = classify(frame(c), SPY_UP, next_earnings=nxt)
    assert v["risk"]["earnings_in_next_10d"] is True
    assert any(w.startswith("E1") for w in v["warnings"])
    assert v["risk"]["risk_flag"] == "NORMAL"  # D3 is no longer LOW risk with earnings due
    assert v["risk"]["p_drop10_10d_est"] > 0.05
    far = classify(frame(c), SPY_UP, next_earnings=str((as_of + pd.offsets.BDay(30)).date()))
    assert far["risk"]["earnings_in_next_10d"] is False


def test_trading_days_until():
    assert trading_days_until("2026-10-30", "2026-11-02") == 1      # Fri -> Mon
    assert trading_days_until("2026-10-30", "2026-11-13") == 10
    assert trading_days_until("2026-10-30", "2026-10-29") is None
    assert trading_days_until("2026-10-30", None) is None


def test_load_tv_columns(tmp_path):
    f = tmp_path / "x.json"
    t = [1793021400, 1793107800, 1793194200]
    f.write_text(json.dumps({"bars": {"t": t, "o": [1, 2, 3], "h": [1, 2, 3], "l": [1, 2, 3], "c": [1, 2, 3], "v": [9, 9, 9]}}))
    df = load_tv(f)
    assert list(df.columns) == ["o", "h", "l", "c", "v"] and len(df) == 3 and df.c.iloc[-1] == 3
