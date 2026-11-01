# The Technical-Analysis Signal Rulebook (for agents)

**Version 2.2.** v2.1.2 plus three evidence-tested additions:
- an **earnings-risk flag (E1)**;
- a **survivorship check** on stocks that later delisted;
- a **forward paper-trading** scoreboard.

Two further candidates were tested and **rejected**: post-earnings-drift signals and fast crash overlays (§6).

**v2.1.2 history.** Revised after three blind agent tests:
- **Round 1:** the agent matched the deterministic engine on 39 of 40 cases and logged 17 ambiguities, all fixed in v2.1.
- **Round 2:** 40 of 40.
- **Round 3, the final exam** on never-seen holdout tickers from 2020–2026: 49 of 50. The one miss came from a rounded input.

In round 3, the agent's BEARISH calls had a 40% chance of a ≥ 20% fall within 60 days and lagged the market by 4.9%. Its BULLISH calls had 5.9% and +0.4%.

It is built from:
- 5 classic books read in full, plus Schabacker's trading chapters;
- surveys of the modern canon and of 25 academic studies;
- the 300 most-viewed technical-analysis videos on YouTube;
- **123 coded rules backtested twice** (246 tests) on about 900 US stocks, plus 22 ETFs and the S&P 500 since 1928;
- reinforcement-learning and machine-learning agents, blind agent tests, and a locked out-of-sample test.

See `experiments/ITERATION_LOG.md` and `BELIEFS_VS_EVIDENCE.md`.

---

## 0. Prime directives (read first, never violate)

1. **No return-forecasting TA signal is presumed.** Of 123 popular TA entry rules tested on about 900 US stocks (2000–2019, after costs, date-clustered statistics, t ≥ 3 hurdle), **none** produced a stock-picking edge that held in both the discovery and validation periods. A walk-forward machine-learning model using 32 TA features combined reached an information coefficient of only about 0.017.
2. **TA predicts RISK much better than RETURN.** Trend health and distance from the 52-week high move the odds of a ≥ 20% fall within 60 trading days. The gap was **2.6–4×** in 2000–2019, on both development and holdout tickers, and **about 1.5–2×** in the locked 2020–2026 test. They barely move expected return.
   - `BULLISH` and `BEARISH` in this rulebook are therefore **risk-class labels** ("low-risk healthy trend" vs "broken, high crash risk").
   - `BULLISH` can legitimately apply to a third or more of stocks in a bull market. That does **not** violate directive 1.
   - Every answer must include the risk assessment.
3. **Answer three separate questions, in order:**
   - Q1: what is the market regime?
   - Q2: is this stock technically healthy or broken?
   - Q3: is now an entry moment or an extension?

   Always say which layer drove the output.
4. **Never cite pattern win-rates from YouTube or books as facts.** Tested on daily US stocks:
   - the "86% MACD strategy" won 47–51% of trades;
   - the "88% RSI pullback" won 69–71%, with no significant edge.
5. **A signal is a probability over a stated horizon, never a certainty.** Always state the horizon (60 trading days), the confidence (`low` or `medium`, never `high`) and the invalidation condition.

---

## 1. Data and exact feature definitions

### 1.1 TradingView MCP calls
| Call | Purpose |
|---|---|
| `mcp-tv-get-ohlcv(symbol, interval="1D", count=300, format="columns")` | Stock daily bars. ≥ 260 are required. |
| `mcp-tv-get-ohlcv("AMEX:SPY", interval="1D", count=300, format="columns")` | Market regime. |
| `mcp-tv-get-earnings-calendar(symbols=[symbol])` | Next report date (`release_next_date`, possibly under `out_of_window`). Feeds earnings flag E1 (§5). |
| `mcp-tv-get-technicals-rating(symbol, "1D")` (optional) | Cross-checks RSI, ADX and MAs. Its Buy/Sell "Recommend" value is **not** a signal: every component it averages was tested in §6 and showed no edge. |

