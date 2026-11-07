"""Broker-path tests for tagym.demo with a fake Alpaca (no network, no keys)."""
import itertools

import pandas as pd
import pytest

import tagym.demo as d

NY = "America/New_York"


class FakeAlpaca:
    def __init__(self, cash=100000.0):
        self.cash = cash
        self.orders_ = {}
        self.pos = {}
        self.ids = itertools.count(1)

    def account(self):
        eq = self.cash + sum(q * 100 for q in self.pos.values())
        return {"cash": str(self.cash), "equity": str(eq), "account_number": "PAPER", "status": "ACTIVE"}

    def clock(self):
        return {"is_open": False, "next_open": "2026-11-02T09:30:00-05:00"}

    def positions(self):
        return [{"symbol": k, "qty": str(v)} for k, v in self.pos.items() if v]

    def orders(self, status="all", after=None, limit=500):
        return [o for o in self.orders_.values() if status == "all" or o["status"] in ("new", "accepted")]

    def order(self, oid):
        return self.orders_[oid]

    def submit(self, symbol, qty, side, type_="market", tif="opg", stop_price=None, client_order_id=None):
        if side == "sell" and type_ == "market":
            resting = sum(int(o["qty"]) for o in self.orders_.values()
                          if o["symbol"] == symbol and o["type"] == "stop" and o["status"] == "new")
            if resting + qty > self.pos.get(symbol, 0):
                raise d.BrokerError("403: insufficient qty available for order")
        oid = f"id{next(self.ids)}"
        self.orders_[oid] = {"id": oid, "symbol": symbol, "qty": str(qty), "side": side, "type": type_,
                             "time_in_force": tif, "stop_price": stop_price, "status": "new", "filled_qty": "0",
                             "client_order_id": client_order_id}
        return self.orders_[oid]

    def cancel(self, oid):
        self.orders_[oid]["status"] = "canceled"

    # test helpers: the exchange fills orders
    def fill(self, oid, price, when="2026-11-02T14:30:05Z"):
        o = self.orders_[oid]
        q = int(o["qty"])
        o.update(status="filled", filled_qty=str(q), filled_avg_price=str(price), filled_at=when)
        sgn = 1 if o["side"] == "buy" else -1
        self.pos[o["symbol"]] = self.pos.get(o["symbol"], 0) + sgn * q
        self.cash -= sgn * q * price


def bars_for(tickers):
    idx = pd.to_datetime(["2026-10-30", "2026-11-02"])
    out = {}
    for t in tickers + ["SPY"]:
        out[t] = pd.DataFrame({"o": [100.0, 101.0], "h": [102.0, 103.0], "l": [99.0, 95.0], "c": [101.0, 102.0],
                               "v": [1e6, 1e6]}, index=idx)
    return out


@pytest.fixture
def tmp_demo(tmp_path, monkeypatch):
    for k in ["STATE", "TRADES", "EQUITY", "FLIPS", "LOG", "REPORT"]:
        monkeypatch.setattr(d, k, tmp_path / getattr(d, k).name)
    monkeypatch.setattr(d, "DEMO", tmp_path)
    return tmp_path


def state_with_orders():
    s = {"initial_capital": 100000.0, "cash": 100000.0, "positions": {}, "spy_base": None, "broker": "alpaca-paper",
         "pending": [{"symbol": "NASDAQ:MSFT", "ticker": "MSFT", "side": "BUY", "shares": 10, "created": "2026-10-30",
                      "rule": "D3", "reason": "BULLISH", "stop": 96.0, "atr": 2.0, "ref_close": 100.0},
                     {"symbol": "NYSE:BRK.B", "ticker": "BRK-B", "side": "BUY", "shares": 5, "created": "2026-10-30",
                      "rule": "D3", "reason": "BULLISH", "stop": 90.0, "atr": 3.0, "ref_close": 100.0}]}
    return s


def test_preopen_submits_opg_and_symbol_mapping(tmp_demo):
    br, s, logs = FakeAlpaca(), state_with_orders(), []
    d.broker_submit(s, br, pd.Timestamp("2026-11-02 08:23", tz=NY), logs)
    sent = list(br.orders_.values())
    assert [o["time_in_force"] for o in sent] == ["opg", "opg"]
    assert {o["symbol"] for o in sent} == {"MSFT", "BRK.B"}  # BRK-B mapped to Alpaca's BRK.B
    assert all(o.get("broker_id") for o in s["pending"])


