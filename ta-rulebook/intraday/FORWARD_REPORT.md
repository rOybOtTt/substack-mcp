# Intraday forward test (replay) - 14 trading days (2026-11-04 to 2026-11-23)

Rules frozen at RULEBOOK v2.3 plus the forward-only hypothesis R2L. $1,000 per trade, 2.5 bps per side, windows xx:35-xx:55
(hours 9-15). Verdict bars (PLAN_30D.md): CANDIDATE = >= 20 days, gross t >= 2 and net mean > 0; PASS = >= 40 days, net t >= 3
and both halves positive. Fewer than 20 days is TOO EARLY, whatever the numbers look like.

| Rule | Days | Trades | Gross bps | Net bps | t gross | t net | Hit rate | P&L | 60-day backtest net | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| R3_orb | 14 | 326 | +8.79 | +3.79 | +1.70 | +0.60 | 49% | +124 | -6.02 | TOO EARLY |
| R7_lead_lag | 13 | 1,064 | +7.33 | +2.33 | +1.68 | +0.41 | 46% | +248 | +18.31 | TOO EARLY |
| R1_vwap_trend | 14 | 4,702 | +3.77 | -1.23 | +1.40 | -0.18 | 43% | -577 | -4.99 | TOO EARLY |
| R8_rsi | 14 | 1,211 | +0.34 | -4.66 | +0.48 | +0.01 | 50% | -565 | -5.20 | TOO EARLY |
| R5_xs_momentum | 14 | 980 | +1.98 | -3.02 | +0.43 | -0.66 | 46% | -296 | -3.82 | TOO EARLY |
| R2_reversal | 14 | 433 | +0.85 | -4.15 | +0.07 | -0.84 | 48% | -180 | -4.43 | TOO EARLY |
| R9_ema_cross | 14 | 1,078 | -0.46 | -5.46 | -0.12 | -2.50 | 41% | -589 | -3.90 | TOO EARLY |
| R6_periodicity | 14 | 3,724 | -0.92 | -5.92 | -0.36 | -2.32 | 46% | -2,206 | -4.21 | TOO EARLY |
| R2L_reversal_long | 14 | 171 | -4.21 | -9.21 | -0.93 | -1.28 | 47% | -157 | n/a | TOO EARLY |
| C0_spy_long | 14 | 98 | -5.38 | -10.38 | -1.40 | -2.70 | 33% | -102 | -5.10 | TOO EARLY |
| R4_mkt_momentum | 14 | 28 | -10.28 | -15.28 | -2.02 | -3.00 | 25% | -43 | -6.10 | TOO EARLY |

## By day

| Day | Trades | Mean net bps | P&L |
|---|---|---|---|
| 2026-11-04 | 1118 | -2.92 | -327 |
| 2026-11-05 | 1172 | -4.93 | -578 |
| 2026-11-06 | 1008 | +5.58 | +563 |
| 2026-11-09 | 1000 | -8.80 | -880 |
| 2026-11-10 | 790 | +0.88 | +70 |
| 2026-11-11 | 843 | -4.08 | -344 |
| 2026-11-12 | 927 | -2.21 | -205 |
| 2026-11-13 | 834 | -5.40 | -450 |
| 2026-11-16 | 976 | -10.22 | -998 |
| 2026-11-17 | 989 | +6.57 | +650 |
| 2026-11-18 | 992 | -4.78 | -474 |
| 2026-11-19 | 1019 | -3.28 | -334 |
| 2026-11-20 | 1121 | +1.76 | +197 |
| 2026-11-23 | 1026 | -12.01 | -1,232 |

## Rules

- **R1_vwap_trend**: Close above VWAP, EMA9 > EMA21, 30-min return > 0, SPY above its VWAP -> long (mirror short)
- **R2_reversal**: 15-min return vs SPY beyond 2.5 sigma -> fade it (liquidity provision)
- **R3_orb**: Fresh break of the 9:30-10:00 opening range with relative volume > 1.2 -> trade the break
- **R4_mkt_momentum**: SPY/QQQ 15:35-15:55 in the direction of the prior-close -> 10:00 move (Gao et al. 2018)
- **R5_xs_momentum**: At xx:35 long the 5 strongest / short the 5 weakest stocks since the open (vs SPY)
- **R6_periodicity**: At xx:35 long top / short bottom quintile of the same window's average return over the past 10 days (Heston-Korajczyk-Sadka)
- **R7_lead_lag**: SPY moved > 0.25% in 10 min and the stock lagged (< 30% of SPY's move) -> catch-up trade
- **R8_rsi**: RSI(14) on 5-min bars < 25 -> long, > 75 -> short (retail TA)
- **R9_ema_cross**: EMA9 crosses EMA21 on the last 5-min bar -> trade the cross (retail TA)
- **C0_spy_long**: Control: always long SPY in every window
- **R2L_reversal_long**: R2 restricted to its long side (buy sharp drops vs SPY): forward-only hypothesis from the backtest
