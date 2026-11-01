# Academic Evidence on Technical Analysis — What Works, When, and When It Doesn't

*Compiled 2026-10-31 for the TA rulebook. The scope is peer-reviewed and working-paper evidence on US stocks and ETFs, with FX and futures evidence included where it is the best available. Raw fetched texts are in the session scratchpad (`web_raw/academic/`) and were not executed.*

**Source labels:** **[full text]** = read from the paper (NBER/SSRN/author/journal PDF); **[abstract only]** = only the abstract or index page was available; **[secondary: X]** = from a named summary (CXO Advisory, CFA Digest, Alpha Architect, ETF.com, or a survey). Numbers not shown were not verified; nothing is filled in from memory.

---

## 0. Bottom line (read this first)

1. **Simple price rules on US large-cap indices had real, snooping-robust predictive power before ~1986–1990 and little or none afterwards, especially after costs** (STW 1999; Bajgrowicz & Scaillet 2012; Park & Irwin 2007). For any daily MA, breakout or oscillator rule on SPY/DIA over 2000–2026, the default is **"no edge after costs"** until it clears a multiple-testing hurdle.
2. **The robust trend effects are slow, diversified or risk-managed:** time-series momentum across many futures (1880–2016); cross-sectional 6–12 month momentum (crash-prone, weak in the US in 2001–2015); 52-week-high anchoring; and long-horizon MA timing, which mainly **cuts volatility and drawdowns** rather than raising returns.
3. **Trend/MA timing pays mostly in a few severe bear markets** (1930–31, 1973–74, 2001–02, 2007–08) and lags in long bull runs (1975–1999) and chop.
4. **Momentum fails in panic rebounds after bear markets** (1932, 2009), in January, and after DOWN market states. Use a crash filter or volatility scaling.
5. **Short-term (1-week to 1-month) reversal is real but is mostly a liquidity-provision premium:** concentrated in illiquid stocks, usually smaller than costs, paying mainly when VIX is high.
6. **Candlesticks, RSI overbought/oversold, divergences, Fibonacci, Elliott waves and Gann have no credible support** in US equities. Chart patterns and S/R are weak or conditional.
7. **Publication and crowding decay are large:** about 58% lower returns after publication; new signals need t > 3; PEAD has been gone in large caps since ~2006.

---

## 1. Paper-by-paper / theme-by-theme evidence

### 1.1 Brock, Lakonishok & LeBaron (1992), "Simple Technical Trading Rules and the Stochastic Properties of Stock Returns" (JF 47(5))
- **Claim:** on the DJIA, MA and trading-range-break (TRB) buy signals earn more than sell signals; post-sell returns are negative and post-buy returns less volatile; results reject random-walk, AR(1), GARCH-M and EGARCH nulls by bootstrap. [abstract only]
- **Sample / rules:** DJIA daily 1897–1986; 26 rules = 10 variable-length MA + 10 fixed-length MA with (short, long, band) ∈ {(1,50,0/1%), (1,150,0/1%), (5,150,0/1%), (1,200,0/1%), (2,200,0/1%)}, plus 6 TRB (break of prior max/min) rules [parameter list: secondary, IAENG WCE2011 replication].
- **Effect size:** BLL's own per-signal means **not verified** (tables paywalled). Per STW, the best BLL-universe rule over 1897–1996 was the **50-day VMA with 1% band: 9.4%/yr vs 4.3% buy-and-hold** [full text, STW].
- **After costs:** Bessembinder & Chan (1998): average break-even **one-way cost 0.22% in 1976–1991 vs estimated actual 0.24–0.26%**, i.e. unprofitable after costs [secondary: Park & Irwin 2004].
- **Decay:** failed out of sample after 1986 (1.2, 1.3).
- **Rulebook implication:** BLL's rules (50/150/200-day MA, 1% band, range breaks) are the canonical **null test bed**: evidence of a pre-1990 inefficiency, not a live edge on US large caps.
- URLs: https://ideas.repec.org/a/bla/jfinan/v47y1992i5p1731-64.html ; https://doi.org/10.1111/j.1540-6261.1992.tb04681.x

### 1.2 Sullivan, Timmermann & White (1999), "Data-Snooping, Technical Trading Rule Performance, and the Bootstrap" (JF 54(5))
- **Claim:** White's Reality Check (RC) over the whole rule universe shows strong in-sample DJIA performance that **does not persist out of sample**. [full text, LSE FMG DP303]
- **Sample / rules:** DJIA 1897–1996 (five subperiods; true out-of-sample 1987–1996) and S&P 500 futures 1984–1996; **7,846** filter, MA (band/delay), S/R channel-breakout and OBV rules.
- **In sample:** best rule = **5-day SMA, 17.2%/yr** (RC p < 0.002) vs 4.3% buy-and-hold, from **6,310 trades (63/yr) → break-even 0.27% per trade**.
- **Out of sample:** the 5-day MA earned **2.8%/yr in 1987–1996 (nominal p = 0.322)**; the BLL universe's RC p ≈ 0.15 (mean) and **0.72 (Sharpe)**; S&P 500 futures full-universe RC p ≈ **0.9**.
- **Rulebook implication:** **never trust the best rule from a search.** Short-window (2–5 day) MA rules showed the best in-sample and worst out-of-sample results. Evaluate every family with RC/SPA/step-wise tests over the full grid.
- URL: https://www.fmg.ac.uk/sites/default/files/2020-11/dp303.pdf

### 1.3 Bajgrowicz & Scaillet (2012), "Technical Trading Revisited: False Discoveries, Persistence Tests, and Transaction Costs" (JFE 106(3))
- **Claim:** "Persistence tests show that... an investor would never have been able to select ex ante the future best-performing rules. Moreover, even in-sample, the performance is completely offset by the introduction of low transaction costs." [full text, SFI WP 08-05]
- **Sample:** DJIA daily, 1897–2011, in six subperiods; the new one is 1997–2011. Rule universe from STW, with False Discovery Rate (FDR) selection.
- **Effect size and costs:**
  - In 1897–1962, one-way costs of **16, 35 and 70 bp** are enough to eliminate all outperforming rules in the three subperiods.
  - **In 1962–2011, no positive performance is detected even at zero cost.**
  - Out of sample, **one-way costs of 5–35 bp** wipe out any remaining performance, even in the early periods.
  - In 1962–1986, only 44% of rules were positive before costs, and most needed costs below 10 bp to break even.
- **Rulebook implication:** **Strongest negative result for classic daily TA on the US index.** It sets the null for SPY/DIA rules in 2000–2026: assume zero edge.
- URLs: https://smallake.kr/wp-content/uploads/2017/12/SSRN-id1095202.pdf ; https://ideas.repec.org/a/eee/jfinec/v106y2012i3p473-491.html