def test_late_submission_uses_day_orders(tmp_demo):
    br, s, logs = FakeAlpaca(), state_with_orders(), []
    d.broker_submit(s, br, pd.Timestamp("2026-11-02 09:40", tz=NY), logs)
    assert all(o["time_in_force"] == "day" for o in br.orders_.values())


def test_sync_fills_places_stops_and_detects_stop_execution(tmp_demo):
    br, s, logs = FakeAlpaca(), state_with_orders(), []
    d.broker_submit(s, br, pd.Timestamp("2026-11-02 08:23", tz=NY), logs)
    for o in s["pending"]:
        br.fill(o["broker_id"], 101.05)
    bars = bars_for(["MSFT", "BRK-B"])
    tr = d.broker_sync(s, br, bars, "midday", pd.Timestamp("2026-11-02 12:23", tz=NY), logs)
    assert len(tr) == 2 and not s["pending"]
    assert s["positions"]["NASDAQ:MSFT"]["shares"] == 10
    stops = [o for o in br.orders_.values() if o["type"] == "stop"]
    assert len(stops) == 2 and all(o["time_in_force"] == "gtc" for o in stops)
    assert tr[0]["slippage_bps_vs_open"] == pytest.approx(4.95, abs=0.01)  # 101.05 vs open 101 = +4.95 bps
    assert s["spy_base"]["open"] == 101.0
    # the exchange triggers MSFT's stop
    sid = s["positions"]["NASDAQ:MSFT"]["stop_order_id"]
    br.fill(sid, 95.9, when="2026-11-02T19:00:00Z")
    tr2 = d.broker_sync(s, br, bars, "preclose", pd.Timestamp("2026-11-02 15:23", tz=NY), logs)
    assert any(t["rule"] == "STOP" for t in tr2) and "NASDAQ:MSFT" not in s["positions"]


def test_trim_cancels_resting_stop_before_selling(tmp_demo):
    br, s, logs = FakeAlpaca(), state_with_orders(), []
    s["pending"] = s["pending"][:1]
    d.broker_submit(s, br, pd.Timestamp("2026-11-02 08:23", tz=NY), logs)
    br.fill(s["pending"][0]["broker_id"], 101.0)
    bars = bars_for(["MSFT"])
    d.broker_sync(s, br, bars, "midday", pd.Timestamp("2026-11-02 12:23", tz=NY), logs)
    s["pending"].append({"symbol": "NASDAQ:MSFT", "ticker": "MSFT", "side": "SELL", "shares": 5, "created": "2026-11-02",
                         "rule": "§8.5", "reason": "earnings trim", "trim": True, "ref_close": 102.0})
    d.broker_submit(s, br, pd.Timestamp("2026-11-03 08:23", tz=NY), logs)  # would raise 403 if the stop still rested
    assert not any(x["action"] == "SUBMIT_FAILED" for x in logs)


def test_append_never_shifts_columns(tmp_demo):
    """A sale (has pnl) after buys (no pnl) must not corrupt the CSV (regression: demo trades.csv, Nov 4)."""
    d.append(d.TRADES, [{"date": "2026-11-02", "symbol": "A", "side": "BUY", "shares": 1, "price": 10.0, "prev_close": 9.9, "gap_pct": 1.0}])
    d.append(d.TRADES, [{"date": "2026-11-04", "symbol": "A", "side": "SELL", "shares": 1, "price": 9.0, "pnl": -1.0}])
    d.append(d.TRADES, [{"date": "2026-11-05", "symbol": "B", "side": "BUY", "shares": 2, "price": 5.0, "prev_close": 5.1, "gap_pct": -2.0},
                        {"date": "2026-11-05", "symbol": "B", "side": "SELL", "shares": 2, "price": 4.0, "pnl": -2.0}])
    t = pd.read_csv(d.TRADES)
    assert len(t) == 4 and list(t.symbol) == ["A", "A", "B", "B"]
    assert t.pnl.dropna().tolist() == [-1.0, -2.0] and t.gap_pct.dropna().tolist() == [1.0, -2.0]
