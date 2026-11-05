# Intraday forward test (replay) - 2 trading days (2026-11-04 to 2026-11-05)

Rules frozen at RULEBOOK v2.3 plus the forward-only hypothesis R2L. $1,000 per trade, 2.5 bps per side, windows xx:35-xx:55
(hours 9-15). Verdict bars (PLAN_30D.md): CANDIDATE = >= 20 days, gross t >= 2 and net mean > 0; PASS = >= 40 days, net t >= 3
and both halves positive. Fewer than 20 days is TOO EARLY, whatever the numbers look like.

| Rule | Days | Trades | Gross bps | Net bps | t gross | t net | Hit rate | P&L | 60-day backtest net | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| C0_spy_long | 2 | 14 | -11.16 | -16.16 | +nan | +nan | 36% | -23 | -5.10 | TOO EARLY |
| R1_vwap_trend | 2 | 705 | +18.18 | +13.18 | +nan | +nan | 52% | +929 | -4.99 | TOO EARLY |
| R2L_reversal_long | 2 | 65 | -31.62 | -36.62 | +nan | +nan | 31% | -238 | n/a | TOO EARLY |
| R2_reversal | 2 | 150 | -20.48 | -25.48 | +nan | +nan | 29% | -382 | -4.43 | TOO EARLY |
| R3_orb | 2 | 87 | +30.45 | +25.45 | +nan | +nan | 62% | +221 | -6.02 | TOO EARLY |
| R4_mkt_momentum | 2 | 4 | -13.04 | -18.04 | +nan | +nan | 25% | -7 | -6.10 | TOO EARLY |
| R5_xs_momentum | 2 | 140 | +11.17 | +6.17 | +nan | +nan | 49% | +86 | -3.82 | TOO EARLY |
| R6_periodicity | 2 | 532 | -1.77 | -6.77 | +nan | +nan | 50% | -360 | -4.21 | TOO EARLY |
| R7_lead_lag | 2 | 192 | +8.63 | +3.63 | +nan | +nan | 54% | +70 | +18.31 | TOO EARLY |
| R8_rsi | 2 | 270 | -42.21 | -47.21 | +nan | +nan | 33% | -1,275 | -5.20 | TOO EARLY |
| R9_ema_cross | 2 | 131 | +10.60 | +5.60 | +nan | +nan | 56% | +73 | -3.90 | TOO EARLY |

## By day

| Day | Trades | Mean net bps | P&L |
|---|---|---|---|
| 2026-11-04 | 1118 | -2.92 | -327 |
| 2026-11-05 | 1172 | -4.93 | -578 |

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