### 1.4 Hsu & Kuan (2005), "Reexamining the Profitability of Technical Analysis with Data Snooping Checks" (JFEc 3(4)); Hsu, Taylor & Wang (2016) (JIE 102)
- **Hsu & Kuan:** Using Reality Check and SPA on simple rules plus "investor strategies" (combinations), they found significant profits in **"young" markets (NASDAQ Composite, Russell 2000)** but not in **"mature" ones (DJIA, S&P 500)**. In-sample period was 1990–2000. After costs, the best young-market rules beat buy-and-hold in most in- and out-of-sample periods. [full text, working-paper version]
- **Caveat (ours):** These are index-level tests. Small-cap index returns contain stale-price autocorrelation, which an investor cannot trade.
- **Hsu, Taylor & Wang (2016):** FX, 30 currencies, 45 years, >21,000 rules, step-wise SPA: predictability varies by subperiod and tracks market immaturity. [abstract only]
- **Rulebook implication:** A TA edge, if any, sits in **less mature, less efficient segments** (small caps, emerging markets, FX). For US ETFs, **IWM/QQQ-type small-cap or tech indices deserve a separate test from SPY/DIA**, using ETF prices, not index prints.
- URLs: https://ideas.repec.org/a/oup/jfinec/v3y2005i4p606-628.html ; https://profiles.wustl.edu/en/publications/technical-trading-is-it-still-beating-the-foreign-exchange-market/

### 1.5 Park & Irwin (2007), "What Do We Know About the Profitability of Technical Analysis?" (J. Economic Surveys 21(4))
- **Claim:**
  - "Among a total of 95 modern studies, 56 studies find positive results... 20 studies obtain negative results, and 19 studies indicate mixed results." [abstract, IDEAS]
  - The 2004 working-paper version counted 92 studies (58 positive, 24 negative, 10 mixed). [full text, AgMAS 04-04]
  - Profits were consistent "at least until the early 1990s". Most studies suffer from **data snooping, ex post rule selection, and poor risk/cost estimation**.
- **Key details** [full text]: rules worked in **FX and futures** far more than in **developed stock markets**; genetic-programming rules (Allen & Karjalainen 1999; Ready 2002; Neely 2003) **underperformed buy-and-hold on the S&P 500 and DJIA**; emerging-market MA rules earned 18.2–32.1%/yr net (Ratner & Leal, 1982–1995); Chang & Osler's FX head-and-shoulders earned ~13% (mark) and ~19% (yen) per year (1973–1994).
- **Rulebook implication:** The weight of evidence is **"profitable before ~1990, in FX/futures/emerging markets, and in-sample."** Developed-market equity results after 1990 are mostly negative.
- URLs: https://ideas.repec.org/a/bla/jecsur/v21y2007i4p786-826.html ; https://ageconsearch.umn.edu/record/37487/files/AgMAS04_04.pdf

### 1.6 Lo, Mamaysky & Wang (2000), "Foundations of Technical Analysis" (JF 55(4))
- **Claim:** with kernel-regression pattern detection, "several technical indicators do provide incremental information and may have some practical value." [full text, NBER w7613]
- **Sample:** CRSP NYSE/AMEX and Nasdaq, 1962–1996, seven 5-year subperiods × 50 random stocks (10 per size quintile).
- **Patterns:** head-and-shoulders and inverse (HS/IHS), broadening, triangle, rectangle and double tops/bottoms (BTOP/BBOT, TTOP/TBOT, RTOP/RBOT, DTOP/DBOT).
- **Measure:** distribution of the 1-day return starting 3 days after completion vs the unconditional distribution, **not trading profit**.
- **Results:** NYSE/AMEX goodness-of-fit significant for 7 of 10 (not BBOT p = 5.1%, TTOP 21.2%, DBOT 16.6%); Kolmogorov–Smirnov significant for **HS, BBOT, RTOP, RBOT, DTOP** (p = 0.000–0.021), not the rest (p = 0.104–0.393). **Nasdaq: all 10 significant. Volume trend adds little.** Costs not tested; the authors say this does not imply excess profits.
- **Rulebook implication:** patterns carry **distributional information, mostly in smaller, less liquid stocks**, not a demonstrated edge. Test HS, rectangles and double tops algorithmically, never discretionarily. Volume confirmation of patterns is unsupported.
- URL: https://www.nber.org/system/files/working_papers/w7613/w7613.pdf

### 1.7 Head-and-shoulders follow-ups: Savin, Weller & Zvingelis (2007); Bender, Osler & Simon (2013); Osler (1998)
- **Savin et al. (JFEc 5(2)):** Modified LMW algorithm plus analyst-style filters on S&P 500 and Russell 2000 stocks, 1990–1999. **Risk-adjusted excess returns of 5–7% per year** from an H&S-top strategy that requires shorting, with 1–3 month horizons. "The success of the strategy rests in part on its identification of negative momentum stocks." [full text, working-paper version]
- **Bender, Osler & Simon (RoF 17(2)):** H&S in US equities "is associated with a substantial rise in trading volume even though it does not profitably predict directional movements." They interpret it as noise trading. [abstract only]
- **Osler (1998) (FRBNY SR42):** H&S trading is positive-feedback noise trading, and its price effects disappear within about two weeks. [abstract only]
- **Rulebook implication:** H&S is at best a **noisy proxy for negative momentum**. Credit the momentum component, not the pattern geometry. **Grade C.**
- URLs: https://www.biz.uiowa.edu/faculty/gsavin/papers/HSrevision_paw_10%2019%2006.pdf ; https://ideas.repec.org/a/oup/revfin/v17y2013i2p625-652.html ; https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr42.pdf

### 1.8 Candlesticks: Marshall, Young & Rose (2006); Caginalp & Laurent (1998); Lu & Shiu (2016)
- **Marshall, Young & Rose (JBF 30(8)):** DJIA component stocks, 1992–2002, **28 candlestick signals**, holds of up to 10 days, bootstrap tests. **No evidence that any signal predicts returns.** The result is robust to entering at the next-day open and across subperiods. [secondary: CXO Advisory; Massey thesis]
- **Caginalp & Laurent (1998):** S&P 500 stocks, 1992–1996. Down-to-up reversal patterns earned **0.56–0.76% net per 2-day hold**. This is a short sample, with no data-snooping control. [secondary: Park & Irwin]
- **Lu & Shiu (2016, Applied Economics):** DJIA 30 stocks, 1974–2009, "every possible 1-day pattern". Several patterns "may well prove to be profitable", with predictive power increasing from 1992. [abstract only; holding periods and costs not visible]
- **Rulebook implication:** The best-controlled US test (Marshall et al.) is null. Positive studies are short-sample or come from searches over many patterns. **Grade D. Never use candlesticks as a standalone entry signal.** At most, use them as an execution-timing tiebreaker, and only after our own holdout tests.
- URLs: https://ideas.repec.org:443/a/eee/jbfina/v30y2006i8p2303-2323.html ; https://www.cxoadvisory.com/technical-trading/candlesticks-fiddlesticks/ ; https://ideas.repec.org/a/taf/applec/v48y2016i35p3345-3354.html

