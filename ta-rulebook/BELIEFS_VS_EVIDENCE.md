# What technical analysts believe vs. what the data shows

This file lines up three bodies of belief with one body of evidence:

- **Classics:** books read in full. Dow and Nelson 1903, Hamilton 1922, Lefèvre/Livermore 1923, Selden 1912, Wyckoff 1910, plus Schabacker 1930, Ch. XIX–XXVII.
- **Modern canon:** Murphy, Edwards & Magee, Bulkowski, Nison, Weinstein, O'Neil, Minervini, Elder, Wilder, Bollinger, Aronson and Connors.
- **YouTube:** the 300 most-viewed technical-analysis videos (519M views) and their top 16 creators.
- **The evidence:** TA Gym backtests on about 1,500 US stocks (2000–2019 discovery and validation), 22 ETFs and the S&P 500 since 1928, cross-checked against 25 academic studies. The locked 2020–2026 and holdout-ticker results are in `experiments/ITERATION_LOG.md` (Phase I) and in RULEBOOK §3 and §7.

Verdict key:

- ✅ **supported**
- 🟡 **supported only as a risk or timing tool**
- ❌ **not supported**
- 🔁 **works in reverse**

## 1. The ten consensus beliefs of the modern canon

| # | Belief (schools holding it) | Measured | Verdict | Rulebook treatment |
|---|---|---|---|---|
| C1 | Trade only with the primary trend: above a rising 200-day MA (Murphy, Weinstein, O'Neil, Minervini, Elder, Connors) | Healthy-trend stocks have 3–4× lower 60-day crash odds. Their *excess return* is ≈0 | 🟡 | Health layer: decides risk, not alpha |
| C2 | The 200-day / 30-week MA and its slope define the regime | Slow index filters cut max drawdown on 91–95% of ETFs and on the S&P in every era. Daily crosses whipsaw | 🟡 | Regime layer = 10-month SMA plus SMA50>SMA200 |
| C3 | Act only on a confirmed close beyond the boundary | All tests used confirmed closes. Patterns still showed no edge | — (necessary, not sufficient) | Built into the engine |
| C4 | Breakouts need volume of at least 1.4–2× average | 52-week-high breakouts showed no edge with or without volume. Low-volume breakouts did *not* do worse | ❌ | Volume dropped as a criterion |
| C5 | Oscillator extremes only matter as pullbacks inside trends | RSI(10)<30 above SMA200: +0.15%/5d in both periods (t≈1). Without the trend filter ≈0. In downtrends slightly negative | 🟡 (direction right, too small to trade) | `PULLBACK` timing label |
| C6 | Use small preset stops (7–10% or 2% of equity) | On random entries, stops cut tail losses (worst-1%: −46% → −11%) but halve mean return | 🟡 | Stops are insurance; size by ATR |
| C7 | Volatility and volume contraction precede valid breakouts (VCP, squeeze, quiet handle) | Tight-base breakout was REVERSED in 2000–14. Squeeze, VCP, Wyckoff dull-range and Livermore 60-day range breakouts showed no edge | ❌ | NOT-a-signal list |
| C8 | Buy relative-strength leaders (RS ≥ 70–80) | No edge on 2000–2019 stocks. **In bear markets: −1.8%/month (t −4.3)** | 🔁 in bear markets | Avoid rule A1 |
| C9 | Support/resistance polarity | Support bounces were negative in 2015–19. Breaks, rejections, round numbers and Fibonacci 61.8% showed no edge | ❌ | NOT-a-signal list |
| C10 | Never buy in Stage 4 (below a declining MA) | Crash odds roughly 2×, holding within every volatility tercile. Mean excess ≈0 (upward-biased by survivorship) | ✅ as risk | BROKEN → `BEARISH` (risk) |

## 2. What the classic books claimed

| Source | Core claim | Measured | Verdict |
|---|---|---|---|
| Dow / Hamilton / Nelson | Primary trends persist and are confirmed by both averages. Don't fight the primary | The BEAR state really is worse (6-month forward −3.2% vs +6.1%). But the timing switch is fragile (1 of 4 thresholds beats buy-and-hold), and confirmation helps only at some thresholds | 🟡 context only |
| Livermore (Reminiscences) | Buy the breakout from a tight range in the direction of the market. New highs beat "bargains". Cut losses, let profits run | Range breakouts and new-high-vs-bargain: no edge. Stops reduce tails but cost return. Fallen leaders and laggards in strong groups: no edge | ❌ (entries) / 🟡 (risk discipline) |
| Livermore / O'Neil | "Leaders of leading groups" | −0.3% / −0.8% the following month (validation t −3.9) | 🔁 at 1-month horizon |
| Selden | Volume on up-days vs down-days reveals accumulation and distribution. Crowds overreact | Up/down volume ratio and distribution near highs: no edge. Overreaction → short-term reversal: ✅ (small) | ❌ / 🟡 |
| Wyckoff | Effort vs result, climaxes, springs, dull-range breakouts, strength on shock days | All NO_EDGE. Stocks that held up best on crash days **lagged** afterwards (t −3.2) | ❌ / 🔁 |
| Schabacker | Patterns (triangles, H&S, doubles), gaps, key-reversal days, quiet pullbacks in bull markets | Patterns, gaps and reversal days: no edge. Quiet pullback: +0.2–0.25% (t≈1.3 in both periods) | ❌ / 🟡 |

## 3. What the most-viewed YouTube creators teach

The 300 videos by topic, view-weighted: full courses 32%, chart patterns 25%, candlesticks 22%, day trading 10%, price action 9%, ICT/smart money 9%, MAs/RSI/MACD/Fibonacci about 4% each. Risk management appears in **0** titles.

| Consensus (creators teaching it, of 16) | Measured | Verdict |
|---|---|---|
| Trade from a level, not mid-range (15) | Support/resistance tests: no edge | ❌ |
| Trade with the higher-timeframe trend (14) | Risk benefit only | 🟡 |
| Candlesticks are triggers in context (13) | 12 Nison patterns with prior-trend context: all NO_EDGE (Marshall et al. 2006 agree) | ❌ |
| Liquidity / stop-hunt narrative, ICT/SMC (9) | Fair-value-gap retrace and liquidity-sweep reversal: real win rates 37–40%, no event-study edge | ❌ |
| Market structure and Fibonacci pullbacks (8) | Fibonacci 61.8% bounce: no edge | ❌ |
| Fixed 1.5–3R targets; wait for the pullback; volume confirmation (6 each) | Pullback > breakout (consistent, small). Volume: no effect | 🟡 / ❌ |

**Claimed-performance strategies, tested on daily US stocks 2000–2019:**

| Strategy (claim) | Real win rate | Edge vs same-date control | Event-study verdict |
|---|---|---|---|
| TradingLab MACD + 200 EMA ("86% win rate") | 51% / 47% | +0.4% / +0.25% per trade | NO_EDGE |
| Rayner Teo RSI(10) pullback ("88%") | 69% / 71% | (control bias) | NO_EDGE (+0.15%/5d, t≈1) |
| Rayner Bollinger(20, 2.5) reversion ("66–94%") | 70% / 68% | +0.7% / −0.2% | inconsistent |
| Rayner 200-day breakout + 6×ATR trail ("35–50% win, payoff > 2") | 42% / 40% ✓ | **−0.9% / −0.2%** (worse than random entry) | profits come from drift and the exit |
| Data Trader Stoch + RSI + MACD ("proven 100×") | 53% / 48% | +0.4% / +0.2% | NO_EDGE |
| ICT fair-value-gap retrace | 40% / 40% | +0.3% / +0.1% | NO_EDGE |
| ICT liquidity sweep | 37% / 40% | 0.0% / +0.2% | NO_EDGE |

## 4. What the academic literature says (graded by the evidence survey)

| TA family | Literature grade | Our result |
|---|---|---|
| Long-window trend / MA timing | B: cuts volatility and drawdown | Same: drawdown insurance, about −1%/yr CAGR |
| Time-series momentum | A for multi-asset futures, B for a single ETF | 12-month TSMOM on S&P: improves drawdown; Sharpe mixed |
| Cross-sectional momentum | B (A before 2000); crashes in 2009 | NO_EDGE 2000–2019; REVERSED in bear markets |
| 52-week high | B, weak after 2000 | NO_EDGE (as return); ✅ as low-risk state |
| Breakouts | C, decayed after 1986 | NO_EDGE / REVERSED |
| Chart patterns | C | NO_EDGE |
| Candlesticks | D | NO_EDGE |
| RSI/oscillators | D (= short-term reversal) | Overbought → small underperformance; oversold → nothing |
| Short-term reversal | B, below costs | Consistent sign, 0.1–0.2%, below costs |
| Volume confirmation | C | NO_EDGE |
| Support/resistance | C | NO_EDGE |
| Divergences, Fibonacci, Elliott, Gann | D | NO_EDGE (divergence, Fibonacci) |

Aronson (2006) tested 6,402 rules on the S&P 500 with a data-mining correction and found none significant. Our sweep (123 rules × 2 periods, 0 confirmed bullish rules) reproduces that conclusion on individual stocks after 2000.

## 5. Bottom line used to write the rulebook

1. **Technical analysis is a risk instrument.** Trend health and distance from the 52-week high sort stocks into crash-risk classes.
   - The classes were 2.6–4× apart in 2000–2019, for both development and holdout tickers and within every volatility level.
   - In the locked 2020–2026 test they were about 1.5–2× apart. The COVID crash hit "healthy" stocks while the regime still read risk-on.
   - In the final blind exam, an agent's BEARISH calls fell ≥ 20% within 60 days 40% of the time, against 5.9% for its BULLISH calls.
2. **It is not, on daily US stocks since 2000, a reliable return predictor.** Popular entry signals, books' setups and YouTube systems don't beat a random stock bought on the same day once statistics are done properly.
3. **Small, consistent timing effects exist.** Short-term overextension lags and pullbacks inside uptrends slightly beat breakouts. They are smaller than trading costs: use them to choose *when* to act, never *whether*.
4. **Market-level slow trend filters are real drawdown insurance** (about −1%/yr of return for about 25 points less drawdown). Fast filters are not.

## 6. v2.2 additions (earnings data, delisted stocks, crash overlays)

| Belief | Measured | Verdict |
|---|---|---|
| "Buy the dip: stocks far below their high are bargains" (value-flavoured TA, YouTube) | Stocks ≥ 40% below their 52-week high: +4.7% over 60 days among survivors, but **−3.4% among later-delisted stocks**, where 48.6% fell another 20% or more | ❌. The apparent edge was survivorship bias. |
| Trend health matters (Weinstein Stage 4, Minervini) | On 76 later-delisted stocks: BEARISH-class crash odds 37.5% vs 14.3% for BULLISH, and BEARISH 60-day return −1.4% vs +4.7% | ✅. Stronger once failures are included. |
| Post-earnings drift / "earnings gap and go" (O'Neil, Ross Cameron, PEAD literature) | 128k earnings events: gap-down drift (−0.8%/60d) held its sign 2000–2019, then vanished or reversed in 2020–26. EPS surprise alone showed no drift | ❌ as a signal. |
| "Avoid holding through earnings" (common trader advice) | A report within 10 trading days raised short-term crash odds 2–3× in every class and every sample, including the locked test | ✅ as a risk flag (E1). |
| Volatility spikes / VIX tell you when to get out (YouTube, market-timing blogs) | Six fast triggers (VIX ≥ 30, VIX +50%, SPY −7%/−10%, realized vol ≥ 30%): no meaningful drop in BULLISH-class crash odds, and Sharpe and drawdown got worse on the index | ❌. Shocks arrive before triggers fire. |
