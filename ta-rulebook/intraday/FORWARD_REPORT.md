# Intraday forward test (replay) - 15 trading days (2026-11-04 to 2026-11-24)

Rules frozen at RULEBOOK v2.3 plus the forward-only hypothesis R2L. $1,000 per trade, 2.5 bps per side, windows xx:35-xx:55
(hours 9-15). Verdict bars (PLAN_30D.md): CANDIDATE = >= 20 days, gross t >= 2 and net mean > 0; PASS = >= 40 days, net t >= 3
and both halves positive. Fewer than 20 days is TOO EARLY, whatever the numbers look like.

| Rule | Days | Trades | Gross bps | Net bps | t gross | t net | Hit rate | P&L | 60-day backtest net | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| R7_lead_lag | 14 | 1,131 | +7.30 | +2.30 | +1.82 | +0.44 | 45% | +260 | +18.31 | TOO EARLY |
| R3_orb | 15 | 350 | +7.85 | +2.85 | +1.60 | +0.44 | 47% | +100 | -6.02 | TOO EARLY |
| R1_vwap_trend | 15 | 5,059 | +2.26 | -2.74 | +0.89 | -0.62 | 41% | -1,386 | -4.99 | TOO EARLY |
| R8_rsi | 15 | 1,291 | +1.12 | -3.88 | +0.57 | +0.07 | 50% | -501 | -5.20 | TOO EARLY |
| R5_xs_momentum | 15 | 1,050 | +2.37 | -2.63 | +0.56 | -0.61 | 46% | -276 | -3.82 | TOO EARLY |
| R9_ema_cross | 15 | 1,161 | -0.09 | -5.09 | +0.04 | -2.48 | 41% | -591 | -3.90 | TOO EARLY |
| R2_reversal | 15 | 443 | +0.56 | -4.44 | -0.09 | -1.05 | 47% | -197 | -4.43 | TOO EARLY |
| R6_periodicity | 15 | 3,990 | -0.84 | -5.84 | -0.35 | -2.45 | 46% | -2,330 | -4.21 | TOO EARLY |
| R2L_reversal_long | 15 | 174 | -3.99 | -8.99 | -0.88 | -1.25 | 48% | -156 | n/a | TOO EARLY |
| C0_spy_long | 15 | 105 | -4.84 | -9.84 | -1.34 | -2.72 | 32% | -103 | -5.10 | TOO EARLY |
| R4_mkt_momentum | 15 | 30 | -12.19 | -17.19 | -2.39 | -3.36 | 23% | -52 | -6.10 | TOO EARLY |

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
| 2026-11-24 | 969 | -9.18 | -889 |

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