### 1.9 Cross-sectional momentum: Jegadeesh & Titman (1993, 2001); Chan, Jegadeesh & Lakonishok (1996)
- **JT (1993) claim:** Buying 6-month winners and selling losers earns about **1% per month, t = 3.07** (1965–1989). [full text of JT2001, which restates JT1993]
- **JT (2001) out of sample** (NBER w7159; stocks under $5 excluded):
  - Top-minus-bottom decile was **1.11% per month in 1965–1989** and **1.01% per month in 1990–1997**.
  - **January:** losers beat winners by **2.92% on average in January** (1965–1989). Outside January the strategy earned 1.47% per month (original sample) and 1.20% (1990s).
  - **Months 13–60 after formation are negative**, with significant reversal in years 4–5.
- **The 12-1 convention:** "12-1" (12-month return skipping the last month) is the Carhart/UMD convention used by Daniel & Moskowitz, not JT1993's (6,6). The skip month avoids the 1-month reversal effect (§1.15).
- **Chan, Jegadeesh & Lakonishok (1996):** Past return and past earnings surprise *each* predict drift over the following 6–12 months (1977–1993). Price momentum is not fully subsumed by earnings momentum. [secondary: CFA Digest]
- **After costs:** Not in these papers. Decay is covered under 1.12 and 1.17.
- **Rulebook implication:** Momentum **exists and was replicated out of sample in the 1990s**. Use 12-1 or 6-1 lookbacks, and skip the most recent month. **Cut or avoid momentum exposure in January.**
- URLs: https://www.nber.org/system/files/working_papers/w7159/w7159.pdf ; https://ideas.repec.org/a/bla/jfinan/v51y1996i5p1681-1713.html

### 1.10 Time-series momentum: Moskowitz, Ooi & Pedersen (2012); Hurst, Ooi & Pedersen (2017); Huang, Li, Wang & Zhou (2020)
- **MOP (JFE 104):** 58 liquid futures (equity indices, FX, commodities, bonds), 1965–2009 (core results from 1985); rule = sign of the past 12-month excess return, 1-month hold, 40% ex-ante vol per position. Returns persist 1–12 months, then partially reverse. Diversified alpha **1.58%/month (t = 7.99)** vs MSCI World/SMB/HML/UMD and **1.09%/month (t = 5.40)** vs AMP "everywhere" factors. Best in **extreme markets** (squared MSCI World return, t = 3.88); VIX and TED terms insignificant. [full text]
- **HOP, "A Century of Evidence on Trend-Following" (JPM 2017):** 67 markets, equal-weighted 1/3/12-month TSMOM, 10% vol target, 1880–2016, net of estimated costs; **positive in every decade**, average per-market gross Sharpe ≈ 0.4 [full text]. The 2014 version reports 1880–2013 **14.9% gross, 11.2% net of 2/20, 9.7% vol, net Sharpe 0.77, 0.00 correlation to US equities**; **2000–2013: 11.3% gross, 7.9% net, net Sharpe 0.62** vs 1.70 in the 1970s and 0.96–0.98 in the 1980s–90s [full text, trendfollowing.com copy]. Strong in large 60/40 drawdowns (the "smile").
- **Huang et al. (JFE 2020), "Time series momentum: Is it there?":** **little asset-by-asset evidence**, in or out of sample; the pooled t-stat is below bootstrap critical values; much TSMOM profit may come from cross-sectional mean differences rather than timing. [abstract only]
- **Rulebook implication:** robust as a **diversified, vol-scaled, multi-asset** strategy (grade A there). As a **timing signal on one US index/ETF** it is weaker and close to MA timing (grade B). Use 12-month and 1/3/12 blends with vol scaling, and expect lower Sharpe post-2000.
- URLs: http://pages.stern.nyu.edu/~lpederse/papers/TimeSeriesMomentum.pdf ; https://fairmodel.econ.yale.edu/ec439/hurst.pdf ; https://www.TrendFollowing.com/whitepaper/Century_Evidence_Trend_Following.pdf ; https://profiles.wustl.edu/en/publications/time-series-momentum-is-it-there/

### 1.11 MA timing of the index: Faber (2007/2013); Zakamulin (2014); Marshall, Nguyen & Visaltanachoti (2017)
- **Faber, "A Quantitative Approach to Tactical Asset Allocation":** month-end price vs 10-month SMA, else T-bills; total return; costs, taxes and slippage excluded. S&P 500 1901–2012: average return 11.26% (buy-and-hold) vs 11.22% (timing); compounded 9.32% vs **10.18%**; **max drawdown 83.66% → 42.24%**; invested ~70% of the time, under one round trip per year; underperforms in about half of all years and in strong bulls such as the 1990s. [full text, 2013 update]
- **Zakamulin (J. Asset Mgmt 2014), "Real-life performance...":** 1926–2012 monthly, SMA and TSMOM with 2–24 month lookbacks, **0.5% one-way cost** for stocks, rolling selection, out-of-sample 1930–2012. Net Sharpe gain ≈ +10% (S&P SMA) and +12% (S&P momentum); under the bootstrap only S&P SMA survives (≈ +7%); 3 of 8 rule/index pairs beat buy-and-hold. Gains come from **1930–31, 1973–74, 2001–02, 2007–08**; timing **underperformed throughout 1975–1999** and in ~80% of exit-to-reentry spells; volatility ~30% lower. [secondary: CXO Advisory; Quantpedia]
- **Marshall, Nguyen & Visaltanachoti (QF 2017):** MA rules often signal earlier than TSMOM, with return gains; **both work best outside large stocks.** [abstract only]
- **Rulebook implication:** long-window MA/TSMOM timing on SPY is a **drawdown-control overlay**, not alpha. Its value sits in a few deep bear markets; expect multi-year bull-market lag. Evaluate monthly or weekly; avoid daily 5–20 day crossovers on SPY.
- URLs: https://mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf ; https://ideas.repec.org/a/pal/assmgt/v15y2014i4d10.1057_jam.2014.25.html ; https://www.cxoadvisory.com/technical-trading/net-performance-of-sma-and-intrinsic-momentum-timing-strategies ; https://ideas.repec.org/a/taf/quantf/v17y2017i3p405-421.html

