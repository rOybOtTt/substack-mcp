"""Blind self-test harness for the rulebook.

generate(): samples random (stock, date) cases, strips identity (no ticker,
no dates, prices rebased to 100) and writes an anonymised packet with the
same information an agent could compute from TradingView OHLCV:
  * indicator snapshot (trend/momentum/oscillators/volume/volatility),
  * 26 weekly bars (rebased OHLC + volume ratio),
  * market context (index regime, breadth),
  * the answer key (forward returns) goes to a SEPARATE file.
score(): joins an agent's JSON answers with the key and grades them.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from .evaluate import forward_returns, universe_benchmark
from .diagnose import fwd_min_return
from .signals import trend_template

ROOT = Path(__file__).resolve().parents[2]
BLIND = ROOT / "blind_tests"


def snapshot(x, t, k, spy_close):
    """Indicator snapshot for stock column k at row t (uses data <= t only)."""
    c, h, l, o, v = (s.iloc[:t + 1, k] for s in (x.c, x.h, x.l, x.o, x.v))
    last = c.iloc[-1]
    def ratio(a): return None if not np.isfinite(a) else round(float(last / a - 1) * 100, 1)
    s20, s50, s150, s200 = (x.sma(n).iat[t, k] for n in (20, 50, 150, 200))
    s200_prev = x.sma(200).iat[t - 21, k]
    s50_prev = x.sma(50).iat[t - 10, k]
    hi52 = c.iloc[-252:].max(); lo52 = c.iloc[-252:].min()
    macd_l, macd_s, macd_h = (m.iat[t, k] for m in x.macd())
    adx, pdi, ndi = (m.iat[t, k] for m in x.adx())
    mid, up, lo_, pb, bw = (m.iat[t, k] for m in x.bb())
    bw_series = x.bb()[4].iloc[t - 126:t + 1, k]
    stk, std = (m.iat[t, k] for m in x.stoch())
    vr50 = x.volr(50).iat[t, k]
    v5 = v.iloc[-5:].mean() / v.iloc[-55:-5].mean()
    up_v = v[c.diff() > 0].iloc[-20:].mean(); dn_v = v[c.diff() < 0].iloc[-20:].mean()
    rng60 = (h.iloc[-61:-1].max() / l.iloc[-61:-1].min() - 1) * 100
    spy = spy_close.iloc[:t + 1]
    spy_m = spy.resample("ME").last()
    if spy.index[-1] != spy_m.index[-1]:  # current month incomplete -> use completed months only
        spy_m = spy_m.iloc[:-1]
    snap = {
        "close_vs_sma20_pct": ratio(s20), "close_vs_sma50_pct": ratio(s50),
        "close_vs_sma150_pct": ratio(s150), "close_vs_sma200_pct": ratio(s200),
        "sma200_slope_1m_pct": round(float(s200 / s200_prev - 1) * 100, 2),
        "sma50_slope_2w_pct": round(float(s50 / s50_prev - 1) * 100, 2),
        "sma50_above_sma200": bool(s50 > s200),
        "pct_from_52w_high": round(float(last / hi52 - 1) * 100, 1),
        "pct_above_52w_low": round(float(last / lo52 - 1) * 100, 1),
        "ret_5d_pct": round(float(x.roc(5).iat[t, k]) * 100, 1),
        "ret_1m_pct": round(float(x.roc(21).iat[t, k]) * 100, 1),
        "ret_3m_pct": round(float(x.roc(63).iat[t, k]) * 100, 1),
        "ret_6m_pct": round(float(x.roc(126).iat[t, k]) * 100, 1),
        "ret_12m_pct": round(float(x.roc(252).iat[t, k]) * 100, 1),
        "rs_6m_percentile_vs_universe": round(float(x.xs_rank(x.roc(126)).iat[t, k]) * 100),
        "rsi14": round(float(x.rsi(14).iat[t, k]), 1), "rsi2": round(float(x.rsi(2).iat[t, k]), 1),
        "macd_line": round(float(macd_l / last * 100), 3), "macd_signal": round(float(macd_s / last * 100), 3),
        "macd_hist_rising": bool(x.macd()[2].iat[t, k] > x.macd()[2].iat[t - 1, k]),
        "adx14": round(float(adx), 1), "plus_di": round(float(pdi), 1), "minus_di": round(float(ndi), 1),
        "bollinger_pctb": round(float(pb), 2), "bollinger_bandwidth_pctile_6m": round(float((bw_series <= bw).mean() * 100)),
        "stoch_k": round(float(stk), 1), "stoch_d": round(float(std), 1),
        "atr14_pct_of_price": round(float(x.natr(14).iat[t, k]) * 100, 2),
        "atr_pct_percentile_vs_universe": round(float(x.xs_rank(x.natr(14)).iat[t, k]) * 100),
        "volume_today_vs_50d": round(float(vr50), 2), "volume_5d_vs_prior_50d": round(float(v5), 2),
        "updown_volume_ratio_20d": round(float(up_v / dn_v), 2) if dn_v > 0 else None,
        "range_60d_pct": round(float(rng60), 1),
        "pct_from_60d_high": round(float(last / c.iloc[-60:].max() - 1) * 100, 1),
        "volume_10d_vs_prior_50d": round(float(v.iloc[-10:].mean() / v.iloc[-60:-10].mean()), 2),
        "last_close_above_5usd": bool(last >= 5),
        "close_location_in_day_range": round(float(x.clv().iat[t, k]), 2),
        "today_ret_pct": round(float(x.ret1().iat[t, k]) * 100, 2),
        "gap_today_pct": round(float(o.iloc[-1] / c.iloc[-2] - 1) * 100, 2),
        "minervini_trend_template": bool(trend_template(x).iat[t, k]),
        "market_index_above_10m_sma": bool(spy_m.iloc[-1] > spy_m.iloc[-10:].mean()),
        "market_index_above_200d_sma": bool(spy.iloc[-1] > spy.iloc[-200:].mean()),
        "market_index_sma50_above_sma200": bool(spy.iloc[-50:].mean() > spy.iloc[-200:].mean()),
        "rsi10": round(float(x.get(("rsi", 10), lambda: __import__("tagym.indicators", fromlist=["rsi"]).rsi(x.c, 10)).iat[t, k]), 1),
        "rsi14_yesterday": round(float(x.rsi(14).iat[t - 1, k]), 1),
        "consecutive_up_closes": int(next((i for i, u in enumerate((c.diff() > 0).iloc[::-1]) if not u), 0)),
        "median_dollar_volume_20d_musd": round(float((c * v).iloc[-20:].median() / 1e6), 1),
        "bars_available": int(c.notna().sum()),
        "market_index_pct_from_52w_high": round(float(spy.iloc[-1] / spy.iloc[-252:].max() - 1) * 100, 1),
        "market_breadth_pct_above_200d": round(float(x.breadth(200).iat[t, k]) * 100),
    }
    # weekly bars rebased to 100 at the first week
    wk = pd.DataFrame({"o": o, "h": h, "l": l, "c": c, "v": v}).iloc[-130:]
    g = wk.groupby(np.arange(len(wk)) // 5)
    W = pd.DataFrame({"o": g.o.first(), "h": g.h.max(), "l": g.l.min(), "c": g.c.last(), "v": g.v.sum()})
    base = W.c.iloc[0]
    W[["o", "h", "l", "c"]] = (W[["o", "h", "l", "c"]] / base * 100).round(1)
    W["vol_vs_avg"] = (W.v / W.v.mean()).round(2)
    weekly = W[["o", "h", "l", "c", "vol_vs_avg"]].values.tolist()
    return snap, weekly


def generate(x, n, period_mask, seed, round_name, horizons=(20, 60), key_dir=None):
    rng = np.random.default_rng(seed)
    ok = (period_mask & x.tradeable & x.sma(200).notna() & x.c.rolling(260).count().ge(260)).values.copy()
    T, K = ok.shape
    # leave room for labels
    ok[-70:, :] = False
    cand = np.argwhere(ok)
    pick = cand[rng.choice(len(cand), n, replace=False)]
    spy = x.mkt("SPY")
    frs = {hh: forward_returns(x.p, hh) for hh in horizons}
    bench = {hh: universe_benchmark(frs[hh], x.tradeable) for hh in horizons}
    fm = fwd_min_return(x.p, 60)
    cases, key = [], []
    for i, (t, k) in enumerate(pick):
        cid = f"{round_name}-{i:03d}"
        snap, weekly = snapshot(x, t, k, spy)
        cases.append({"case_id": cid, "indicators": snap,
                      "weekly_bars_rebased_[o,h,l,c,vol_vs_avg]_oldest_first": weekly})
        rec = {"case_id": cid, "ticker": x.c.columns[k], "date": str(x.c.index[t].date())}
        for hh in horizons:
            rec[f"ret{hh}"] = float(frs[hh].iat[t, k]); rec[f"exc{hh}"] = float(frs[hh].iat[t, k] - bench[hh].iat[t])
        rec["maxdd60"] = float(fm.iat[t, k])
        key.append(rec)
    d = BLIND / round_name
    d.mkdir(parents=True, exist_ok=True)
    (d / "cases.json").write_text(json.dumps(cases, indent=0))
    kd = Path(key_dir) if key_dir else d
    kd.mkdir(parents=True, exist_ok=True)
    (kd / f"{round_name}_answer_key.json").write_text(json.dumps(key, indent=1))
    return d


def score(round_name, answers_file="answers.json", key_dir=None):
    d = BLIND / round_name
    kd = Path(key_dir) if key_dir else d
    key = pd.DataFrame(json.loads((kd / f"{round_name}_answer_key.json").read_text())).set_index("case_id")
    ans = pd.DataFrame(json.loads((d / answers_file).read_text())).set_index("case_id")
    j = key.join(ans, how="inner")
    j["signal"] = j["signal"].str.upper().str.replace(" ", "_")
    out = {"n": len(j)}
    for s in ["BULLISH", "NO_SIGNAL", "BEARISH"]:
        g = j[j.signal == s]
        out[s] = {"n": int(len(g)), "exc20": float(g.exc20.mean()) if len(g) else None,
                  "exc60": float(g.exc60.mean()) if len(g) else None,
                  "ret60": float(g.ret60.mean()) if len(g) else None,
                  "hit60_excess>0": float((g.exc60 > 0).mean()) if len(g) else None,
                  "p_dd20": float((g.maxdd60 <= -0.2).mean()) if len(g) else None}
    # directional accuracy on cases where agent took a side
    side = j[j.signal != "NO_SIGNAL"]
    if len(side):
        sgn = np.where(side.signal == "BULLISH", 1, -1)
        out["directional_hit_exc60"] = float((np.sign(side.exc60) == sgn).mean())
        out["avg_signed_exc60"] = float((sgn * side.exc60).mean())
    if "risk_flag" in j:
        rf = j.risk_flag.astype(str).str.upper().isin(["TRUE", "HIGH", "YES"])
        out["risk_flag"] = {"flagged_p_dd20": float((j[rf].maxdd60 <= -0.2).mean()) if rf.any() else None,
                            "unflagged_p_dd20": float((j[~rf].maxdd60 <= -0.2).mean()) if (~rf).any() else None,
                            "n_flagged": int(rf.sum())}
    (d / "score.json").write_text(json.dumps(out, indent=1))
    return out, j
