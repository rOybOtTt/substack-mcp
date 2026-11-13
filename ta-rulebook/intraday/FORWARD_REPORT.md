# Intraday forward test (replay) - 8 trading days (2026-11-04 to 2026-11-13)

Rules frozen at RULEBOOK v2.3 plus the forward-only hypothesis R2L. $1,000 per trade, 2.5 bps per side, windows xx:35-xx:55
(hours 9-15). Verdict bars (PLAN_30D.md): CANDIDATE = >= 20 days, gross t >= 2 and net mean > 0; PASS = >= 40 days, net t >= 3
and both halves positive. Fewer than 20 days is TOO EARLY, whatever the numbers look like.

| Rule | Days | Trades | Gross bps | Net bps | t gross | t net | Hit rate | P&L | 60-day backtest net | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| R1_vwap_trend | 8 | 2,466 | +8.70 | +3.70 | +3.31 | +1.30 | 47% | +912 | -4.99 | TOO EARLY |
| R3_orb | 8 | 175 | +16.05 | +11.05 | +1.84 | +1.08 | 54% | +193 | -6.02 | TOO EARLY |
| R7_lead_lag | 7 | 582 | +5.62 | +0.62 | +1.39 | -0.07 | 46% | +36 | +18.31 | TOO EARLY |
| R9_ema_cross | 8 | 612 | +0.62 | -4.38 | +0.40 | -1.09 | 43% | -268 | -3.90 | TOO EARLY |
| R5_xs_momentum | 8 | 560 | +1.25 | -3.75 | +0.23 | -0.68 | 46% | -210 | -3.82 | TOO EARLY |
| C0_spy_long | 8 | 56 | -0.72 | -5.72 | -0.15 | -1.21 | 36% | -32 | -5.10 | TOO EARLY |
| R6_periodicity | 8 | 2,128 | -0.93 | -5.93 | -0.25 | -1.58 | 46% | -1,263 | -4.21 | TOO EARLY |
| R8_rsi | 8 | 748 | -10.42 | -15.42 | -0.25 | -0.60 | 45% | -1,153 | -5.20 | TOO EARLY |
| R2L_reversal_long | 8 | 104 | -3.47 | -8.47 | -0.51 | -0.81 | 40% | -88 | n/a | TOO EARLY |
| R2_reversal | 8 | 245 | -4.89 | -9.89 | -0.53 | -1.09 | 38% | -242 | -4.43 | TOO EARLY |
| R4_mkt_momentum | 8 | 16 | -17.65 | -22.65 | -3.21 | -4.12 | 12% | -36 | -6.10 | TOO EARLY |

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