### 1.12 MA timing of volatility-sorted portfolios; the trend factor; MA distance (MAD)
- **Han, Yang & Zhou (JFQA 48(5), 2013), "A New Anomaly":** NYSE/AMEX 1963–2009, deciles by prior-year daily volatility; hold the decile when its price is above its N-day MA (10/20/50/100/200), else T-bills, 1-day delay. 10-day MA abnormal returns **8.42%–18.70%/yr**, rising with volatility (CAPM alphas 9.31%–21.76%); 20-day 7.93%–20.78%; 200-day mostly above 5%; Sharpe ~3–4× buy-and-hold. Break-even costs ≈ **0.29%–1.12%** by decile and MA length, often below actual frictions in-sample. [secondary: CFA Digest; CXO] *Our caveat:* equal-weighted high-volatility portfolios contain stale-price autocorrelation that may be untradeable.
- **Han, Zhou & Zhu (JFE 122(2), 2016), "A trend factor":** cross-sectional combination of MA signals across horizons. In the financial crisis it earned **0.75%/month vs −2.03% for the market and −3.88% for momentum** [abstract mirror]; working-paper 3-factor alpha 1.54%/month vs 1.07% for momentum [secondary: CXO].
- **Avramov, Kaplanski & Subrahmanyam (RFE 2021), "Moving average distance":** MA21 ÷ MA200 sorted cross-sectionally, June 1977–October 2015: **>12%/yr**, surviving momentum, 52-week high, trend factor, reversals, PEAD and costs, strongest on the long side. **2001–2015 Fama–MacBeth: momentum t = 0.70, 52-week high t = −1.26, trend t = 0.45, MAD t = 2.80.** [full text, SSRN 3111334]
- **Rulebook implication:** MA signals carry most information on **high-volatility, hard-to-arbitrage stocks**, which are also the costliest. MAD (21/200) is the one MA-type selection signal with documented post-2000 survival; it is a single paper, so replicate it (grade B).
- URLs: https://ideas.repec.org/a/cup/jfinqa/v48y2013i05p1433-1461_00.html ; https://rpc.cfainstitute.org/research/cfa-digest/2014/08/a-new-anomaly-the-cross-sectional-profitability-of-technical-analysis-digest-summary ; https://www.cxoadvisory.com/?p=7901 ; https://ideas.repec.org/a/eee/jfinec/v122y2016i2p352-375.html ; https://anderson-review.ucla.edu/wp-content/uploads/2021/03/Avramov-Kaplanski-Subra_2018_SSRN-id3111334.pdf

### 1.13 Technical indicators predicting the equity premium: Neely, Rapach, Tu & Zhou (2014, Management Science 60(7))
- **Claim:** 14 technical indicators (MA(s,l) with s ∈ {1,2,3} and l ∈ {9,12}; momentum over 9 and 12 months; on-balance-volume MA rules) predict the monthly S&P 500 equity premium as well as or better than macro variables, in and out of sample. [full text, St. Louis Fed WP 2010-008]
- **Effect size:** a buy signal predicts a next-month premium **48–94 bp higher** than a sell signal (in-sample R² up to 1.03% for MA(2,12)). Out of sample (1966–2011) all technical R²OS are positive, with **CER gains up to 317 bp/yr (282 bp net of costs)**, above 1,000 bp in recessions for 10 of 14 indicators. The indicators **detect the falling premium near business-cycle peaks**.
- **Rulebook implication:** monthly MA/momentum states of the index are valid **risk-on/risk-off regime variables**, most useful near cyclical peaks. OBV MA rules perform like price rules at index level.
- URL: https://files.stlouisfed.org/files/htdocs/wp/2010/2010-008.pdf

### 1.14 52-week high: George & Hwang (2004); Li & Yu (2012)
- **George & Hwang (JF 59(5)):** [full text]
  - **Rule:** rank stocks on price ÷ 52-week high; long the top 30%, short the bottom 30%; hold 6 months. Sample: July 1963–December 2001, all CRSP stocks.
  - **Monthly returns:**

    | Strategy | All months | Excluding January |
    |---|---|---|
    | 52-week high | **0.45% (t = 2.00)** | **1.23%** |
    | JT (6,6) momentum | 0.48% (t = 2.35) | 1.07% |
    | Industry momentum | 0.45% (t = 3.43) | 0.50% |

  - Nearness to the 52-week high **dominates past returns** in forecasting, and **52-week-high profits do not reverse in the long run**, unlike JT momentum.
- **Li & Yu (JFE 104, 2012):** At the index level, **nearness to the Dow's 52-week high positively predicts future market returns, while nearness to its all-time high negatively predicts them** (anchoring and attention). [abstract only]
- **Decay:** In 2001–2015 the 52-week-high effect was **t = −1.26** in AKS's Fama–MacBeth tests (see 1.12).
- **Rulebook implication:**
  - "Within X% of the 52-week high" is a better momentum proxy than raw return, and its profits do not reverse. Grade B, because recent US evidence is weak.
  - An **all-time-high** index reading is *not* a bullish signal by itself (Li & Yu).
- URLs: https://www.bauer.uh.edu/tgeorge/papers/gh4-paper.pdf ; https://experts.umn.edu/en/publications/investor-attention-psychological-anchors-and-stock-return-predict/

### 1.15 Short-term reversal: Jegadeesh (1990); Lehmann (1990); Avramov, Chordia & Goyal (2006); Nagel (2012)
- **Jegadeesh (JF 45(3), 1990):** negative first-order serial correlation in monthly stock returns; last month's losers beat winners next month. [abstract only; magnitudes not verified]
- **Lehmann (QJE 1990; NBER w2533):** weekly reversal, NYSE/AMEX 1962–1986. Last week's winners return **−0.35% to −0.55%/week**, losers **+0.86% to +1.24%/week**; the zero-cost portfolio was positive in ~90% of weeks and survived one-way costs of 0.05–0.2%, despite more than 2,000 round trips per week. [full text]
- **Avramov, Chordia & Goyal (JF 61(5), 2006):** reversals are **mainly in losers** and largest in **high-turnover, low-liquidity stocks**; "contrarian trading strategy profits are smaller than the likely transactions costs." [full text, working paper]
- **Nagel (RFS 25(7), 2012), "Evaporating Liquidity":** 5-day reversal returns proxy for liquidity-provision returns. Over 1998–2010 they ran ~**1%/day in 1998 and 2000/01**, decayed to **<0.2%/day by 2007**, then "exploded" in 2008. **VIX predicts reversal returns and conditional Sharpe**; no losing 3-month period before costs. A 1-point VIX rise predicts **+9 bp** of reversal return (Drechsler et al.) [secondary]. [full text, NBER w17653]
- **Rulebook implication:** short-term mean reversion is a **liquidity-provision trade**: best in **high-VIX regimes** and on losers, concentrated in illiquid names where costs eat it. On liquid large caps require elevated VIX and cheap execution (grade B). "Oversold" oscillators are the folk version of this effect.
- URLs: https://ideas.repec.org/a/bla/jfinan/v45y1990i3p881-98.html ; https://www.nber.org/system/files/working_papers/w2533/w2533.pdf ; https://users.nber.org/~confer/2004/mmsu04/goyal.pdf ; https://www.nber.org/papers/w17653.pdf