Use only **completed** daily bars. If the market is open, drop the last bar. The reference implementation is `platform/tagym/live.py`:

```
python -m tagym.live stock.json spy.json --symbol EXCH:TICKER --next-earnings YYYY-MM-DD [--drop-last]
```

It returns the §9 JSON. When code execution is available, **prefer running it** to hand calculation, and report its output.

### 1.2 Definitions
C, H, L and V are daily close, high, low and volume. t is the last completed bar. All windows end at t and include it.

| Feature | Exact definition |
|---|---|
| `SMA_n` | Mean of the last n closes. |
| `SMA200_slope_1m` | SMA200(t) / SMA200(t−21) − 1. **Rising** if > 0, **falling** if < 0. Strict sign; there is no dead-band. |
| `pct_from_52w_high` | C(t) / max(C over the last 252 bars) − 1. Close-based. |
| `pct_from_60d_high` | C(t) / max(C over the last 60 bars) − 1. Close-based. |
| `RSI14`, `RSI10` | Wilder RSI. |
| `ATR%` | Wilder ATR14 / C(t). **High-vol**: if a cross-sectional ATR percentile is supplied, high-vol ⇔ percentile ≥ 67 (the percentile **overrides**). Otherwise high-vol ⇔ ATR% ≥ 3.0% (≈ the top tercile of US stocks). |
| `%B > 1` | C(t) above the upper Bollinger band (SMA20 + 2 × population stdev of 20 closes). |
| `ret5` | C(t) / C(t−5) − 1. |
| `up_streak` | Number of consecutive closes above the prior close, counting today. |
| `vol10_vs_prior50` | Mean V over the last 10 bars / mean V over the 50 bars before those. |
| `$vol20` | Median of C × V over the last 20 bars. |
| `RS6` | 6-month return minus SPY's 6-month return (126 bars). "Top-decile RS": if an RS percentile is supplied, top-decile ⇔ percentile ≥ 90 (it overrides). Otherwise top-decile ⇔ RS6 > +25 pts. |
| SPY month-end test | Last **completed** month-end close > mean of the last 10 completed month-end closes. A month counts as completed from the first trading day of the next month, or on the calendar month-end itself if that is a trading day. This is the convention used in every backtest; it can lag by one day around month-ends. |

All thresholds are **inclusive as written**. "Within ±x" means |value − cut-off| ≤ x.

**Rounded inputs.** Sometimes you are given pre-computed, rounded values instead of bars (for example `-10.0`, `-0.0` or `%B = 1.0`).
- Read `-0.0` as *below* zero.
- Apply the comparison exactly as written to the printed value.
- If a printed value sits exactly on a cut-off, also put it in `near_threshold` and set confidence to `low`.
- Whenever bars are available, compute at full precision instead, preferably with `live.py`. In blind tests, the only agent–engine disagreements came from 1-decimal rounding.

---

## 2. Layer Q1: market regime (index level)

| Regime | Definition |
|---|---|
| `RISK_ON` | SPY month-end test true **and** SPY SMA50 > SMA200. |
| `RISK_OFF` | Both false. |
| `MIXED` | Exactly one is true. |

The daily 200-day price cross, breadth and "% from 52w high" are **not** regime inputs, because daily rules whipsaw.

**Evidence.**
- S&P 500, 1929–1999: the 10-month rule cut max drawdown from −86% to −52%; Sharpe rose from 0.40 to 0.57.
- S&P 500, 2000–2019: max drawdown −57% → −21%; Sharpe 0.30 → 0.58.
- 22 ETFs, 2000–2019: max drawdown improved on 95% of ETFs and Sharpe on 64%, at a cost of about 1%/yr CAGR.
- Daily 200-day crosses made Sharpe *worse* on 64% of ETFs.
- Dow Theory is fragile: only 1 of 4 swing thresholds beat buy-and-hold.

The regime is a **risk dial**. It never creates a stock signal by itself.

