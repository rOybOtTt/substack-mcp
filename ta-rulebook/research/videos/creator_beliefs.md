# What the most-viewed YouTube TA educators teach, rebuilt without transcripts

Corpus: the 300 most-viewed TA videos (519 M views). The top 15 channels hold 366 M views (70.6%). ICT/SMC topics cover 43 videos but only ~9% of views.

## 1. Method and limitations

**What was not possible.** I had no transcripts. A YouTube watch page fetched with WebFetch redirects to Google's bot-check page (`google.com/sorry`), so I did not use watch pages at all. I also did not use transcript or "AI video summary" sites (lilys.ai, videohighlight, chaindesk, sozai, pickscribe, render.com YouTube mirrors), Invidious or Piped. Where a search-engine snippet that came from such a page was the only lead, I tag it **[snippet]** and never use it as a rule source. One more refusal: when a site refused a fetch (403/406), I did not retry with different headers.

**What the CSV gives.** The `description` field is a ~120-character search snippet, not the full description. It is useful mainly for funnels and claims, and for one chapter list (Trade with Purab).

**Confidence grades** (used throughout):
- **A** = the creator's own written rules.
- **B** = a third-party implementation or test of the named strategy (code, replication).
- **C** = titles, snippet descriptions and course/sales pages only. These show *what topics* a creator teaches, not the exact rules.

**Sources per creator.** Raw pages are saved under `/tmp/claude-0/-home-user-substack-mcp/bd2a3180-4a74-5075-a5b0-357ed5501f5e/scratchpad/web_raw/creators/`, with a URL index in `_sources.txt`.