### 1.16 Long-term reversal: De Bondt & Thaler (1985)
- **Claim:** Prior 36-month losers (35-stock portfolios) beat prior winners by about **25% (24.6%) over the next 36 months**, 1932–1977 formation dates. The gain is concentrated in January, and there is no reversal for 1-year formation periods. [secondary: Alpha Architect; abstract only]
- JT2001 confirms negative momentum-portfolio returns in **years 4–5** after formation.
- **Rulebook implication:** 3–5 year reversal is a slow, value-like effect, irrelevant for swing trading; it argues against holding momentum positions beyond ~12 months.
- URLs: https://breesefine7110.tulane.edu/wp-content/uploads/sites/16/2015/10/Debondt-and-Thaler.pdf ; https://alphaarchitect.com/2015/01/quantitative-momentum-research-long-term-return-reversal/

### 1.17 Momentum regimes and crashes: Cooper, Gutierrez & Hameed (2004); Daniel & Moskowitz (2016); Barroso & Santa-Clara (2015)
- **CGH (JF 59(3)):** market state = sign of the lagged multi-year market return (main spec 36 months). 1929–1995: **0.93%/month after UP markets vs −0.37% after DOWN**; UP-market momentum reverses long-run; international replications mixed. [abstract only]
- **Daniel & Moskowitz (JFE 2016; NBER w20439):** 1927–2013 winner decile +15.3%/yr excess, loser −2.5%; WML Sharpe 0.71 vs market 0.40; CAPM alpha 22.3%/yr (t = 8.5). **Crashes occur in "panic" states** (after declines, with high volatility, during rebounds): the loser decile rose **232%** in July–August 1932, and **163%** in March–May 2009 while the market rose 26%. Bear indicator: CRSP VW 24-month return below 0, when WML beta falls ~1.13. Dynamic mean/variance scaling **roughly doubles alpha and Sharpe** (1.18 across markets). [full text]
- **Barroso & Santa-Clara (JFE 2015):** scaling by momentum's own realized volatility "virtually eliminates crashes and nearly doubles the Sharpe ratio" [abstract]; 0.53 → 0.97 over 1927–2011 [secondary: ETF.com].
- **Rulebook implication (hard rule):** when the market's 24-month return is negative *and* volatility is high, cut or switch off long-short momentum, avoid shorting past losers into a V-shaped rebound, and volatility-target momentum books.
- URLs: https://academicnewsletter.sufe.edu.cn/info/361185 ; https://www.nber.org/system/files/working_papers/w20439/w20439.pdf ; https://ciencia.ucp.pt/en/publications/momentum-has-its-moments/

### 1.18 Volatility-managed portfolios: Moreira & Muir (2017); Cederburg et al. (2020)
- **Moreira & Muir (JF 2017; NBER w22208):** [full text]
  - **Rule:** scale exposure by the inverse of the previous month's realized variance.
  - **Market factor:** alpha of **4.9% per year**, appraisal ratio 0.33, and a **25% higher Sharpe ratio**. Mean-variance utility gain about 65%.
  - **After costs:** survives realistic costs, including at the 98th-percentile VIX.
  - Lagged volatility barely predicts returns but strongly predicts future volatility.
- **Cederburg, O'Doherty, Wang & Yan (JFE 138, 2020):** Across **103 equity strategies**, real-time volatility-managed versions do not systematically beat unmanaged ones. The cause is unstable spanning regressions. Out-of-sample Sharpe is lower for 72 of 103 [secondary: CXO]. Momentum, ROE and betting-against-beta degraded less [secondary: Alpha Architect].
- **Rulebook implication:** Volatility scaling is a sound **risk** tool, robust for keeping position risk constant. Its **alpha** is not robust out of sample except for momentum-type books. Use it for sizing, not as a signal. Grade B.
- URLs: https://www.nber.org/system/files/working_papers/w22208/w22208.pdf ; https://www.lehigh.edu/~xuy219/research/COWY.pdf

### 1.19 Volume: Lee & Swaminathan (2000); Gervais, Kaniel & Mingelgrin (2001); Llorente, Michaely, Saar & Wang (2002)
- **Lee & Swaminathan (JF 55(5)):** [full text]
  - **Setup:** NYSE/AMEX, 1965–1995; volume measured as turnover.
  - **Momentum spread by volume (J = 6, K = 6):** **1.46% per month in high-volume stocks versus 0.54% in low-volume stocks** (difference 0.91% per month, about 11% annualized).
  - **But high-volume winners reverse faster.** Low-volume losers beat high-volume losers by 1.02% per month (J = 9, K = 6), and low-volume winners beat high-volume winners by 0.26% per month.
  - Momentum reverses within 5 years. Over long horizons, the "early-stage" combination (long low-volume winners, short high-volume losers) is best.
  - High turnover marks glamour stocks.
- **Gervais, Kaniel & Mingelgrin (JF 56(3)):** [full text, Wharton WP 1-99]
  - **Setup:** NYSE, 1963–1996, 50-day windows. Formation-day volume is compared with the prior 49 days; top and bottom 10%.
  - **Result:** the **high-volume return premium**. Zero-cost returns are **0.35% (1 day) to 0.94% (20 days)** for small stocks and 0.12%–0.50% for large stocks (t ≈ 3 or higher).
  - The premium is **stronger when the volume spike comes without an extreme return**: 10- and 20-day returns of 1.55% and 2.02% for small stocks in the weekly sample. It appears permanent and is attributed to visibility.
- **Llorente et al. (RFS 15(4)):** High-volume days with *hedging* trades are followed by **reversal**. High-volume days with *speculative/informed* trades are followed by **continuation**. Which one dominates depends on information asymmetry. [abstract only]
- **Rulebook implication:** classic "volume confirms the breakout" is **not** supported (LMW: volume trend adds little; Bender et al.: H&S raises volume without predicting direction). Supported instead: (1) an abnormal-volume spike *without* a big price move is mildly bullish over the next month; (2) momentum is stronger but shorter-lived in high-turnover names; (3) volume helps separate informed moves (continue) from liquidity moves (reverse). **Grade C as "confirmation."**
- URLs: https://www.johnhcochrane.com/s/lee_swaminathan_returns_volume_JF.pdf ; https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/9901.pdf ; https://www.johnhcochrane.com/s/llorente_michaely_saar_wang_volume_rfs.pdf

