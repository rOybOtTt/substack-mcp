"""tagym.dashboard export: shapes the dashboard relies on (no network)."""
import json

import pandas as pd

import tagym.dashboard as db
import tagym.demo as d

NY = "America/New_York"


def setup(tmp_path, monkeypatch, state):
    for k in ["STATE", "TRADES", "EQUITY", "FLIPS", "LOG", "REPORT"]:
        monkeypatch.setattr(d, k, tmp_path / getattr(d, k).name)
    monkeypatch.setattr(d, "DEMO", tmp_path)
    monkeypatch.setattr(db, "OUT", tmp_path / "dashboard")
    monkeypatch.setattr(db, "MARKS", tmp_path / "marks.csv")
    monkeypatch.setattr(db, "PAPER", tmp_path)
    monkeypatch.setattr(db, "JOURNAL", tmp_path / "journal.csv")
    d.save_state(state)
    pd.DataFrame([{"date": "2026-10-30", "equity": 100000.0, "cash": 100000.0, "positions": 0,
                   "spy_benchmark": 100000.0, "pending_orders": 1}]).to_csv(d.EQUITY, index=False)
    pd.DataFrame([{"as_of": "2026-10-30", "symbol": "NASDAQ:MSFT", "ticker": "MSFT", "sector": "IT", "signal": "BULLISH",
                   "row": "D3", "regime": "RISK_ON", "health": "HEALTHY", "timing": "NORMAL", "risk_flag": "NORMAL",
                   "p_dd20_60d_est": 0.06, "p_drop10_10d_est": 0.03, "earnings_due_10d": False, "close": 100.0}]
                 ).to_csv(tmp_path / "journal.csv", index=False)


def state():
    return {"initial_capital": 100000.0, "cash": 98990.0, "broker": "simulated", "spy_base": {"date": "2026-11-02", "open": 500.0},
            "positions": {"NASDAQ:MSFT": {"ticker": "MSFT", "shares": 10, "entry_date": "2026-11-02", "entry_price": 101.0,
                                          "stop": 96.0, "atr_at_entry": 2.0, "trimmed": False}},
            "pending": [{"symbol": "NYSE:KO", "ticker": "KO", "side": "BUY", "shares": 5, "created": "2026-11-02",
                         "rule": "D3", "reason": "BULLISH", "stop": 60.0, "atr": 1.0, "ref_close": 65.0}]}


def test_export_marks_book_and_json(tmp_path, monkeypatch):
    setup(tmp_path, monkeypatch, state())
    monkeypatch.setattr(db, "last_prices", lambda t: {"MSFT": 105.0, "KO": 64.0, "SPY": 505.0})
    when = pd.Timestamp("2026-11-02 12:23", tz=NY)
    files = db.export("midday", when=when)
    eq = files["equity"]
    assert [r["mode"] for r in eq] == ["close", "midday"]  # seeded from equity.csv, then this run
    assert eq[-1]["equity"] == 98990.0 + 10 * 105.0 and eq[-1]["spy_benchmark"] == 101000.0
    held = next(r for r in files["book"] if r["status"] == "Held")
    assert held["pnl"] == 40.0 and held["value"] == 1050.0
    assert any(r["status"] == "Buy at next open" for r in files["book"])
    assert files["journal"][0]["earnings_due_10d"] is False
    for name in files:  # strict JSON (no NaN) that the dashboard can read
        json.loads((tmp_path / "dashboard" / f"{name}.json").read_text())
    db.export("midday", when=when + pd.Timedelta(minutes=5))  # a re-run of the same slot replaces its mark
    assert len(pd.read_csv(tmp_path / "marks.csv")) == 2
