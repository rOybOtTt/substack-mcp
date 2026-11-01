"""Survivorship check: apply the frozen rulebook to stocks that were later DELISTED
(random sample from EODHD's delisted NYSE/NASDAQ common stocks)."""
from __future__ import annotations

import glob
import os

import numpy as np
import pandas as pd

from .data import load, clean, DATA_DIR
from .features import Ctx

DL_DIR = DATA_DIR.parent / "delisted" / "csv"


def load_delisted(index: pd.DatetimeIndex):
    fields = {k: {} for k in ["Open", "High", "Low", "Close", "Volume"]}
    meta = {}
    for f in sorted(glob.glob(str(DL_DIR / "*.csv"))):
        t = os.path.basename(f)[:-4]
        d = pd.read_csv(f, parse_dates=["Date"]).set_index("Date").sort_index()
        d = d[~d.index.duplicated()]
        if len(d) < 300 or d["Close"].isna().all():
            continue
        adj = (d["Adjusted_close"] / d["Close"]).replace([np.inf, -np.inf], np.nan).fillna(1.0)
        for k in ["Open", "High", "Low", "Close"]:
            fields[k][t] = (d[k] * adj).reindex(index)
        fields["Volume"][t] = d["Volume"].reindex(index)
        meta[t] = {"first": d.index[0], "last": d.index[-1], "last_close": float(d["Close"].iloc[-1]),
                   "peak_close": float(d["Close"].max())}
    panel = {k: pd.DataFrame(v) for k, v in fields.items()}
    return panel, pd.DataFrame(meta).T


def build_ctx():
    ref = load("stocks")["Close"].index
    p, meta = load_delisted(ref)
    p = clean(p)
    return Ctx(p, market=load("etf")["Close"]), meta
