# Feedback-Loop Iteration Log

Each iteration = **hypothesis → coded test → measured result → decision → rulebook change**.
Two kinds of iterations are logged:

* **Meta-iterations (#1-#60+)**: changes to the platform, the learning agents, the rulebook structure and its parameters, blind tests.
* **Rule-level tests (246)**: 123 coded TA rules × 2 periods (train 2000-2014, validation 2015-2019), table at the bottom. Each rule test is its own hypothesis-test-decision cycle.

## The loop and its guard-rails

```
 books / videos / papers ──► hypothesis ──► code rule (tagym/signals*.py)
        ▲                                           │
        │                                  TRAIN 2000-2014, ticker group A (60%)
        │                                           │  verdict (pre-registered)
 rulebook edit ◄── decision ◄── VALID 2015-2019 (group A) ◄┘
        │
        └─► (once, at the end) LOCKED TEST: 2020-2026 + unseen ticker group B (40%)
```

* **Pre-registered verdicts** (fixed before any test): `SIGNAL` needs net excess > 0 and min(event-t, calendar-t) ≥ 3.0 (Harvey-Liu-Zhu multiple-testing hurdle); `WEAK` ≥ 2; `REVERSED` ≤ −2; `VOL_ARTIFACT` if the vol-matched t collapses. A train `SIGNAL` must keep its sign with t ≥ 2 in validation.
* **Statistics**: entry at next open; excess vs the equal-weight universe *and* vs a volatility-tercile-matched benchmark; per-date clustering with Newey-West errors; calendar-time portfolios; 10 bps per side costs; events in the last 90 days of a period are embargoed (their labels would leak).
* **Lock**: the test period and group-B tickers raise `PermissionError` unless explicitly unlocked; every unlock is appended to `test_access_log.md`.
* **Survivorship**: today's S&P 1500 members only (delisted names missing). All stock tests use *excess* returns vs the same biased universe; market-timing conclusions come from indices/ETFs, which have no survivorship bias.

---

## Phase A — Build and calibrate the judge

| # | Iteration | Result | Decision / change |
|---|---|---|---|
| 1 | Download 1,503 S&P 1500 stocks + 36 ETFs/indices (1995-2026, split/dividend adjusted); bad-print filter; tradeable = price ≥ $5 and 20-day median $-volume ≥ $5M | 1,502 tickers with data, 8,011 days | adopted |
| 2 | **Validate data against TradingView MCP** (NVDA Sep-2008, JPM Mar-2020, SPY Oct-2026) | yfinance/TV ratio constant within each window (0.9147, 0.8368 = dividend adjustment); SPY last 5 bars identical to the cent | data accepted; daily returns identical |
| 3 | Positive control: a cheating look-ahead signal | t = +39, hit 95% | evaluator detects real edges |
| 4 | 5 random placebo signals | calendar-portfolio t biased negative by cost drag (−2.5%/yr) | **fix**: verdict t-stats on gross excess; net reported separately |
| 5 | 30 random placebos (calibration) | event-t sd 1.16, calendar-t sd 0.83, mean ≈ 0 | keep min(event t, calendar t) ≥ 3 → conservative hurdle |

## Phase B — First sweep of popular rules

| # | Iteration | Result | Decision |
|---|---|---|---|
| 6 | Batch 1: 68 popular rules on TRAIN, EW benchmark | 1 SIGNAL (RSI14 crossing above 70 is *bearish*), almost everything else NO_EDGE; trend/breakout rules negative in 2000-2014 | need regime + volatility diagnostics |

## Phase C — Learning agents (reinforcement learning)

| # | Iteration | Result | Decision |
|---|---|---|---|
| 7 | **RL v1**: tabular Thompson-sampling contextual bandit, 5,832 joint TA states, reward = 20-day excess − cost, walk-forward 2000-2014 | −0.21% per long decision; only 87 states had ≥500 observations; best/worst learned states sorted by **volatility**, not TA | discovered beta/volatility confound |
| 8 | Evaluator upgrade: volatility-matched benchmark + `VOL_ARTIFACT` verdict | all later tests report vol-matched t | adopted |
| 16 | **RL v2**: Bayesian linear Thompson bandit on one-hot TA features × market regime, vol-matched reward, online 2000→2019 (decide before outcome is revealed) | long 36% of the time in 2000 → <8% after 2006 (*it learned to abstain*); net reward −0.13% (2000-14), +0.05% (2015-19), not significant; IC 0.012-0.025. Learned interactions: RS leaders good only in bull regimes; laggards/oversold rebound in bear regimes | `NO_SIGNAL` as default; regime hypotheses → batch 3 |
| 19 | **ML ceiling**: gradient boosting on 32 TA features, 5-year rolling training, 15 yearly out-of-sample tests | rank-IC 0.016 (2005-14), 0.018 (2015-19); top-decile 20-day vol-matched excess +0.16% / +0.31% vs 0.20% round-trip cost | even all features combined ≈ break-even after costs → rulebook must not promise alpha |

## Phase D — Market-level (index/ETF) timing — no survivorship bias

| # | Iteration | Result | Decision |
|---|---|---|---|
| 9 | S&P 500 1929-1999 & 2000-2019: 10-month SMA, daily SMA200, SMA200±2%, SMA50>200 state, 12-month TSMOM, SMA50 | slow rules: max DD −86%→−49-52% and −57%→−21%, Sharpe up in both eras; daily SMA50 lost money 2000-19 | regime layer uses slow rules only |
| 10 | 22 ETFs (sectors, international, bonds, gold, REITs) 2000-2019 | 10-month SMA: MaxDD better on 95%, Sharpe on 64%, CAGR −0.8%/yr; daily SMA200: Sharpe worse on 64% | regime = 10-month SMA **and** SMA50>SMA200 |
| 11 | Dow Theory (Hamilton/Nelson) on DJIA+DJT, 4 swing thresholds × 3 variants | only 6% threshold beats B&H (Sharpe 0.68-0.75 vs 0.54); confirmation helps at 4-6%, hurts at 8-10%; BEAR state: 6-month fwd −3.2% vs +6.1% | WEAK/fragile → context only |

## Phase E — What TA really predicts: risk

| # | Iteration | Result | Decision |
|---|---|---|---|
| 12 | 8 technical states × 2 periods: next-60-day P(≥20% drawdown), forward vol, returns | below falling SMA200: 23.9% vs 11.6% (train), 15.5% vs 7.9% (valid); within 5% of 52w high: 7.1% vs 18.0%; returns ≈ equal | **health layer** created |
| 13 | Same, *within* volatility terciles | effect persists in every tercile (1.4-2.9x) | health is not just volatility in disguise |
| 20 | 7 exit rules on 30,000 random entries × 2 periods | 8% stop: worst-1% −46%→−11%, P(loss>20%) 7.6%→0.2%, mean 2.6%→1.5%; MA exits worst | stops = insurance (Section 8) |
| 21 | Per-stock trend switching (3 variants × 2 periods) | Sharpe lower for ~80% of stocks (biased toward B&H by survivorship) | don't switch single stocks on the 200-day |

## Phase F — Full rule sweeps (books, regime, YouTube)

| # | Iteration | Result | Decision |
|---|---|---|---|
| 14-15 | Batch 2: 77 rules (MA, breakouts, momentum, oscillators, reversal, volume, divergence, S/R, 12 candlesticks, 9 chart patterns) TRAIN + VALID | train 68 NO_EDGE / 4 REVERSED / 4 WEAK / 1 SIGNAL; valid 75 / 1 / 1 / 0; **no bullish rule confirmed** | Section 6 NOT-a-signal list |
| 17-18 | Batch 3: 40 rules from Livermore/Lefèvre, Selden, Wyckoff, Schabacker + regime + confluence | 1 train SIGNAL (5 up-closes bearish) **failed validation**; REVERSED: RS leaders in bear markets −1.8%/mo (t −4.3); leader-of-leading-group −0.8%/mo (valid t −3.9); shock-day resilience −0.9% (t −3.2) | Avoid rules A1, A2, A4 |
| 41 | 8 YouTube "claimed" systems, trade simulation vs same-date random control | win rates 37-71% (claims 86-94%); breakout entries worse than random (−0.9%/−0.2% per trade) | Rule A3; claims marked unreliable |
| 42 | Event-study re-test of the best YouTube candidate (RSI10<30 above SMA200) + 4 ablations + MACD/200EMA | +0.15%/+0.14% 5-day excess, t 1.4/0.9 → NO_EDGE; no-trend-filter and downtrend versions ≈ 0 or negative | **lesson**: exit-rule-dependent trade sims flatter signals (controls exit faster); event studies are the arbiter. PULLBACK kept as timing only |

## Phase G — Rulebook assembly and fine-tuning

| # | Iteration | Result | Decision |
|---|---|---|---|
| 22 | Rulebook v1 classifier (regime → health → extension → decision table) | P(dd≥20%/60d): BULLISH 7.0%/5.5%, NO_SIGNAL 14.7%/9.4%, BEARISH 24.3%/15.7%; excess returns ≈ 0 | structure kept |
| 23-40 | Fine-tuning grid: healthy cut-off (−10/−15/−25% from high) × broken cut-off (−30/−40/−50%) × extension filter on/off, TRAIN then VALID (18 settings) | every setting separates risk 2.5-4x (robust, not over-fit); best: −10% & extension on (3.97x train, 3.21x valid) | **v2** parameters |
| 43 | Consistency: single-stock live engine vs panel engine on 190 random cases | 184/190 → mismatches from cross-sectional 5-day rank (not computable for one stock) | extension redefined (ATR-scaled 5-day move / 5 up closes) → 190/190 |
| 44 | v2 re-evaluated | BULLISH 6.6% / 5.4%, BEARISH 24.3% / 15.7% crash odds; worst-5% −16.9% vs −35.1% | frozen for blind tests |
| 45 | Health classes on 29 ETFs 2000-2019 (no survivorship bias) | P(dd≥10% / ≥20% in 60d): HEALTHY+RISK_ON 11.8% / 1.4%; BROKEN 35.1% / 13.9%; any RISK_OFF 35.6% / 15.4%; 60-day return 2.2% vs 1.4% vs 0.7% | risk layer confirmed on survivorship-free instruments (and returns are lower in bad states, which survivor stocks hide) |
| 46 | Risk calibration: P(dd≥20%/60d) for every decision row × regime, train & valid | D3/RISK_ON 6.0%; D2 15.6-20.8% (31.7% in 2000-14 RISK_OFF); D6 11-17% | calibrated table in RULEBOOK §5 and `live.py` |

## Phase H — Blind tests of the rulebook *as written* (agents never see tickers, dates or outcomes)

| # | Iteration | Result | Decision |
|---|---|---|---|
| 47 | **Blind round 1**: fresh agent + RULEBOOK v2.0 + 40 anonymised VALID-period cases (answer key stored outside its reach) | agent = engine on **39/40**; BULLISH n=18: 60d excess +5.4%, 0% had a ≥20% drawdown; BEARISH n=10: +1.5%, 10%; NO_SIGNAL n=12: −0.4%, 8%; risk-flagged 9.1% vs 3.4% drawdown rate. The 1 miss: text said "RSI just crossed 70" while engine uses RSI ≥ 70. Agent logged **17 ambiguities** | rewrite as v2.1 |
| 48 | Agent-suggested BROKEN clause B3 (C<SMA200 & SMA50<SMA200 & ≥25% off high) tested on TRAIN/VALID | BEARISH crash odds 24.30→24.42% (train), 15.66→15.82% (valid); NO_SIGNAL odds down in both | adopted (v2.1) |
| 49 | RULEBOOK v2.1: exact feature table, inclusive thresholds, one EXTENDED definition (any of 4), evaluation order, ATR≥3% high-vol proxy (top tercile cut-off measured at 2.9%), confidence/near-threshold policy, A1 on every row, regime inputs pinned to completed months | — | frozen definitions |
| 50 | Engine consistency v2.1 (single-stock live engine vs panel engine) | **224/224** agreement | live engine = backtested engine |
| 51 | **Blind round 2**: fresh agent + RULEBOOK v2.1 + 40 new VALID cases | agent = engine on **40/40**; signal, row, regime, health and timing unambiguous for every case; BULLISH n=15: 0% had a ≥20% drawdown, 60d excess +2.2%; BEARISH n=14: 14.3%, −4.1%; NO_SIGNAL n=11: 9.1%, −3.7%; risk-flagged 14.3% vs 3.8% | v2.1.1 wording fixes for secondary fields only: percentile overrides the ATR/RS proxies, exhaustive confidence list, A1 tied to the 10-month test, MIXED high-vol → NORMAL |

## Phase I — The ONE-TIME locked out-of-sample test (rules frozen at v2.1 before unlocking; see `test_access_log.md`)

| # | Iteration | Result | Decision |
|---|---|---|---|
| 52 | Index/ETF regime 2020-2026 (never seen) | S&P 500: rulebook regime (10m SMA **and** SMA50>200) max DD −33.9%→−14.1%, Sharpe 0.72→0.82, CAGR 13.3%→9.6%; 22 ETFs: MaxDD better on 95% (median +17.8 pts), Sharpe better on 55%, median CAGR −3.2%/yr (V-shaped 2020/2023 recoveries) | regime layer confirmed as drawdown insurance; cost higher than in-sample |
| 53 | Rulebook classes on 600 **never-seen holdout tickers**, 2000-2014 / 2015-2019 | P(dd≥20%/60d) BULLISH 7.5% / 5.7% vs BEARISH 26.3% / 15.0% (3.5x / 2.6x) | risk layer replicates on new stocks |
| 54 | Rulebook classes, **2020-2026**, discovery and holdout tickers | BULLISH 12.1-12.8%, NO_SIGNAL 15.3-15.7%, BEARISH 18.9-19.6% (ratio ~1.5x); BEARISH raw returns higher (loser rebounds), vol-matched excess −0.5% | ordering holds, magnitude weaker |
| 55 | Diagnostic by year (no tuning) | 2020: BULLISH 34% (COVID crash hit healthy stocks while regime read RISK_ON); 2021/2023/2024: 7.4/9.3/7.3% vs 18.1/14.3/16.4%; excl. Q1-2020: 9.1% vs 17.7% | **new documented limitation**: health ≠ protection from exogenous market shocks; calibration table now also reports 2020-26 observed rates |
| 56 | 20 key rules on discovery tickers 2020-26 and holdout tickers in all periods (60 + 20 tests) | EXTENDED family negative in 18/18 rule-sample cells (incl. holdout 2020-26); A1 confirmed on holdout (−1.38%/mo, t −4.75); A2 3/3; Donchian-20 and double-bottom negative everywhere (2020-26 REVERSED); candles/patterns/MACD/golden cross/52w breakout/Fibonacci/support: no edge in any OOS cell; RSI10 pullback positive 6/6 (small); quiet pullback mixed; A4 mixed | A4 downgraded to "no edge"; quiet pullback flagged weak; everything else stands |

## Phase J — Live practice on TradingView (forward test)

| # | Iteration | Result | Decision |
|---|---|---|---|
| 57 | An agent ran the full workflow through the TradingView MCP (9 symbols, 270 daily bars each) → `live.py` → verdicts; NVDA indicators cross-checked against `mcp-tv-get-technicals-rating` | RSI14 35.056, SMA50 221.749, SMA200 204.385 — **0.000% difference** from TradingView; signals as of 2026-10-30: AAPL/MSFT/JPM/UNH BULLISH (D3), XOM healthy-but-extended (D4), NVDA (low confidence, at SMA200) & TSLA NO_SIGNAL, INTC BEARISH (D2) | forward predictions logged in `live_journal_2026-11-01.md`, to be scored ~2026-11-30 and ~2027-01-28 |
| 58 | Re-ran the saved live bars through the final v2.1 engine | identical signals | journal valid for v2.1 |

## Phase K — Final blind exam and freeze

| # | Iteration | Result | Decision |
|---|---|---|---|
| 59 | **Blind round 3 (final exam)**: fresh agent + RULEBOOK v2.1.1 + 50 cases from **never-seen holdout tickers in the locked 2020-2026 period** | agent = engine on **49/50** (the miss: a value printed as −10.0 that was truly just below −10%); BULLISH n=17: 5.9% had a ≥20% drawdown in 60d, excess +0.4%; NO_SIGNAL n=23: 17.4%, −1.2%; **BEARISH n=10: 40.0%, excess −4.9%**; risk-flagged 40% vs 12.5% | v2.1.2 wording: rounded inputs on a cut-off → near_threshold/low confidence; near_threshold scope; band edges (≤); A3 warning at a 52w closing high on D3; D4 in a bad market mentions it. Engine mirrors the two warnings |
| 60 | Freeze v2.1.2; publish answer keys of all blind rounds (`blind_tests/answer_keys/`) | — | final |

### Totals
* **60 meta-iterations** of the build → test → learn → revise loop (platform calibration, RL ×2, ML, timing, risk, exits, 18-setting fine-tuning grid, YouTube systems, 3 blind agent rounds, locked test, live TradingView run).
* **246 rule-level hypothesis tests** in development (123 rules × 2 periods) + **80 locked out-of-sample tests** (20 key rules × 4 ticker/period cells) + 18 grid settings × 2 periods + 8 YouTube systems × 2 periods (trade simulation).
* Locked data accessed only after the rules were frozen; every access logged in `test_access_log.md`.

---

## Appendix — all 246 rule-level tests (123 rules × train/valid, discovery tickers)

Columns: excess = mean excess return over the rule's horizon h (trading days) vs the equal-weight universe; t = event-study Newey-West t / calendar-portfolio t / volatility-matched t; hit = share of events beating the universe. Verdicts are pre-registered (see top). Final locked-test results for the 20 key rules are in `results/final_rules_A.csv` and `results/final_rules_B.csv`.

| Rule | Family | Claim | h | train N | train excess | train t (event/cal/vol-matched) | train hit | train verdict | valid N | valid excess | valid t (event/cal/vol-matched) | valid hit | valid verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `death_cross` | trend | bear | 60 | 3629 | -0.04% | +0.23 / -0.02 / +0.38 | 50.0% | **NO_EDGE** | 2233 | -0.11% | -0.14 / -0.32 / -0.08 | 50.6% | **NO_EDGE** |
| `ema_20_50_cross` | trend | bull | 40 | 11854 | -0.14% | -1.07 / -2.14 / -1.49 | 49.2% | **NO_EDGE** | 6941 | -0.39% | -1.10 / -1.45 / -0.87 | 48.3% | **NO_EDGE** |
| `ema_9_21_cross` | trend | bull | 20 | 28105 | +0.11% | +0.67 / +0.64 / +0.66 | 50.4% | **NO_EDGE** | 16531 | -0.04% | -0.04 / +0.09 / -0.14 | 50.0% | **NO_EDGE** |
| `golden_cross` | trend | bull | 60 | 3496 | -0.73% | -2.47 / -1.97 / -2.75 | 46.7% | **NO_EDGE** | 2139 | +0.11% | -0.21 / +0.26 / -1.30 | 51.0% | **NO_EDGE** |
| `ma_stack_bull` | trend | bull | 60 | 21092 | -0.13% | -2.51 / -1.34 / -2.40 | 48.3% | **NO_EDGE** | 11129 | +0.07% | +0.89 / -0.28 / +2.35 | 49.9% | **NO_EDGE** |
| `price_cross_above_sma200` | trend | bull | 60 | 8970 | -0.64% | -3.13 / -2.76 / -3.42 | 47.1% | **REVERSED** | 5477 | -0.39% | -1.63 / -0.28 / -1.94 | 48.4% | **NO_EDGE** |
| `price_cross_below_sma200` | trend | bear | 60 | 9225 | -0.55% | -2.15 / -2.07 / -1.93 | 47.3% | **WEAK** | 5582 | -0.26% | -0.71 / -0.50 / -0.99 | 48.4% | **NO_EDGE** |
| `stage4_breakdown` | trend | bear | 60 | 1090 | -1.23% | -2.31 / -2.30 / -1.88 | 46.2% | **WEAK** | 731 | +0.47% | +0.73 / +1.16 / +0.96 | 52.4% | **NO_EDGE** |
| `trend_template` | trend | bull | 60 | 11580 | -0.14% | -1.88 / -0.90 / -1.49 | 48.4% | **NO_EDGE** | 6804 | -0.00% | -0.43 / -0.48 / +0.45 | 49.2% | **NO_EDGE** |
| `weinstein_stage2_breakout` | trend | bull | 60 | 633 | -1.75% | -3.16 / -0.85 / -3.13 | 44.1% | **NO_EDGE** | 330 | -1.21% | -2.47 / -0.85 / -1.58 | 44.2% | **NO_EDGE** |
| `base_breakout` | breakout | bull | 40 | 5895 | -0.44% | -2.39 / -2.32 / -2.99 | 47.7% | **REVERSED** | 3719 | -0.08% | -0.31 / -0.74 / -0.05 | 51.4% | **NO_EDGE** |
| `donchian20_breakout` | breakout | bull | 20 | 29245 | -0.14% | -2.21 / -1.46 / -2.45 | 48.8% | **NO_EDGE** | 16837 | -0.24% | -2.28 / -1.53 / -2.18 | 48.8% | **NO_EDGE** |
| `donchian55_breakout` | breakout | bull | 40 | 13509 | -0.40% | -2.11 / -2.34 / -2.47 | 48.0% | **REVERSED** | 7829 | -0.04% | -0.78 / -0.13 / -0.78 | 49.8% | **NO_EDGE** |
| `far_from_52w_high` | breakout | bear | 60 | 4493 | +1.21% | -3.10 / -1.15 / -4.08 | 51.8% | **NO_EDGE** | 1600 | +0.19% | -0.87 / +0.08 / -1.43 | 49.4% | **NO_EDGE** |
| `gap_down_volume` | breakout | bear | 20 | 1969 | +0.25% | +0.12 / -0.56 / +0.39 | 48.1% | **NO_EDGE** | 1226 | +0.49% | +1.61 / +1.04 / +1.70 | 48.4% | **NO_EDGE** |
| `gap_up_volume` | breakout | bull | 20 | 2224 | +0.04% | +0.33 / +1.26 / +0.16 | 49.6% | **NO_EDGE** | 1099 | -0.22% | -0.64 / -0.54 / -0.69 | 48.9% | **NO_EDGE** |
| `high_52w_breakout` | breakout | bull | 60 | 8261 | -0.10% | -1.10 / -1.54 / -1.29 | 48.3% | **NO_EDGE** | 4791 | +0.12% | +0.07 / -0.22 / +0.51 | 50.7% | **NO_EDGE** |
| `high_52w_breakout_vol` | breakout | bull | 60 | 6011 | -0.13% | +0.06 / -2.04 / -0.25 | 48.7% | **NO_EDGE** | 3195 | +0.26% | +0.32 / +0.02 / +1.00 | 52.2% | **NO_EDGE** |
| `low_52w_breakdown` | breakout | bear | 60 | 2468 | +0.76% | -0.41 / +0.15 / -0.58 | 52.0% | **NO_EDGE** | 1722 | -0.32% | -1.33 / -1.44 / -1.25 | 50.6% | **NO_EDGE** |
| `near_52w_high` | breakout | bull | 60 | 20705 | +0.02% | -2.06 / -1.43 / -2.17 | 48.7% | **NO_EDGE** | 12437 | +0.20% | -0.02 / -0.54 / +0.34 | 50.8% | **NO_EDGE** |
| `adx_trend_up` | momentum | bull | 20 | 11128 | -0.12% | -1.94 / -1.28 / -1.90 | 48.3% | **NO_EDGE** | 6111 | -0.31% | -2.32 / -0.76 / -1.77 | 48.3% | **NO_EDGE** |
| `macd_bear_cross` | momentum | bear | 20 | 52462 | -0.06% | -1.85 / -0.34 / -1.81 | 49.2% | **NO_EDGE** | 30321 | -0.07% | -1.14 / -0.35 / -0.52 | 49.1% | **NO_EDGE** |
| `macd_bull_cross` | momentum | bull | 20 | 52045 | -0.08% | -1.58 / -1.31 / -1.13 | 49.3% | **NO_EDGE** | 29815 | -0.00% | -0.39 / -0.63 / -0.19 | 49.9% | **NO_EDGE** |
| `macd_bull_cross_below0` | momentum | bull | 20 | 26421 | +0.05% | +1.05 / +0.31 / +1.50 | 50.0% | **NO_EDGE** | 15798 | +0.05% | -0.57 / -0.56 / -0.31 | 50.5% | **NO_EDGE** |
| `macd_zero_cross` | momentum | bull | 40 | 21537 | +0.01% | -0.60 / +0.63 / -0.71 | 49.5% | **NO_EDGE** | 12847 | -0.20% | -0.55 / -1.01 / -0.43 | 48.9% | **NO_EDGE** |
| `mom_12_1_bottom_decile` | momentum | bear | 21 | 5974 | -0.15% | -0.43 / -0.46 / -1.33 | 47.8% | **NO_EDGE** | 3480 | -0.20% | -0.67 / -0.41 / -0.97 | 48.7% | **NO_EDGE** |
| `mom_12_1_top_decile` | momentum | bull | 21 | 6151 | -0.25% | -1.38 / -1.24 / -1.08 | 48.7% | **NO_EDGE** | 3537 | -0.16% | -0.69 / -0.31 / -0.06 | 49.0% | **NO_EDGE** |
| `rs_top_decile_6m` | momentum | bull | 21 | 6200 | -0.27% | -1.59 / -1.33 / -1.16 | 48.4% | **NO_EDGE** | 3573 | -0.10% | -0.64 / -0.12 / -0.32 | 48.9% | **NO_EDGE** |
| `rsi_cross_50_up` | momentum | bull | 20 | 37648 | +0.03% | +0.40 / +0.41 / +0.50 | 49.5% | **NO_EDGE** | 21457 | +0.03% | +0.98 / +0.96 / +1.21 | 50.2% | **NO_EDGE** |
| `bb_lower_close` | oscillator | bull | 10 | 22251 | -0.02% | +0.67 / -0.33 / +1.04 | 48.7% | **NO_EDGE** | 13968 | +0.14% | +1.16 / +1.14 / +1.31 | 50.6% | **NO_EDGE** |
| `bb_upper_close` | oscillator | bear | 10 | 28932 | -0.14% | -2.10 / -2.03 / -1.72 | 48.9% | **WEAK** | 16619 | -0.19% | -1.14 / -1.47 / -1.13 | 48.6% | **NO_EDGE** |
| `rsi14_overbought` | oscillator | bear | 10 | 14674 | -0.21% | -3.05 / -3.12 / -2.90 | 46.8% | **SIGNAL** | 8755 | -0.16% | -2.27 / -1.89 / -2.23 | 48.8% | **NO_EDGE** |
| `rsi14_oversold` | oscillator | bull | 10 | 8302 | +0.20% | +1.75 / +1.19 / +1.71 | 50.0% | **NO_EDGE** | 5797 | -0.03% | -0.05 / +0.09 / +0.05 | 49.2% | **NO_EDGE** |
| `rsi14_oversold_exit` | oscillator | bull | 10 | 8264 | +0.05% | +0.51 / +0.85 / +0.82 | 48.7% | **NO_EDGE** | 5777 | -0.08% | +0.22 / -0.41 / -0.07 | 48.2% | **NO_EDGE** |
| `rsi2_connors` | oscillator | bull | 5 | 35040 | +0.08% | +0.79 / +1.16 / +1.40 | 49.6% | **NO_EDGE** | 18345 | +0.00% | -0.46 / -1.58 / -0.07 | 50.2% | **NO_EDGE** |
| `rsi2_connors_nofilter` | oscillator | bull | 5 | 58537 | +0.04% | +1.74 / +1.98 / +2.14 | 49.3% | **NO_EDGE** | 32564 | -0.02% | -0.51 / -1.90 / +0.13 | 49.9% | **NO_EDGE** |
| `stoch_overbought_cross` | oscillator | bear | 10 | 33871 | -0.05% | -0.71 / -0.95 / -0.20 | 48.9% | **NO_EDGE** | 19467 | -0.12% | -1.63 / -1.79 / -1.59 | 49.5% | **NO_EDGE** |
| `stoch_oversold_cross` | oscillator | bull | 10 | 26247 | +0.02% | +0.59 / +0.00 / +0.75 | 48.9% | **NO_EDGE** | 14903 | +0.04% | +0.50 / +0.88 / +0.71 | 49.5% | **NO_EDGE** |
| `pullback_in_uptrend` | reversal | bull | 10 | 35714 | +0.04% | +1.21 / -0.65 / +2.05 | 49.0% | **NO_EDGE** | 17479 | +0.08% | -0.36 / -0.93 / -0.12 | 50.7% | **NO_EDGE** |
| `pullback_to_sma50` | reversal | bull | 20 | 9220 | -0.21% | -1.34 / -2.15 / -1.39 | 47.8% | **NO_EDGE** | 4798 | +0.21% | +1.15 / +0.02 / +1.16 | 51.4% | **NO_EDGE** |
| `short_term_loser` | reversal | bull | 5 | 26284 | +0.09% | +1.50 / +1.44 / +2.52 | 49.8% | **NO_EDGE** | 15421 | +0.05% | +0.61 / +0.30 / +0.91 | 49.8% | **NO_EDGE** |
| `short_term_winner` | reversal | bear | 5 | 27054 | -0.18% | -4.07 / -2.92 / -4.56 | 47.7% | **WEAK** | 15669 | -0.10% | -1.44 / -1.50 / -2.13 | 48.9% | **NO_EDGE** |
| `bb_squeeze_breakout` | volatility | bull | 20 | 5635 | -0.23% | -1.91 / -1.79 / -2.04 | 48.7% | **NO_EDGE** | 2932 | -0.25% | -0.26 / -1.92 / +0.02 | 48.0% | **NO_EDGE** |
| `breakout_low_volume` | volume | bull | 40 | 5284 | -0.21% | -0.90 / -0.79 / -0.74 | 47.7% | **NO_EDGE** | 3263 | -0.02% | -0.10 / +0.02 / +0.03 | 49.8% | **NO_EDGE** |
| `capitulation_volume` | volume | bull | 20 | 1011 | +0.76% | +0.55 / +0.17 / +0.51 | 54.4% | **NO_EDGE** | 460 | +1.16% | +0.65 / +1.21 / +0.67 | 52.0% | **NO_EDGE** |
| `cmf_strong` | volume | bull | 20 | 16754 | -0.04% | -1.66 / -1.00 / -1.85 | 49.3% | **NO_EDGE** | 9367 | -0.05% | +0.09 / -0.91 / +0.52 | 49.3% | **NO_EDGE** |
| `obv_new_high_lead` | volume | bull | 20 | 5067 | -0.09% | -0.68 / -1.00 / -0.72 | 50.0% | **NO_EDGE** | 3477 | -0.17% | -1.31 / -1.52 / -1.26 | 49.5% | **NO_EDGE** |
| `volume_thrust_down` | volume | bear | 20 | 2288 | +0.23% | +0.38 / -0.54 / +0.76 | 50.8% | **NO_EDGE** | 1356 | -0.07% | -0.72 / -0.87 / -0.70 | 46.7% | **NO_EDGE** |
| `volume_thrust_up` | volume | bull | 20 | 2318 | -0.07% | -0.46 / -0.35 / -0.60 | 49.5% | **NO_EDGE** | 1055 | +0.12% | +0.08 / -0.20 / +0.11 | 51.8% | **NO_EDGE** |
| `rsi_bear_divergence` | divergence | bear | 20 | 7363 | -0.07% | -0.92 / -1.67 / -1.08 | 49.5% | **NO_EDGE** | 4202 | -0.18% | -1.25 / -0.52 / -1.47 | 48.8% | **NO_EDGE** |
| `rsi_bull_divergence` | divergence | bull | 20 | 2792 | +0.20% | +0.42 / +0.91 / +0.50 | 50.6% | **NO_EDGE** | 1954 | +0.12% | +0.10 / -1.03 / +0.31 | 50.7% | **NO_EDGE** |
| `fib_618_bounce` | sr | bull | 20 | 8699 | -0.20% | -2.16 / -1.58 / -2.24 | 47.9% | **NO_EDGE** | 4241 | -0.04% | +1.13 / -0.53 / +1.49 | 49.1% | **NO_EDGE** |
| `resistance_reject` | sr | bear | 20 | 10225 | +0.05% | +0.76 / -0.22 / +0.42 | 49.1% | **NO_EDGE** | 5806 | +0.02% | -0.23 / -0.59 / -0.15 | 49.5% | **NO_EDGE** |
| `round_number_breakout` | sr | bull | 20 | 4648 | -0.46% | -2.63 / -2.63 / -2.07 | 47.8% | **REVERSED** | 3060 | -0.25% | -1.66 / -0.62 / -0.84 | 48.4% | **NO_EDGE** |
| `support_bounce` | sr | bull | 20 | 6182 | -0.18% | -1.02 / -1.18 / -1.41 | 48.2% | **NO_EDGE** | 4132 | -0.38% | -2.06 / -2.17 / -1.81 | 49.1% | **REVERSED** |
| `support_break` | sr | bear | 20 | 5452 | +0.02% | -0.04 / -0.11 / -0.00 | 49.9% | **NO_EDGE** | 3487 | -0.21% | -0.96 / -0.79 / -0.64 | 48.9% | **NO_EDGE** |
| `cdl_bear_engulfing` | candlestick | bear | 10 | 19485 | +0.01% | -0.73 / -0.59 / -0.39 | 49.1% | **NO_EDGE** | 10964 | -0.08% | -1.20 / -1.77 / -1.06 | 49.5% | **NO_EDGE** |
| `cdl_bull_engulfing` | candlestick | bull | 10 | 13557 | +0.14% | +2.41 / +0.46 / +2.43 | 49.8% | **NO_EDGE** | 6598 | +0.05% | +0.48 / -0.17 / +0.55 | 49.4% | **NO_EDGE** |
| `cdl_dark_cloud` | candlestick | bear | 10 | 2425 | +0.02% | +0.39 / +1.49 / +0.71 | 49.1% | **NO_EDGE** | 1194 | +0.01% | +0.46 / -0.39 / +0.96 | 48.7% | **NO_EDGE** |
| `cdl_doji_after_down` | candlestick | bull | 10 | 31503 | +0.09% | +1.53 / +0.94 / +1.88 | 50.0% | **NO_EDGE** | 18054 | +0.09% | +0.71 / +0.72 / +1.17 | 49.7% | **NO_EDGE** |
| `cdl_doji_after_up` | candlestick | bear | 10 | 43555 | -0.08% | -1.67 / -0.83 / -1.54 | 48.5% | **NO_EDGE** | 24388 | -0.10% | -1.47 / -2.36 / -1.11 | 49.5% | **NO_EDGE** |
| `cdl_evening_star` | candlestick | bear | 10 | 6691 | +0.06% | +0.03 / -0.51 / +0.31 | 49.3% | **NO_EDGE** | 3185 | -0.13% | -0.62 / -0.98 / -0.36 | 48.5% | **NO_EDGE** |
| `cdl_hammer` | candlestick | bull | 10 | 13342 | +0.19% | +1.71 / +1.69 / +1.21 | 50.2% | **NO_EDGE** | 6657 | -0.02% | +1.04 / +1.06 / +0.92 | 49.7% | **NO_EDGE** |
| `cdl_morning_star` | candlestick | bull | 10 | 5317 | -0.08% | +0.07 / -0.39 / +0.10 | 48.3% | **NO_EDGE** | 3083 | -0.02% | +0.95 / -0.76 / +0.78 | 49.6% | **NO_EDGE** |
| `cdl_piercing` | candlestick | bull | 10 | 1928 | -0.45% | -1.31 / -1.65 / -1.21 | 46.9% | **NO_EDGE** | 907 | +0.41% | +0.42 / +0.57 / +0.58 | 52.6% | **NO_EDGE** |
| `cdl_shooting_star` | candlestick | bear | 10 | 14030 | -0.04% | -0.61 / -0.50 / -0.67 | 48.7% | **NO_EDGE** | 7288 | -0.20% | -2.23 / -2.26 / -2.11 | 48.1% | **WEAK** |
| `cdl_three_black_crows` | candlestick | bear | 10 | 1505 | -0.47% | -1.19 / -0.06 / -0.79 | 46.8% | **NO_EDGE** | 691 | +0.24% | +0.67 / -0.49 / +0.19 | 49.5% | **NO_EDGE** |
| `cdl_three_white_soldiers` | candlestick | bull | 10 | 1349 | -0.20% | +0.13 / +0.78 / +0.20 | 47.9% | **NO_EDGE** | 660 | -0.53% | -1.42 / -1.61 / -1.69 | 47.9% | **NO_EDGE** |
| `pat_asc_triangle` | chart_pattern | bull | 40 | 1468 | -0.42% | -1.21 / -1.07 / -1.28 | 47.2% | **NO_EDGE** | 907 | -0.10% | -0.17 / +0.04 / -0.10 | 51.9% | **NO_EDGE** |
| `pat_bull_flag` | chart_pattern | bull | 20 | 354 | +0.10% | +0.19 / -0.43 / +0.05 | 51.7% | **NO_EDGE** | 161 | -1.07% | -2.23 / -1.52 / -1.80 | 44.7% | **NO_EDGE** |
| `pat_cup_handle` | chart_pattern | bull | 60 | 174 | -0.34% | -0.79 / -1.09 / -0.64 | 49.4% | **NO_EDGE** | 110 | +0.18% | +0.03 / -1.15 / -0.21 | 49.1% | **NO_EDGE** |
| `pat_desc_triangle` | chart_pattern | bear | 40 | 1081 | +0.59% | +1.93 / +0.76 / +2.02 | 51.6% | **NO_EDGE** | 673 | +0.40% | +1.07 / +0.24 / +0.88 | 49.9% | **NO_EDGE** |
| `pat_double_bottom` | chart_pattern | bull | 40 | 3960 | -0.11% | +0.30 / -0.59 / -0.12 | 49.9% | **NO_EDGE** | 2187 | -0.66% | -2.05 / -0.85 / -1.60 | 47.4% | **NO_EDGE** |
| `pat_double_top` | chart_pattern | bear | 40 | 3047 | +0.03% | +0.33 / +0.47 / +0.21 | 48.3% | **NO_EDGE** | 1646 | +0.78% | +0.52 / +0.74 / +0.56 | 52.3% | **NO_EDGE** |
| `pat_head_shoulders` | chart_pattern | bear | 40 | 1198 | +0.04% | +0.45 / -0.13 / +0.40 | 50.8% | **NO_EDGE** | 757 | -0.29% | -0.34 / -0.90 / -0.09 | 48.2% | **NO_EDGE** |
| `pat_inv_head_shoulders` | chart_pattern | bull | 40 | 1554 | -0.56% | -1.80 / -2.32 / -1.76 | 48.0% | **NO_EDGE** | 947 | +0.51% | +1.59 / +1.44 / +1.62 | 52.8% | **NO_EDGE** |
| `pat_vcp` | chart_pattern | bull | 40 | 3005 | -0.36% | -2.12 / -1.79 / -1.94 | 47.5% | **NO_EDGE** | 1808 | +0.22% | +0.48 / -0.20 / +0.76 | 51.9% | **NO_EDGE** |
| `donchian20_chop_only` | books | bull | 20 | 22206 | -0.12% | -1.91 / -1.13 / -2.25 | 48.8% | **NO_EDGE** | 12502 | -0.24% | -2.17 / -1.14 / -2.29 | 48.9% | **NO_EDGE** |
| `donchian20_trending_only` | books | bull | 20 | 15701 | -0.24% | -2.15 / -1.81 / -3.05 | 48.1% | **NO_EDGE** | 9167 | -0.30% | -2.02 / -1.68 / -1.46 | 48.1% | **NO_EDGE** |
| `leader_in_strong_group` | books | bull | 21 | 3902 | -0.29% | -2.58 / -1.29 / -2.57 | 48.4% | **NO_EDGE** | 2232 | -0.82% | -3.89 / -2.37 / -3.76 | 47.0% | **REVERSED** |
| `liv_bargain_upmkt` | books | bull | 60 | 3664 | -0.30% | -0.58 / +0.10 / -0.42 | 47.0% | **NO_EDGE** | 1811 | +0.11% | +0.06 / +0.26 / +0.00 | 48.8% | **NO_EDGE** |
| `liv_climax_top` | books | bear | 20 | 421 | +0.50% | +1.06 / +0.58 / +1.13 | 50.1% | **NO_EDGE** | 151 | +0.54% | +0.51 / -0.39 / +0.54 | 48.3% | **NO_EDGE** |
| `liv_failed_followthrough` | books | bear | 20 | 4067 | -0.17% | -0.79 / -1.56 / -0.08 | 46.8% | **NO_EDGE** | 2924 | -0.06% | -0.69 / -0.54 / -1.01 | 50.5% | **NO_EDGE** |
| `liv_fallen_leader` | books | bear | 60 | 1214 | +0.01% | -0.99 / +0.49 / -1.18 | 48.0% | **NO_EDGE** | 906 | +0.91% | +2.00 / +1.23 / +2.96 | 49.9% | **NO_EDGE** |
| `liv_laggard_strong_group` | books | bear | 60 | 4142 | +0.17% | +0.78 / +1.47 / +1.13 | 50.4% | **NO_EDGE** | 2341 | -0.43% | -1.46 / +0.14 / -1.69 | 47.8% | **NO_EDGE** |
| `liv_new_high_upmkt` | books | bull | 60 | 7496 | -0.04% | +0.21 / -0.38 / +0.42 | 48.4% | **NO_EDGE** | 4745 | +0.00% | -0.02 / -0.55 / +0.06 | 50.1% | **NO_EDGE** |
| `liv_range_breakout` | books | bull | 60 | 4716 | -0.24% | -0.38 / -1.38 / +0.52 | 47.9% | **NO_EDGE** | 3442 | +0.24% | +0.23 / +0.02 / -0.06 | 52.0% | **NO_EDGE** |
| `liv_range_breakout_nomkt` | books | bull | 60 | 4941 | -0.17% | -0.42 / -0.73 / +0.26 | 48.2% | **NO_EDGE** | 3606 | +0.18% | +0.09 / +0.13 / -0.18 | 51.6% | **NO_EDGE** |
| `sch_breakaway_gap` | books | bull | 20 | 13196 | -0.05% | -0.06 / -0.38 / -0.12 | 49.4% | **NO_EDGE** | 8678 | -0.18% | -1.13 / -1.61 / -0.71 | 49.0% | **NO_EDGE** |
| `sch_exhaustion_gap` | books | bear | 20 | 1550 | +0.25% | +0.47 / +0.38 / +0.94 | 48.0% | **NO_EDGE** | 459 | -0.17% | -0.52 / -1.04 / -0.67 | 48.8% | **NO_EDGE** |
| `sch_key_reversal_top` | books | bear | 10 | 2043 | +0.06% | +0.50 / +1.79 / +0.43 | 49.0% | **NO_EDGE** | 1139 | -0.25% | -2.41 / -1.57 / -2.08 | 49.1% | **NO_EDGE** |
| `sch_loud_pullback_bull` | books | bear | 20 | 6746 | -0.01% | -0.09 / +0.08 / -0.57 | 48.1% | **NO_EDGE** | 4869 | +0.09% | -0.06 / +0.74 / -0.02 | 50.0% | **NO_EDGE** |
| `sch_quiet_pullback_bull` | books | bull | 20 | 4160 | +0.25% | +1.37 / +1.07 / +1.32 | 50.3% | **NO_EDGE** | 3017 | +0.21% | +1.30 / +0.61 / +1.81 | 50.6% | **NO_EDGE** |
| `sch_shakeout_spring` | books | bull | 20 | 1063 | -0.29% | -1.09 / -1.42 / -1.16 | 47.5% | **NO_EDGE** | 530 | -0.11% | -0.24 / +0.50 / -0.06 | 46.6% | **NO_EDGE** |
| `sch_thrust_followthrough` | books | bull | 10 | 617 | -0.08% | -0.08 / -0.33 / -0.40 | 49.6% | **NO_EDGE** | 511 | -0.63% | -2.49 / -2.41 / -2.38 | 44.4% | **REVERSED** |
| `selden_distribution_near_high` | books | bear | 20 | 1791 | -0.05% | -1.11 / -0.97 / -0.86 | 47.9% | **NO_EDGE** | 1225 | +0.23% | +1.13 / +0.44 / +1.11 | 51.3% | **NO_EDGE** |
| `selden_updown_vol_strong` | books | bull | 20 | 5736 | -0.06% | -0.56 / -0.65 / -0.44 | 49.0% | **NO_EDGE** | 2733 | +0.11% | +0.22 / -0.22 / +0.51 | 50.5% | **NO_EDGE** |
| `wyc_buying_climax` | books | bear | 20 | 461 | -0.63% | -0.92 / -0.63 / -0.86 | 46.2% | **NO_EDGE** | 216 | +0.51% | +0.33 / +0.32 / +0.49 | 53.2% | **NO_EDGE** |
| `wyc_dull_range_breakout` | books | bull | 20 | 2128 | +0.04% | +0.33 / -0.82 / +0.32 | 49.3% | **NO_EDGE** | 1013 | -0.29% | -0.95 / -2.12 / -0.64 | 48.1% | **NO_EDGE** |
| `wyc_effort_without_result` | books | bear | 20 | 84 | -1.56% | -1.38 / -1.22 / -0.66 | 35.7% | **NO_EDGE** | 58 | -0.93% | -0.77 / +0.18 / -0.80 | 53.4% | **NO_EDGE** |
| `wyc_low_volume_retest` | books | bull | 20 | 5002 | -0.04% | +0.73 / +0.61 / +0.87 | 49.8% | **NO_EDGE** | 2634 | +0.26% | +0.61 / -0.08 / +0.47 | 52.1% | **NO_EDGE** |
| `wyc_resilience_on_shock` | books | bull | 20 | 6345 | -0.91% | -3.19 / -1.02 / -3.83 | 45.8% | **NO_EDGE** | 1939 | -0.28% | -0.45 / +0.58 / -0.11 | 45.8% | **NO_EDGE** |
| `wyc_selling_climax` | books | bull | 20 | 341 | +0.74% | -0.27 / +0.75 / -0.34 | 53.4% | **NO_EDGE** | 207 | +1.32% | +1.33 / +0.40 / +1.63 | 57.5% | **NO_EDGE** |
| `wyc_small_giveback_in_correction` | books | bull | 60 | 3074 | -0.21% | -0.98 / -0.19 / -3.76 | 46.9% | **NO_EDGE** | 137 | +0.04% |  / +0.42 /  | 39.4% | **INSUFFICIENT** |
| `wyc_streak_5down` | books | bull | 5 | 15941 | +0.09% | +1.44 / +0.78 / +1.39 | 49.9% | **NO_EDGE** | 8796 | +0.08% | +1.74 / -0.08 / +1.95 | 50.2% | **NO_EDGE** |
| `wyc_streak_5up` | books | bear | 5 | 20073 | -0.13% | -3.13 / -3.11 / -3.04 | 48.4% | **SIGNAL** | 12978 | +0.03% | +1.11 / -0.36 / +0.71 | 50.3% | **NO_EDGE** |
| `wyc_weakest_on_shock` | books | bear | 20 | 6147 | +1.11% | +2.37 / +1.38 / +2.71 | 51.5% | **NO_EDGE** | 1909 | +0.62% | +1.33 / +0.11 / +1.43 | 53.5% | **NO_EDGE** |
| `rs_laggards_bear_mkt` | regime | bull | 21 | 1667 | +0.83% | +0.76 / +0.77 / +0.88 | 52.4% | **NO_EDGE** | 565 | +1.09% |  / +0.84 /  | 55.2% | **INSUFFICIENT** |
| `rs_laggards_bull_mkt` | regime | bear | 21 | 4356 | +0.08% | +0.39 / -0.39 / +0.04 | 50.4% | **NO_EDGE** | 2951 | -0.21% | -0.51 / -0.44 / -0.70 | 47.7% | **NO_EDGE** |
| `rs_leaders_bear_mkt` | regime | bull | 21 | 1724 | -1.80% | -4.31 / -2.84 / -3.95 | 43.7% | **REVERSED** | 574 | -0.87% |  / -0.71 /  | 44.4% | **INSUFFICIENT** |
| `rs_leaders_bull_mkt` | regime | bull | 21 | 4476 | +0.33% | +0.81 / +0.21 / +0.65 | 50.3% | **NO_EDGE** | 2999 | +0.04% | +0.25 / +0.04 / +0.39 | 49.7% | **NO_EDGE** |
| `rsi30_bear_mkt` | regime | bull | 10 | 2724 | +0.37% | +0.46 / -0.04 / +0.57 | 50.7% | **NO_EDGE** | 785 | +0.71% | +0.92 / +0.60 / +0.89 | 55.3% | **NO_EDGE** |
| `rsi30_bull_mkt` | regime | bull | 10 | 5115 | +0.03% | +1.21 / +1.15 / +1.33 | 48.9% | **NO_EDGE** | 5048 | -0.11% | -0.35 / +0.45 / -0.15 | 48.6% | **NO_EDGE** |
| `st_loser_bear_mkt` | regime | bull | 5 | 7078 | +0.04% | +0.30 / +1.01 / +0.81 | 49.6% | **NO_EDGE** | 2130 | +0.30% | +2.12 / +1.32 / +2.10 | 52.9% | **NO_EDGE** |
| `st_loser_bull_mkt` | regime | bull | 5 | 19206 | +0.10% | +2.08 / +1.03 / +3.04 | 49.8% | **NO_EDGE** | 13291 | +0.01% | -0.01 / -0.04 / +0.26 | 49.3% | **NO_EDGE** |
| `confluence_breakout` | confluence | bull | 60 | 3569 | -0.13% | +0.28 / -0.05 / +0.35 | 48.1% | **NO_EDGE** | 2137 | +0.66% | +2.10 / +0.55 / +2.65 | 53.2% | **NO_EDGE** |
| `confluence_pullback` | confluence | bull | 20 | 1414 | -0.14% | -0.06 / -1.25 / +0.22 | 47.1% | **NO_EDGE** | 803 | +0.25% | +0.88 / +0.20 / +0.96 | 51.3% | **NO_EDGE** |
| `yt_macd_200ema` | youtube | bull | 15 | 12501 | -0.11% | -0.97 / -2.25 / -0.75 | 49.4% | **NO_EDGE** | 6940 | +0.03% | -0.31 / -0.45 / -0.51 | 50.8% | **NO_EDGE** |
| `yt_rsi10_any_trend` | youtube | bull | 5 | 14545 | +0.01% | +0.36 / -1.24 / +0.69 | 49.6% | **NO_EDGE** | 9523 | +0.00% | -1.67 / -1.44 / -1.08 | 49.7% | **NO_EDGE** |
| `yt_rsi10_downtrend` | youtube | bull | 5 | 10339 | -0.04% | +0.64 / +0.40 / +0.98 | 48.8% | **NO_EDGE** | 6985 | -0.04% | -1.35 / -1.48 / -0.88 | 48.4% | **NO_EDGE** |
| `yt_rsi10_pullback` | youtube | bull | 5 | 5893 | +0.15% | +1.38 / +0.18 / +1.65 | 51.1% | **NO_EDGE** | 3468 | +0.14% | +0.94 / +0.08 / +1.02 | 52.7% | **NO_EDGE** |
| `yt_rsi10_pullback_h10` | youtube | bull | 10 | 5893 | +0.07% | +0.66 / -1.03 / +0.56 | 48.8% | **NO_EDGE** | 3468 | +0.32% | +1.77 / -0.60 / +1.85 | 52.9% | **NO_EDGE** |
| `yt_rsi10_pullback_rising200` | youtube | bull | 5 | 5642 | +0.17% | +1.55 / +0.60 / +1.91 | 51.1% | **NO_EDGE** | 3353 | +0.13% | +1.08 / -0.21 / +1.14 | 52.8% | **NO_EDGE** |

### Rule definitions (source of each belief)

- `death_cross`: SMA50 crosses below SMA200 = bearish
- `ema_20_50_cross`: EMA20 crosses above EMA50
- `ema_9_21_cross`: YouTube day/swing traders: EMA9 crosses above EMA21
- `golden_cross`: Popular YouTube/Investopedia: SMA50 crosses above SMA200
- `ma_stack_bull`: C>SMA50>SMA150>SMA200 & SMA200 rising (Minervini partial), monthly sample
- `price_cross_above_sma200`: Close crosses above 200-day SMA (Granville/Faber)
- `price_cross_below_sma200`: Close crosses below 200-day SMA = sell
- `stage4_breakdown`: Weinstein: close crosses below falling 150d SMA on volume
- `trend_template`: Minervini Trend Template (all 8 criteria), monthly sample
- `weinstein_stage2_breakout`: Weinstein: close crosses above rising 30-wk(150d) SMA, vol>=2x, RS>0
- `base_breakout`: Tight 30-day base (range<=15%) then close>base high on vol>=1.5x, above SMA200
- `donchian20_breakout`: Turtle System 1: close above 20-day high
- `donchian55_breakout`: Turtle System 2: close above 55-day high
- `far_from_52w_high`: >=40% below 52-wk high, monthly sample (anchoring loser)
- `gap_down_volume`: Gap down >=4% on volume >=2x and closes weak
- `gap_up_volume`: Gap up >=4% on volume >=2x and holds (close>open) - 'gap and go'/earnings gap
- `high_52w_breakout`: Close above prior 252-day high (Livermore/O'Neil/Darvas)
- `high_52w_breakout_vol`: 52-wk high breakout on volume >=1.5x 50d avg (O'Neil)
- `low_52w_breakdown`: Close below prior 252-day low = bearish
- `near_52w_high`: George-Hwang: within 5% of 52-wk high, monthly sample
- `adx_trend_up`: Wilder: ADX crosses above 25 with +DI>-DI
- `macd_bear_cross`: MACD line crosses below signal
- `macd_bull_cross`: MACD line crosses above signal line
- `macd_bull_cross_below0`: MACD bullish cross while MACD<0 (popular 'stronger' variant)
- `macd_zero_cross`: MACD crosses above zero
- `mom_12_1_bottom_decile`: Bottom decile 12-1 month return, monthly
- `mom_12_1_top_decile`: Jegadeesh-Titman: top decile 12-1 month return, monthly
- `rs_top_decile_6m`: IBD-style RS: top decile 6-month return vs universe, monthly
- `rsi_cross_50_up`: RSI(14) crosses above 50 (momentum regime shift)
- `bb_lower_close`: Close below lower Bollinger band = buy (band 'bounce')
- `bb_upper_close`: Close above upper Bollinger band = overbought/sell
- `rsi14_overbought`: Classic: RSI(14) crosses above 70 = overbought sell
- `rsi14_oversold`: Classic: RSI(14) crosses below 30 = oversold buy
- `rsi14_oversold_exit`: RSI(14) crosses back above 30 from below
- `rsi2_connors`: Connors: C>SMA200 and RSI(2)<10
- `rsi2_connors_nofilter`: RSI(2)<10 without trend filter
- `stoch_overbought_cross`: %K crosses below %D while both > 80
- `stoch_oversold_cross`: Lane: %K crosses above %D while both < 20
- `pullback_in_uptrend`: Uptrend (C>SMA200, SMA50>SMA200) and 3 consecutive down closes
- `pullback_to_sma50`: Uptrend and low touches SMA50 then closes above it
- `short_term_loser`: Bottom decile 5-day return (short-term reversal)
- `short_term_winner`: Top decile 5-day return (short-term reversal)
- `bb_squeeze_breakout`: Bollinger squeeze: bandwidth at 6-mo low within 5d, then close > upper band
- `breakout_low_volume`: 52w-high breakout on BELOW-average volume (claimed to fail)
- `capitulation_volume`: Selling climax: down>=4%, vol>=3x, after >=25% drop from 60d high
- `cmf_strong`: Chaikin Money Flow crosses above +0.20
- `obv_new_high_lead`: OBV at 60-day high while price is NOT (accumulation divergence)
- `volume_thrust_down`: Down >=4% on vol >=3x, close in bottom 25% (distribution)
- `volume_thrust_up`: Up >=4% on vol >=3x, close in top 25% of range (institutional buying)
- `rsi_bear_divergence`: Price higher 20d high, RSI lower high, RSI>60
- `rsi_bull_divergence`: Price lower 20d low than 20d ago, RSI higher low, RSI<40
- `fib_618_bounce`: Uptrend leg >=20% in 60d, pullback to 61.8% retrace (+-2%), bullish close
- `resistance_reject`: High tags prior 60-120d high (within 1.5%) and closes in bottom 30%
- `round_number_breakout`: Close crosses above a round number (10/25/50/100/...) for the first time in 60d
- `support_bounce`: Low within 1.5% of prior 60-120d swing low, close up from it (bounce)
- `support_break`: Close breaks >2% below prior 60-120d swing low
- `cdl_bear_engulfing`: Nison candlestick pattern (with prior-trend context)
- `cdl_bull_engulfing`: Nison candlestick pattern (with prior-trend context)
- `cdl_dark_cloud`: Nison candlestick pattern (with prior-trend context)
- `cdl_doji_after_down`: Nison candlestick pattern (with prior-trend context)
- `cdl_doji_after_up`: Nison candlestick pattern (with prior-trend context)
- `cdl_evening_star`: Nison candlestick pattern (with prior-trend context)
- `cdl_hammer`: Nison candlestick pattern (with prior-trend context)
- `cdl_morning_star`: Nison candlestick pattern (with prior-trend context)
- `cdl_piercing`: Nison candlestick pattern (with prior-trend context)
- `cdl_shooting_star`: Nison candlestick pattern (with prior-trend context)
- `cdl_three_black_crows`: Nison candlestick pattern (with prior-trend context)
- `cdl_three_white_soldiers`: Nison candlestick pattern (with prior-trend context)
- `pat_asc_triangle`: Ascending triangle: flat tops, rising lows, upside breakout
- `pat_bull_flag`: Bull flag: >=20% pole in <=15 bars, <=50% retrace, break above pole high
- `pat_cup_handle`: O'Neil cup-with-handle: 12-35% cup, handle in upper half, breakout on vol>=1.4x
- `pat_desc_triangle`: Descending triangle: flat bottoms, falling highs, downside break
- `pat_double_bottom`: Edwards&Magee/Bulkowski double bottom: close above middle peak
- `pat_double_top`: Double top: close below middle trough
- `pat_head_shoulders`: Head & shoulders top: close below neckline
- `pat_inv_head_shoulders`: Inverse head & shoulders: close above neckline
- `pat_vcp`: Minervini VCP: 3 contracting pullbacks, last <=10%, breakout on vol>=1.5x
- `donchian20_chop_only`: H-WYC-9: 20d breakout during chop (ER < 0.2) - claimed to fail
- `donchian20_trending_only`: H-WYC-9: 20d breakout only when efficiency ratio(20) >= 0.3 (not chop)
- `leader_in_strong_group`: Livermore/O'Neil: leader of a leading group, monthly
- `liv_bargain_upmkt`: H-LIV-3b: 15-25% off high but above SMA200 ('looks cheap')
- `liv_climax_top`: H-LIV-11: buying climax after +50% in 6 months
- `liv_failed_followthrough`: H-LIV-5: breakout fails to follow through in 3 days
- `liv_fallen_leader`: H-LIV-7: former RS leader fails while index near highs
- `liv_laggard_strong_group`: H-LIV-8b: 'Chester' laggard in a top-tercile group
- `liv_new_high_upmkt`: H-LIV-3a: close at 252d high while market up
- `liv_range_breakout`: Livermore H-LIV-1: 60d range<=15% breakout, market up
- `liv_range_breakout_nomkt`: H-LIV-1 without market filter (ablation)
- `sch_breakaway_gap`: H-SCH-6: gap up out of a tight 20d range to a new high
- `sch_exhaustion_gap`: H-SCH-6: gap up after +25% in 30d (exhaustion)
- `sch_key_reversal_top`: H-SCH-8: new 20d high intraday, closes in bottom 25%, vol>=2x
- `sch_loud_pullback_bull`: H-SCH-10 control: same pullback on heavy volume ('not over')
- `sch_quiet_pullback_bull`: H-SCH-10: 7-15% pullback on dry volume in a bull market
- `sch_shakeout_spring`: H-SCH-5 / Wyckoff spring: undercut 40d low, close back above on vol
- `sch_thrust_followthrough`: H-SCH-11: wide-range thrust to 20d high + 3 higher-high/low days
- `selden_distribution_near_high`: Selden: near highs, down-day volume dominates (distribution)
- `selden_updown_vol_strong`: Selden: up-day volume >= 1.5x down-day volume (accumulation)
- `wyc_buying_climax`: H-WYC-3: wide-range high-volume up day after +25% in 40d
- `wyc_dull_range_breakout`: H-WYC-1: narrow 20d range (bottom 20%) on drying volume, close > 20d high on vol>=1.5x
- `wyc_effort_without_result`: H-WYC-2: huge volume, tiny range, near highs after +15% (distribution/churning)
- `wyc_low_volume_retest`: H-WYC-11: new low on much lower volume, closes in upper half
- `wyc_resilience_on_shock`: H-WYC-6: top-decile relative return on a SPY -2% day
- `wyc_selling_climax`: H-WYC-3: wide-range high-volume down day after -20% in 40d
- `wyc_small_giveback_in_correction`: H-WYC-12: in a >=10% market correction, stocks giving back least of their advance (monthly)
- `wyc_streak_5down`: H-WYC-10: 5 consecutive down closes -> bounce
- `wyc_streak_5up`: H-WYC-10: 5 consecutive up closes -> exhaustion
- `wyc_weakest_on_shock`: H-WYC-6 mirror: bottom decile on a SPY -2% day
- `rs_laggards_bear_mkt`: Daniel-Moskowitz: losers rebound in bear/rebound markets (claimed bullish)
- `rs_laggards_bull_mkt`: Bottom-decile 6m RS in a bull market (avoid)
- `rs_leaders_bear_mkt`: Top-decile 6m RS when market below 10m SMA (momentum-crash risk)
- `rs_leaders_bull_mkt`: RL-v2 + O'Neil: top-decile 6m RS when market above 10m SMA (monthly)
- `rsi30_bear_mkt`: RSI14<30 while market in downtrend
- `rsi30_bull_mkt`: RSI14<30 while market in uptrend
- `st_loser_bear_mkt`: Bottom-decile 5d return, market down
- `st_loser_bull_mkt`: Bottom-decile 5d return, market up
- `confluence_breakout`: Trend template + 52w-high breakout + vol>=1.5x + market up
- `confluence_pullback`: Uptrend + pullback to SMA50 + RSI<45 + bullish candle (YouTube confluence)
- `yt_macd_200ema`: TradingLab: close>EMA200, MACD bull cross below zero
- `yt_rsi10_any_trend`: RSI(10)<30 without trend filter (ablation)
- `yt_rsi10_downtrend`: RSI(10)<30 BELOW SMA200 (ablation: falling knife)
- `yt_rsi10_pullback`: Rayner Teo: close>SMA200 & RSI(10)<30 (first fire in 10d)
- `yt_rsi10_pullback_h10`: Same, 10-day horizon
- `yt_rsi10_pullback_rising200`: RSI(10)<30 above a RISING SMA200

## Phase L — v2.2 hardening (Fiscal AI, EODHD, TradingView)

| # | Iteration | Result | Decision |
|---|---|---|---|
| 61 | Data sourcing. Fiscal AI: `companies_list` covers 12,011 companies, but only 170 inactive US names, mostly recent M&A, and its earnings history is fiscal-period-end dates from 2015 onward. EODHD: 33,182 delisted US common stocks and a full historical earnings calendar | Fiscal AI unsuitable for survivorship and earnings-date backtests; EODHD used for both | — |
| 62 | **Survivorship check**: frozen v2.1 classes applied to a random sample of 90 delisted NYSE/NASDAQ stocks (76 usable, 38 ever tradeable, 34 ended ≥80% below peak) | P(dd≥20%/60d): BULLISH 14.3%, NO_SIGNAL 23.9%, BEARISH 37.5% (ordering holds; absolute risk ≈2× survivors); BEARISH 60d return −1.4% vs BULLISH +4.7%; "≥40% below 52w high" +4.7% in survivors vs −3.4% in delisted (P(dd20) 48.6%) | rulebook §3: survivorship-adjusted numbers; deep drawdowns are not bargains |
| 63 | **Earnings flag** (128k EODHD earnings events 2000-2026, 1,501 stocks): P(≥10% drop in 10 trading days), earnings due vs not, by class, development periods | BULLISH 8.5%/7.3% vs 3.1%/2.6%; NO_SIGNAL 12.0%/11.7% vs 7.6%/4.3%; BEARISH 19.0%/14.8% vs 16.5%/8.3% | candidate E1 |
| 64 | **Post-earnings drift**: 9 rules (all events, gap up/down ±5% with ≥2× volume, EPS surprise ±10%, surprise and reaction agreeing, reaction deciles), development periods | none at t ≥ 3; gap-down −0.87%/−0.76% (t −1.4/−2.5), gap-up +0.27%/+0.51%; EPS surprise alone ≈ 0 or wrong sign | 4 candidates frozen for the locked test |
| 65 | **Locked test of 63-64** (holdout tickers in all periods + discovery tickers 2020-26; logged) | E1 replicated in **every** cell (BULLISH 8.5-12.2% vs 2.7-5.8%); drift rules **vanished or reversed** in 2020-26 (gap-down +0.45%, −0.29%; bottom decile +0.79%, +0.15%) | **E1 adopted**; post-earnings drift → NOT-a-signal |
| 66 | **Crash overlays** (VIX ≥ 30, VIX +50%/5d, SPY −7%/−10% in 20d, 20-day realized vol ≥ 30%, combinations), designed on 2000-2019 only | BULLISH crash odds 6.60% → ≥6.47% at best (only 1-7% of calls removed); on SPY, 5 of 6 overlays worsened Sharpe and drawdown through whipsaw | **all rejected** (pre-set criterion not met); shocks stay a documented limitation |
| 67 | Engine v2.2: `--next-earnings`, E1 warning, `p_drop10_10d_est`, D3 risk LOW → NORMAL when earnings due, version stamp | verified on live AAPL bars | — |
| 68 | **Unit tests**: 10 pytest cases (D1-D6, regime, A1, E1, business-day counter, TradingView JSON loader) | 10/10 pass | — |
| 69 | **Forward paper trading**: 98-stock sector-balanced watchlist; TradingView earnings calendar (98 next dates); first journal 2026-10-30 (23 BULLISH / 42 NO_SIGNAL / 33 BEARISH; 23 with earnings due) | 8 closes cross-checked against TradingView: **0.000%** difference | daily scheduled job + automatic scoreboard |
| 70 | Claude skill `ta-signal`; RULEBOOK v2.2 (§3 survivorship, §5 E1, §6 rejected candidates, §8 risk rules 5-6, §11 forward validation) | — | v2.2 frozen |

## Phase M — Intraday: hourly 20-minute windows (Nov 2 2026)

Question: can the user's agent trade short horizons (10-20 minutes) inside a 20-minute window each market hour?

| # | Hypothesis | Test | Result | Decision |
|---|---|---|---|---|
| 71 | Ten intraday rules, pre-registered before any result: VWAP trend (R1), 2.5-sigma reversal vs SPY (R2), opening-range breakout with relative volume (R3), market intraday momentum 15:35-15:55 (R4, Gao et al. 2018), cross-sectional momentum since the open (R5), intraday periodicity (R6, Heston-Korajczyk-Sadka), SPY lead-lag catch-up (R7), RSI(14) 25/75 on 5-minute bars (R8), EMA 9/21 cross (R9), control always-long SPY (C0) | `tagym/intraday_bt.py`: 100 symbols, 60 days of 5-minute bars (Aug 10 to Nov 2 2026), windows xx:35-xx:55 for hours 9-15, entries at xx:35/40/45, exit at the xx:55 open, 2.5 bps per side, date-clustered t. Verdict bar: PASS = net t >= 2.6 and both halves positive | **0 of 10 pass; all REJECT.** Gross edges between -1.1 and +1.2 bps per trade against 5 bps round-trip cost. Best gross t: EMA cross 1.59, periodicity 1.27, cross-sectional momentum 1.11. Even at 1 bp per side every rule is negative net. R4 also fails on 2 years of hourly SPY/QQQ (-0.6 bps gross, 1,440 trades). R7 fired on only 2 days (untestable) | Intraday TA in 20-minute windows goes on the NOT-a-signal list (final wording after the live day) |
| 72 | The live trader reproduces the backtest | Replayed the 12:35 window of Nov 2 through the live code path | 126 of 126 trades identical (rule, symbol, side) | Live and backtest share `bar_signals`; parity confirmed |
| 73 | Asymmetry inside R2 | Split by side | Buying sharp relative drops +3.2 bps gross (567 trades); shorting sharp spikes -3.1 bps | Below costs either way; noted, not traded as a separate rule (it was not pre-registered) |

| 74 | Live paper forward test, all 10 rules | `tagym/intraday.py`, 8 windows (Nov 2 13:35 → Nov 3 15:35), 1,007 trades, $1,000 units, 2.5 bps/side, simulated fills at the next 1-minute bar | +2.3 bps gross, **−2.7 net** per trade, −$268; 2 of 8 windows positive (t −1.3). Rules within noise of the backtest except R6 periodicity (+5.7 gross on one correlated day) | Intraday stays NOT-a-signal (RULEBOOK §12, v2.3). R6 kept on the forward watch list only |
| 75 | Execution with free data | Decision-to-fill delay; live fill vs the backtest's price | 40 s mean delay; shortfall +0.3 bps mean (median 0, ±5.4 per trade); 1 unfilled of 1,008; no stale bars | Execution is not the bottleneck; the edge is |
| 76 | Operations | Scheduled windows run vs planned | 8 of 10 ran; Nov 3 09:35 and 10:35 missed (worker restart); one window needed a resume (closed correctly at its xx:55 prices) | Resume logic kept; missed windows reported, not back-filled |

**Conclusion of Phase M.** Intraday TA on liquid US large caps in 20-minute windows has no edge after realistic costs. One live day measures execution, not edge, and it agrees with the backtest. Rulebook → v2.3 (§12).
