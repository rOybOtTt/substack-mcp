"""Minimal Alpaca PAPER-trading client (REST v2), used by tagym.demo when keys are present.

Keys are read from environment variables, never from files or chat:
    ALPACA_API_KEY_ID, ALPACA_API_SECRET_KEY        (paper-account keys)
    ALPACA_BASE_URL  (optional; defaults to https://paper-api.alpaca.markets)
Refuses to run against the live-trading URL.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request

PAPER_URL = "https://paper-api.alpaca.markets"


class BrokerError(RuntimeError):
    pass


class Alpaca:
    def __init__(self, key, secret, base=PAPER_URL):
        if "paper-api" not in base:
            raise BrokerError("refusing to trade: ALPACA_BASE_URL is not the paper-trading endpoint")
        base = base.rstrip("/")
        if base.endswith("/v2"):  # accept the endpoint as Alpaca's dashboard shows it (".../v2")
            base = base[:-3]
        self.key, self.secret, self.base = key, secret, base

    @classmethod
    def from_env(cls):
        k, s = os.environ.get("ALPACA_API_KEY_ID"), os.environ.get("ALPACA_API_SECRET_KEY")
        if not k or not s:
            return None
        return cls(k, s, os.environ.get("ALPACA_BASE_URL", PAPER_URL))

    def _req(self, method, path, body=None, params=None):
        url = self.base + path + ("?" + urllib.parse.urlencode(params) if params else "")
        data = json.dumps(body).encode() if body is not None else None
        r = urllib.request.Request(url, data=data, method=method, headers={
            "APCA-API-KEY-ID": self.key, "APCA-API-SECRET-KEY": self.secret, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(r, timeout=30) as resp:
                txt = resp.read().decode()
                return json.loads(txt) if txt else None
        except urllib.error.HTTPError as e:
            raise BrokerError(f"{method} {path} -> {e.code}: {e.read().decode()[:300]}") from None

    # --- endpoints
    def account(self):
        return self._req("GET", "/v2/account")

    def clock(self):
        return self._req("GET", "/v2/clock")

    def positions(self):
        return self._req("GET", "/v2/positions")

    def orders(self, status="all", after=None, limit=500):
        p = {"status": status, "limit": limit, "direction": "asc", "nested": "false"}
        if after:
            p["after"] = after
        return self._req("GET", "/v2/orders", params=p)

    def order(self, oid):
        return self._req("GET", f"/v2/orders/{oid}")

    def submit(self, symbol, qty, side, type_="market", tif="opg", stop_price=None, client_order_id=None):
        body = {"symbol": symbol, "qty": str(int(qty)), "side": side, "type": type_, "time_in_force": tif}
        if stop_price is not None:
            body["stop_price"] = f"{stop_price:.2f}"
        if client_order_id:
            body["client_order_id"] = client_order_id[:128]
        return self._req("POST", "/v2/orders", body)

    def cancel(self, oid):
        try:
            return self._req("DELETE", f"/v2/orders/{oid}")
        except BrokerError as e:
            if "404" in str(e) or "422" in str(e):  # already filled / cancelled
                return None
            raise


def to_alpaca(ticker: str) -> str:
    """yfinance ticker -> Alpaca symbol (BRK-B -> BRK.B)."""
    return ticker.replace("-", ".")