### 1.20 Support/resistance and round numbers: Osler (2000, 2005); Kavajecz & Odders-White (2004); Bhattacharya, Holden & Jacobsen (2012)
- **Osler (2000, FRBNY EPR), "Support for Resistance":** S/R levels published by **6 FX firms**, January 1996–March 1998 (mark, yen, pound), 1-minute data. Rates **bounced off published levels 60.8% of the time vs 56.2% for random levels**; published beat random in all 16 firm-currency pairs, with predictive power lasting at least 5 business days; firms disagreed widely. Over 70% of levels end in 0 and 96% in 0 or 5. [full text]
- **Osler (FRBNY SR150), stop-loss cascades:** trends accelerate when price reaches levels where **stop-loss orders cluster** (just beyond round numbers); the effect lasts hours, not days. [full text, abstract]
- **Kavajecz & Odders-White (RFS 17(4)):** equity S/R and MA signals **locate depth already resting in the limit order book**, i.e. liquidity rather than direction. [abstract only]
- **Bhattacharya, Holden & Jacobsen (Mgmt Sci 58(2)):** across >100M US trades, liquidity demanders net **buy just below and sell just above round numbers**, at a cost of ~$1B/yr. [abstract only]
- **Rulebook implication:** S/R and round numbers mark **where order flow clusters** (slightly more bounces, faster breaks). The evidence is intraday and FX-heavy, with no peer-reviewed profitable equity S/R strategy after costs. Use S/R for **execution and stops** (stops away from obvious round numbers, limits in front of them), not alpha (grade C).
- URLs: https://www.newyorkfed.org/medialibrary/media/research/epr/00v06n2/0007osle.pdf ; https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr150.pdf ; https://ideas.repec.org/a/oup/rfinst/v17y2004i4p1043-1071.html ; https://ideas.repec.org/a/inm/ormnsc/v58y2012i2p413-431.html

### 1.21 Earnings drift, gaps and overnight effects: Martineau (2022); Chan, Jegadeesh & Lakonishok (1996); Lou, Polk & Skouras (2019)
- **Martineau (Critical Finance Review 11, 2022), "Rest in Peace PEAD":** "For large stocks, PEAD have been non-existent since 2006 but has only disappeared recently for microcap stocks." Prices of all-but-microcaps are now about 6 times more responsive on the announcement day than in 1984–1990. Disputed by later papers (Dickerson, Julliard & Mueller) on design grounds. [full text, abstract]
- **Earnings-gap implication:** A post-earnings gap in a large cap is mostly fully priced on day 0–1. "Gap-and-go" continuation in large caps after 2006 should be presumed **zero** unless our own tests show otherwise. CJL (1996) showed earnings-surprise momentum was real in 1977–1993, and it decayed later.
- **Lou, Polk & Skouras (JFE 134, 2019), "A Tug of War":** Across 14 strategies, profits are earned **entirely overnight** (momentum and others) or **entirely intraday**, with opposite-signed returns in the other session. Momentum profits arise overnight. Institutions trade intraday against momentum. [full text, abstract]
- **Rulebook implication:**
  - For momentum entries, close-to-close or close-to-open capture matters. Entering at the open gives up the overnight leg.
  - Fading gaps or trading intraday trends must be tested separately for the overnight and intraday components.
- URLs: https://cfr.ivo-welch.info/published/papers/martineau2021rest.pdf ; https://ideas.repec.org/a/bla/jfinan/v51y1996i5p1681-1713.html ; https://personal.lse.ac.uk/polk/research/TugOfWar.pdf

### 1.22 Breakouts (Donchian, 52-week, all-time-high)
- **BLL's TRB rules** were profitable in the DJIA before 1986 but decayed like the MA rules. STW's channel and S/R rules were part of the universe that failed in 1987–1996.
- **Zarattini, Pagani & Wilcox (2025, SSRN 5084316), "Does Trend-Following Still Work on Stocks?":** [secondary: Concretum Group, Harbourfront summaries]
  - Practitioner working paper (not peer-reviewed; exact returns not verified): survivorship-free liquid US stocks, 1950–2024, >66,000 long-only trades. Entry on a **close at or above the all-time high**; exit on a never-lowered ATR trailing stop. Under 7% of trades produce most profits; reported to hold out of sample in 2005–2024; turnover needs control.
- **Rulebook implication:** Breakouts overlap heavily with 52-week-high and TSMOM signals. The edge, if any, comes from a **heavy right tail** (a few huge winners), so position rules (no early profit-taking, wide trailing stops) matter more than entry precision. Grade C on standalone peer-reviewed evidence.
- URL: https://concretumgroup.com/does-trend-following-still-work-on-stocks/

### 1.23 Oscillators / RSI / Connors-type rules
- **No peer-reviewed US-equity test** of RSI overbought/oversold with data-snooping control was found. STW's 7,846-rule universe contains no oscillators. Park & Irwin's surveyed studies find oscillators no better than MA rules in developed equities.
- **Practitioner out-of-sample check (CXO Advisory, 2009):** XLK above its 200-day MA with 2-day RSI < 30 gave 24 trades at +0.25%/trade before frictions ("probably... net unprofitability"); an SPY variant gave 12 trades at +0.69%/trade and no signals after 2007. In-sample claims "may have substantial data snooping bias."
- **Rulebook implication:** The only defensible content of "oversold" is **short-term reversal / liquidity provision** (§1.15). Expect it to work in high-VIX regimes and on losers, and to be small after costs on liquid ETFs. As a standalone signal: grade D. As a reversal proxy inside a trend filter: test it, but expect C at best.
- URL: https://cxoadvisory.com/?p=3932

### 1.24 Divergences, Fibonacci, Elliott waves, Gann
- **Divergences** (price versus RSI or MACD): no peer-reviewed tests found.
- **Fibonacci:** Osler (2000) lists the "50% rule" and 38.2/61.8% retracements as dealer conventions but tests published levels, not ratios. Gurrib et al. (Financial Innovation 2022) report favorable results on US energy stocks and crypto, from a narrow sample with no multiple-testing control [abstract only]. A Pakistan cement study matched only 27% of supports and 36% of resistances to Fibonacci levels.
- **Elliott waves:** only small or regional studies (e.g., a 2017 USD/EUR paper), with subjective wave labelling that cannot be tested out of sample. No mainstream finance-journal tests.
- **Gann:** no academic tests found.
- **Rulebook implication:** **Grade D. Exclude these as signals.** If a Fibonacci level coincides with a round number or a prior swing high or low, credit the round-number or swing order-clustering effect (§1.20), not the ratio.
- URLs: https://ideas.repec.org/a/spr/fininn/v8y2022i1d10.1186_s40854-021-00311-8.html ; https://ideas.repec.org/a/ibn/ibrjnl/v10y2017i6p1-18.html

### 1.25 Data snooping, publication decay and costs: McLean & Pontiff (2016); Harvey, Liu & Zhu (2016); Hou, Xue & Zhang (2020); Chordia, Subrahmanyam & Tong (2014)
- **McLean & Pontiff (JF 71(1)):** [full text]
  - Across 97 predictors, returns are **26% lower out of sample** (the upper bound on data mining) and **58% lower after publication**. That implies about 32% is lost to publication-informed trading.
  - Bigger in-sample returns decay more. Returns are higher in high-idiosyncratic-risk, illiquid stocks.