---

## 3. Layer Q2: stock technical health (the robust layer)

| Health | Definition (first match wins) |
|---|---|
| `HEALTHY` | C > SMA200 **and** SMA200 rising **and** SMA50 > SMA200 **and** pct_from_52w_high ≥ −10% |
| `BROKEN` | Any of:<br>**(B1)** C < SMA200 and SMA200 falling;<br>**(B2)** pct_from_52w_high ≤ −40%;<br>**(B3)** C < SMA200 and SMA50 < SMA200 and pct_from_52w_high ≤ −25% |
| `NEUTRAL` | Everything else. A fresh dip below a still-rising SMA200 that is not deep (B3 fails) is deliberately NEUTRAL. |

**Evidence: P(the stock falls ≥ 20% from entry within 60 trading days).**

- Development: discovery tickers, 2000–2019.
- **Locked out-of-sample test**: 600 never-seen holdout tickers, and the 2020–2026 period scored once.

| Class | Dev 2000–14 | Dev 2015–19 | Holdout 2000–14 | Holdout 2015–19 | **Test 2020–26** (all tickers) | Test, excl. Q1-2020 |
|---|---|---|---|---|---|---|
| BULLISH | 6.6% | 5.4% | 7.5% | 5.7% | **12.1–12.8%** | 9.1% |
| NO_SIGNAL | 14.2% | 9.1% | 15.3% | 9.2% | 15.3–15.7% | 13.3% |
| BEARISH | 24.4% | 15.8% | 26.3% | 15.0% | **18.9–19.6%** | 17.7% |

**Limitation found in the locked test.** The ordering held in most years (2021: 7.4% vs 18.1%; 2024: 7.3% vs 16.4%). It failed when a market-wide shock arrived while the slow regime still read `RISK_ON`. In Q1 2020 (COVID), 34% of BULLISH-class stocks fell ≥ 20%; in 2025, 14.6%.

**The health layer forecasts trend-related drawdowns, not sudden exogenous crashes.** Never describe BULLISH as "safe". Say "lower crash risk than other stocks, unless the whole market breaks".

- The effect holds within every volatility tercile (1.4–2.9×).
- It also holds on 29 survivorship-free ETFs. P(≥ 10% fall in 60 days) is 11.8% for HEALTHY + RISK_ON against 35.1% for BROKEN, and mean 60-day return is 2.2% against 1.4%.
- Expected *excess* returns between stock classes are ≈ 0 (±0.4% over 60 days).
- **Survivorship check (v2.2).** The development universe is today's index members, so later-delisted stocks were missing. I applied the frozen rulebook to a random sample of 90 NYSE/NASDAQ stocks that were later delisted (EODHD). 76 had usable histories and 38 were ever tradeable; 34 of the 76 ended ≥ 80% below their peak.

  | Delisted stocks | P(≥ 20% fall in 60d) | P(≥ 40% fall in 60d) | 60-day return |
  |---|---|---|---|
  | BULLISH | 14.3% | 1.9% | +4.7% |
  | NO_SIGNAL | 23.9% | 6.0% | −0.8% |
  | BEARISH | **37.5%** | **15.4%** | **−1.4%** |

  - The class ordering holds (2.6×), but absolute risk is about **2× higher** than in survivors.
  - Among delisted names, BEARISH also had worse *returns*; survivorship had hidden that.
  - Stocks ≥ 40% below their 52-week high returned +4.7% over 60 days among survivors, but **−3.4% among delisted stocks**, with a 48.6% chance of a further ≥ 20% fall.
  - Deep drawdowns are **not** bargains, whatever the survivor-only data suggests.

---

## 4. Layer Q3: entry timing (small but consistent effects)

Evaluate **EXTENDED for every stock**. Evaluate **PULLBACK only for HEALTHY stocks that are not EXTENDED**. Otherwise the timing label is `NORMAL`.

