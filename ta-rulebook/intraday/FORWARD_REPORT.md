# Intraday forward test (replay) - 7 trading days (2026-11-04 to 2026-11-12)

Rules frozen at RULEBOOK v2.3 plus the forward-only hypothesis R2L. $1,000 per trade, 2.5 bps per side, windows xx:35-xx:55
(hours 9-15). Verdict bars (PLAN_30D.md): CANDIDATE = >= 20 days, gross t >= 2 and net mean > 0; PASS = >= 40 days, net t >= 3
and both halves positive. Fewer than 20 days is TOO EARLY, whatever the numbers look like.

| Rule | Days | Trades | Gross bps | Net bps | t gross | t net | Hit rate | P&L | 60-day backtest net | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| R1_vwap_trend | 7 | 2,206 | +9.27 | +4.27 | +3.19 | +1.39 | 48% | +941 | -4.99 | TOO EARLY |
| R3_orb | 7 | 166 | +16.77 | +11.77 | +1.81 | +1.13 | 54% | +195 | -6.02 | TOO EARLY |
| R7_lead_lag | 6 | 527 | +4.19 | -0.81 | +0.82 | -0.95 | 44% | -43 | +18.31 | TOO EARLY |
| R5_xs_momentum | 7 | 490 | +3.78 | -1.22 | +0.67 | -0.21 | 46% | -60 | -3.82 | TOO EARLY |
| R9_ema_cross | 7 | 511 | +1.71 | -3.29 | +0.60 | -0.74 | 44% | -168 | -3.90 | TOO EARLY |
| C0_spy_long | 7 | 49 | -0.56 | -5.56 | -0.10 | -1.02 | 37% | -27 | -5.10 | TOO EARLY |
| R8_rsi | 7 | 692 | -10.71 | -15.71 | -0.19 | -0.49 | 45% | -1,087 | -5.20 | TOO EARLY |
| R6_periodicity | 7 | 1,862 | -0.87 | -5.87 | -0.20 | -1.36 | 46% | -1,093 | -4.21 | TOO EARLY |
| R2L_reversal_long | 7 | 102 | -3.52 | -8.52 | -0.50 | -0.76 | 41% | -87 | n/a | TOO EARLY |
| R2_reversal | 7 | 239 | -5.22 | -10.22 | -0.66 | -1.16 | 38% | -244 | -4.43 | TOO EARLY |
| R4_mkt_momentum | 7 | 14 | -15.35 | -20.35 | -2.66 | -3.53 | 14% | -28 | -6.10 | TOO EARLY |

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