- **Harvey, Liu & Zhu (RFS 2016; NBER w20592):** Given extensive data mining, a new factor "needs to clear a much higher hurdle, with a t-ratio greater than 3.0... most claimed research findings in financial economics are likely false." [full text]
- **Hou, Xue & Zhang (RFS 33(5), 2020):** With NYSE breakpoints and value weighting, **65% of 452 anomalies fail at t = 1.96, and 82% fail at t = 2.78**. Replicated anomalies are much smaller than originally reported. Momentum and value are among the survivors [secondary: Alpha Architect].
- **Chordia, Subrahmanyam & Tong (JAE 58, 2014):** Anomaly returns roughly **halved after decimalization (2001)**. The decline is linked to hedge fund assets, short interest and turnover. [abstract only]
- **Rulebook implication:**
  - Require **t ≥ 3** (or a Reality Check/SPA/FDR-adjusted p < 0.05) on *our own* grid.
  - Haircut backtested Sharpe by 50% or more for any rule found by search.
  - Report value-weighted or liquid-universe results.
  - Assume post-2001 effects are about half of pre-2001 effects.
- URLs: https://Www.Gwern.net/doc/economics/2016-mclean.pdf ; https://www.nber.org/system/files/working_papers/w20592/w20592.pdf ; https://ideas.repec.org/a/oup/rfinst/v33y2020i5p2019-2133..html ; https://ink.library.smu.edu.sg/lkcsb_research/4735

---

## 2. Evidence grade by TA family

Grades:
- **A:** robust, replicated, survives costs.
- **B:** some support, or regime-dependent.
- **C:** weak or mixed.
- **D:** no evidence, or negative.

The grade refers to US stocks/ETFs unless noted.

| TA family | Grade | One-line justification |
|---|---|---|
| Trend / MA timing (index level, long window: 10-month or 200-day) | **B** | Cuts volatility (about 30%) and max drawdown (Faber 83.7%→42.2%). Out-of-sample net Sharpe gain is only about +7–12% (Zakamulin) and comes from a few bear markets. Short-window daily MA rules are **D** (STW, Bajgrowicz & Scaillet). |
| Time-series momentum | **A** (diversified multi-asset futures) / **B** (single US index or ETF) | 137 years positive in every decade (HOP), alpha t = 5.4–8.0 (MOP). Asset-by-asset evidence is weak (Huang et al. 2020), and post-2000 net Sharpe is lower (0.62 for 2000–13). |
| Cross-sectional momentum (12-1 / 6-6) | **B** (A pre-2000) | About 1%/month and replicated out of sample in the 1990s (JT2001), surviving the HXZ replication. But crash-prone (DM), dead in January, after DOWN markets (CGH) and in 2001–2015 (t = 0.70). |
| 52-week-high proximity | **B** | George & Hwang 0.45%/month (1.23% ex-January), no long-run reversal; index version from Li & Yu. 2001–2015 t = −1.26 (AKS). |
| Breakouts (Donchian / range / ATH) | **C** | BLL TRB decayed after 1986. Modern support is practitioner-only (Zarattini et al., not peer-reviewed). Mostly duplicates momentum and 52-week-high signals. |
| Chart patterns (H&S, double top, rectangles) | **C** | LMW shows distributional information (stronger on Nasdaq), not profits. Savin et al. found 5–7%/yr (1990s, needs shorts, mostly negative momentum). Bender et al.: no profitable predictive power. |
| Candlesticks | **D** | Marshall et al.: 28 signals on DJIA stocks, 1992–2002, no predictive power. Positive studies are short-sample or come from pattern searches. |
| Oscillators / RSI overbought-oversold | **D** | No peer-reviewed US-equity support with snooping control. Practitioner out-of-sample tests are marginal after frictions. Any value is just short-term reversal. |
| Short-term reversal (1-week / 1-month) | **B** | Large gross effect (Lehmann, Jegadeesh), but concentrated in illiquid losers and smaller than costs (ACG). Pays mainly when the VIX is high (Nagel). |
| Volume confirmation | **C** | Volume adds little to patterns (LMW), and high-volume winners reverse faster (Lee & Swaminathan). Narrow positive findings: abnormal volume without a price move is bullish (GKM), and volume helps classify informed vs liquidity moves (Llorente et al.). |
| Support / resistance & round numbers | **C** | FX intraday bounce 60.8% vs 56.2% random (Osler). Order clustering at round numbers in equities. No evidence of profitable equity S/R strategies after costs. |
| Divergences | **D** | No peer-reviewed tests found. |
| Fibonacci retracements | **D** | Only narrow, uncontrolled studies. Any effect is better explained by round-number or swing-level order clustering. |
| Elliott waves | **D** | Subjective and untestable out of sample. Only small regional studies. |
| Gann | **D** | No academic tests found. |
| *(supporting)* Volatility-managed sizing | **B** | Market alpha 4.9% and Sharpe +25% (Moreira & Muir), but real-time out-of-sample is not robust across 103 strategies (Cederburg et al.). Use for risk, not alpha. |
| *(supporting)* MA-distance 21/200 (cross-sectional) | **B** | More than 12%/yr, significant 2001–2015 (t = 2.80) when momentum, 52-week high and trend were not. Single study. |
| *(supporting)* PEAD / earnings-gap drift | **C** (D for large caps after 2006) | Martineau: gone in large caps since 2006 and in microcaps recently. Contested. |

---

## 3. Conditions under which signals fail

Numbers are in the §1 entries cited.

1. **Long, calm bull markets.** Trend/MA timing lags buy-and-hold for years: 1975–1999 on the S&P (§1.11), and about half of all years under Faber's rule. Judge timing rules over full cycles and on drawdown/Sharpe, never on a 2–5 year window.
2. **No deep bear market in the window.** Timing alpha comes almost entirely from 1930–31, 1973–74, 2001–02 and 2007–08 (§1.11).
3. **Fast V-shaped crash and rebound.** Slow trend rules exit and re-enter late. *(Inferred from 1–2; not a published 2020-specific result. Test on 2018-Q4, 2020-Q1 and 2022.)*
4. **Panic rebounds kill momentum.** When the 24-month market return is below 0 and volatility is high, beaten-down losers surge: 1932 and 2009 (§1.17). Momentum also loses after DOWN market states (−0.37%/month versus +0.93% after UP states).
5. **January.** Losers beat winners by about 2.9% (§1.9). Pause or halve momentum and 52-week-high books.
6. **Volatility cuts both ways.**
   - High VIX *helps* short-term reversal (§1.15).
   - High VIX *hurts* momentum (§1.17).
   - MA timing has bigger gross alpha on high-volatility stocks, which are also the costliest to trade (§1.12).
   - TSMOM does best in extreme market months (§1.10).
7. **Costs and turnover.** The rules that win a search are short-window, high-turnover rules: the 5-day MA had a 0.27%/trade break-even (§1.2). One-way costs of 5–35 bp erase out-of-sample DJIA rule profits (§1.3). Reversal profits are smaller than effective spreads in the names where they are largest (§1.15).
   - **Assumed costs:** at least 2–5 bp per side for SPY/QQQ, 10–20 bp for large caps, 30–100+ bp for small or illiquid names, plus slippage on gap opens.
   - **Test:** reject any rule whose net Sharpe at twice the assumed cost is not positive.