| Label | Exact condition | Measured effect (excess vs market; same sign in both periods) |
|---|---|---|
| `EXTENDED` | **Any** of:<br>(a) RSI14 ≥ 70;<br>(b) %B > 1;<br>(c) ret5 > 2.2 × ATR% × √5;<br>(d) up_streak ≥ 5 | −0.1% to −0.2% over the next 5–10 days. Crossing RSI 70: t = −3.05 / −2.27. Top-decile 5-day winners: t = −4.1 / −1.4. |
| `PULLBACK` | HEALTHY, not EXTENDED, and either RSI10 < 30, or (−15% ≤ pct_from_60d_high ≤ −7% and vol10_vs_prior50 ≤ 0.70) | +0.14% to +0.25% (t ≈ 1–1.7; not significant alone) |

**Out-of-sample:**
- **EXTENDED** underperformance kept its sign in **18 of 18** rule-sample cells: 3 rules × 6 samples (development, holdout tickers, and 2020–26 for both ticker groups). The range was −0.04% to −0.21%.
- **PULLBACK via RSI10 < 30** stayed positive in 6 of 6 samples (+0.11% to +0.25% over 5 days).
- **The quiet-pullback variant** was positive in 5 of 6 samples but small and noisy (−0.18% to +0.25%). Treat it as weak.

These are timing refinements, never stand-alone signals. The edges are smaller than a round-trip trading cost. Breakout entries did **worse** than random entries into the same uptrending stocks (−0.9% / −0.2% per trade), so prefer `PULLBACK` moments to `EXTENDED` ones.

---

## 5. The decision table

Apply the rows in order; the first match wins.

| # | Condition | Output | What to tell the user |
|---|---|---|---|
| D1 | < 260 bars, or C < $5, or $vol20 < $5M (skip a test whose input is unavailable) | `NO_SIGNAL` | "Insufficient data or untradeable; TA statistics don't apply." |
| D2 | health = BROKEN | **`BEARISH`** (risk signal) | "Technically broken. Crash risk is about 16–21% vs about 6% for healthy names. Avoid new longs, reduce size, tighten risk. This is not by itself a short-sale recommendation." |
| D3 | HEALTHY **and** RISK_ON **and** not EXTENDED | **`BULLISH`** (low-risk trend) | "Healthy uptrend in a healthy market: the lowest crash-risk class. Expected outperformance is small; the edge is risk, not return." If the timing label is PULLBACK, add "favourable entry zone". |
| D4 | HEALTHY **and** EXTENDED | `NO_SIGNAL` | "The trend is fine, but buying after a spike has lagged. Wait for a pullback." If regime ≠ RISK_ON, also say "and the market is unhealthy" and check A1. |
| D5 | HEALTHY **and** regime ≠ RISK_ON | `NO_SIGNAL` | "Healthy stock in an unhealthy market." Check rule A1. |
| D6 | Everything else (NEUTRAL) | `NO_SIGNAL` | "No technical edge." |

**Earnings flag E1 (v2.2), checked on every row.** If the next scheduled report falls within **10 trading days**:
- attach warning E1;
- report `p_drop10_10d_est` from the table below;
- downgrade a D3 `risk_flag` from LOW to NORMAL.

The signal itself does not change: earnings timing predicts *risk*, not direction.

| Class | P(≥ 10% drop within 10 trading days): earnings due | no earnings due |
|---|---|---|
| BULLISH | **9.6%** | 3.9% |
| NO_SIGNAL | 13.2% | 7.1% |
| BEARISH | 17.8% | 12.6% |

These are means of 6 samples: development 2000–14 and 2015–19, the 600 holdout tickers in all three periods, and 2020–26. The flag replicated in **every** sample (for example BULLISH 8.5–12.2% with earnings due, against 2.7–5.8% without). A healthy stock with earnings due carries the short-term crash risk of an average stock.

