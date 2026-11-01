# 06 — Modern Technical-Analysis Canon: Survey of Rules, Stay-Out Conditions, and Testable Hypotheses

**Purpose.** This file pulls the concrete, operational rules out of the modern technical-analysis canon so the trading agent's rulebook can say (a) when a signal *exists*, and (b) when a signal does **not** exist, meaning stay out or no-signal. Each school gets core beliefs, entry rules, exit/stop rules, explicit stay-out conditions, and numbered hypotheses (`H-<SCHOOL>-n`) that can be tested on **daily OHLCV** data.

**Sources and their limits.** No pirated full texts were used. The sources are author websites (thepatternsite.com, bollingerbands.com), StockCharts ChartSchool (raw markdown saved under `scratchpad/web_raw/canon/`), AAII, *Stocks & Commodities* reprints, publisher pages, and named secondary summaries. investors.com, investopedia.com and traders.com could not be fetched from this session, so O'Neil/IBD rules are taken from AAII and secondary write-ups. Each claim carries a reliability tag:

- **[P]** primary: the author's own site or article.
- **[S]** reputable secondary: ChartSchool, AAII, CXO, O'Reilly/Wiley blurbs.
- **[W]** weak secondary: blog, forum or AI-style summary. Treat as unverified.
- **[B]** a standard rule from the book that I could not verify verbatim online in this session.

**Conventions used in every hypothesis.**

- Bars are indexed *t*, with fields O, H, L, C, V. `SMA(x,n)` and `EMA(x,n)` are moving averages. `ADV(n) = SMA(V,n)`. `ATR(n)` uses Wilder smoothing.
- Weekly bars are resampled from daily bars (Friday close). `W-SMA30` ≈ daily `SMA150`.
- A signal is evaluated on the close of day *t*. The fill is at O(t+1) unless the school specifies a close fill.
- Forward return is `R(h) = C(t+h)/O(t+1) − 1`, for h ∈ {1, 5, 10, 20, 60}.
- "Edge" means mean `R(h)` minus the unconditional mean `R(h)` over the same universe and dates. It is also checked against a random-entry baseline with the same holding period. Aronson's critique (§10) requires detrended returns as well.
- "Index" means daily OHLCV for ^GSPC or SPY.
- All hypotheses together form one test family. Promotion needs a multiple-testing correction (§10).

---

## 1. John Murphy — *Technical Analysis of the Financial Markets*