| Creator (views) | Sources | Grade |
|---|---|---|
| Rayner Teo (21.9 M) | tradingwithrayner.com pages:<br>[moving-average-indicator](https://www.tradingwithrayner.com/moving-average-indicator/)<br>[ultimate-candlestick-patterns-trading-course](https://www.tradingwithrayner.com/ultimate-candlestick-patterns-trading-course/)<br>[trading-strategy-winning-rate-of-88-89](https://www.tradingwithrayner.com/trading-strategy-winning-rate-of-88-89/)<br>[mean-reversion-trading-strategy](https://www.tradingwithrayner.com/mean-reversion-trading-strategy/)<br>[bollinger-band-trading-system](https://www.tradingwithrayner.com/bollinger-band-trading-system/)<br>[trend-following-strategy](https://www.tradingwithrayner.com/trend-following-strategy/)<br>[swing-trading-strategies](https://www.tradingwithrayner.com/swing-trading-strategies/)<br>[swing-trading-techniques-that-work](https://www.tradingwithrayner.com/swing-trading-techniques-that-work/)<br>[macd-indicator](https://www.tradingwithrayner.com/macd-indicator/)<br>[rsi-indicator-cheat-sheet](https://www.tradingwithrayner.com/rsi-indicator-cheat-sheet/)<br>[how-to-avoid-false-breakout](https://www.tradingwithrayner.com/how-to-avoid-false-breakout/)<br>[when-should-you-not-trade-with-the-trend](https://www.tradingwithrayner.com/when-should-you-not-trade-with-the-trend/)<br>[range-vs-trending-market](https://www.tradingwithrayner.com/range-vs-trending-market/)<br>[golden-cross-trading-strategy](https://www.tradingwithrayner.com/golden-cross-trading-strategy/)<br>[bollinger-bands-trading-strategy](https://www.tradingwithrayner.com/bollinger-bands-trading-strategy/)<br>[the-ultimate-chart-patterns-trading-course](https://www.tradingwithrayner.com/the-ultimate-chart-patterns-trading-course/)<br>[win-rate](https://www.tradingwithrayner.com/win-rate/) | A |
| Ross Cameron / Warrior Trading (16.0 M) | [bull-flag-trading](https://www.warriortrading.com/bull-flag-trading/)<br>[momentum-day-trading-strategy](https://www.warriortrading.com/momentum-day-trading-strategy/)<br>[simplest-day-trading-strategy](https://www.warriortrading.com/simplest-day-trading-strategy/)<br>[macd](https://www.warriortrading.com/macd/)<br>(The gap-and-go URL returned an image, not text.) | A |
| ICT (2.5 M) + SMC | [theinnercircletrader.com](https://theinnercircletrader.com/) (home page only)<br>Unofficial concept site innercircletrader.net:<br>[FVG](https://innercircletrader.net/tutorials/fair-value-gap-trading-strategy/)<br>[order block](https://innercircletrader.net/tutorials/ict-order-block/)<br>[OTE](https://innercircletrader.net/tutorials/ict-optimal-trade-entry-ote-pattern/)<br>[Silver Bullet](https://innercircletrader.net/tutorials/ict-silver-bullet-strategy/)<br>[killzones](https://innercircletrader.net/tutorials/master-ict-kill-zones/)<br>[Power of 3](https://innercircletrader.net/tutorials/ict-power-of-3/)<br>[2022 model](https://innercircletrader.net/tutorials/complete-ict-trading-strategy-2022/)<br>Counter-evidence: [FVG placebo study](https://www.tradingview.com/script/Kbq3WncE-Fair-Value-Gap-FVG-Statistics-with-Placebo-Control/) | B |
| TradingLab (34.7 M) | Independent replications of the MACD video:<br>[Stats Edge](https://letters.statsedgetrading.com/p/i-tested-a-viral-86-win-rate-macd)<br>[Profits on Autopilot](https://profitsonautopilot.substack.com/p/the-ultimate-algotrading-guide-part)<br>Medium and GitHub tests (403 to fetch; seen via search)<br>[tradinglab.ai](https://tradinglab.ai/) (signals funnel) | B (MACD), C (rest) |
| Data Trader (20.2 M) | [TradingView implementation of Stoch+RSI+MACD](https://www.tradingview.com/script/Sxz75MZJ-Data-Trader-Stoch-RSI-MACD-Strategy-Indicator) | B (one strategy), C (rest) |
| The Trading Channel (46.6 M) | [EAP course/sales page](https://thetradingchannel.org/video-sales-page)<br>[free course page](https://ttcforexcourse.com/bfc) | C+ |
| TJR, Smart Risk (adjacent) | TradingView implementations:<br>[TJR checklist](https://www.tradingview.com/script/IYLMKdC6-TJR-Strategy-Indicator/)<br>[TJR Seek and Destroy](https://www.tradingview.com/script/9yqF7p26-TJR-SEEK-AND-DESTROY/) | B/C |
| Trading Rush (tester, not top 15) | [MACD 200×](https://tradingrush.net/i-tested-macd-200-times-brutal-test-win-rate/)<br>[BB+RSI](https://tradingrush.net/bollinger-bands-rsi-trading-strategy-tested-100-times-will-this-make-profit-for-you/)<br>[BB 100×](https://tradingrush.net/i-risked-bollinger-bands-trading-strategy-100-times-heres-what-happened-indicator-strategies/)<br>["87%"](https://tradingrush.net/testing-87-win-rate-strategy-100-times-actually-worked/) | A (for its own tests) |
| Wysetrade, Brad Goh, Fractal Flow, JeaFx, Craig Percoco, Trade Prime, Trading 212, Pushkar Raj Thakur, Neeraj Joshi, Trade with Purab | CSV titles and snippets, plus home pages:<br>[wysetrade.com](https://wysetrade.com/)<br>[fractalflowpro.com](https://www.fractalflowpro.com/)<br>[jeafx.com](https://www.jeafx.com/)<br>[inevitrade.com](https://inevitrade.com/)<br>[craigpercoco.com](https://craigpercoco.com/)<br>Trading 212 learn pages returned 403. All are sales funnels with no rule text. | C |

**Limits that matter for use.**
1. For 10 of the 16 creators I can say *what topics* they teach, not their exact parameters.
2. Belief counts in §2 are lower bounds. A creator scores only if their written material, a third-party implementation, or a title/description shows the belief.
3. Rayner Teo and Ross Cameron are over-represented in the exact rules, because they are the two who publish rules in text.
4. Most strategies were designed for intraday forex, crypto or small caps. §5 says where I translated them to daily stock bars.

## 2. Consensus beliefs, ranked by number of creators (out of the 16: top 15 + ICT)

Evidence codes: W = written rules, X = third-party implementation, T = title/snippet only. Counts are lower bounds.

| # | Belief | n/16 | Who |
|---|---|---|---|
| 1 | **Trade from a level** (S/R, supply/demand zone, MA, FVG/OB), not mid-range | 15 | Rayner W, Ross W, ICT X, TTC W, TradingLab X; T: Data Trader, Wysetrade, Brad Goh, JeaFx, Fractal Flow, Trading 212, Pushkar, Neeraj, Trade Prime, Craig |
| 2 | **Trade with the higher-timeframe trend/bias** (rising 200/50 MA, HH/HL, "daily bias") | 14 | Rayner W, Ross W ("strong daily chart above the MAs"), ICT X, TTC W, TradingLab X, Data Trader X; T: Trading 212, Wysetrade, Brad Goh, JeaFx, Fractal Flow, Pushkar, Neeraj, Trade Prime |
| 3 | **Candlesticks are triggers in context only** (13 teach candles; ≥7 explicitly say "not in isolation") | 13 | Rayner W, TTC W, Ross W; T: TradingLab ("Candlestick Patterns Don't Work (Unless You Do This)"), Trade Prime ("…That Actually Work"), Wysetrade, Fractal Flow, JeaFx, Data Trader, Brad Goh, Pushkar, Neeraj, Purab |
| 4 | **Liquidity / stop-hunt narrative**: obvious stops get run, false breaks are engineered | 9 | ICT X, Rayner W (1-ATR stop buffer); T: Brad Goh, Fractal Flow, Neeraj, Pushkar, TradingLab, Data Trader, Craig |
| 5 | **Market structure** (HH/HL, BOS/CHoCH) defines trend and reversal | 8 | Rayner W, TTC W, ICT X; T: Brad Goh (×4), JeaFx (×2), Neeraj, Pushkar, Fractal Flow |
| 6 | **Fibonacci pullback entry** (50–61.8%, or OTE 62–79%) | 8 | ICT X; T: Trading 212, Wysetrade (×3), Brad Goh (×2), Data Trader, Trade Prime, Pushkar, Neeraj |
| 7 | **Stop at invalidation plus a fixed 1.5–3R target** | 6+ | Ross W (2:1), Rayner W, TTC W, TradingLab X (1.5R), Data Trader X (1.5R), ICT X (1:3) |
| 8 | **Don't chase; wait for a pullback, retest or confirmation** | 6 | Rayner W, Ross W, TTC W, ICT X ("Do not pre-position"); T: TradingLab, Data Trader |
| 9 | **Volume/participation confirms the move** | 6 | Ross W (RVOL ≥ 2), Rayner W; T: Pushkar, Neeraj, Data Trader, Trade Prime (VWAP) |
| 10 | **Indicators lag: use them as filters or confluence, never alone** | 5 | Rayner W, Ross W, TTC W, TradingLab X ("By itself, not that powerful"), Data Trader X |
| 11 | **RSI extremes are not reversal signals in trends**; use as trend filter or divergence | 5 | Rayner W; T: Trading 212, Neeraj ("You Are Using It WRONG!"), Pushkar, Wysetrade |
| 12 | **Avoid chop/ranges with trend tools** | 4 | Rayner W ("Avoid using them in range markets"), Ross W ("chopping around sideways are useless"), TTC W, ICT X |
| 13 | **Top-down multi-timeframe analysis** | 4 | Rayner W, Ross W, TTC W, ICT X |
| 14 | **Risk ~1% per trade and size off the stop** | 3 | Rayner W, Ross W, TTC W |
| 15 | **Time of day matters** (intraday only) | 3 | Ross W (9:30–11:30 ET), ICT X (killzones), Neeraj T (9:20 am) |

**Read-through.** The near-universal core is trend + level + candle trigger. Rayner calls it "TAE" (Trend, Area of value, Entry trigger). SMC calls it bias + PD array + MSS. Warrior calls it a strong daily chart + pullback to VWAP/9 EMA + first candle to make a new high. All three versions are testable on daily stock bars (§5).

## 3. What the creators teach

### 3.0 The 25 most-viewed videos

| Rank | Channel | Video | What it teaches | Grade |
|---|---|---|---|---|
| 1 | Pushkar Raj Thakur | Candlestick course ep. 1 | Single-candle anatomy; part 1 of 3; demat-referral funnel | C |
| 2 | The Trading Channel | "Only TA video you'll ever need" (77 min) | Candles, trend reading, "structure" S/R, a few indicators, entry patterns (mirrors the EAP Basics syllabus) | C+ |
| 3 | Pushkar | TA for beginners | Identify trends, draw support and resistance | C |
| 4 | Craig Percoco | Start day trading 2025 | Beginner roadmap; Inevitrade funnel | C |
| 5 | Rayner Teo | Ultimate candlestick course | Body vs wick; 5 reversal triggers; TAE framework; never trade candles in isolation | A |
| 6 | TradingLab | ONLY candlestick guide | Pattern catalogue; the channel says candles "don't work" without context | C |
| 7 | Trade with Purab | Candlestick full course | Chapters include indecision candles, three-line strike, live chart patterns | C |
| 8 | Wysetrade | Ultimate chart patterns | Classical patterns; sells posters and guides | C |
| 9 | The Trading Channel | Only day-trading strategy | Rules-based pullback strategy (rules paywalled) | C |
| 10 | Fractal Flow | Chart patterns guide | Patterns, "science-based" framing | C |
| 11 | Fractal Flow | Candlestick guide | Patterns with "advantages and [disadvantages]" | C |
| 12 | Wysetrade | Ultimate candlestick course | Candle reading | C |
| 13 | Wysetrade | Best trend lines strategy | Trend lines, break/retest | C |
| 14 | TradingLab | MACD [86% win rate] | 200 EMA + MACD cross below zero + support, 1.5R (CP-1) | B |
| 15 | Pushkar | TA in Hindi | General TA | C |
| 16 | TradingLab | Avoid false breakouts | Rule not recovered. Rayner's page with the identical title: don't chase; need a ≥ 10-candle buildup; stop below it | C (A Rayner) |
| 17 | Pushkar | Reversal chart patterns | Double top/bottom, head-and-shoulders | C |
| 18 | Data Trader | Candlestick guide | Patterns; PDF via Telegram | C |
| 19 | Ross Cameron | Read candlestick charts | Candle basics → bull flag, first-candle-new-high entry | A |
| 20 | Pushkar | Price action masterclass | Price action; "AutoTrender" indicator funnel | C |
| 21 | The Trading Channel | Only candlestick video | Candles; proprietary "TCSC" entry | C |
| 22 | Trading 212 | Fibonacci retracements | Retracement entry and exit points (broker education) | C |
| 23 | Data Trader | Every strategy in 12 min | Taxonomy: trend, mean reversion, breakout, scalping | C |
| 24 | Umar Punjabi | Read charts (35 min) | Chart reading; VIP Telegram funnel | C |
| 25 | Brad Goh | Supply & demand course | Zones; claims "$2.5M+" from a "mechanical" system | C |

### 3.1 Rayner Teo (A): the most rule-explicit creator, and stock-focused

**Core beliefs**
- Trend first, defined by a rising 200 EMA with price above it. For a short-term trend, price above a rising 20 EMA.
- Trend strength = MA steepness.
- Enter at an "area of value": the space between the 20 and 50 EMA, support, or a trendline.
- Candles are only triggers.
- Stocks drift up long-term, so "avoid shorting the stock market," especially above the 200-day MA.

**Entry rules (MA strategy)**
1. 200 EMA pointing higher and price above it.
2. Wait for "two tests" of dynamic support at the 20/50 MA.
3. Go long on the third test.
4. Stop: 2 ATR. Exit: "when candle close beyond 50 EMA".

**Swing strategies**
- *Stuck in a box*: price breaks below range support, then closes back above it. Long next candle. Stop 1 ATR below the candle low. Take profit before resistance.
- *Catch the wave*: trend respects the 50 MA; bullish rejection at the MA; long next candle. Stop 1 ATR below the low. Target just before the swing high.
- *Fade the move*: strong momentum into resistance that takes out the prior high, then a strong bearish close. Short next candle. Stop 1 ATR above the high. Target before the nearest swing low.

**Indicator uses**
- Higher-timeframe MACD line vs signal line as a direction filter.
- RSI(200) > 50 as a long-term uptrend filter.
- RSI dips below 30 and re-crosses above it: entry trigger. Exit when RSI crosses above 50.
- Bollinger Bands in an uptrend: buy a close below the lower band followed by a bullish reversal candle.

**Stops and targets**
- Swing trades: stop 1 ATR beyond structure, not just under support, to avoid stop hunts. Target just before the opposing level. "Scale half, ride half."
- Trend trades: no target; trail with an MA or ATR.

**Do NOT trade**
- In ranges with MA or MACD tools.
- When price is overextended from a respected MA, far from structure, at the upper channel boundary, or far from an area of value.
- Breakouts after "a huge break out with strong and bullish candles" with no buildup.
- Short pullbacks in stocks.

### 3.2 Ross Cameron, Warrior Trading (A): small-cap momentum day trading

**Core beliefs**
- "Momentum is what day trading is all about."
- Trade only "stocks at extremes", i.e. once-a-year events.
- "It's better to trade sub-par patterns on the best stocks than perfect patterns on the wrong stocks."

**Stock filters**
- Float under 100 M shares, ideally under 20 M ("20-20" rule: < 20 M float, < $20 price).
- "Strong Daily Charts (above the Moving Averages and with no nearby resistance)".
- Relative volume ≥ 2× (time-of-day adjusted).
- A catalyst (PR, earnings, FDA). A gap up for gap-and-go.

**Entry (bull flag)**
- Flagpole on high relative volume; 2–3 red pullback candles on lighter volume.
- Retrace ≤ 50%; must not break VWAP or the 9 EMA.
- Enter on "the first candle to make a new high". "Breakout or bailout."

**Stops and targets**
- Stop at the pullback low. He prefers a ~20¢ stop and 2:1 profit/loss.
- Sell ½ at the first target, then move the stop to breakeven.
- Exit on the first red 5-minute candle close, or on an "extension bar".

**MACD (12/26/9, "don't change these")**
- Trade only when MACD is positive / the MACD line is above the signal line.
- When it crosses below: "a clear indicator to stop trading".

**Filters and do-NOT**
- Trade 9:30–11:30 ET; after 11:30, only the 5-minute chart.
- Avoid low-relative-volume or non-obvious stocks.
- Daily bull flags are "perfectly valid", but upcoming earnings "will easily override" them.

**Claims**: see CP-9.

### 3.3 ICT (Michael Huddleston) and SMC derivatives (B; unofficial concept site plus community code)

**Core beliefs**
- Price is delivered by an "algorithm" seeking liquidity (resting stops above highs and below lows) and rebalancing imbalances.
- Retail breakouts are the manipulation leg ("Judas swing", Power of 3: Accumulation, Manipulation, Distribution).
- ICT's own top-300 video attacks other educators as "frauds … poor copycats".

**Definitions**
- *FVG*: 3 candles where the 1st candle's high and the 3rd candle's low do not overlap (bullish). Entry on the retrace into the gap, often at its 50% "consequent encroachment".
- *Order block*: the last opposite candle before a displacement that breaks structure. Strict version: the second candle takes the OB's low and closes above its high, plus a lower-timeframe FVG and MSS.
- *OTE*: Fibonacci retracement 0.62–0.79, precise level 0.705.
- *Killzones* (NY time): London 02:00–05:00, NY 07:00–09:00.
- *Silver Bullet* windows: 03–04, 10–11, 14–15 NY.

**2022 model**
1. Higher-timeframe daily bias.
2. Session sweep of the prior range high or low against the bias.
3. Lower-timeframe MSS with displacement.
4. Enter at the PD array (FVG/OB) tap.
5. Stop beyond the swept extreme; target the opposite liquidity.
6. "When even one is missing, I stand aside."

**Do NOT**
- Trade outside the windows.
- Pre-position before the MSS.
- Take counter-bias OTEs without a higher-timeframe reason.

**TJR (community implementation)**: an 8-factor checklist.
1. Session active.
2. 1H MA bias.
3. Liquidity sweep: wick beyond a swing/session level, close back inside.
4. BOS by an impulse candle with body > 50% of its range.
5. FVG.
6. Order block.
7. Optional SMT divergence.
8. Displacement close beyond the 79% Fibonacci level of the candle.

**Smart Risk**, **Fractal Flow** ("Learn ICT Concepts in 30 Minutes"), **Neeraj Joshi** (ICT/SMC/FVG in Hindi) and **Brad Goh** (SMC course) re-teach the same vocabulary.

### 3.4 TradingLab (B for MACD, C otherwise)

- Snippets frame indicators as weak alone ("By itself, not that powerful").
- The trading style is a "3-step formula" (*The Only Trading Strategy You'll Ever Need*).
- Videos on FVG "secrets", supply/demand, false breakouts, Bollinger Band + RSI, and scalping ("backtested and proven to work!").
- Monetisation is a signals service ("Real-time buy/sell signals").
- The only recoverable exact rules are the MACD video's (CP-1).
- Do-NOT (title-level): candlesticks without context; naive breakouts.

### 3.5 Data Trader (B for one strategy, C otherwise)

- Indicator-stack day trading for forex and crypto, with stocks named in titles.
- Strategy videos: MACD, MA crossover, trend lines, Stochastic, BB breakout, Fibonacci, FVG, volume profile.
- Funnels: Telegram and a custom indicator.
- The one written rulebook is the Stoch + RSI + MACD strategy (CP-7).
- The MACD "high winrate" video pairs MACD with a 100 EMA trend filter and a 1.5× stop target **[snippet]**.

### 3.6 The Trading Channel (C+)

- "Structure trading" (support/resistance levels), trend reading, and "the pullback strategy" with full "entries, stops and targets".
- Proprietary entries: "TCSC" candle, "DT/DB kicker", "123 reversal", "swing reversal". Multi-timeframe and multiple-target management.
- An ATR video calls ATR the "Most Useful Indicator On The PLANET". ATR presumably sizes stops and targets.
- Explicitly teaches backtesting and "optimizing a portfolio" by dropping pairs that don't fit the strategy. That is a curve-fitting red flag.
- Pitch: "Only around 6% of traders will ever learn enough to become consistently profitable." EAP costs $197/month.

### 3.7 Wysetrade (C)

- Fourteen top-300 videos: chart patterns, candlesticks, trend lines, a price-action strategy, a moving-average strategy, an RSI "Wysetrade Method", "UNFAIR" Fibonacci, "15 Best Price Action Strategies", Bollinger Bands "INSANELY ACCURATE", Ichimoku.
- The site sells "Candlesticks & Chart Patterns Guides" and promotes a TradingView affiliate link.
- No written rules found. Beliefs inferred: trend lines plus key levels plus candle confirmation, Fibonacci pullbacks, and RSI as a trend/level tool rather than overbought/oversold.

### 3.8 Brad Goh, "The Trading Geek" (C)

- Supply & demand (×3), SMC, market structure (×4), trendline-break, Fibonacci and breakout videos.
- Claims a "mechanical trading system" and "$2.5M+ in profits" after "blowing 7 accounts".
- Inferred core: structure-defined trend, zones of origin, and a trendline/structure break as the trigger.

### 3.9 Fractal Flow (C)

- Positions itself as multidisciplinary (economics, physics, neuroscience) and "DO NOT make fake promises".
- Courses on fractal price action, statistical arbitrage, volatility and gamma scalping.
- YouTube content is pattern catalogues, ICT and Wyckoff. Patterns are presented with their "advantages and [disadvantages]". This is the one channel that signals limits up front.

### 3.10 JeaFx (C)

- Candles as "a story": "the ONLY THREE types of candlestick pattern ~ how to read every body & wick".
- Market-structure courses (68 min and "the ONLY lesson"), supply-and-demand masterclasses, Wyckoff.
- Sales page: "Why your definition of a good trade is probably wrong", "balance the probabilities", "$24m+ Student Success".

### 3.11 Trading 212 (C, broker education)

- Textbook use: moving averages "to identify the trend direction … set support and resistance levels … crossovers to confirm trend reversals".
- Fibonacci entry and exit points.
- RSI ("being popular doesn't [mean …]"), Bollinger Bands.
- CFD-risk disclaimers.

### 3.12 Craig Percoco (C)

- Beginner day-trading roadmaps; a "FULL Technical Analysis Day Trading Guide".
- Sells a $67 preset TradingView layout.
- **[snippet]**: buy the retrace into a fair value gap left by a big push, using a LuxAlgo FVG indicator.
- Claim: "Made Me $30k/Month".

### 3.13 Trade Prime (C)

- "7 Candlestick Patterns That Actually Work", "MACD … 4 Advanced Strategies", "Fibonacci … 3 Advanced Strategies", "Moving Averages … 7 HACKS", "90% of Traders Use VWAP Wrong!"
- Gumroad program.

### 3.14 Indian Hindi-language channels: Pushkar Raj Thakur (88.8 M, #1 by views), Neeraj Joshi, Trade with Purab (C)

These are full syllabi for Indian equities.

- **Pushkar** covers candles (single/double/triple episodes), reversal, continuation and neutral chart patterns, support/resistance and trend identification, RSI and RSI divergence, SMA/EMA, Fibonacci, volume, breakout/breakdown, intraday momentum-stock selection, Bollinger Bands, Ichimoku, SMC. Monetisation: a broker demat-account referral and "AutoTrender" indicator subscriptions.
- **Neeraj** adds a "9:20 am Intraday Strategy – VWAP + MA". **[snippet]**: 5-minute VWAP with a 7 EMA; EMA vs VWAP decides long or short. He also covers volume analysis, MACD and RSI divergence ("You Are Using It WRONG!"), and full ICT/SMC courses.
- **Purab** covers candles (indecision candles, three-line strike) and chart patterns.
- Inferred core: the generic consensus in §2, applied to NSE stocks.

## 4. Claimed-performance strategies (for backtesting)

**CP-1 TradingLab, "BEST MACD Trading Strategy [86% Win Rate]"** ([video](https://www.youtube.com/watch?v=rf_EQvubKlk), 4.6 M views)
- Rules, as replicated by independent coders:
  - Price above the 200 EMA.
  - MACD(12,26,9) line crosses above the signal line *below the zero line*.
  - Price at support.
  - Stop "below the 200 EMA" (Trading Rush's version uses the pullback low).
  - Target 1.5 × risk. Shorts mirror.
  - Timeframe: the original demo was intraday crypto (Ethereum, 15-minute).
- **Claim: 86% win rate**, shown with "a screen recording of three cherry-picked trades", no backtest.
- **Independent results:**
  - [Stats Edge](https://letters.statsedgetrading.com/p/i-tested-a-viral-86-win-rate-macd): 21% win rate on ETH 15-minute, about −40%; break-even before costs on ES.
  - [Profits on Autopilot](https://profitsonautopilot.substack.com/p/the-ultimate-algotrading-guide-part): daily ES over 27 years, histogram-cross variant, 32% win rate, "lost money last 5 years".
  - Medium (GoldenAlgoTrader): ~36%.
  - GitHub gold 1-hour test: 47.8% / 63.3%.
  - Breakeven at 1.5R is 40%.

**CP-2 Rayner Teo, "Trading Strategy with a Winning Rate of 88.89%"** ([page](https://www.tradingwithrayner.com/trading-strategy-winning-rate-of-88-89/))
- Rules (S&P 500, daily):
  - Index above its 200-day MA.
  - RSI(10) < 30 → buy next day's open.
  - Exit at the next open after RSI(10) > 40, or after 10 trading days. No price stop.
- Claim (1996–2019): 36 trades; win rate 88.89%; annual return 2.13%; average gain +1.43%; average loss −0.87%.

**CP-3 Rayner Teo, "Mean Reversion Trading Strategy That Works (86.84% Winning Rate)"** ([page](https://www.tradingwithrayner.com/mean-reversion-trading-strategy/); credited to Connors & Alvarez)
- Same rules as CP-2, reported as 38 trades over 25 years.
- Stock version:
  - Market above its 200-day MA; stock RSI(10) < 30.
  - Filter/rank stocks by 100-day ROC.
  - 10% per stock, maximum 10 positions; same exit.
  - Claim: "Average annual return: 12.29%" (Russell 1000).

**CP-4 Rayner Teo, Bollinger Band system ("+7,605% / +7,577.84% over 30 years")** ([page](https://www.tradingwithrayner.com/bollinger-band-trading-system/))
- Rules (Russell 1000, daily):
  - Stock above its 200-day SMA.
  - Close below the lower BB(20, **2.5σ**).
  - Limit buy 3% below the last close.
  - If over-subscribed, rank by the 100-day price increase.
  - 20% per position, maximum 5 positions.
  - Sell when RSI(2) > 50, or after 10 trading days.
- Claim: net +7,577.84%; 1,365 trades; average annual +15.56%; max drawdown −23.20%.
- The win rate is stated as **"94%"** and, in the same page, **"66%"**. The 94% is probably the share of winning years (28 of 30).

**CP-5 Rayner Teo, trend following** ([page](https://www.tradingwithrayner.com/trend-following-strategy/))
- Rules (20 futures markets, daily):
  - Long when the close is the highest of the last 200 days; short at the lowest close.
  - 6 ATR trailing stop (ATR period not stated).
- Claim (2000–2025): total +2,866%; 14.51%/yr; win rate 45.77%; max drawdown 37.7%.

**CP-6 Rayner Teo, site banner** "This Trading Method Averaged 17.53% A Year Over The Last 24 Years". Rules undisclosed (paid product). Not testable.

**CP-7 Data Trader, "Most Effective Stochastic + RSI + MACD Trading Strategy (Proven 100x)"** (816 K views; [TradingView implementation](https://www.tradingview.com/script/Sxz75MZJ-Data-Trader-Stoch-RSI-MACD-Strategy-Indicator))
- Settings: Stochastic(14,3,3), RSI(14), MACD(12,26,9); 15-minute to 1-hour charts **[snippet]**.
- Long:
  - Stoch %K and %D oversold (< 20).
  - Then RSI > 50 and MACD line > signal.
  - Stop below the last swing low; target 1.5× the stop.
- Shorts mirror.
- Claim: "high win rate … back testing the strategy 100x" **[snippet]**. The exact number was not recovered.
- Independent: the TradingView author says it "generates barely, if any, signals". A Python test found 6 trades.

**CP-8 Data Trader, "Most Effective MACD Strategy for Daytrading" ("High Winrate")** **[snippet]**: MACD + 100 EMA trend filter, 1.5R. Low confidence; test as a CP-1 variant with a 100 EMA.

**CP-9 Ross Cameron.**
- Bull-flag/momentum rules as in §3.2.
- Claims: "accuracy of 69%" over "24,268 day trades"; "over $10 million in gross profit"; "$2k → $65,662.04 in 30 days" (video title).
- All self-reported, with Warrior's own disclaimer: "Ross's results are not typical."
- No payoff ratio is published alongside the 69%.

**CP-10 ICT Silver Bullet** ([page](https://innercircletrader.net/tutorials/ict-silver-bullet-strategy/); the site author's claim, not Huddleston's)
- Rules:
  1. Mark 15-minute buy-side and sell-side liquidity.
  2. In the 10–11 NY window, wait for an MSS with displacement on the 1–5 minute chart.
  3. Enter on the FVG tap; stop beyond the FVG-creating candle; target the next liquidity (~1:3).
- Claim: "55–65% win rate … with a 1:3 average risk-reward target".
- ICT's own claim: a setup that "repeats every day and yields five handles".
- Intraday index futures/forex only; no daily analogue except H-YT-17/20.

**CP-11 Trade Pro, "Simple Trading Strategy That 'Turned $1000 into $50000' Tested 100 Times – Bollinger Bands + MA"** (1.3 M views). Exact rules **not recoverable** from legitimate written sources; reposts carry only the title. Treat the claim as untested marketing. A generic BB + MA pullback is covered by H-YT-3.

**CP-12 Trading Rush, "I Tested MACD 200 Times"**
- Rules: 30-minute entries; MACD cross below zero; price above the 200 MA; stop below the pullback; 1.5R.
- Results:
  - ~60% win rate in hand-picked "extremely good" trending markets (gold uptrend, daily price above its 9 EMA).
  - 32% in hand-picked "bad" markets.
  - "around a breakeven win rate" over 100,000 automated trades.

**CP-13 Trading Rush, BB + RSI 100 trades**
- Rules: RSI < 30, then the first close above the middle BB → long; stop below the lower BB; 1.5R.
- Result: "approximately 35 percent", i.e. a loss at 1.5R. Relevant to TradingLab's "Bollinger Band + RSI Trading Strategy That Actually Works".

**CP-14 Trading Rush, "87% win rate"**: produced by scaling in (1% + 1% + 1%) toward support with a fixed stop. A win-rate artefact of position management, not a signal.

**CP-15 Income claims with no testable rules**
- TJR: "+$1,000,000 From One Simple Strategy".
- Craig Percoco: "$30k/Month"; also "$18,517/month [100x Strategy]" **[snippet]**.
- Brad Goh: "$2.5M+".
- JeaFx: "$24m+ Student Success".
- TradingLab scalping: "backtested and proven to work!".
- Wysetrade BB: "INSANELY ACCURATE".
- Rayner: "3 Proven Swing Trading Strategies". The rules are in §3.1; no statistics are given.

## 5. Testable hypotheses on daily stock OHLCV

**Conventions** (apply to all hypotheses unless stated):
- Signal on the close of *t*; entry at the open of *t+1*.
- Limits fill at min(open, limit) if low ≤ limit. A stop gapped through fills at the open. If stop and target fall in the same bar, the stop counts first.
- ATR = Wilder ATR(14); RSI is Wilder's; MACD(12,26,9); Stochastic slow (14,3,3); BB = SMA(20) ± kσ; V50 = SMA50 of volume; RVOL = V/V50.
- Trend filters:
  - F1: close > SMA200.
  - F2: F1 and SMA200 above its value 20 bars ago.
  - F3: RSI(200) > 50.
  - F4: SMA50 > SMA200.
  - F5: SPY > its own SMA200.
- Universe: US stocks, price ≥ $5, 20-day average dollar volume ≥ $5 M.
- Report: N, win rate, average win/loss in R, expectancy in R, profit factor, breakeven win rate = 1/(1+payoff), and 5/10/20-day forward returns.
- **Placebo**: the same stock, a random bar within ±60 days in the same filter state, with identical stop/target geometry.

**H-YT-1 Trend-filter meta (consensus #2).**
- Rerun every long rule under F0 (none) and F1–F5.
- Prediction: F2 ≥ F1 > F0.
- Check F3 agrees with F1 on more than 90% of days.

**H-YT-2 RSI(10) pullback (CP-2/3).**
- SPY: F1 and RSI(10) < 30 → buy. Exit after RSI(10) > 40, or at the open of day 11.
- Stocks: F5 and RSI(10) < 30; rank by ROC(100); 10 slots × 10%.
- Claims to check: ~88% win rate, +1.43%/−0.87%, 2.13%/yr (index), 12.29%/yr (stocks).

**H-YT-3 BB(20, 2.5) reversion (CP-4).**
- Universe: top 1,000 by market cap.
- Signal: F1 and close < lower band → limit at 0.97 × close, valid *t+1* only.
- Rank by ROC(100); 5 slots × 20%.
- Exit after RSI(2) > 50, or after 10 days. No stop.
- Check 15.56%/yr, max drawdown 23.2%, and whether the trade win rate is 66% or 94%.

**H-YT-4 200-day closing-high breakout plus 6 × ATR(20) trailing stop from the highest close (CP-5, futures → stocks).**
- Variants: ATR(14); 4× and 8× multiples; the short mirror.
- Prediction: win rate 35–50%, payoff > 2.

**H-YT-5 "Third test" of the 20–50 EMA band (Rayner).**
- F2 using EMA200.
- Test = low ≤ EMA20 with close ≥ EMA50. Tests must be separated by a new 10-day high. Reset on a close < EMA50.
- Buy after the 3rd test; stop entry − 2 × ATR; exit after a close < EMA50.
- Compare the 1st and 2nd tests.

**H-YT-6 MACD + 200 EMA (CP-1, intraday → daily).**
- Signal: close > EMA200; MACD line crosses above signal with both < 0.
- Stop variants: S1 = EMA200 (minimum 0.5 × ATR away); S2 = 10-bar low.
- Target 1.5R; maximum hold 30 bars.
- Optional "support" filter: low within 1 × ATR of EMA50, or of a ≥ 20-day-old pivot low, in the last 5 bars.
- Benchmarks: 86% claimed vs 40% breakeven.

**H-YT-7 Stoch + RSI + MACD (CP-7, 15-minute/1-hour → daily).**
- %K and %D < 20 on some bar in [*t*−5, *t*]; then RSI(14) > 50 and MACD > signal. Take the first such bar only.
- Stop: 10-bar low; target 1.5R.
- Report signals per stock-year.

**H-YT-8 Gap-and-go, daily version (Ross; intraday → daily).**
- Day 0: gap ≥ 5%; RVOL ≥ 2 (also 5); $1–20 price; close in the top 30% of range.
- Day 1: buy stop at day-0 high; stop day-0 low; 2R target.
- "Breakout-or-bailout" variant: exit at the close if close ≤ entry.

**H-YT-9 Daily bull flag (Ross).**
- Pole: gain ≥ max(15%, 4 × ATR) in ≤ 5 bars, with volume ≥ 1.5 × V50.
- Flag: 2–5 bars, ≥ 2 down closes, retrace ≤ 50%, flag volume < pole volume, no close < EMA9.
- Buy stop above the prior high; stop at the flag low; target 2R.
- Ross's warning signs (retrace > 50%, heavy flag volume, close < EMA9) should predict failure.
- Skip if earnings fall within 5 bars.

**H-YT-10 MACD gates.** Split the H-YT-8/9/11/20 signals by daily MACD > signal and > 0 (Ross's "front side") and by weekly MACD > signal (Rayner). Prediction: gated entries do better.

**H-YT-11 Buildup vs chase (Rayner; TradingLab #16).**
- Breakout: close > the prior 50-day high.
- Buildup: the prior 10 bars span ≤ 2 × ATR, within 5% of the high. Stop: buildup low.
- Chase: breakout bar range ≥ 2 × ATR, no buildup. Stop: 2 × ATR.
- Target 2R. Also measure the 5-bar false-break rate.

**H-YT-12 Overextension (Rayner, Ross).**
- Within F2, bucket z = (close − EMA50)/ATR into < 1, 1–2, 2–3, 3–4, > 4.
- Prediction: forward returns fall, and the probability of revisiting EMA20 rises, with z.
- Extension bar (range ≥ 3 × ATR, close in the top 20%) → 5-day reversal?

**H-YT-13 Range false break ("stuck in a box").**
- Box: 40-bar span ≤ 20%, ≥ 2 touches per side.
- Trigger: low < support − 0.25 × ATR, close > support.
- Stop: low − 1 × ATR. Target: resistance − 0.25 × ATR.

**H-YT-14 50-MA pullback ("catch the wave").**
- SMA50 rising; ≥ 80% of the last 60 closes above it.
- Low ≤ 1.01 × SMA50, close > SMA50, CLV ≥ 0.33.
- Stop: low − 1 × ATR. Target: the 20-day high. Skip if the target is < 1R.

**H-YT-15 "Fade the move" short.**
- 5-day gain ≥ 3 × ATR, a new 20-day high, then a bearish bar (CLV ≤ −0.33).
- Stop: high + 1 × ATR. Target: 20-day low or 2R.
- Prediction: no edge under F1.

**H-YT-16 Candles in context (consensus #3).**
- Patterns:
  - Hammer: lower wick ≥ 2 × body, upper wick ≤ 25% of range, close in the top third.
  - Bullish engulfing.
- Contexts:
  - C1: anywhere.
  - C2: F2 and within 0.5 × ATR of the EMA20–50 band or a ≥ 20-day-old pivot low.
  - C3: below a falling SMA200.
- Stop: pattern low − 0.25 × ATR; target 2R.
- Prediction: C2 > C1 ≈ placebo > C3.

**H-YT-17 FVG retrace (ICT/SMC).**
- Bullish FVG: low_t > high_{t−2}; middle body ≥ 1 × ATR closing in its top 25%; gap ≥ 0.25 × ATR; close > SMA50.
- Limit at the gap midpoint, valid for 10 bars.
- Stop: middle-bar low − 0.1 × ATR. Targets: 2R and 3R.
- **The placebo is mandatory.** The prior study found no edge in 14 of 14 cells.

**H-YT-18 Order block without look-ahead.**
- OB = the last bearish bar *j* before a close above the 10-bar high, within 5 bars, by a bar with body ≥ 1 × ATR. The zone is known only at that close.
- Limit at high_j for 20 bars; stop low_j − 0.1 × ATR; target 2R.
- Strict variant: low_{j+1} < low_j.
- Also report the version counted from *j*, to measure the hindsight inflation.

**H-YT-19 Retracement depth.**
- Within F2, range = 5-bar pivot low *L* → 20-day high *H*, with *H* − *L* ≥ 4 × ATR.
- Limits at 0.382, 0.5, 0.618 and 0.705.
- Stop: *L* − 0.25 × ATR. Targets: *H*, and *H* + 0.272 × range.
- Competing claims: ICT (0.62–0.79) vs Trading 212/Wysetrade (0.5–0.618) vs the null (depth only changes R:R).

**H-YT-20 Liquidity-sweep reversal (ICT/TJR, intraday → daily).**
- Trigger: low < prior 20-day low − 0.1 × ATR, close back above it, close > open; F2.
- Optional BOS confirmation: close > 5-bar high within 3 bars.
- Stop: sweep low − 0.1 × ATR. Target: the 20-day high or 2R.
- Compare against breakdown continuation.

**H-YT-21 Ex-ante vs hindsight regime (Trading Rush 60% vs 32%).** Split H-YT-6 trades by ADX(14) ≥ 25 and CHOP(14) < 50 measured at *t*, versus ADX measured over *t*+1 to *t*+20. Prediction: only the hindsight split is large.

**H-YT-22 RSI re-cross (Rayner).**
- F3 and RSI(14) crosses up through 30.
- Stop: dip low − 0.5 × ATR. Exit: RSI > 50 or 15 bars.
- Compare against the unfiltered and counter-trend versions (the classic oversold buy).

**H-YT-23 Golden-cross hold (Rayner).** Hold while SMA50 > SMA200. Report whipsaws (reversals within 20 bars), exposure, CAGR and max drawdown vs buy-and-hold.

**H-YT-24 Volume confirmation (consensus #9).** For H-YT-9/11 and 20-day-high breakouts, split by breakout RVOL (≥ 2, 1–2, < 1) and by flag/pole volume ratio (< 0.7 vs > 1). Prediction: monotone in volume.

**H-YT-25 Earnings exclusion.** For every hypothesis, split signals with earnings in [*t*+1, *t*+5]. Prediction: lower win rate and higher variance.

**H-YT-26 Win rate vs edge.** For H-YT-2/3 vs H-YT-4, report payoff, expectancy, exposure-adjusted CAGR and max drawdown vs SPY. Does CP-2's 89% win rate at 2.13%/yr underperform passive exposure?

## 6. Contradictions and red flags

**Contradictions between creators**
- **Breakouts.** Ross buys the "first candle to make a new high" and high-of-day flat tops. Rayner says "chasing breakouts is for losers" and wants a buildup first. ICT/TJR call the same breakout the *manipulation* leg and fade it after a sweep. H-YT-11 and H-YT-20 decide this on daily data.
- **Targets.** Rayner's trend following uses none ("no profit targets"). TradingLab and Data Trader use 1.5R, Ross 2:1, ICT 1:3.
- **Win rate.** Rayner's win-rate article says win rate "means very little on its own" and that trend following wins 30–45%. The same site headlines 88.89% and 86.84% systems.
- **MACD.** TradingLab buys crosses *below* zero. Ross wants MACD *positive* (the "front side"). Rayner trusts only the higher-timeframe cross and says lower-timeframe crosses whipsaw in ranges.
- **RSI.** Three uses compete: oversold reversal (Trading 212/Pushkar style), trend filter (RSI(200) > 50), and buy-oversold-in-uptrend (Connors RSI(10)).
- **Stops.** Classic stops sit just beyond the swing (Ross, Data Trader). Rayner and ICT say those are the stops that get hunted: add a 1-ATR buffer, or stop beyond the swept extreme.
- **Fibonacci.** The 61.8% "golden ratio" vs ICT's 0.705.
- **Shorting.** Rules born in forex are symmetric. Rayner says don't short stocks in uptrends.

**Red flags**
1. **Win rate with no payoff, cost or sample size.**
   - TradingLab: 86% with no backtest; replications find 21–48%.
   - Ross: 69% with no average win/loss.
   - Data Trader: "Proven 100x", yet the rule barely fires.
   - Rayner CP-2: 89% at 2.13%/yr. With 36 trades the 95% confidence interval is about ±10 pp.
2. **Inconsistent numbers.** The same RSI(10) rule is reported as 88.89% / 36 trades and as 86.84% / 38 trades. One page gives the BB system's win rate as both 94% and 66%.
3. **Hindsight selection.**
   - Trading Rush drew its "good/bad market" boxes after the fact.
   - The Trading Channel teaches "optimizing a portfolio" by keeping the pairs that tested well.
   - Order blocks are "drawn back on the earlier candle as though it had been known", and tools delete failed zones.
   - In the placebo-controlled test, FVGs showed no edge over size-matched random zones.
4. **Admitted cherry-picking.** "(Duh, I cherry-picked this chart.)" (Rayner). Ross's case study is the day's +200% top gainer.
5. **Unfalsifiable framing.** In ICT's "algorithm/smart money" story, any failed level becomes "manipulation" or an "inducement". No failure condition is ever stated.
6. **Income claims, survivorship and sales incentives.** TJR +$1 M, Craig $30k/month, Brad Goh $2.5 M, JeaFx "$24m+", Ross $2k → $65k: none is audited, and channels that failed are not in the top 300. Nearly every channel sells courses, signals, indicators or referrals, and titles promise totality ("The Only … You Will Ever Need").
7. **Transfer risk.** Most claimed numbers come from intraday forex, crypto or futures. The daily stock systems that do exist (Rayner's) are long-published Connors rules whose edge may have decayed.

**Bottom line for the rulebook.** A signal "exists", for these creators, when trend, level and trigger align. They say "no trade" in these cases:
- chop;
- price extended from its mean;
- breakouts without a buildup or volume;
- just before news or earnings;
- outside the session windows;
- no defined invalidation point.

These conditions are testable (H-YT-1, 11, 12, 16, 21, 24, 25). The headline win rates are not credible as stated.