**Rule A1 is checked on every row.** If the SPY month-end test is **false** (SPY below its 10-month SMA, whatever the SMA50/200 state) and RS6 is top-decile, attach the A1 warning. Such a stock can never be BULLISH.

**Nothing in §6 may change the output by itself.** That covers candlestick patterns, chart patterns, indicator crossovers, Fibonacci levels, support/resistance touches, divergences, volume spikes, ICT/SMC concepts and TradingView's Buy/Sell rating. If one is present, list it under `ignored_noise`.

### Risk calibration: P(≥ 20% fall within 60 days), mean of 2000–14 and 2015–19

| Row | RISK_ON | MIXED | RISK_OFF |
|---|---|---|---|
| D2 BEARISH | 15.6% | 16.9% | 20.8% (31.7% in 2000–14) |
| D3 BULLISH | 6.0% | n/a | n/a |
| D4 healthy, extended | 6.8% | 12.1% | 11.1% |
| D5 healthy, bad market | n/a | 9.8% | 12.3% |
| D6 neutral | 11.1% | 14.5% | 16.7% |

The calibration above comes from the development periods. In the **locked 2020–2026 test** (which includes the COVID crash), the observed rates were harsher: BULLISH 12.5%, NO_SIGNAL 15.5%, BEARISH 19.2%. Report the development estimate as `p_drawdown20_60d_est`. When a conservative view is asked for, also report the test value as `p_drawdown20_60d_2020_26_observed`; `live.py` outputs both.

---

## 6. NOT-a-signal list (tested; no robust edge)

Every rule here was coded exactly and tested on about 900 stocks over 2000–2014 and again over 2015–2019. Benchmarks were the equal-weight universe and a volatility-matched universe, after costs.

| Family | Tested | Result |
|---|---|---|
| Moving-average crosses | Golden/death cross, price × SMA200, EMA 9/21, EMA 20/50, MA stack, Minervini trend template | No edge. Golden cross and price-above-200 were *negative* in 2000–14 (t ≈ −2.5 / −3.1). |
| Breakouts | 52-week high (± volume), Donchian 20/55, tight base, Livermore 60-day range, Bollinger squeeze, gaps, Weinstein Stage 2 | No edge. Donchian-20 was negative in both periods (t ≈ −2.2). |
| Momentum indicators | MACD (4 variants), ADX > 25, RSI > 50, 12-1 momentum, RS deciles, leader of the leading group | No edge after 2000. |
| Oscillators as reversal calls | RSI < 30, RSI > 70 as a sell, Connors RSI(2), stochastics, Bollinger touches | Oversold buys: no edge. Overbought is timing information only (§4). |
| Candlesticks | 12 Nison patterns with prior-trend context | All NO_EDGE, matching Marshall, Young & Rose (2006). |
| Chart patterns | Double top/bottom, H&S and inverse H&S, triangles, bull flag, cup-with-handle, VCP | All NO_EDGE. Bulkowski reports failure rates rose 2–4× after 1991. |
| Support/resistance | Bounce, break, rejection, round numbers, Fibonacci 61.8% | No edge. Support bounces were *negative* in 2015–19. |
| Volume | Thrusts, capitulation, OBV, CMF, up/down volume, effort vs result, climaxes, springs | No edge. |
| Divergences | RSI bullish and bearish divergence | No edge. |
| YouTube "claimed" systems | MACD + 200 EMA (claimed 86%), Stoch + RSI + MACD, ICT fair-value gap, ICT liquidity sweep, 50-MA pullback, 200-day breakout, RSI(10) pullback | Real win rates 37–71%. No significant event-study edge. |
| Dow Theory | Industrials confirmed by Transports | Fragile; use as context only. |
| Post-earnings drift (v2.2) | Earnings-day gap ±5% on ≥ 2× volume; top/bottom-decile earnings reaction; EPS surprise ≥ +10% / ≤ −10%; surprise and reaction agreeing (128k earnings events, EODHD) | No rule reached t ≥ 3. The gap-down drift (−0.8%/60d, same sign in 2000–14 and 2015–19) **vanished or reversed in 2020–26** (+0.45%, −0.29%). EPS surprise alone showed no drift. |
| Fast crash overlays (v2.2) | VIX ≥ 30; VIX +50% in 5 days; SPY −7% / −10% in 20 days; 20-day realized vol ≥ 30%; combinations (designed on 2000–19 only) | Cut BULLISH crash odds by at most 0.17 pts. On the index they **worsened** Sharpe and drawdown (whipsaw). Shocks arrive before any trigger can fire. |