**Core beliefs.** Market action discounts everything. Prices trend, and history rhymes. Analysis runs top-down: longer timeframes set the trend, and shorter ones time the entry. Moving averages *confirm* trends but do not *predict* them. Oscillators work best in trading ranges. Volume should confirm the trend. ([ChartSchool, 10 Laws](https://chartschool.stockcharts.com/table-of-contents/overview/john-murphys-10-laws-of-technical-trading) [S])

**Murphy's 10 Laws of Technical Trading, condensed** [S]:

1. **Map the trends.** Read monthly and weekly charts first, then daily and intraday. Trade with the intermediate and long-term trend.
2. **Spot the trend and go with it.** Buy dips in uptrends and sell rallies in downtrends. The longer chart sets the trend; the shorter chart times the entry.
3. **Find the low and high of it.** Buy near support (a prior reaction low) and sell near resistance (a prior peak). Broken resistance becomes support, and broken support becomes resistance.
4. **Know how far to backtrack.** Pullbacks commonly retrace 50% of the prior move. The minimum is about 1/3 and the maximum about 2/3. Fibonacci 38% and 62% are also watched. The first buy zone in an uptrend pullback is 33–38%.
5. **Draw the line.** A trendline joins two successive lows (or two successive highs). It is valid once touched at least 3 times. A break often signals a trend change, and longer, more-tested lines matter more.
6. **Follow that average.** The 20-day MA is short-term, the 50-day intermediate and the 200-day major. Crossover pairs are 5/20, 20/50 and 50/200. EMAs are preferred for crossovers.
7. **Learn the turns.** RSI(9 or 14) is overbought above 70 and oversold below 30. Stochastics(14) is overbought at 80 and oversold at 20. Divergences warn of turns. These work best in ranges. Weekly signals filter daily signals.
8. **Know the warning signs (MACD, Appel).** Buy when the fast line crosses above the slow line while both are below zero. Sell on a cross down from above zero. Weekly signals take precedence. The histogram warns earlier.
9. **Trend or not a trend (ADX).** A rising ADX means a trending market, which favors moving averages. A falling ADX means a trading market, which favors oscillators.
10. **Know the confirming signs (volume).** Volume should be heavier on up days in an uptrend. Falling volume warns that the trend is ending.

**Additional book rules [B].**

- **3% penetration criterion.** A trendline or support/resistance break counts only after a close beyond it by about 3%. This is mainly for long-term lines.
- **Two-day rule.** Alternatively, require two successive closes beyond the line. This is corroborated by a forum summary ([rava.com](https://foro.rava.com/foro3/viewtopic.php?p=1826711) [W]). ChartSchool gives the same two filter types, a 3% price filter or a 3-day time filter ([ChartSchool double top](https://chartschool.stockcharts.com/table-of-contents/chart-analysis/chart-patterns/double-top-reversal) [S]).

**Entry.** Pullback within a higher-timeframe uptrend into the 33–62% retracement zone or onto support/MA, then a trigger: MA crossover, oscillator turning up from oversold, or MACD cross below zero.
**Exit/stop.** A trendline break confirmed by 3% or by 2 closes. A close below the swing low. An opposite MA cross.
**Stay out.** The weekly trend opposes the daily setup. ADX is falling, so MA-crossover signals should be ignored. ADX is rising, so oscillator reversal signals should be ignored. Volume is not confirming. A retracement deeper than about 2/3 means the trend is suspect.

**Hypotheses (daily OHLCV).**

- **H-MUR-1 (trend alignment).** EMA(5)/EMA(20) bullish crosses earn higher 20-day excess return when C > SMA200 and SMA50 > SMA200 than when either condition fails.
- **H-MUR-2 (penetration filter).** Consider closes beyond a 60-bar high or low. Requiring the close to be ≥3% beyond, *or* two consecutive closes beyond, cuts the false-break rate vs. a 1-close/any-margin break. A false break is a close back inside within 10 bars. The 20-day expectancy should be unchanged or better.
- **H-MUR-3 (retracement zone).** Use uptrends with C > SMA200 and SMA200(t) > SMA200(t−20). Define swings with a 10% zigzag. Pullbacks that retrace 33–62% of the last up-swing, then close above the prior day's high, beat pullbacks that retrace >66% (R20).
- **H-MUR-4 (ADX regime switch).** Compare EMA20/EMA50 cross signals against RSI(14) cross-up-through-30 signals. When ADX(14) > 20 and ADX(t) > ADX(t−5), the crosses outperform. When ADX(14) < 20 and falling, the RSI signals outperform.
- **H-MUR-5 (MACD location).** MACD(12,26,9) bullish signal-line crosses that occur with MACD < 0 outperform crosses with MACD > 0 (R20).
- **H-MUR-6 (volume confirmation).** Over 50 bars, take Σ(V on up days) / Σ(V on down days). A ratio > 1.2 predicts higher R20 than a ratio < 0.8 among stocks with C > SMA50.

---

## 2. Edwards & Magee — *Technical Analysis of Stock Trends*

**Core beliefs [B].** The book is Dow-theory derived. A trend is assumed in force until a definite reversal signal appears. Price "areas" (reversal and consolidation formations) reveal shifts in supply and demand. The formations are head-and-shoulders, double/triple tops and bottoms, rectangles, symmetrical/ascending/descending triangles, flags and pennants ("fly at half-mast"), wedges, and breakaway/runaway/exhaustion gaps. Measuring formulas project the pattern height. Support and resistance swap roles after a break. Bassetti's later editions replace Dow Theory signals with Magee's **basing-points** procedure for progressive stops ([sack.de TOC](https://www.sack.de/edwards-magee-bassetti-technical-analysis-of-stock-trends/9781032241821) [S]).

**Entry rules [B].**

- Act on a **decisive** breakout: a close beyond the boundary, conventionally by about 3%.
- **Upside** breakouts should come on clearly expanded volume. **Downside** breakouts do not need volume.
- Symmetrical-triangle breakouts are most reliable when they occur roughly ½ to ¾ of the way from the base to the apex. Breakouts very near the apex lose potency.
- Return moves (throwbacks or pullbacks) to the broken boundary are common and offer a second entry.

**Exit/stop [B].** Use progressive stops below **basing points**, the lows of successive minor corrections, ratcheted up as the trend makes new highs. Exit on a confirmed opposite-pattern breakout.
**Stay out [B].** A pattern before a decisive close beyond its boundary. An upside break on shrinking volume. A triangle breakout near the apex. No prior trend for a "reversal" pattern to reverse.

Modern corroboration from ChartSchool [S]:

- Head-and-shoulders: "isn't complete … until the neckline support is broken," ideally on expanding volume ([ChartSchool H&S](https://chartschool.stockcharts.com/table-of-contents/chart-analysis/chart-patterns/head-and-shoulders-top)).
- Double tops: peaks within about 3% of each other, a trough ≥10% deep, peaks about a month apart. "Wait for support to be broken" ([ChartSchool double top](https://chartschool.stockcharts.com/table-of-contents/chart-analysis/chart-patterns/double-top-reversal)).
- Flags: need a sharp, high-volume prior move. Duration 1–12 weeks, ideally 1–4 ([ChartSchool flag](https://chartschool.stockcharts.com/table-of-contents/chart-analysis/chart-patterns/flag-pennant)).

**Hypotheses.**

- **H-EM-1 (asymmetric volume).** For closes above a 40–120-bar consolidation high, V ≥ 1.5×ADV50 lowers the Bulkowski 5% break-even failure rate vs. V < ADV50. For downside breaks, the volume effect is smaller and may not be significant.
- **H-EM-2 (apex location).** Symmetrical-triangle breakouts at 50–75% of the base-to-apex distance beat those beyond 75% (R20, failure rate).
- **H-EM-3 (measuring rule).** After an H&S-top neckline close-break, compute target = neckline − (head − neckline). Price reaches it within 60 bars in about 50% of cases (Bulkowski reports 51%; §3).
- **H-EM-4 (basing-point stop).** Define a basing point as a pullback low followed by 3 bars that each make a higher high. A stop 1×ATR(14) below the latest basing point gives back less open profit in trend trades than a fixed 8% stop, with similar or better total return.
- **H-EM-5 (trend persistence).** After a close at a new 252-bar high, P(C(t+60) > C(t)) exceeds the unconditional 60-bar up-probability.

---

## 3. Thomas Bulkowski — *Encyclopedia of Chart Patterns* and thepatternsite.com (statistics)

### 3.1 Definitions behind the numbers (read these before using any statistic)

- **Break-even failure rate** is the share of patterns that fail to move at least 5% in the breakout direction ([glossary](https://thepatternsite.com/glossary.html) [P]).
- **Throwback / pullback** means price returns to the breakout price within 30 days after an up or down breakout.
- **Ultimate high** is the highest peak before a ≥20% decline. **Ultimate low** is the reverse.
- **Average rise / decline** is a "perfect trade": from the open the day after the breakout to the ultimate high or low, with no commissions ([top10](https://thepatternsite.com/top10.html) [P]). These figures are **optimistic upper bounds**, not achievable trade returns.
- **Bull/bear split.** A bear market is the S&P 500 down 20%. Bulkowski's bear windows are 3/24/2000–10/10/2002 and 10/12/2007–3/6/2009.
- **Busted pattern.** After the breakout, price moves ≤10%, then closes beyond the opposite side of the pattern.
- **Performance rank** is out of 39 patterns for up breakouts and 36 for down breakouts (1 = best).

### 3.2 Core chart-pattern statistics (bull market, from each pattern's page)

| Pattern (URL) | Breakout | Perf. rank | BE failure | Avg move | Throwback / pullback | % hit target | N | Notes |
|---|---|---|---|---|---|---|---|---|
| H&S top ([hst](https://thepatternsite.com/hst.html)) | down | 9/36 | 19% | −16% | 68% pullback | 51% | >2,800 | Volume highest on left shoulder; pullbacks hurt |
| H&S bottom ([hsb](https://thepatternsite.com/hsb.html)) | up | 13/39 | 11% | +45% | 65% | 71% | 3,197 | Best after 0–3-month prior decline; throwbacks hurt |
| Double top, Eve & Eve ([eedt](https://thepatternsite.com/eedt.html)) | down | 12/36 | 20% | −16% | 65% | 43% | 942 | **60%** of twin peaks never confirm (no close below valley) |
| Double bottom, Adam & Adam ([aadb](https://thepatternsite.com/aadb.html)) | up | 26/39 | 16% | +39% | 67% | 73% | 1,154 | **48%** chance price keeps falling if bought before confirmation; stop below lower bottom |
| Double bottom, Eve & Eve ([eedb](https://thepatternsite.com/eedb.html)) | up | 5/39 | 12% | +50% | 65% | 65% | 952 | Same 48% pre-confirmation warning |
| Ascending triangle ([at](https://thepatternsite.com/at.html)) | up / down | 16/39 · 30/36 | 17% · 38% | +43% · −13% | 64% · 63% | 70% · 44% | >1,400 | Up breakout 63% of the time; breakout at 64% of the way to apex; 46% of down breakouts bust |
| Descending triangle ([dt](https://thepatternsite.com/dt.html)) | up / down | 33/39 · 15/36 | 22% · 23% | +38% · −15% | 60% · 58% | 64% · 50% | >1,300 | Up 53%; avoid middle third of yearly range; performance "almost in half since the 1990s" |
| Symmetrical triangle ([st](https://thepatternsite.com/st.html)) | up / down | **36/39 · 34/36** | 25% · 37% | +34% · −12% | 62% · 65% | 58% · 36% | >3,000 | Up 60%; breakout at 74% to apex; breakout volume above the 30-day average helps |
| Flag ([flags](https://thepatternsite.com/flags.html)) | up / down | not ranked | **44% · 45%** | +9% · −8% | — | 46% · 46% | "hundreds" | <3 weeks long; tight flags beat loose ones |
| Pennant ([pennants](https://thepatternsite.com/pennants.html)) | up / down | n/a | **54% · 54%** | +7% · −6% | — | 35% · 32% | >1,600 | Half-staff (equal legs) works only 30% of the time |
| High & tight flag ([htf](https://thepatternsite.com/htf.html)) | up | 30/39 | 15% | +39% | 67% | 82% (half-height) | 1,028 | Needs a ≥90% rise in ≤2 months; buy only on close above highest peak |
| Cup with handle ([cup](https://thepatternsite.com/cup.html)) | up | **3/39** | **5%** | +54% | 62% | 61% | 913 | Cup 7–65 weeks; stop at handle low; handles shorter than the 22-day median do better. In a study of 300 cups (1990–Mar 2024), 47% "dropped substantially" within 2 months of breakout |
| Rectangle top ([recttops](https://thepatternsite.com/recttops.html)) | up / down | 4/39 · 32/36 | 15% · 34% | +51% · −13% | 66% · 64% | 78% · 54% | >1,000 | Up 63%; partial rise predicts down breakout 75% of the time |
| Rectangle bottom ([rectbots](https://thepatternsite.com/rectbots.html)) | up / down | 8/39 · 14/36 | 15% · 24% | +48% · −16% | 64% · 66% | 79% · 55% | >900 | Up 59%; needs ≥5 touches; tall rectangles beat short ones |

Failure *ranks* from [id75](https://thepatternsite.com/id75.html) [P], in the order performance/failure:

- Cup with handle 3/2
- H&S bottom 13/10
- H&S top 9/10
- Eve & Eve double bottom 5/13
- Symmetrical triangle up 36/36 (worst on both)
- Rectangle top up 4/23

### 3.3 Decay over decades, stress periods, and realistic horizons

- **Decay** ([TimePerformance](https://thepatternsite.com/TimePerformance.html) [P]). Average rise to the ultimate high, 1990s → 2000s → 2010s:
  - flags 14% → 12% → **6%**
  - pennants 10% → 7% → **4%**
  - descending triangle up 51% → 37% → 27%
  - symmetrical triangle up 41% → 38% → 29%
  - cup with handle 49% → 54% → 55% (stable; 2010s rank 6 of 56)
  - Medians are far below averages (e.g., HSB median 23% in the 2010s vs. a 44% average), so the distributions are right-skewed.
- **Failure-rate study** ([FailureRates](https://thepatternsite.com/FailureRates.html) [P]). Covers 13,932 patterns of 23 types, 1991–2008. Patterns "fail between two and four times more often now than they did in the past."
  - The upward 10%-failure rate rose from 11% (1991) to 44% (2007).
  - In the 2008 bear market, only 12% of upward-breakout patterns gained ≥40%, vs. 60% in 2000.
  - Downward-breakout 10% failures jumped from 15% to 48% in the 2002→2003 bear-to-bull transition: "you do not want to be short when the bear market ends."
- **Realistic 1–3-month returns** ([BestPatterns](https://www.thepatternsite.com/BestPatterns.html) [P], >30,000 samples, data from 2021, flagged by the author as outdated). Gain after 2 months:
  - high & tight flag +21%
  - Eve & Eve double bottom +12%
  - rectangle bottom +11%
  - flag +9%
  - H&S top −8%
  - Cup with handle ranked 11th.
- **Breakout volume** ([volbkout](https://www.thepatternsite.com/volbkout.html) [P]). "Heavy" means breakout-day volume above the 30-day average. In bull markets, 26 up-breakout patterns prefer heavy volume, 7 prefer light volume (including high & tight flag), and 5 show no preference (including cup with handle). Volume is therefore **not** a universal confirmer.
- **Busted patterns** ([Busted](https://thepatternsite.com/Busted.html) [P]). "The move is often stronger from a failed chart pattern than from one that works." Busted triple tops (bull market, N=145) rose an average 42%.
- **Weinstein stages tested by Bulkowski** ([Stages](https://www.thepatternsite.com/Stages.html) [P]). Sample of 440 buys and 444 sales, Apr 1987–Feb 2010:

  | Buy in stage | Avg gain | % profitable | N |
  |---|---|---|---|
  | 1 | +13.2% | 69.3% | 127 |
  | 2 | +4.1% | 56.9% | 116 |
  | 3 | −5.9% | 14.5% | 69 |
  | 4 | −8.3% | 24.4% | 127 |

  Best combination: buy in Stage 1 and sell in Stage 2, +25.9% (N=62).

### 3.4 Candlestick statistics (*Encyclopedia of Candlestick Charts*)

- **Method.** More than 100 candle types tested on 4.7 million daily candle lines. Price change is measured from the close of the pattern day 1, 3, 5 and 10 days ahead. The overall rank sums these across bull/bear markets and up/down breakouts ([S&C reprint](https://www.fidelity.com/bin-public/060_www_fidelity_com/documents/Top10CandlesWork_620095.pdf) [P]; [glossary](https://thepatternsite.com/glossary.html)). Many top performers are rare (e.g., bullish abandoned baby: 293 occurrences in 4.7M lines). Bulkowski: "more samples will show that the rare candle patterns won't perform as well."
- **Top 10 overall** ([CandlePerformers](https://thepatternsite.com/CandlePerformers.html) [P]):
  1. bearish three-line strike (84% bullish reversal)
  2. bullish three-line strike (65% bearish reversal)
  3. three black crows (78%)
  4. evening star (72%)
  5. upside tasuki gap (57% continuation)
  6. inverted hammer (65% bearish continuation)
  7. matching low (61%)
  8. bullish abandoned baby (70%)
  9. two black gapping (68%)
  10. bearish breakaway (63%)
- **Top reversal rates** ([CandleReverse](https://thepatternsite.com/CandleReverse.html)): three stars in the south 86%, bearish three-line strike 84%, three white soldiers 82%, identical three crows 79%, bearish engulfing 79%, morning star 78%.
- **Top continuation rates** ([CandleContinue](https://thepatternsite.com/CandleContinue.html)): mat hold 78%, rising three methods 74%.
- **Common candles are near-random.**
  - Hammer: bullish reversal 60% of the time, "not far from random (50%)"; overall rank 65/103 ([Hammer](https://thepatternsite.com/Hammer.html)).
  - Bullish engulfing: 63% reversal but overall rank **84/103**. Post-breakout performance "can be dreadful." Avoid it in a downward primary trend ([BullEngulfing](https://thepatternsite.com/BullEngulfing.html)).
  - Bearish engulfing: 79% reversal but overall rank **91/103** ([BearEngulfing](https://thepatternsite.com/BearEngulfing.html)).
  - Lesson: a high "reversal %" (direction of the next close-break) does not mean a large move.
- **Context tips** ([CandleTips](https://thepatternsite.com/CandleTips.html)). "Bullish candles perform much better in a primary uptrend." Trade bearish candles only in downtrends.

### 3.5 Rules and stay-out conditions derived from Bulkowski

**Entry rules.** Wait for confirmation, defined as a close beyond the pattern boundary. Prefer cup-with-handle, rectangles, H&S bottoms, Eve & Eve double bottoms and bump-and-run bottoms. Prefer breakouts in the lower or upper third of the yearly range. Prefer a short prior trend.
**Stops.** Just beyond the opposite side of the pattern: below the lower bottom, the handle low, or the lower trendline.
**Stay out.**

- Before confirmation: 48–60% of candidates never confirm.
- Flags and pennants on daily stock data: 44–54% failure and 4–9% average moves, which are thin after costs.
- Symmetrical triangles: worst-ranked pattern.
- Breakouts in the middle third of the 52-week range.
- Loose or jagged flags.
- Rare candles with too few samples.
- Bullish candles in a primary downtrend.
- Shorting into the end of a bear market.

**Hypotheses.**

- **H-BUL-1 (confirmation).** Define a double bottom as two lows within 4% of each other, 10–60 bars apart, with a ≥10% rally between them. Entering on the close above the intervening peak beats entering at the second low (expectancy per trade, stop below the lower low). The share of candidates that never confirm within 60 bars is 45–60%.
- **H-BUL-2 (rank replication, out of sample 2010–2025).** The 5% break-even failure rate of up-breakouts is lower for cup-with-handle and rectangles than for symmetrical triangles, which in turn is lower than for flags and pennants.
- **H-BUL-3 (decay).** The median 60-bar post-breakout return for each pattern class is lower in 2015–2025 than in 1995–2005.
- **H-BUL-4 (throwbacks hurt).** Up-breakouts that return to the breakout price within 30 bars have a lower R60 than those that do not. Condition only on information available at the throwback date to avoid look-ahead.
- **H-BUL-5 (yearly-range location).** Breakouts in the top or bottom third of the 252-bar range beat middle-third breakouts (R20).
- **H-BUL-6 (bust trade).** Take an up-breakout that moves ≤10% and then closes below the pattern low. A short entered on that close earns a larger R20 decline than the pattern's average down-breakout.
- **H-BUL-7 (candles near random).** Hammer, bullish/bearish engulfing and doji show no FDR-significant R10 excess. Bullish candles show positive excess only when C > SMA200 and SMA200 is rising.
- **H-BUL-8 (stage timing).** Buys in Stage 1, or Stage 2 within 10% above the base breakout, beat buys in Stages 3–4 (R60). Stages are defined as in §5.

---

## 4. Steve Nison — *Japanese Candlestick Charting Techniques*

**Core beliefs.** Candles show shifts in market direction early, but they give poor price targets. Use Western support/resistance for targets ([Shortform summary](https://www.shortform.com/summary/japanese-candlestick-charting-techniques-summary-steve-nison) [W]). A "reversal" pattern means the prior trend *may change*, often into sideways action, not necessarily that it will reverse. Patterns must be read against the prior trend and support/resistance, including the polarity principle. Candles complement Western tools; they do not replace them.

**Entry rules** (ChartSchool, which cites Nison [S]; [bullish reversals](https://chartschool.stockcharts.com/table-of-contents/chart-analysis/candlestick-charts/candlestick-bullish-reversal-patterns)):

- **A prior downtrend is required.** Tests: C < EMA20, lower highs and lows, or below a trendline.
- **Confirmation within 1–3 days**: a gap up, a long white candle, or a high-volume advance. Without it the pattern is neutral, at best a potential support level. The exception is the abandoned baby.
- **Definitions.**
  - Hammer: lower shadow ≥2× body, little or no upper shadow, and a range that is large vs. the prior 10–20 bars.
  - Piercing: closes above the midpoint of the prior black body.
  - Engulfing: the second body engulfs the first; the first is not a doji.
  - Morning star: long black, small gapped body, long white.
- The strongest signals add support, a positive oscillator divergence, and buying pressure (OBV/CMF).

**Exit/stop [B].** Use the extreme of the signal pattern, e.g., the hammer's low, as the stop. A close beyond it negates the signal.
**Stay out.** No preceding trend. The pattern sits in the middle of a range. No confirmation within 3 bars. Bullish candles in a primary downtrend (Bulkowski). Doji-labelling of near-doji bars. The candle offers poor risk/reward vs. nearby resistance.

**Hypotheses.**

- **H-NIS-1 (confirmation).** Define a hammer as: lower shadow ≥ 2× body; upper shadow ≤ 0.1× range; range ≥ ATR(14); C < EMA20; C(t) < C(t−10). Hammers confirmed by a close above the hammer high within 3 bars beat unconfirmed hammers (R10 from the confirmation bar vs. from the hammer bar).
- **H-NIS-2 (at support).** Bullish reversal candles within 1×ATR(14) of the 50-bar low or SMA200 beat the same candles elsewhere (R10).
- **H-NIS-3 (reversal = stall).** After a bearish engulfing in an uptrend (C > SMA50 and SMA50 rising), the 10-bar realized range contracts relative to the prior 10 bars more often than R10 < −5% occurs. Test the frequency against the unconditional base rate.
- **H-NIS-4 (trendless candles).** Candles that appear when |C(t)/C(t−10) − 1| < 1×ATR(14)/C carry zero R10 edge.

---

## 5. Stan Weinstein — *Secrets for Profiting in Bull and Bear Markets*

**Core beliefs.** Every stock cycles through four stages read from the weekly chart and the **30-week MA** ([LuxAlgo](https://www.luxalgo.com/library/concept/weinstein-stage-analysis/) [W]; [Bulkowski Stages](https://www.thepatternsite.com/Stages.html) [P]):

1. Base: flat MA, sideways range.
2. Advance: breakout, then a rising MA with price above it. "Stage 2 is the ideal time to buy."
3. Top: MA flattens, price crosses it, swings get wide. Take profits or sell half.
4. Decline: price below a falling MA. Volume on the decline is not a reliable signal.

Analysis runs top-down: market → sector → stock. Relative strength is measured with **Mansfield RS** = (stock/index ratio ÷ its 52-week average − 1)×100. A buy wants RS > 0 or turning positive ([LuxAlgo](https://www.luxalgo.com/library/concept/weinstein-stage-analysis/) [W]).

**Entry.** A weekly close above Stage-1 resistance with the 30-week MA flattening or turning up, **breakout volume at least ~2× the recent weekly average** (commonly "2× the prior 4 weeks" [B]; secondary sources say "previous few weeks"), and RS positive or improving. Little overhead resistance. A second chance comes on a pullback toward the breakout level.
**Exit/stop [B].** Initial stop below the base low or the last significant correction low. Once in Stage 2, trail it below the rising 30-week MA and successive higher lows. Sell, or sell half, when Stage 3 develops. Short on a Stage-4 breakdown (volume not required). Short candidates need negative RS.
**Stay out.** Never buy below a declining 30-week MA (Stage 4). Never short above a rising one. Do not buy Stage 1 or Stage 3 ranges. "Stand aside in between" stages. Avoid breakouts into nearby overhead supply. Avoid breakouts while the market itself is in Stage 4.

**Hypotheses.** Weekly bars are built from daily data; MRS = Mansfield RS vs. SPY.

- **H-WEI-1 (full breakout spec).** Signal: weekly close > max(H) of the prior 10–30 weeks; W-SMA30 slope over 4 weeks ≥ 0; weekly V ≥ 2× mean of the prior 4 weeks; MRS > 0. These beat breakouts missing the volume or RS condition (R60, 5% failure rate).
- **H-WEI-2 (Stage 4 is no-signal).** Stocks with C < W-SMA30 and W-SMA30 falling over 4 weeks have negative 13-week excess return vs. SPY. Long setups of any kind in this state have lower expectancy.
- **H-WEI-3 (MA trail).** Exiting on a weekly close below W-SMA30 beats a fixed 8% stop on CAGR and on profit give-back for Stage-2 entries.
- **H-WEI-4 (overhead supply).** Breakouts whose 504-bar high lies 0–10% above the breakout price underperform breakouts at new 504-bar highs (R60).
- **H-WEI-5 (market stage).** Stage-2 stock breakouts taken while SPY is above a rising W-SMA30 beat those taken while SPY is in Stage 4.

---

## 6. William O'Neil — *How to Make Money in Stocks* (technical side of CAN SLIM)

**Core beliefs.** Buy leaders emerging from sound bases near new highs, on heavy volume, and only during confirmed market uptrends. Cut losses mechanically. "Stocks that seem too high-priced … often go even higher" ([AAII](https://www.aaii.com/files/journal/pdf/9874_william-oneil-can-slim-approach-to-selecting-growth-stocks.pdf) [S]).

**Entry rules.**

- **Base: cup with handle.**
  - Prior uptrend of about 30% or more.
  - U-shaped cup, depth 12–33% (deeper in bear markets), base at least about 7 weeks.
  - Handle ≥1 week, in the upper half of the base, drifting down on contracting volume, not deeper than the low teens.
  - Pivot just above the handle high; O'Neil used +$0.10.
  - Sources: [LuxAlgo](https://www.luxalgo.com/library/concept/cup-with-handle-base/) [W]; [ChartSchool](https://chartschool.stockcharts.com/table-of-contents/chart-analysis/chart-patterns/cup-with-handle) [S], which places the cup's invention in the 1988 book. Bulkowski's own spec is cup 7–65 weeks ([cup](https://thepatternsite.com/cup.html)).
- **Breakout volume about 40–50%+ above average** [W].
- Buy within a few percent of the pivot. The 5% "buy zone" is widely cited [B].
- **RS rank ≥80; avoid stocks below 70.** From 1950 to 2008 the best performers averaged RS 87 before their big moves ([AAII](https://www.aaii.com/files/journal/pdf/9874_william-oneil-can-slim-approach-to-selecting-growth-stocks.pdf) [S]).
- **Market direction (M).**
  - **Follow-through day (FTD)**: day 4 or later of a rally attempt, the index up ≥1% (original rule), 1.7% (mid-2000s IBD) or about 1.25% (recent IBD), on volume above the prior day ([LuxAlgo FTD](https://www.luxalgo.com/library/concept/follow-through-day/) [W]).
  - **Distribution day**: the index down ≥0.2% on volume above the prior day. Each one counts for 25 sessions, or until the index rallies 5% above that day's close. Four to six in the window flags a top ([LuxAlgo DD](https://www.luxalgo.com/library/concept/distribution-days/) [W]).

**Exit/stop.**

- Sell if the stock falls **7–8% below the purchase price**. Do not raise this level as the stock rises.
- Take **20–25% profits**, making "a 3-to-1 profit-to-loss ratio."
- Wait at least 13 weeks before concluding a stock is not advancing properly ([AAII](https://www.aaii.com/files/journal/pdf/9874_william-oneil-can-slim-approach-to-selecting-growth-stocks.pdf) [S]).
- **8-week hold rule**: a stock that gains ≥20% within ≤3 weeks of breakout is held at least 8 weeks, in uptrending markets only ([TraderLion](https://traderlion.com/trading-strategies/the-8-week-hold-rule/) [W]).
- Go about 25% into cash when the market peaks.

**Stay out.**

- No confirmed uptrend: no FTD since the correction low, or a cluster of distribution days.
- Stocks with RS < 70.
- V-shaped cups.
- Handles in the lower half of the base or rising handles.
- Breakouts on light volume.
- Price more than about 5% above the pivot.
- "Buying stocks on the way down" or laggards and sympathy plays.

**Evidence caveat.** IBD has cited a 70–80% FTD success rate. Rob Hanna's 2008 Quantifiable Edges study of S&P 500 FTDs since 1971 found success near a coin flip. IBD's claim is that no major rally began without an FTD ([LuxAlgo](https://www.luxalgo.com/library/concept/follow-through-day/) [W]). An FTD is permission to buy, not a buy signal.

**Hypotheses.** RS proxy = 12-month return with the latest quarter double-weighted, ranked as a percentile across the universe.

- **H-ONL-1 (breakout volume).** Cup-with-handle breakouts per the spec above with V ≥ 1.4×ADV50 beat those with V < ADV50: higher R20/R60 and lower rate of hitting a −8% stop first.
- **H-ONL-2 (chasing).** Entries ≤5% above the pivot have higher expectancy than entries 5–10% above it.
- **H-ONL-3 (3:1 rule × regime).** A −8% stop with a +20% target (whichever hits first, 60-bar cap) has positive expectancy only when the market is in a "confirmed uptrend": an FTD has occurred and there are fewer than 5 distribution days in the last 25 sessions.
- **H-ONL-4 (FTD value).** SPY R60 after an FTD (day ≥ 4, +≥1.25%, V > V(t−1)) exceeds unconditional R60. The failure rate (index undercuts the rally low within 20 bars) is ≥40%.
- **H-ONL-5 (distribution clusters).** When ≥5 distribution days occur in 25 sessions, SPY R20 is lower and stock-breakout 5% failure rates are higher.
- **H-ONL-6 (RS filter).** Breakouts with an RS proxy ≥ 80 beat those with RS < 70 (R60).

---

## 7. Mark Minervini — *Trade Like a Stock Market Wizard*

**Core beliefs.** Trade only Stage-2 leaders: SEPA combines trend, fundamentals, catalyst and a precise entry point. Volatility contraction precedes major advances. Losses are geometric, so cut them small.

**Trend Template — all 8 criteria, as quoted from the book** ([EliteTrader thread](https://elitetrader.com/et/threads/mark-minervinis-trend-template-question.359356/post-5400734) [W, verbatim quotes]):

1. The current stock price is above both the 150-day (30-week) and the 200-day (40-week) moving average.
2. The 150-day MA is above the 200-day MA.
3. The 200-day MA is trending up for at least 1 month (preferably 4–5 months minimum in most cases).
4. The 50-day (10-week) MA is above both the 150-day and the 200-day MA.
5. The current stock price is trading above the 50-day MA.
6. The current stock price is at least 30% above its 52-week low. Many of the best selections are 100%, 300% or more above it.
7. The current stock price is within at least 25% of its 52-week high; the closer the better.
8. The relative strength ranking (IBD) is no less than 70, preferably in the 80s or 90s.

**VCP (volatility contraction pattern)** ([finermarketpoints](https://www.finermarketpoints.com/post/trade-like-stock-market-wizard-vcp-chapter) [W]):

- 2–3+ contractions, each about half the depth of the prior one, e.g., ~20–25% → 10–15% → 3–8%.
- Volume declines with each contraction and dries up in the last one.
- Pivot = high of the final tight contraction.
- Base about 4–12 weeks.
- Breakout volume about 40–50%+ above average.
- Entries within 5% of the pivot are favored.

**Exit/stop.**

- Stop just below the final contraction low.
- An "absolute maximum line in the sand" of **10%**; the average loss should be "much less" ([Substack summary](https://tradingresourcehub.substack.com/p/maths-of-trading-and-crunching-numbers) [W]). Secondary sources give a 7–8% working stop and a 45–50% win rate with 20–30% average winners ([finermarketpoints](https://www.finermarketpoints.com/post/3-key-lessons-from-trade-like-a-stock-market-wizard) [W]).
- Take partial profits around 20–25%. Trail the rest with the 10-day MA or a 15–20% trailing stop.

**Stay out.** Any Trend Template criterion fails (Stage 1, 3 or 4). Loose, wide bases. No volume dry-up. Price extended more than 5–10% beyond the pivot. Repeated 10% stops being hit, which per Minervini means a poor environment or poor entries.

**Hypotheses.**

- **H-MIN-1 (template).** Stocks passing criteria 1–7 plus an RS proxy ≥ 70 (with "rising ≥1 month" = SMA200(t) > SMA200(t−21)) have positive 63-bar excess return. Failing stocks have lower excess.
- **H-MIN-2 (ablation).** Removing each criterion in turn identifies which ones carry the edge. Prediction: criteria 3, 7 and 8 matter most; criterion 6 matters least.
- **H-MIN-3 (VCP).** Signal requires:
  - ≥2 successive pullbacks, each with depth ≤ 0.6× the previous one;
  - final pullback ≤ 10% deep;
  - ADV10 during the final pullback < 0.7×ADV50;
  - close above the final-contraction high with V ≥ 1.5×ADV50.
  These beat generic 252-bar-high breakouts that pass the template (R20/R60, failure rate).
- **H-MIN-4 (loss truncation).** Stop = max(final-contraction low, entry × 0.90). Realized average loss is ≤7%, and expectancy stays > 0 even at a ≤50% win rate.

---

## 8. Alexander Elder — *Trading for a Living*

**Core beliefs.** Trading rests on psychology, method and money, and money management is the survival rule. Look at multiple timeframes, with the higher one about 5× the trading timeframe. Volume measures commitment ([ChartSchool Force Index](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/force-index) [S]).

**Triple Screen** (secondary [W], e.g. the [TakeProfit summary](https://takeprofitapp.com/en/learn/triple-screen-trading-system)):

1. **Screen 1, weekly trend.** The slope of the weekly MACD-Histogram, or a weekly EMA. Trade only in that direction.
2. **Screen 2, daily oscillator against the trend.** Buy weakness in a weekly uptrend: Force Index(2) < 0, Elder-ray Bear Power < 0 but rising, or Stochastic/Williams %R oversold.
3. **Screen 3, entry.** A trailing buy-stop one tick above the prior day's high, moved down each day until filled or the weekly trend turns.

**Indicators.**

- **Force Index** = (C − C(t−1))×V. Use a 13-EMA for trend and a 2-EMA for correction timing. Elder recommends a 22-day EMA for trend plus a 2-day Force Index for pullbacks ([ChartSchool](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/force-index) [S]).
- **Elder-ray.** Bull Power = H − EMA13 and Bear Power = L − EMA13. Trade only in the direction of the EMA13 slope. Buy when Bear Power < 0 with a bullish divergence; short when Bull Power > 0 with a bearish divergence ([IncredibleCharts](https://www.incrediblecharts.com/indicators/elder_ray_index.php) [S]).
- **Impulse System.** Green = EMA13 rising and MACD-H(12,26,9) rising. Red = both falling. Blue = mixed. The long-term trend uses a 65-day EMA (5×13). "Enter cautiously but exit fast" ([ChartSchool Impulse](https://chartschool.stockcharts.com/table-of-contents/chart-analysis/chart-types/elder-impulse-system) [S]).
- **Chandelier Exit**, featured in Elder's books: 22-day high − 3×ATR(22) ([ChartSchool](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/chandelier-exit) [S]).

**Money rules.**

- **2% rule**: never risk more than 2% of equity on one trade.
- **6% rule**: "never lose more than 6 percent of your capital in any one month." Count open risk as (price − stop)×shares plus slippage. Stop opening new trades once the 6% is reached ([IncredibleCharts](https://www.incrediblecharts.com/trading/6_percent_rule.php) [S]).

**Stay out.** Daily setups against the weekly screen. Long entries on red Impulse bars, and shorts on green. A trade whose stop distance needs more than 2% equity risk at minimum size. Any new trade once monthly losses plus open risk reach 6%.

**Hypotheses.**

- **H-ELD-1 (triple screen).** Setup: weekly MACD-H(t) > MACD-H(t−1) and daily EMA2(Force Index) < 0. Entry: buy-stop at H(t)+0.01 on following days. Initial stop: the low of the entry bar or the prior bar. These trades beat the same daily setups taken without the weekly filter.
- **H-ELD-2 (impulse veto).** Adding "no long entry on a red Impulse bar" to a breakout system raises expectancy and cuts the stop-out rate.
- **H-ELD-3 (Elder-ray).** EMA13 rising, Bear Power < 0, and Bear Power(t) > Bear Power(t−1) predicts positive R10 excess.
- **H-ELD-4 (risk rules).** For a fixed signal set, 2% risk sizing plus a 6% monthly circuit-breaker reduces max drawdown vs. sizing without the breaker, at a CAGR cost of ≤10% relative.

---

## 9. Indicator Originators — Wilder (RSI, ADX, ATR, Parabolic SAR), Bollinger, Appel (MACD), Lane (Stochastics)

### Wilder — *New Concepts in Technical Trading Systems* (1978)

ChartSchool pages: [RSI](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/relative-strength-index-rsi), [ADX](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/average-directional-index-adx), [ATR](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/average-true-range-atr), [Parabolic SAR](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/parabolic-sar) [S].

- **RSI(14).** Overbought >70, oversold <30. Signals come from divergences and **failure swings**. A bullish failure swing is: RSI goes below 30, bounces, pulls back while holding above 30, then breaks its prior high.
  - Overbought/oversold "work best when prices move sideways within a range." Divergences "are misleading in a strong trend."
  - Constance Brown's ranges: RSI holds 40–90 in bull markets (40–50 acts as support) and 10–60 in bear markets.
  - Wilder smoothing needs about 250 bars to converge.
- **ADX(14) / DMI.** ADX > 25 means a strong trend; ADX < 20 means no trend; 20–25 is a gray zone, and many use 20.
  - System: with ADX > 25, buy when +DI crosses above −DI. The initial stop is the signal day's low, and the signal stays valid while that low holds. Sell signals mirror this, with the signal day's high as the stop.
  - ADX needs about 150 bars to stabilize and "tends to filter as many good signals as bad."
- **ATR.** Default 14; Wilder often used 8. It measures volatility, not direction.
- **Parabolic SAR.** Acceleration factor starts at 0.02, steps +0.02 per new extreme, and caps at 0.20. It works best in trends and whipsaws in ranges.
- **Stay out.** RSI reversal trades when ADX > 25. DMI crosses when ADX < 20. PSAR in ranges. Indicator values computed on fewer than 150 bars of history.

### John Bollinger — Bollinger Bands

Bollinger's 22 rules ([bollingerbands.com](https://www.bollingerbands.com/bollinger-band-rules) [P]):

- Defaults are 20 periods and 2 SD. Use 10/1.9 or 50/2.1 for shorter or longer settings.
- **"Tags are not signals."** A touch of the upper band is not a sell, and a touch of the lower band is not a buy.
- **A close outside the bands is initially a continuation**, not a reversal.
- Price can "walk the band" in strong trends.
- Pair the bands with a *volume* indicator rather than another momentum indicator.
- About 90% of prices fall inside the default bands, not 95%.
- %b gives the position within the bands. BandWidth identifies **the Squeeze**.

Rules from ChartSchool:

- **Squeeze**: BandWidth near the low of its 6-month range, then a band break. The squeeze is direction-neutral. Confirm with S/R breaks and volume indicators (A/D, CMF, MFI, OBV); "unconfirmed band breaks are subject to failure" ([ChartSchool squeeze](https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/bollinger-band-squeeze) [S]).
- **%b with MFI(10)**: an uptrend begins when %b > 0.8 and MFI(10) > 80; a downtrend when %b < 0.2 and MFI(10) < 20. Treat %b < 0 as oversold only inside a bigger uptrend ([ChartSchool %B](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/b-indicator) [S]).

### Gerald Appel — MACD

- MACD = EMA12 − EMA26, signal line = EMA9 of MACD, histogram = the difference.
- Signals: signal-line crosses, zero-line crosses and divergences. MACD is unbounded, so it is not used for overbought/oversold. Crosses at extremes are suspect ([ChartSchool MACD](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/macd-moving-average-convergence-divergence-oscillator) [S]).
- Murphy's rule (§1): buy crosses below zero; weekly signals take precedence.

### George Lane — Stochastics

- %K(14) with %D = SMA3. 80/20 thresholds.
- Lane: a %D divergence is the "only signal which will cause you to buy or sell."
- Bull/bear **set-ups**: price makes a lower high while the oscillator makes a higher high, which anticipates a tradable low.
- Confirm a divergence with a %K/%D cross, a move back through 20/80, a cross of 50, and a price S/R break.
- Overbought readings in uptrends are strength, not a sell signal ([ChartSchool Stochastic](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/stochastic-oscillator-fast-slow-and-full) [S]).

**Hypotheses.**

- **H-WIL-1.** RSI(14) cross-up-through-30 earns positive R10 excess when ADX(14) < 20. When ADX > 25 and −DI > +DI, the excess is ≤ 0.
- **H-WIL-2.** +DI/−DI bullish crosses with ADX > 25, exited on a close below the signal-bar low or after 20 bars, beat the same crosses with ADX < 20.
- **H-WIL-3.** Bullish RSI(14) failure swings beat plain RSI < 30 crosses (R10).
- **H-WIL-4.** As a trailing exit, PSAR(0.02, 0.20) beats a 20-bar time exit when ADX > 25 at entry and underperforms when ADX < 20.
- **H-BOL-1 (tags not signals).** After C > upper BB(20,2), R5 and R10 are ≥ the unconditional mean. Shorting upper-band closes has negative expectancy.
- **H-BOL-2 (squeeze).** Signal: BandWidth(20,2) at or below its 125-bar minimum, then a close outside a band. |R20| exceeds the unconditional |R20|. Direction is ~50% accurate unless CMF(20) agrees in sign, in which case accuracy is > 55%.
- **H-BOL-3 (%b in context).** %b < 0 with C > SMA50 and SMA50 rising gives positive R5. %b < 0 with SMA50 falling gives no edge.
- **H-APP-1.** A MACD-histogram upturn below zero precedes the MACD signal-line cross by ≥1 bar, with equal or better R20 expectancy.
- **H-LAN-1.** Stochastic(14,3,3) bullish divergences confirmed by %D > 50 beat raw %K < 20 cross-ups. A divergence here means a price lower low and a %D higher low, with the first low below 20.

---

## 10. David Aronson — *Evidence-Based Technical Analysis* (2007) — the critical filter

**What was tested.** **6,402** simple rules were back-tested on the **S&P 500, Nov 1, 1980 – Jul 1, 2005**. The rules covered trend-following, extreme-value/reversal and divergence families. Inputs were price plus market-breadth, volume and rate series: OBV, accumulation-distribution volume, money flow, negative/positive volume index, advance-decline ratio, net volume ratio, new highs–lows ratio, debt prices and interest-rate spreads. Sources: [O'Reilly Ch. 8 description](https://www.oreilly.com/library/view/evidence-based-technical-analysis/9780470008744/xhtml/Chapter08.html) [S]; [CXO review](https://www.cxoadvisory.com/technical-trading/evidence-based-technical-analysis-applying-the-scientific-method-and-statistical-inference-to-trading-signals-chapter-by-chapter-review) [S].

**Method.**

- Returns were benchmarked against **detrended** S&P 500 daily returns. This removes the false credit a long-biased rule earns from market drift (position bias).
- Data-mining bias was controlled with an **enhanced version of White's Reality Check** and **Masters' Monte Carlo permutation method**. Both are compute-intensive tests of whether the *best* of N rules beats the null once the search itself is accounted for.

**Result.** "None of the 6,402 rules tested on the S&P 500 index" showed statistically significant outperformance after adjusting for data-mining bias ([CXO](https://www.cxoadvisory.com/technical-trading/evidence-based-technical-analysis-applying-the-scientific-method-and-statistical-inference-to-trading-signals-chapter-by-chapter-review) [S]). One review reports that the best rules showed more than 10% annualized in-sample returns but **p > 0.8** after correction ([EarnForex review](https://www.earnforex.com/guides/book-review-evidence-based-technical-analysis-by-david-aronson/) [W]). Aronson's framing: the historical performance of the best rule is upwardly biased, "a combined effect of randomness and data mining" ([Wiley](https://www.wiley-vch.de/en/areas-interest/finance-economics-law/evidence-based-technical-analysis-978-0-470-00874-4) [S]).

**Factors that determine data-mining bias** (Ch. 6, via CXO):

- More rules tested increases the bias.
- A larger sample decreases it.
- Higher correlation among rules decreases it.
- More outliers increase it.
- Greater variation of returns across rules decreases it.

**Related literature.** Sullivan, Timmermann and White's bootstrap study gives the probability that the best rule did *not* beat the benchmark on S&P 500 futures 1987–1996 as nearly 12%, i.e. not significant ([FMG DP303](https://www.fmg.ac.uk/sites/default/files/2020-11/dp303.pdf), search summary [W]).

**Rulebook implications.** No single-indicator rule from §§1–9 or §§11–12 should be trusted on its in-sample p-value. The default answer for any untested rule is **"no signal."**

**Hypotheses (meta-rules for this rulebook).**

- **H-ARO-1 (family-wise test).** For every `H-*` in this file run on the same universe, the best in-sample rule's out-of-sample (2016–2025) excess is materially lower than its in-sample excess. Only rules with White Reality Check/SPA or Monte-Carlo-permutation p < 0.05, with the whole family counted, are promoted.
- **H-ARO-2 (position-bias correction).** For long-only rules, excess return over zero minus excess return over detrended returns ≈ (fraction of time long) × (mean daily drift). Long-biased rules in §§5–7 lose a measurable part of their apparent edge after detrending.
- **H-ARO-3 (replication).** Simple index-level rules fail WRC at 5% on ^GSPC daily data 1980–2025. Examples: SMA(n) price crosses for n ∈ {10…200}, N-day channel breakouts, RSI(14) 30/70, MACD crosses.
- **H-ARO-4 (cross-sectional robustness).** A rule that survives must show the same sign of edge in ≥70% of non-overlapping 5-year subperiods and in two disjoint stock universes.

---

## 11. Al Brooks — price action (*Reading Price Charts Bar by Bar*, *Trading Price Action* trilogy)

**Core beliefs.** Every bar is read for who controls the market. Markets spend most of their time in ranges; Brooks estimates 70–80%. In trading ranges, **most breakout attempts fail** (about 80% per secondary accounts), and most reversal attempts in trends also fail ([NexusFi](https://nexusfi.com/a/strategies/trading-range-price-action-strategies) [W]; [Brooks forum](https://www.brookstradingcourse.com/support-forum/general-trading-discussion/trading-range-breakout/) [W]).

- **Trader's equation**: take a trade only if P(win)×Reward > (1−P)×Risk, computed with *actual* risk.
- Brooks prefers **second entries** ("H2/L2"), meaning the second pullback attempt.
- **"Always-in"**: the trader is always either long or short in direction.
- Measured moves project the height of the leg or range.
- The work is mostly on intraday E-mini charts; on daily stock data the concepts transfer only by analogy.

**Entry.** In trends, buy pullbacks: an H2 in a bull trend. In ranges, fade the extremes. Buy breakouts only after a strong, follow-through breakout bar, with a target ≥2× risk when the probability is low.
**Stop.** Beyond the signal bar or the swing.
**Stay out.** The middle of a trading range. Weak breakout bars inside a range. Low-probability setups whose reward is under 2× risk.

**Hypotheses.**

- **H-BRK-1 (range breakouts fail).** Define a range regime as ADX(14) < 20 and a 20-bar high–low range ≤ 4×ATR(14). Closes above the 20-bar high in this regime close back below it within 5 bars more often than 50% (Brooks suggests about 80%). In trend regimes (ADX > 25), the failure rate is lower.
- **H-BRK-2 (second entry).** Context: C > SMA50 and SMA50 rising. Define a pullback-attempt trigger as a close above the prior bar's high after ≥1 lower low. The second such trigger after a 10-bar high beats the first (R10, stop at the pullback low).
- **H-BRK-3 (strong breakout bar).** Breakouts whose bar has body ≥ 0.7×range, range ≥ 1.5×ATR(14) and a close in the top 20% of the bar reach the measured-move target (breakout + 20-bar range height) within 20 bars more often than weaker breakout bars.
- **H-BRK-4 (trader's equation filter).** Keep only setups where empirical p̂ × target > (1 − p̂) × stop distance, with p̂ estimated from data before the trade date. This raises system expectancy vs. unfiltered setups.

---

## 12. Larry Connors — RSI(2) mean reversion (*Short Term Trading Strategies That Work*, with C. Alvarez)

**Published rules** ([ChartSchool RSI(2)](https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/rsi-2) [S]):

1. **Trend filter**: long only when C > SMA200; short only when C < SMA200.
2. **Setup**: RSI(2) < 10 for a buy, or > 90 for a short. Connors tested 0–10 and 90–100. Returns were higher below 5 than below 10, and higher above 95 than above 90.
3. **Entry**: just before the close, which Connors prefers, or at the next open.
4. **Exit**: long on a close above SMA5; short on a close below SMA5.
5. **No stops.** In his testing of "hundreds of thousands of trades," stops "hurt" performance on stocks and indices.

Philosophy: "buy pullbacks, not breakouts" and "sell oversold bounces, not support breaks." The book also says "statistically, there is no edge using the 14-period RSI" and that "the lower the RSI, the greater the performance": RSI(2) < 2 beat < 5 ([Oxford Strat quoting the book](https://oxfordstrat.com/?p=16240) [S]). ConnorsRSI(3,2,100) = mean of RSI(3), RSI of up/down streak length(2), and 100-day PercentRank of 1-day return ([ChartSchool ConnorsRSI](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/connorsrsi) [S]).

**Independent replications** (not Connors' own numbers):

| Study | Universe / period | Rules | Win rate | Payoff | Result |
|---|---|---|---|---|---|
| [Oxford Capital Strategies](https://oxfordstrat.com/?p=16240) [S] | 5 equity-index futures, 1980–2016, $50 round-turn costs, 6×ATR stop | RSI<5–15, exit SMA5–10 | 69.8–75.5% | avg win / avg loss 0.49–0.61; PF 1.40–1.71 | Sharpe 0.28–0.56; CAGR 0.34–1.17% at 1% risk; "underperforms alternative momentum models" |
| [Backtrex](https://backtrex.com/en/backtests/connors-rsi-2-sp-500) [W] | SPX CFD, Oct 2016–Oct 2026, long and short | RSI<5 / >95, SMA200, SMA5 exit | 71.2% (73 trades) | avg win 1.22% vs avg loss 2.10%; PF 1.43 | +18.1% total vs buy-and-hold +255.4%; CAGR 1.7%; max DD −21.5% |
| [Backtest Substack](https://backtest.substack.com/p/the-2-period-rsi-a-simple-system) [W] | Nasdaq-100 members, Dec 2006–2025, 4 slots | C>SMA200, C<SMA5, RSI(2)<10, exit C>SMA5 | 64.3% | +2.33% avg win / −3.02% avg loss; PF 1.45 | 17.84% annual; max DD 29.15%; Sharpe 1.10 |

**What the replications show.**

- Win rates are high, but the average winner is smaller than the average loser.
- Time in the market is low.
- A cross-section of stocks works better than a single index.
- Index-level shorts drag on results.
- Tail losses are real when there is no stop.

**Stay out.** C < SMA200 for longs. RSI(2) between 10 and 90, i.e. no setup. Earnings gaps: ChartSchool notes the gaps that "wreak havoc" clustered in earnings season. Single-index use with a short side in strong bull markets.

**Hypotheses.**

- **H-CON-1 (core).** Buy at C(t) when C > SMA200 and RSI(2) < 10. Exit at the first close above SMA5. Expected: win rate 60–75%, mean trade > 0 after 10 bps costs, average win < average loss, exposure < 30%.
- **H-CON-2 (monotonic depth).** Mean trade return increases as the threshold drops through RSI(2) < 10, < 5, < 2.
- **H-CON-3 (trend filter is load-bearing).** The same setup with C < SMA200 has lower mean trade return and fatter left tails. Treat it as no-signal.
- **H-CON-4 (stops).** Adding a 2.5×ATR(14) stop lowers mean trade return (Connors' claim) but cuts the 1st-percentile trade loss and max drawdown. Report both effects.
- **H-CON-5 (RSI(14) has no edge).** RSI(14) < 30 with the same filter and exit has a mean trade not significantly different from zero, while RSI(2) < 10 is significant.
- **H-CON-6 (pullback > breakout).** Within C > SMA200, R5 after a new 10-bar closing low exceeds R5 after a new 10-bar closing high. This is the short-horizon reversal that conflicts with breakout schools.

---

## 13. Cross-School Synthesis

### 13.1 Consensus rules (appear in ≥3 schools)

| # | Consensus rule | Schools | Operational default for the rulebook |
|---|---|---|---|
| C1 | **Trade only with the higher-timeframe or primary trend**; counter-trend setups are no-signal | Murphy L1–2; Weinstein (Stage 2 only); O'Neil (M); Minervini (Trend Template); Elder (Screen 1, Impulse); Connors (SMA200); Nison/Bulkowski (candles work in primary trend); Lane/Bollinger (oversold only in uptrends) | Long only if C > SMA200 and SMA200(t) > SMA200(t−21); or weekly C > W-SMA30 and W-SMA30 rising |
| C2 | **The long MA (200-day / 30-week ≈ 150-day) and its slope define regime** | Murphy; Weinstein; Minervini; Connors; ChartSchool scans | SMA200 slope over 21 bars; SMA150 > SMA200 |
| C3 | **Wait for confirmation: a close beyond the boundary, not an intraday pierce or a pattern-in-progress** | Bulkowski (48–60% never confirm); Edwards & Magee; Murphy (3% / 2-day); Nison (1–3-day confirmation); Weinstein (weekly close); Lane (divergence confirmation); Bollinger ("tags are not signals") | Signal only on a close beyond; optional ≥2% or 2-close filter |
| C4 | **Upside breakouts need expanding volume** | Edwards & Magee; Murphy L10; O'Neil (+40–50%); Weinstein (~2×); Minervini (+40–50%); Bulkowski (heavy volume helps 26 up-patterns) | V ≥ 1.4×ADV50 on the breakout bar. Not required for downside breaks |
| C5 | **Oscillator extremes are only meaningful in ranges or as pullbacks within trends; in strong trends overbought means strength** | Murphy L7/L9; Wilder/ChartSchool RSI; Lane; Bollinger (walk the band); Connors (oversold only above SMA200); Elder (oscillator against weekly trend) | Gate oscillator signals by ADX < 20 (range) or by trend direction (pullback-only) |
| C6 | **Predefined small loss limits** | O'Neil 7–8%; Minervini ≤10%; Elder 2%/6%; Weinstein (below base); Wilder (signal-bar extreme); Bulkowski (below pattern); Edwards & Magee (basing points) | Hard stop = pattern or swing invalidation, capped at 8–10% or ~2–3 ATR |
| C7 | **Volatility and volume contraction precede valid breakouts** | Bollinger (squeeze); Minervini (VCP); O'Neil (quiet handle); Bulkowski (volume falls 78–86% of the time in triangles); Edwards & Magee (diminishing triangle volume) | BandWidth at a 125-bar low or ADV10/ADV50 < 0.7 before the breakout |
| C8 | **Relative-strength leadership** | O'Neil (RS ≥ 80); Minervini (RS ≥ 70); Weinstein (Mansfield > 0) | 12-month RS percentile ≥ 70, or C/SPY above its 52-week average |
| C9 | **Support/resistance polarity** | Murphy L3; Edwards & Magee; Nison (polarity); ChartSchool (support turned resistance) | Broken level becomes the reference for stops and retest entries |
| C10 | **Never buy a stock in a downtrend (Stage 4 / below a declining long MA)** | Weinstein; Minervini; O'Neil ("on the way down"); Bulkowski stage stats (Stage-4 buys −8.3%, 24% profitable) | Hard veto |

### 13.2 Conflicts between schools

| Issue | Side A | Side B | Resolution path (test) |
|---|---|---|---|
| Breakouts vs. pullbacks | Buy breakouts/pivots near highs: O'Neil, Minervini, Weinstein, Bulkowski | Buy pullbacks, not breakouts: Connors; 80% of range breakouts fail: Brooks; buy weakness in uptrends: Elder | H-CON-6, H-BRK-1, H-ONL-1, segmented by ADX regime and holding period (short-horizon reversal vs. multi-week momentum) |
| Stops | Mandatory: O'Neil, Minervini, Elder, Weinstein, Wilder | "Stops hurt performance": Connors | H-CON-4; judge by tail risk and drawdown, not only mean |
| Overbought | Sell or avoid overbought: Wilder 70; Lane 80 | Buy strength or new highs: O'Neil, Minervini; close outside the band = continuation: Bollinger | H-BOL-1, H-MIN-1 |
| Oversold depth | RSI(14) < 30: Wilder, Murphy | RSI(2) < 5–10; RSI(14) has "no edge": Connors | H-CON-5 |
| Divergences | Primary signals: Wilder, Lane ("only signal") | Misleading in strong trends; reversed meaning (Cardwell): ChartSchool | H-LAN-1, H-WIL-3 |
| Stage of entry | Buy the Stage-2 breakout: Weinstein | Bulkowski data: Stage-1 buys +13.2% vs Stage-2 +4.1% | H-BUL-8 |
| Profit-taking | Fixed 20–25% target: O'Neil | Trail with MA/ATR: Weinstein, Elder (Chandelier), Minervini (10-day MA); quick SMA5 exit: Connors | Holding-period-specific tests |
| Retests | Retest/throwback = second-chance entry: Edwards & Magee, ChartSchool, Weinstein | Throwbacks *hurt* performance (occur 58–68% of the time): Bulkowski | H-BUL-4 |
| Candle "reversal %" | Reversal patterns signal turns: Nison | High reversal % does not mean a big move (bearish engulfing 79% reversal, rank 91/103): Bulkowski | H-BUL-7, H-NIS-1 |
| MA type | EMAs better for crossovers: Murphy; EMA13/22/65: Elder | SMAs: Bollinger, Weinstein, Minervini, Connors | Treat as a parameter; count in the test family |
| ADX trend threshold | 25: Wilder | 20: common practice / ChartSchool | Sensitivity grid {20, 25} |
| Volume confirmation | Universal requirement: Edwards & Magee, O'Neil, Weinstein | Pattern-dependent; some patterns prefer light breakout volume: Bulkowski | Per-pattern test (H-EM-1) |
| Does any simple rule work? | All schools above | None of 6,402 rules significant after data-mining correction: Aronson | H-ARO-1…4 gate every promotion |

### 13.3 Most commonly used parameters

| Parameter | Values (school) |
|---|---|
| Short MA | SMA5 exit (Connors); 10-day trail (Minervini); EMA13 (Elder); SMA20 / EMA20 (Murphy, Bollinger, Nison downtrend test); EMA22 (Elder) |
| Intermediate MA | SMA50 (Murphy, Minervini); EMA65 = 5×13 (Elder) |
| Long MA | 30-week ≈ SMA150 (Weinstein, Minervini); SMA200 (Murphy, Minervini, Connors) |
| MA crossover pairs | 5/20, 20/50, 50/200 (Murphy); 12/26 EMA = MACD (Appel) |
| MA slope test | SMA200 rising ≥1 month (~21 bars), preferably 4–5 months (Minervini) |
| RSI | 14 with 70/30 (Wilder; Murphy also 9); 2 with <10 / <5 / <2 buy and >90 / >95 sell (Connors); bull range 40–90, bear range 10–60 (Brown) |
| Stochastics | (14,3) or (14,3,3), 80/20, 50 centerline (Lane, Murphy) |
| MACD | 12, 26, 9 |
| ADX / DMI | 14; >25 trend, <20 no trend |
| ATR | 14 (8 in Wilder's work); Chandelier 22 × 3 (LeBeau / Elder) |
| Bollinger | 20 / 2.0; 10 / 1.9; 50 / 2.1; squeeze = BandWidth at 6-month (~125-bar) low; %b 0.8 / 0.2 with MFI(10) 80 / 20 |
| Parabolic SAR | AF 0.02 start, +0.02 step, 0.20 max |
| Force Index | EMA2 (timing), EMA13 (trend), 39/100 (longer) |
| Volume multiples | ≥1.4–1.5× average (O'Neil, Minervini); ≥2× recent weekly average (Weinstein); above 30-day average = "heavy" (Bulkowski); above prior day (FTD, distribution day) |
| Breakout filters | 3% close beyond; 2-close or 3-day time filter (Murphy, ChartSchool); confirmation close (Bulkowski) |
| Retracements | 33–38% / 50% / 62–66% (Murphy) |
| Pattern geometry | Cup 7–65 weeks, depth 12–33%, handle ≥1 week in the upper half and ≤ ~12% deep (O'Neil, Bulkowski); double top/bottom peaks within 3%, ≥10% valley, ~1 month apart (ChartSchool, Bulkowski); flags < 3 weeks (Bulkowski) or 1–12 weeks (ChartSchool); high & tight flag ≥90% rise in ≤2 months |
| Trend Template | ≥30% above 52-week low; within 25% of 52-week high; RS ≥ 70 |
| Market timing (IBD) | FTD on day ≥4 with +1.0 / 1.25 / 1.7%; distribution day −0.2% on higher volume, 25-session window, 5% expiry; 4–6 distribution days = warning |
| Stops | 7–8% (O'Neil); ≤10% hard cap (Minervini); 2% of equity per trade and 6% per month (Elder); signal-bar extreme (Wilder); below pattern low (Bulkowski); none (Connors) |
| Targets | 20–25% (O'Neil); measured move × Bulkowski "% meeting target" (e.g., ×0.51 for H&S tops, ×0.61 for cups) |
| Bulkowski measurement windows | throwback/pullback ≤30 days; bust ≤10% move; ultimate high/low = 20% reversal |

### 13.4 Master "no-signal / stay-out" list for the agent

These items are distilled from §§1–12. Each one is a veto unless the corresponding hypothesis fails in testing.

1. Long setups while C < SMA200 with SMA200 falling, or weekly Stage 4 (C1, C10).
2. Patterns before a confirming close beyond the boundary (C3).
3. Upside breakouts on V < ADV50 for volume-sensitive patterns (C4).
4. Oscillator reversal trades when ADX(14) > 25 against the trend, and MA/DMI crossovers when ADX < 20 (C5).
5. Range-middle breakouts: the middle third of the 52-week range (Bulkowski) or the middle of a trading range (Brooks).
6. Daily flags and pennants as stand-alone signals: 44–54% break-even failure and 4–9% average moves.
7. Common single candles without trend, support and next-bar confirmation; rare candles with N < 100.
8. Entries more than 5% above the pivot (O'Neil/Minervini).
9. Any trade whose stop exceeds 10% of price, or needs more than 2% of equity risk; no new trades after −6% for the month (Elder).
10. A market regime with ≥5 distribution days in 25 sessions, or no follow-through since the correction low (O'Neil).
11. Mean-reversion longs (RSI(2)) when C < SMA200, or into earnings dates (Connors/ChartSchool).
12. Any rule that has not passed the family-wise data-mining test (Aronson). The default is no signal.

---

### Source index (all accessed 2026-10-31)

- **Bulkowski** (thepatternsite.com): hst, hsb, eedt, aadb, eedb, at, dt, st, flags, pennants, htf, cup, recttops, rectbots, top10, id73, id75, rank, glossary, FailureRates, BestPatterns, volbkout, TimePerformance, Busted, Stages, CandlePerformers, CandleReverse, CandleContinue, CandleTips, Hammer, BullEngulfing and BearEngulfing (.html). Also the *S&C* V.29:6 reprint (Fidelity PDF, text saved locally).
- **ChartSchool** (raw `.md` saved to `scratchpad/web_raw/canon/`): Murphy 10 Laws; RSI(2); ConnorsRSI; ADX; ATR; Parabolic SAR; Bollinger Bands; Squeeze; %B; Force Index; Elder Impulse; MACD; Stochastic; RSI; Price Relative; Cup with Handle; H&S Top; Flag/Pennant; Double Top; Chandelier Exit; Candlestick Bullish Reversals.
- **Other:** bollingerbands.com rules; AAII CAN SLIM PDF (text saved locally); CXO Aronson review; O'Reilly EBTA Ch. 8; Wiley EBTA page; EarnForex review; IncredibleCharts (6% rule, Elder-ray); LuxAlgo (Weinstein, cup base, FTD, distribution days); EliteTrader (Trend Template quote); finermarketpoints (VCP, Minervini risk); Oxford Strat, Backtrex and Backtest Substack (RSI(2) replications); NexusFi and Brooks forum (Brooks); Shortform (Nison).
- **Blocked in this session:** investors.com, investopedia.com, traders.com (403), marketsmithindia (DNS). IBD-specific thresholds are therefore marked [W] or [B].
