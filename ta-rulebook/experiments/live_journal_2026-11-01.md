# Live journal — 2026-11-01 (forward test of RULEBOOK v2.1 on live TradingView data)

**Status: FORWARD PREDICTIONS, not yet scored.** These signals were produced on Sunday 2026-11-01 from the
last completed daily bar (Friday **2026-10-30**; the market was closed, so the last bar was not dropped).
They are to be scored after **20 and 60 trading days**: score dates **≈ 2026-11-30** (20th NYSE session) and
**≈ 2027-01-27** (the exact 60th NYSE session after 2026-10-30 is **2027-01-28**, counting the Thanksgiving,
Christmas, New Year's Day and MLK Day closures).

## 1. Provenance

| Item | Value |
|---|---|
| Data call | `mcp-tv-get-ohlcv(symbol, interval="1D", count=270, format="columns")`, one call per symbol |
| Window | 270 daily bars, 2025-10-06 → 2026-10-30 (same 270 timestamps for every symbol) |
| Raw bars | `bars` object saved verbatim to `/tmp/claude-0/-home-user-substack-mcp/bd2a3180-4a74-5075-a5b0-357ed5501f5e/scratchpad/live/<TICKER>.json`. Checked: all 6 arrays have length 270; last close, max(h), min(l), Σv and first open match each response's `summary` block exactly |
| Engine | `python3 -m tagym.live <TICKER>.json SPY.json --symbol <EXCH:TICKER>` (no `--drop-last`) |
| Engine version | `platform/tagym/live.py` sha256 `8e5da132…a4770` (v2.1: B3 clause, calibrated `p_drawdown20_60d_est`, `near_threshold`). Every output below was re-run once and came out byte-identical |
| Rulebook | `RULEBOOK.md` v2.1 |

*Integrity note.* While this run was in progress, `live.py` (00:16 UTC) and `RULEBOOK.md` (00:17 UTC) were updated from v2.0 to v2.1 by another process. This run did not modify them. All outputs below come from the v2.1 engine (hash above). Under the v2.0 code the signal and decision row would be the same for all 8 stocks: the new B3 clause fires for none of them (TSLA closes above its SMA200, and INTC is already BROKEN via B2). Only the `p_drawdown20_60d_est`, `risk_flag` and `confidence` fields differ.

## 2. Market regime (Q1)

SPY close 755.72. Last completed month-end used by the engine is 762.63 (Sep 30), against a 10-month mean of 720.88, so the month-end test is **true**. SMA50 is 767.49 against SMA200 at 728.85, so the cross test is **true**. Regime: **RISK_ON**.

The engine treats Oct 30 as an *incomplete* month, because it is not the calendar month-end, even though it was October's last session. With October counted (755.72 vs a mean of 728.26) the test is still true, so the regime does not change. This is flagged for the maintainers and was not changed here.

## 3. Signal table

| Symbol | Signal | Row | Regime | Health | Timing | Risk flag | Close | % from 52w high | RSI14 | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| NASDAQ:NVDA | NO_SIGNAL | D6 | RISK_ON | NEUTRAL | NORMAL | NORMAL | 204.64 | −14.5 | 35.1 | More than 10% off the high, so not HEALTHY. SMA200 is rising and SMA50 > SMA200, so not BROKEN. The close is only +0.1% above SMA200, so `near_threshold` is set and confidence is **low**. p(≥20% fall) 11.1%. TV rating "SELL" ignored (§1.1) |
| NASDAQ:AAPL | **BULLISH** | D3 | RISK_ON | HEALTHY | NORMAL | LOW | 344.63 | −1.2 | 55.3 | ATR% 2.00, RS6 +18.2 pts. p 6.0% |
| NASDAQ:MSFT | **BULLISH** | D3 | RISK_ON | HEALTHY | NORMAL | LOW | 521.91 | −4.0 | 49.0 | ATR% 2.28, RS6 +21.1 pts. p 6.0% |
| NYSE:JPM | **BULLISH** | D3 | RISK_ON | HEALTHY | NORMAL | LOW | 337.04 | −7.7 | 49.0 | Weakest member of the D3 group: 2.3 pts from the −10% cut, SMA200 slope only +0.39%/month, close +4.4% over SMA200. p 6.0% |
| NYSE:XOM | NO_SIGNAL | D4 | RISK_ON | HEALTHY | EXTENDED | NORMAL | 187.25 | 0.0 | 73.0 | RSI14 crossed above 70 on 10/30, at a 52-week closing high. "Healthy but extended; wait for a pullback." A3: don't buy the breakout bar. p 6.8% |
| NASDAQ:TSLA | NO_SIGNAL | D6 | RISK_ON | NEUTRAL | NORMAL | NORMAL | 399.81 | −18.4 | 60.9 | The close is above SMA200 (+3.8%), so neither B1 nor B3 applies. But SMA200 is falling (−2.1%/month) and SMA50 < SMA200, so not HEALTHY. ret5 is +7.4%, below the extended cut of about 16.5%. ATR% 3.36 is high-vol. p 11.1% |
| NYSE:UNH | **BULLISH** | D3 | RISK_ON | HEALTHY | NORMAL | LOW | 406.97 | −6.7 | 56.1 | ATR% 2.69. p 6.0% |
| NASDAQ:INTC | **BEARISH** | D2 | RISK_ON | BROKEN | NORMAL | HIGH | 65.76 | −53.3 | 25.1 | Fell −28.6% on 10/30 on 455.6M shares (about 4× average). BROKEN via B2 (≤ −40% from high). The close is 24.3% under SMA200, which is still rising. ATR% 10.6. p 15.6% (calibrated; probably an understatement for a stock this volatile and recently gapped). Oversold RSI and the volume climax are **not** buy signals (§6) |

**Ignored noise (§6, never changes the output):** NVDA's TradingView rating (SELL, value −0.49; MA summary STRONG_SELL). INTC's oversold RSI14 of 25 and RSI10 of 21, and its capitulation-like volume spike. XOM's 52-week-high "breakout".

**Summary:** 4 BULLISH (AAPL, MSFT, JPM, UNH), 1 BEARISH (INTC), 3 NO_SIGNAL (NVDA, TSLA, XOM). No A1 warnings, because SPY is above its 10-month SMA.

## 4. Independent cross-check — NVDA vs `mcp-tv-get-technicals-rating("NASDAQ:NVDA","1D")`

The engine's own functions (`tagym.live.rsi`, pandas rolling means) were applied to the saved bars and compared with TradingView's snapshot:

| Indicator | Engine | TradingView | Diff |
|---|---|---|---|
| RSI14 (Wilder) | 35.0560 | 35.0560 | 0.0000% |
| SMA50 | 221.7486 | 221.7486 | 0.0000% |
| SMA200 | 204.3846 | 204.3846 | 0.0000% |
| SMA10 / SMA20 / SMA100 (extra) | 214.6320 / 221.4595 / 214.5198 | 214.632 / 221.4595 / 214.5198 | 0.0000% |

**No discrepancy > 1%. All values match to 4 decimals.** TradingView's price (204.64) also matches the last close. Its snapshot volume (168,384,547) differs from the bar volume (168,386,423) by 0.001%. That difference is irrelevant, because no rule here uses the last bar's volume alone.

## 5. Scoring method (to run on 2026-11-30 and ≈ 2027-01-27/28)

This uses the same definitions as the backtest (`tagym.diagnose.fwd_min_return`).

- **Entry** = the open of the next session after the signal bar, Mon 2026-11-02 (O₁). Use the same entry for SPY. As a secondary check, also report close-to-close from the 10/30 close.
- **Return** over N sessions (N = 20, 60) = C(N) / O₁ − 1. **Excess** = stock return − SPY return.
- **Max drawdown** = min(close over sessions 1..N) / O₁ − 1. **Crash hit** = max drawdown ≤ −20%.
- Fetch with `mcp-tv-get-ohlcv(symbol,"1D",date_from="2026-10-30",format="columns")`. Use only completed bars.

**Class expectations to compare against (RULEBOOK §3 and §5, RISK_ON column):**

| Class | Names | P(≥ 20% fall within 60d) | Expected excess return |
|---|---|---|---|
| D3 BULLISH (low-risk trend) | AAPL, MSFT, JPM, UNH | 6.0% | ≈ 0 (±0.4% over 60d). The edge is risk, not return |
| D4 healthy and extended | XOM | 6.8% | ≈ 0. Short-term timing lag of −0.1% to −0.2% over 5–10 days (too small to judge on one name) |
| D6 neutral | NVDA, TSLA | 11.1% | ≈ 0 |
| D2 BEARISH (broken) | INTC | 15.6% (higher in reality: survivorship bias, ATR% 10.6) | ≈ 0. Not a short-sale call |

**Verdict rules (n = 8 is a sanity check, not a statistical test):**
1. **Risk ordering (primary):** mean and worst 60-day max drawdown should rank D2 (INTC) worse than D6 (NVDA, TSLA), and D6 worse than D3 (AAPL, MSFT, JPM, UNH). Record whether the ordering holds.
2. **Crash hits vs calibration:** count hits per class. With 4 D3 names at 6%, the chance of 0 hits is about 78%; 2 or more D3 hits would be a red flag. One INTC hit is "expected-ish" (p ≈ 16%+). Hits in D6 are consistent at p ≈ 11% each.
3. **Return (secondary, not a claim):** the rulebook predicts no reliable excess-return difference between classes. Record each name's excess vs SPY. Do **not** score D3 names "right" because they beat SPY, or INTC "right" because it lagged. Report it only as a check that no large class-level return edge appears.
4. **Invalidations:** for each D3 name, note whether the invalidation fired before the score date (close below SMA200, SMA200 rolling over, more than 10% off the 52w high, or regime leaving RISK_ON). For INTC, note whether health recovered (close above a rising SMA200 and within 40% of the 52w high). Also note whether SPY's regime changed.
5. The 20-day check (2026-11-30) is interim: report max drawdown and excess so far. The official verdict is at 60 days.

**Entry reference closes (10/30):** SPY 755.72 · NVDA 204.64 · AAPL 344.63 · MSFT 521.91 · JPM 337.04 · XOM 187.25 · TSLA 399.81 · UNH 406.97 · INTC 65.76.

## 6. Full engine outputs (verbatim)

### NASDAQ:NVDA
```json
{
 "symbol": "NASDAQ:NVDA",
 "as_of": "2026-10-30",
 "signal": "NO_SIGNAL",
 "decision_row": "D6",
 "layers": {
  "regime": "RISK_ON",
  "health": "NEUTRAL",
  "timing": "NORMAL"
 },
 "risk": {
  "p_drawdown20_60d_est": 0.111,
  "risk_flag": "NORMAL",
  "atr_pct": 3.04
 },
 "confidence": "low",
 "near_threshold": [
  "close_vs_sma200"
 ],
 "horizon_days": 60,
 "features": {
  "close": 204.64,
  "pct_from_52w_high": -14.5,
  "pct_from_60d_high": -14.5,
  "volume_10d_vs_prior_50d": 0.85,
  "close_vs_sma200_pct": 0.1,
  "sma200_rising": true,
  "sma50_gt_sma200": true,
  "rsi14": 35.1,
  "rsi10": 31.1,
  "rsi14_crossed_above_70_today": false,
  "close_above_upper_bb": false,
  "ret5_pct": -3.0,
  "rs_6m_vs_spy_pct": -1.7,
  "spy_above_10m_sma": true,
  "spy_sma50_gt_sma200": true
 },
 "warnings": [],
 "invalidation": "n/a"
}
```

### NASDAQ:AAPL
```json
{
 "symbol": "NASDAQ:AAPL",
 "as_of": "2026-10-30",
 "signal": "BULLISH",
 "decision_row": "D3",
 "layers": {
  "regime": "RISK_ON",
  "health": "HEALTHY",
  "timing": "NORMAL"
 },
 "risk": {
  "p_drawdown20_60d_est": 0.06,
  "risk_flag": "LOW",
  "atr_pct": 2.0
 },
 "confidence": "medium",
 "near_threshold": [],
 "horizon_days": 60,
 "features": {
  "close": 344.63,
  "pct_from_52w_high": -1.2,
  "pct_from_60d_high": -1.2,
  "volume_10d_vs_prior_50d": 1.04,
  "close_vs_sma200_pct": 16.2,
  "sma200_rising": true,
  "sma50_gt_sma200": true,
  "rsi14": 55.3,
  "rsi10": 53.7,
  "rsi14_crossed_above_70_today": false,
  "close_above_upper_bb": false,
  "ret5_pct": -0.9,
  "rs_6m_vs_spy_pct": 18.2,
  "spy_above_10m_sma": true,
  "spy_sma50_gt_sma200": true
 },
 "warnings": [],
 "invalidation": "close below SMA200, SMA200 rolls over, >10% off the 52w high, or regime leaves RISK_ON"
}
```

### NASDAQ:MSFT
```json
{
 "symbol": "NASDAQ:MSFT",
 "as_of": "2026-10-30",
 "signal": "BULLISH",
 "decision_row": "D3",
 "layers": {
  "regime": "RISK_ON",
  "health": "HEALTHY",
  "timing": "NORMAL"
 },
 "risk": {
  "p_drawdown20_60d_est": 0.06,
  "risk_flag": "LOW",
  "atr_pct": 2.28
 },
 "confidence": "medium",
 "near_threshold": [],
 "horizon_days": 60,
 "features": {
  "close": 521.91,
  "pct_from_52w_high": -4.0,
  "pct_from_60d_high": -4.0,
  "volume_10d_vs_prior_50d": 1.0,
  "close_vs_sma200_pct": 19.2,
  "sma200_rising": true,
  "sma50_gt_sma200": true,
  "rsi14": 49.0,
  "rsi10": 44.5,
  "rsi14_crossed_above_70_today": false,
  "close_above_upper_bb": false,
  "ret5_pct": -0.5,
  "rs_6m_vs_spy_pct": 21.1,
  "spy_above_10m_sma": true,
  "spy_sma50_gt_sma200": true
 },
 "warnings": [],
 "invalidation": "close below SMA200, SMA200 rolls over, >10% off the 52w high, or regime leaves RISK_ON"
}
```

### NYSE:JPM
```json
{
 "symbol": "NYSE:JPM",
 "as_of": "2026-10-30",
 "signal": "BULLISH",
 "decision_row": "D3",
 "layers": {
  "regime": "RISK_ON",
  "health": "HEALTHY",
  "timing": "NORMAL"
 },
 "risk": {
  "p_drawdown20_60d_est": 0.06,
  "risk_flag": "LOW",
  "atr_pct": 1.88
 },
 "confidence": "medium",
 "near_threshold": [],
 "horizon_days": 60,
 "features": {
  "close": 337.04,
  "pct_from_52w_high": -7.7,
  "pct_from_60d_high": -7.7,
  "volume_10d_vs_prior_50d": 0.84,
  "close_vs_sma200_pct": 4.4,
  "sma200_rising": true,
  "sma50_gt_sma200": true,
  "rsi14": 49.0,
  "rsi10": 50.3,
  "rsi14_crossed_above_70_today": false,
  "close_above_upper_bb": false,
  "ret5_pct": 1.6,
  "rs_6m_vs_spy_pct": 3.0,
  "spy_above_10m_sma": true,
  "spy_sma50_gt_sma200": true
 },
 "warnings": [],
 "invalidation": "close below SMA200, SMA200 rolls over, >10% off the 52w high, or regime leaves RISK_ON"
}
```

### NYSE:XOM
```json
{
 "symbol": "NYSE:XOM",
 "as_of": "2026-10-30",
 "signal": "NO_SIGNAL",
 "decision_row": "D4",
 "layers": {
  "regime": "RISK_ON",
  "health": "HEALTHY",
  "timing": "EXTENDED"
 },
 "risk": {
  "p_drawdown20_60d_est": 0.068,
  "risk_flag": "NORMAL",
  "atr_pct": 2.12
 },
 "confidence": "medium",
 "near_threshold": [],
 "horizon_days": 60,
 "features": {
  "close": 187.25,
  "pct_from_52w_high": 0.0,
  "pct_from_60d_high": 0.0,
  "volume_10d_vs_prior_50d": 0.96,
  "close_vs_sma200_pct": 21.1,
  "sma200_rising": true,
  "sma50_gt_sma200": true,
  "rsi14": 73.0,
  "rsi10": 74.9,
  "rsi14_crossed_above_70_today": true,
  "close_above_upper_bb": false,
  "ret5_pct": 2.2,
  "rs_6m_vs_spy_pct": 17.7,
  "spy_above_10m_sma": true,
  "spy_sma50_gt_sma200": true
 },
 "warnings": [],
 "invalidation": "n/a"
}
```

### NASDAQ:TSLA
```json
{
 "symbol": "NASDAQ:TSLA",
 "as_of": "2026-10-30",
 "signal": "NO_SIGNAL",
 "decision_row": "D6",
 "layers": {
  "regime": "RISK_ON",
  "health": "NEUTRAL",
  "timing": "NORMAL"
 },
 "risk": {
  "p_drawdown20_60d_est": 0.111,
  "risk_flag": "NORMAL",
  "atr_pct": 3.36
 },
 "confidence": "medium",
 "near_threshold": [],
 "horizon_days": 60,
 "features": {
  "close": 399.81,
  "pct_from_52w_high": -18.4,
  "pct_from_60d_high": -1.9,
  "volume_10d_vs_prior_50d": 1.11,
  "close_vs_sma200_pct": 3.8,
  "sma200_rising": false,
  "sma50_gt_sma200": false,
  "rsi14": 60.9,
  "rsi10": 62.4,
  "rsi14_crossed_above_70_today": false,
  "close_above_upper_bb": false,
  "ret5_pct": 7.4,
  "rs_6m_vs_spy_pct": -2.6,
  "spy_above_10m_sma": true,
  "spy_sma50_gt_sma200": true
 },
 "warnings": [],
 "invalidation": "n/a"
}
```

### NYSE:UNH
```json
{
 "symbol": "NYSE:UNH",
 "as_of": "2026-10-30",
 "signal": "BULLISH",
 "decision_row": "D3",
 "layers": {
  "regime": "RISK_ON",
  "health": "HEALTHY",
  "timing": "NORMAL"
 },
 "risk": {
  "p_drawdown20_60d_est": 0.06,
  "risk_flag": "LOW",
  "atr_pct": 2.69
 },
 "confidence": "medium",
 "near_threshold": [],
 "horizon_days": 60,
 "features": {
  "close": 406.97,
  "pct_from_52w_high": -6.7,
  "pct_from_60d_high": -4.2,
  "volume_10d_vs_prior_50d": 0.88,
  "close_vs_sma200_pct": 12.2,
  "sma200_rising": true,
  "sma50_gt_sma200": true,
  "rsi14": 56.1,
  "rsi10": 55.0,
  "rsi14_crossed_above_70_today": false,
  "close_above_upper_bb": false,
  "ret5_pct": -2.7,
  "rs_6m_vs_spy_pct": 5.5,
  "spy_above_10m_sma": true,
  "spy_sma50_gt_sma200": true
 },
 "warnings": [],
 "invalidation": "close below SMA200, SMA200 rolls over, >10% off the 52w high, or regime leaves RISK_ON"
}
```

### NASDAQ:INTC
```json
{
 "symbol": "NASDAQ:INTC",
 "as_of": "2026-10-30",
 "signal": "BEARISH",
 "decision_row": "D2",
 "layers": {
  "regime": "RISK_ON",
  "health": "BROKEN",
  "timing": "NORMAL"
 },
 "risk": {
  "p_drawdown20_60d_est": 0.156,
  "risk_flag": "HIGH",
  "atr_pct": 10.6
 },
 "confidence": "medium",
 "near_threshold": [],
 "horizon_days": 60,
 "features": {
  "close": 65.76,
  "pct_from_52w_high": -53.3,
  "pct_from_60d_high": -48.4,
  "volume_10d_vs_prior_50d": 1.28,
  "close_vs_sma200_pct": -24.3,
  "sma200_rising": true,
  "sma50_gt_sma200": true,
  "rsi14": 25.1,
  "rsi10": 21.0,
  "rsi14_crossed_above_70_today": false,
  "close_above_upper_bb": false,
  "ret5_pct": -24.4,
  "rs_6m_vs_spy_pct": -38.9,
  "spy_above_10m_sma": true,
  "spy_sma50_gt_sma200": true
 },
 "warnings": [],
 "invalidation": "health recovers: close back above a rising SMA200 and within 40% of the 52w high"
}
```