---

## 7. Avoid rules (claims that worked in reverse)

- **A1.** Top-decile 6-month RS stocks bought while SPY is below its 10-month SMA underperformed by **−1.8% per month** (t = −4.3, 2000–14) and by −0.9% in 2015–19. Momentum crashes happen after bear markets.
- **A2.** Stocks that held up best on SPY −2% days lagged afterwards (−0.9% over 20 days, t = −3.2). The hardest-hit stocks rebounded. Don't read crash-day resilience as strength.
- **A3.** Don't buy the breakout bar itself. It did worse than random entries with the same exits. If today's close is the 52-week closing high (`pct_from_52w_high` = 0) on a D3 row, attach an A3 warning ("prefer a pullback entry"). The output stays unchanged.
- **A4 (downgraded after the locked test).** "Leader of the leading group" was −0.3% and −0.8% next month in development, but −0.3%, −0.2% and +0.4% out-of-sample. Result: no edge, so never treat it as a reason to buy.

**Locked out-of-sample confirmation (holdout tickers and 2020–2026):**
- **A1** was confirmed on holdout tickers: −1.38%/month, t = −4.75. 2020–26 had too few months below the 10-month SMA to judge (+0.9%, insufficient).
- **A2** was negative in 6 of 6 samples, 4 of them out-of-sample.
- **A3**: 20-day breakouts were negative in 6 of 6 samples. In 2020–26 they were REVERSED for both ticker groups (t ≈ −2.0 to −2.2).
- Double-bottom breakouts were negative in every cell (2020–26: −0.6%, t = −2.6).

**Weak but consistent context (never a signal).** Top-decile RS stocks while the market is RISK_ON did about +0.3% the next month. That held in 6 of 6 samples, but never at t ≥ 3. The pattern was first learned by the RL agent and later confirmed in sign.

---

## 8. Risk-management rules (attach to every BULLISH or BEARISH output)

1. **Stops are insurance, not edge.** On random entries an 8% stop cut the worst-1% outcome from −46% to −11%, and the chance of losing more than 20% from 7.6% to 0.2%. It also roughly halved the mean return.
   - Prefer wide stops (2–3 × ATR14 or about 8%).
   - Moving-average exits were the most expensive.
2. **Size by volatility.** Make position risk proportional to 1/ATR%. A high-vol BULLISH stock gets `risk_flag = NORMAL`, not LOW.
3. **Don't switch individual stocks in and out on their 200-day line.** It lowered Sharpe for about 80% of stocks.
4. **Hedge or de-risk at market level with the slow regime (§2).** Expect about −1%/yr of return for about 25 points less drawdown. In 2020–26 the cost was about −3%/yr.
5. **Earnings (E1).** Size down, or widen the stop, ahead of a report within 10 trading days. Never treat a post-earnings gap as a signal (§6).
6. **No signal protects against market-wide shocks.** Diversification and position size are the only defences that worked; every fast overlay tested failed.

---

## 9. Output schema (one JSON object per symbol)

