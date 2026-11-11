# Intraday forward test (replay) - 6 trading days (2026-11-04 to 2026-11-11)

Rules frozen at RULEBOOK v2.3 plus the forward-only hypothesis R2L. $1,000 per trade, 2.5 bps per side, windows xx:35-xx:55
(hours 9-15). Verdict bars (PLAN_30D.md): CANDIDATE = >= 20 days, gross t >= 2 and net mean > 0; PASS = >= 40 days, net t >= 3
and both halves positive. Fewer than 20 days is TOO EARLY, whatever the numbers look like.

| Rule | Days | Trades | Gross bps | Net bps | t gross | t net | Hit rate | P&L | 60-day backtest net | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| R1_vwap_trend | 6 | 1,861 | +10.57 | +5.57 | +3.31 | +1.65 | 48% | +1,037 | -4.99 | TOO EARLY |
| R3_orb | 6 | 151 | +17.43 | +12.43 | +1.60 | +1.03 | 54% | +188 | -6.02 | TOO EARLY |
| R7_lead_lag | 5 | 468 | +4.80 | -0.20 | +0.86 | -0.62 | 45% | -9 | +18.31 | TOO EARLY |
| R9_ema_cross | 6 | 446 | +1.92 | -3.08 | +0.59 | -0.55 | 46% | -137 | -3.90 | TOO EARLY |
| R5_xs_momentum | 6 | 420 | +1.66 | -3.34 | +0.27 | -0.54 | 44% | -140 | -3.82 | TOO EARLY |
| R6_periodicity | 6 | 1,596 | +0.46 | -4.54 | +0.09 | -0.93 | 47% | -725 | -4.21 | TOO EARLY |
| C0_spy_long | 6 | 42 | -1.46 | -6.46 | -0.23 | -1.01 | 38% | -27 | -5.10 | TOO EARLY |
| R2L_reversal_long | 6 | 101 | -3.50 | -8.50 | -0.45 | -0.67 | 42% | -86 | n/a | TOO EARLY |
| R8_rsi | 6 | 603 | -16.99 | -21.99 | -0.49 | -0.76 | 43% | -1,326 | -5.20 | TOO EARLY |
| R2_reversal | 6 | 231 | -5.55 | -10.55 | -0.72 | -1.15 | 38% | -244 | -4.43 | TOO EARLY |
| R4_mkt_momentum | 6 | 12 | -16.42 | -21.42 | -2.45 | -3.19 | 17% | -26 | -6.10 | TOO EARLY |

## By day

| Day | Trades | Mean net bps | P&L |
|---|---|---|---|
| 2026-11-04 | 1118 | -2.92 | -327 |
| 2026-11-05 | 1172 | -4.93 | -578 |
| 2026-11-06 | 1008 | +5.58 | +563 |
| 2026-11-09 | 1000 | -8.80 | -880 |
| 2026-11-10 | 790 | +0.88 | +70 |
| 2026-11-11 | 843 | -4.08 | -344 |

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
