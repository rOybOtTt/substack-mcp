# Intraday forward test (replay) - 4 trading days (2026-11-04 to 2026-11-09)

Rules frozen at RULEBOOK v2.3 plus the forward-only hypothesis R2L. $1,000 per trade, 2.5 bps per side, windows xx:35-xx:55
(hours 9-15). Verdict bars (PLAN_30D.md): CANDIDATE = >= 20 days, gross t >= 2 and net mean > 0; PASS = >= 40 days, net t >= 3
and both halves positive. Fewer than 20 days is TOO EARLY, whatever the numbers look like.

| Rule | Days | Trades | Gross bps | Net bps | t gross | t net | Hit rate | P&L | 60-day backtest net | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| R1_vwap_trend | 4 | 1,285 | +11.53 | +6.53 | +2.28 | +1.21 | 51% | +840 | -4.99 | TOO EARLY |
| R7_lead_lag | 4 | 429 | +5.69 | +0.69 | +1.37 | -0.04 | 46% | +29 | +18.31 | TOO EARLY |
| R3_orb | 4 | 126 | +18.45 | +13.45 | +0.96 | +0.52 | 55% | +169 | -6.02 | TOO EARLY |
| R9_ema_cross | 4 | 315 | +2.18 | -2.82 | +0.49 | -0.24 | 48% | -89 | -3.90 | TOO EARLY |
| R5_xs_momentum | 4 | 280 | +3.50 | -1.50 | +0.37 | -0.16 | 46% | -42 | -3.82 | TOO EARLY |
| R2L_reversal_long | 4 | 98 | -2.81 | -7.81 | +0.26 | +0.05 | 42% | -76 | n/a | TOO EARLY |
| R2_reversal | 4 | 225 | -5.01 | -10.01 | +0.23 | -0.16 | 39% | -225 | -4.43 | TOO EARLY |
| R6_periodicity | 4 | 1,064 | +1.01 | -3.99 | +0.15 | -0.58 | 50% | -424 | -4.21 | TOO EARLY |
| C0_spy_long | 4 | 28 | -1.05 | -6.05 | -0.11 | -0.61 | 43% | -17 | -5.10 | TOO EARLY |
| R8_rsi | 4 | 440 | -26.04 | -31.04 | -0.63 | -0.81 | 40% | -1,366 | -5.20 | TOO EARLY |
| R4_mkt_momentum | 4 | 8 | -21.24 | -26.24 | -2.49 | -3.08 | 12% | -21 | -6.10 | TOO EARLY |

## By day

| Day | Trades | Mean net bps | P&L |
|---|---|---|---|
| 2026-11-04 | 1118 | -2.92 | -327 |
| 2026-11-05 | 1172 | -4.93 | -578 |
| 2026-11-06 | 1008 | +5.58 | +563 |
| 2026-11-09 | 1000 | -8.80 | -880 |

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