```json
{
  "symbol": "NASDAQ:XYZ",
  "as_of": "YYYY-MM-DD (last completed daily bar)",
  "signal": "BULLISH | BEARISH | NO_SIGNAL",
  "decision_row": "D1..D6",
  "layers": {"regime": "RISK_ON|MIXED|RISK_OFF", "health": "HEALTHY|NEUTRAL|BROKEN", "timing": "EXTENDED|PULLBACK|NORMAL"},
  "rulebook_version": "2.2",
  "risk": {"p_drawdown20_60d_est": 0.06, "p_drawdown20_60d_2020_26_observed": 0.125,
           "p_drop10_10d_est": 0.039, "earnings_in_next_10d": false, "next_earnings": "YYYY-MM-DD",
           "risk_flag": "LOW|NORMAL|HIGH", "atr_pct": 2.1},
  "confidence": "low | medium",
  "near_threshold": ["inputs within a hair of a cut-off"],
  "horizon_days": 60,
  "invalidation": "e.g. close below SMA200 with SMA200 turning down",
  "warnings": ["A1 ..."],
  "evidence": ["rule ids / measured stats used"],
  "ignored_noise": ["e.g. bullish engulfing (NOT a signal, §6)"]
}
```

**`p_drawdown20_60d_est`** comes from the §5 calibration table.

**`risk_flag`:**
- `HIGH` if BROKEN, or if high-vol in RISK_OFF.
- `LOW` if D3, not high-vol, and no earnings due within 10 trading days.
- `NORMAL` otherwise. That includes a high-vol, non-BROKEN stock in a MIXED regime, and a high-vol D3 stock.

**`confidence`:** `medium` by default. Downgrade to `low` if **any** of the inputs below is within its band, whether or not crossing it would change the output. **This list is exhaustive**: other thresholds (the −25% of B3, the PULLBACK cuts, the ATR cuts, the D1 floor) never lower confidence.
- pct_from_52w_high within ±1 pt of −10% or −40%;
- C within ±1% of SMA200;
- |SMA200_slope_1m| < 0.1%;
- RSI14 within ±1 of 70.

`near_threshold` lists **only** these four inputs, plus any rounded value printed exactly on a cut-off. Near-misses on other cut-offs may go under `warnings`; they never change confidence.

---

## 10. Worked micro-examples

- *4% below its 52w high, above a rising SMA200, SMA50 > SMA200, RSI14 = 58, ATR% 1.8, RISK_ON.* → D3 `BULLISH`, risk LOW, p ≈ 6%.
- *Same stock, but RSI14 = 72 after a +11% week.* → D4 `NO_SIGNAL` (healthy but extended; wait).
- *45% below its 52w high, with a bullish engulfing candle and an RSI divergence today.* → D2 `BEARISH`. The candle and divergence go under `ignored_noise`.
- *11% below a still-rising SMA200, SMA50 < SMA200, 27% off the high.* → D2 `BEARISH` via B3.
- *18% below its high, above SMA200, SMA200 slope −0.05%, MACD bull cross.* → D6 `NO_SIGNAL`. Confidence is low (slope near zero), and the MACD cross goes under `ignored_noise`.
- *A top-RS, HEALTHY, not-extended stock while SPY is below its 10-month SMA.* → D5 `NO_SIGNAL` with the A1 warning. If it is also extended, D4 matches first, and the A1 warning is still attached.

---

## 11. Forward validation (paper trading)

The rulebook is now scored forward on live data.

- Every US trading day, a scheduled job applies it to a 98-stock, sector-balanced watchlist (`paper/watchlist.csv`), using TradingView's next earnings dates.
- Each verdict is appended to `paper/journal.csv`. Our closes are cross-checked against TradingView in `paper/integrity_log.csv`; the first 8 checks differed by 0.000%.
- Each call is graded once its 10-, 20- and 60-day windows have passed. `paper/SCOREBOARD.md` compares realized crash rates with the expected ones above, using a binomial 95% test.
- If a class shows `calibrated? = NO` for several consecutive weeks, re-run the evidence pipeline before trusting the numbers.

The first verdicts (2026-10-30) were 23 BULLISH, 42 NO_SIGNAL and 33 BEARISH. The 10-day scores mature in mid-November 2026, the 60-day scores in late January 2027.
