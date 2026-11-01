"""Data layer for TA Gym.

Downloads split/dividend-adjusted daily OHLCV with yfinance and stores one
parquet file per field (rows = dates, columns = tickers).

Survivorship caveat: the universe is *today's* S&P 1500 constituents, so
stocks that were delisted/bankrupt between 1995 and today are missing.
TA Gym therefore scores every stock signal as EXCESS return versus the
equal-weight average of the same (equally biased) universe on the same
dates, and re-checks key rules on ETFs/indices (no survivorship bias).
"""
from __future__ import annotations

import os
import time
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(os.environ.get(
    "TAGYM_DATA",
    "/tmp/claude-0/-home-user-substack-mcp/bd2a3180-4a74-5075-a5b0-357ed5501f5e/scratchpad/data"))
FIELDS = ["Open", "High", "Low", "Close", "Volume"]

ETFS = ["SPY", "QQQ", "IWM", "DIA", "MDY", "XLK", "XLF", "XLE", "XLV", "XLI", "XLY",
        "XLP", "XLU", "XLB", "EFA", "EEM", "TLT", "IEF", "GLD", "SLV", "USO", "VNQ",
        "SMH", "IYT", "EWJ", "EWZ", "FXI", "HYG", "LQD"]
INDICES = ["^GSPC", "^DJI", "^DJT", "^IXIC", "^RUT", "^VIX", "^NDX"]


def universe_tickers(which=("sp500", "sp400", "sp600")) -> pd.DataFrame:
    frames = []
    for name in which:
        df = pd.read_csv(DATA_DIR / f"{name}_constituents.csv")
        df = df.rename(columns={"Symbol": "ticker", "GICS Sector": "sector"})
        df["index"] = name
        frames.append(df[["ticker", "sector", "index"]])
    u = pd.concat(frames).drop_duplicates("ticker")
    u["ticker"] = u["ticker"].str.replace(".", "-", regex=False)  # BRK.B -> BRK-B
    return u.reset_index(drop=True)


def download(tickers, start="1995-01-01", end=None, batch=60, tag="stocks"):
    import yfinance as yf
    parts = {f: [] for f in FIELDS}
    for i in range(0, len(tickers), batch):
        chunk = tickers[i:i + batch]
        for attempt in range(4):
            try:
                d = yf.download(chunk, start=start, end=end, auto_adjust=True,
                                progress=False, group_by="column", threads=True)
                break
            except Exception as e:  # network hiccup / rate limit
                print("retry", attempt, e)
                time.sleep(5 * (attempt + 1))
        else:
            continue
        for f in FIELDS:
            x = d[f]
            if isinstance(x, pd.Series):
                x = x.to_frame(chunk[0])
            parts[f].append(x)
        print(f"{tag}: {min(i + batch, len(tickers))}/{len(tickers)}", flush=True)
        time.sleep(1.5)
    for f in FIELDS:
        panel = pd.concat(parts[f], axis=1)
        panel = panel.loc[:, ~panel.columns.duplicated()].sort_index()
        panel.index = pd.to_datetime(panel.index).tz_localize(None)
        panel.to_parquet(DATA_DIR / f"{tag}_{f}.parquet")
    return True


def load(tag="stocks", start=None, end=None) -> dict[str, pd.DataFrame]:
    out = {}
    for f in FIELDS:
        p = pd.read_parquet(DATA_DIR / f"{tag}_{f}.parquet")
        if start is not None:
            p = p.loc[start:]
        if end is not None:
            p = p.loc[:end]
        out[f] = p.astype("float64")
    return out


def clean(panel: dict[str, pd.DataFrame], min_price=5.0, min_dollar_vol=5e6) -> dict[str, pd.DataFrame]:
    """Basic hygiene: drop impossible bars, and build a tradeability mask.

    tradeable[t, k] is True if close >= min_price and 20-day median dollar
    volume >= min_dollar_vol, both known at t (no look-ahead).
    """
    o, h, l, c, v = (panel[k] for k in FIELDS)
    bad = (h < l) | (c <= 0) | (o <= 0) | c.isna()
    for k in ["Open", "High", "Low", "Close"]:
        panel[k] = panel[k].mask(bad)
    # kill absurd one-day jumps that revert (bad prints): |r|>80% and reverses next day
    r = c.pct_change(fill_method=None)
    spike = (r.abs() > 0.8) & (r.shift(-1).abs() > 0.4) & (np.sign(r) != np.sign(r.shift(-1)))
    for k in ["Open", "High", "Low", "Close"]:
        panel[k] = panel[k].mask(spike)
    dv = (panel["Close"] * panel["Volume"]).rolling(20, min_periods=15).median()
    panel["tradeable"] = (panel["Close"] >= min_price) & (dv >= min_dollar_vol)
    return panel


if __name__ == "__main__":
    import sys
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("etf", "all"):
        download(ETFS + INDICES, tag="etf", batch=40)
    if what in ("stocks", "all"):
        u = universe_tickers()
        u.to_csv(DATA_DIR / "universe.csv", index=False)
        download(u["ticker"].tolist(), tag="stocks")
