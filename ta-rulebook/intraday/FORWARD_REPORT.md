# Intraday forward test (replay) - 12 trading days (2026-11-04 to 2026-11-19)

Rules frozen at RULEBOOK v2.3 plus the forward-only hypothesis R2L. $1,000 per trade, 2.5 bps per side, windows xx:35-xx:55
(hours 9-15). Verdict bars (PLAN_30D.md): CANDIDATE = >= 20 days, gross t >= 2 and net mean > 0; PASS = >= 40 days, net t >= 3
and both halves positive. Fewer than 20 days is TOO EARLY, whatever the numbers look like.

| Rule | Days | Trades | Gross bps | Net bps | t gross | t net | Hit rate | P&L | 60-day backtest net | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| R1_vwap_trend | 12 | 3,875 | +6.51 | +1.51 | +2.23 | +0.55 | 45% | +583 | -4.99 | TOO EARLY |
| R3_orb | 12 | 245 | +13.03 | +8.03 | +2.13 | +1.09 | 54% | +197 | -6.02 | TOO EARLY |
| R7_lead_lag | 11 | 864 | +8.16 | +3.16 | +1.60 | +0.51 | 47% | +273 | +18.31 | TOO EARLY |
| R5_xs_momentum | 12 | 840 | +3.06 | -1.94 | +0.66 | -0.42 | 46% | -163 | -3.82 | TOO EARLY |
| R9_ema_cross | 12 | 944 | -0.62 | -5.62 | -0.10 | -2.15 | 41% | -531 | -3.90 | TOO EARLY |
| R2_reversal | 12 | 381 | -0.40 | -5.40 | -0.12 | -0.90 | 47% | -206 | -4.43 | TOO EARLY |
| R8_rsi | 12 | 1,054 | -7.01 | -12.01 | -0.33 | -0.83 | 47% | -1,266 | -5.20 | TOO EARLY |
| R6_periodicity | 12 | 3,192 | -1.00 | -6.00 | -0.41 | -2.44 | 46% | -1,915 | -4.21 | TOO EARLY |
| C0_spy_long | 12 | 84 | -4.86 | -9.86 | -1.15 | -2.33 | 33% | -83 | -5.10 | TOO EARLY |
| R2L_reversal_long | 12 | 165 | -5.04 | -10.04 | -1.15 | -1.46 | 46% | -166 | n/a | TOO EARLY |
| R4_mkt_momentum | 12 | 24 | -9.02 | -14.02 | -1.59 | -2.47 | 29% | -34 | -6.10 | TOO EARLY |

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