8. **Small caps and illiquidity.** Effects concentrate in microcaps and illiquid "young" markets (§1.4, §1.6, §1.25). Part of that is untradeable stale-price autocorrelation. Always report results for a liquid universe (top 500–1000 by dollar volume, price above $5) separately.
9. **Crowding and publication.** Effects drop about 58% after publication and roughly halved after 2001 decimalization (§1.25). Classic DJIA rules died after about 1986–1990, and PEAD died in large caps around 2006. In 2001–2015 the US momentum, 52-week-high and trend signals were insignificant (§1.12). Use 2010–2026 as the primary evaluation window.
10. **Statistical illusions:**
    - best-of-N selection (STW: 17.2% in-sample became 2.8% out of sample);
    - pooled-regression TSMOM (§1.10);
    - discretionary pattern labelling;
    - treating "distribution differs" as "profitable" (§1.6).
    - **Hurdle:** t ≥ 3, or a Reality Check/SPA/FDR-adjusted p < 0.05 over the full grid searched.

---

## 4. Parameterizations worth testing on 2000–2026 US daily data

**Protocol for every test:** point-in-time, survivorship-free universes; signal at close t, trade at close t+1 (open t+1 reported separately); costs per §3 item 7; **holdout 2019-01 to 2026-10, untouched until the grid is frozen**; report CAGR, volatility, Sharpe, max drawdown, turnover, break-even cost, Reality Check/SPA p-value over the grid, and subperiods (2000–02, 2003–07, 2008–09, 2010–19, 2020, 2022, 2023–26).

### 4.1 Index/ETF trend overlays (SPY, QQQ, IWM, sector SPDRs, TLT, GLD)
1. **Faber:** month-end close vs 10-month SMA, long or T-bills; also 8 and 12 months to check for a plateau rather than a peak.
2. **BLL (1,200,1%):** daily close vs SMA200 ± 1%; also weekly evaluation to cut whipsaw.
3. **TSMOM:** sign of the 12-month excess return, monthly; plus the HOP 1/3/12-month blend at 10% target volatility.
4. **Neely MA(1,12)/MA(2,12)** on monthly closes as a risk-on/off flag for other strategies.
5. **50/200 crossover** as a benchmark only.
- *Expectation:* lower drawdown and higher Sharpe than buy-and-hold over full cycles, similar or lower CAGR, lagging in 2010–2019. Compare IWM/QQQ with SPY (Hsu & Kuan).

### 4.2 Volatility scaling (sizing layer, not a signal)
- Weight = target (10–15%) ÷ realized volatility from 20-day or 1-month variance (Moreira & Muir), capped at 1.0–1.5×; also EWMA with a 20–60 day half-life. Apply to buy-and-hold, to 4.1 and to 4.3. Expect a robust risk benefit and fragile alpha (Cederburg et al.).

### 4.3 Cross-sectional momentum (S&P 500 / S&P 1500 constituents)
1. **12-1** (252-day return skipping the last 21 days), decile/quintile, monthly rebalance, equal and value weights; also 6-1 with a 6-month hold.
2. **Crash filter (Daniel & Moskowitz):** if the 24-month SPY return is below 0 **and** 126-day market volatility is above its 80th percentile, drop the short leg or cut the book 50–100%.
3. **Vol-scaled WML (Barroso & Santa-Clara):** scale by target ÷ 126-day realized WML volatility.
4. **Market-state filter (CGH):** trade only if the trailing 36-month (check: 12-month) market return is above 0.
5. **January:** skip or halve exposure. **Overnight vs intraday:** decompose returns and compare close vs open entry (Lou, Polk & Skouras).

### 4.4 52-week high and MA distance
1. **George & Hwang:** price ÷ 252-day high, top 30% long (optional bottom 30% short), 6-month overlapping holds; also as a filter (take long trend signals only within 5–10% of the 52-week high).
2. **MAD:** MA21 ÷ MA200 decile sort, monthly; compare long-only top decile with long-short.
3. **Li & Yu index state:** SPY nearness to its 52-week high vs its all-time high as 1–12 month predictors.

### 4.5 Breakouts
1. **All-time-high or 252-day-high close breakout** with a k × ATR(20) trailing stop, k ∈ {3, 5, 8, 10}, never lowered; liquid universe (dollar volume > $20M, price > $10). Report the trade P&L distribution (the thesis rests on the top ~5–7% of trades).
2. **Donchian 20/55-day entry, 10/20-day exit** on sector ETFs. Measure redundancy against 4.3 and 4.4.

### 4.6 Short-term reversal / "oversold"
1. **Weekly reversal (Lehmann):** S&P 500 stocks ranked on prior 5-day return net of industry; long the bottom decile, 5-day hold; also long-only losers (ACG).
2. **VIX-conditioned (Nagel):** trade only when VIX > 25 (also 20, 30, and above its 1-year median). Expect returns to scale with VIX.
3. **Connors-style RSI(2) on SPY/QQQ:** close > SMA200 and RSI(2) < {5, 10, 15}, buy at the close; exit when RSI(2) > 70, close > SMA5, or after 10 days; 2–5 bp cost. Small expected edge; demand t ≥ 3 on the holdout.

### 4.7 Volume
1. **GKM premium:** day-t volume above the 90th percentile of the prior 49 days with |return| < 1σ; forward 1/5/20-day returns vs a matched control.
2. **Lee & Swaminathan:** 12-1 momentum × turnover terciles; test "early-stage" (long low-volume winners, short high-volume losers) over 6–12 months.
3. **Falsification:** do breakouts with volume > 1.5–2× the 50-day average beat those without? The literature predicts no.

### 4.8 Patterns, candles, S/R and earnings gaps (mostly falsification tests)
1. **LMW kernel-regression detection** of HS, IHS, double tops/bottoms and rectangles on S&P 500 stocks; 1–20 day conditional vs unconditional returns, bootstrapped.
2. **Candlesticks:** all 1-day and 3-day patterns, 1–10 day holds, FDR control. Expect null.
3. **Round numbers:** next-day returns after closes just above vs just below whole-dollar or $X0 levels, and breaks of prior swing highs. Use for stop and limit placement, not alpha.
4. **Earnings gaps:** top/bottom-decile 3-day announcement return, or a gap above 2σ, vs the 60-day post-event return; split by size and by pre/post-2006. Prior: about zero for large caps (Martineau).

---

*Sources were fetched 2026-10-31. Every number above is labelled by where it came from. Gaps that could not be filled: BLL's own tables (paywalled), Jegadeesh (1990) magnitudes, the full CGH tables, and exact returns in Zarattini et al. (2025).*
