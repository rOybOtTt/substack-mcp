"""Intraday trader: rule logic and P&L bookkeeping (no network)."""
import types

import numpy as np
import pandas as pd
import pytest

import tagym.intraday as I
from tagym.intraday_bt import bar_signals


def bar(**k):
    base = dict(c=100.0, vwap=99.0, ema9=100.0, ema21=99.0, ret30=0.01, sig5=0.001, ret15=0.0, ret10=0.0,
                orh=101.0, orl=98.0, relvol=1.0, rsi=50.0)
    base.update(k)
    return types.SimpleNamespace(**base)


def test_vwap_trend_needs_market_agreement():
    assert bar_signals("AAPL", 13 * 60 + 35, bar(), bar(c=500, vwap=499), None)["R1_vwap_trend"] == 1
    assert "R1_vwap_trend" not in bar_signals("AAPL", 13 * 60 + 35, bar(), bar(c=498, vwap=499), None)


def test_reversal_fades_extreme_relative_move():
    s = bar_signals("AAPL", 13 * 60 + 35, bar(ret15=-0.01, sig5=0.001), bar(ret15=0.0), None)
    assert s["R2_reversal"] == 1  # z = -0.01 / (0.001 * sqrt 3) < -2.5


def test_orb_only_on_a_fresh_break_after_10_30():
    b, pb = bar(c=101.5, relvol=1.5), bar(c=100.5)
    assert bar_signals("AAPL", 10 * 60 + 35, b, None, pb)["R3_orb"] == 1
    assert "R3_orb" not in bar_signals("AAPL", 10 * 60 + 25, b, None, pb)
    assert "R3_orb" not in bar_signals("AAPL", 10 * 60 + 35, b, None, bar(c=101.2))  # already broken


@pytest.fixture
def tmp_io(tmp_path, monkeypatch):
    monkeypatch.setattr(I, "IDIR", tmp_path)
    for k, n in (("STATE", "state.json"), ("TRADES", "trades.csv"), ("SESSIONS", "sessions.csv"),
                 ("LOG", "log.csv"), ("REPORT", "REPORT.md")):
        monkeypatch.setattr(I, k, tmp_path / n)
    return tmp_path


def test_fill_and_close_bookkeeping(tmp_io):
    idx = pd.date_range("2026-11-02 13:30", "2026-11-02 13:59", freq="1min")
    px = pd.Series(np.linspace(100, 101, len(idx)), index=idx)
    one = {"AAPL": pd.DataFrame({"o": px, "h": px, "l": px, "c": px, "v": 1.0})}
    sess = {"id": "t", "date": "2026-11-02", "hour": 13, "started": "x", "decisions": [], "positions": [], "taken": [],
            "orders": [{"rule": "R9_ema_cross", "symbol": "AAPL", "side": -1, "minute": 35,
                        "decided_at": "2026-11-02 13:35:20", "fill_after": "2026-11-02 13:36:00"}]}
    I.fill_entries(sess, one)
    assert sess["positions"][0]["entry_px"] == px["2026-11-02 13:36"]
    assert sess["positions"][0]["bt_entry_px"] == px["2026-11-02 13:35"]
    state = {"equity": 100000.0}
    rows = I.close_all(sess, one, state)
    r = rows[0]
    gross = -1 * (px["2026-11-02 13:55"] / px["2026-11-02 13:36"] - 1) * 1e4
    assert r["gross_bps"] == pytest.approx(gross, abs=0.01) and r["net_bps"] == pytest.approx(gross - 5, abs=0.01)
    assert state["equity"] == pytest.approx(100000 + 1000 * (gross - 5) / 1e4, abs=0.01)
    assert r["shortfall_bps"] < 0  # a short entered a minute later, after the price rose: the delay helped


def test_no_session_outside_windows(tmp_io, monkeypatch):
    monkeypatch.setattr(I, "now_ny", lambda: pd.Timestamp("2026-11-02 13:50"))
    assert I.run_session(5) == "SESSION DONE"
    assert I.load_state()["session"] is None


def test_forward_verdict_bars():
    import tagym.intraday_fwd as fw
    days = pd.bdate_range("2026-11-04", periods=45)

    def ev(gross_by_day):
        return pd.DataFrame({"rule": "RX", "sym": "AAA", "day": days[:len(gross_by_day)], "hour": 10, "minute": 35,
                             "side": 1, "gross_bps": gross_by_day})
    rng = np.random.default_rng(0)
    assert fw.summarize(ev(list(rng.normal(30, 3, 10)))).verdict.iloc[0] == "TOO EARLY"        # < 20 days never passes
    assert fw.summarize(ev(list(rng.normal(30, 3, 25)))).verdict.iloc[0] == "CANDIDATE"        # strong, but < 40 days
    assert fw.summarize(ev(list(rng.normal(30, 3, 45)))).verdict.iloc[0] == "PASS"
    assert fw.summarize(ev(list(rng.normal(0, 5, 45)))).verdict.iloc[0] == "NO EDGE"
    assert fw.summarize(ev(list(rng.normal(3, 5, 45)))).verdict.iloc[0] in ("NO EDGE", "CANDIDATE")  # +3 gross < 5 cost
