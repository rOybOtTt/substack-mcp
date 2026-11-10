# Intraday forward test (replay) - 5 trading days (2026-11-04 to 2026-11-10)

Rules frozen at RULEBOOK v2.3 plus the forward-only hypothesis R2L. $1,000 per trade, 2.5 bps per side, windows xx:35-xx:55
(hours 9-15). Verdict bars (PLAN_30D.md): CANDIDATE = >= 20 days, gross t >= 2 and net mean > 0; PASS = >= 40 days, net t >= 3
and both halves positive. Fewer than 20 days is TOO EARLY, whatever the numbers look like.

| Rule | Days | Trades | Gross bps | Net bps | t gross | t net | Hit rate | P&L | 60-day backtest net | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| R1_vwap_trend | 5 | 1,534 | +11.34 | +6.34 | +2.92 | +1.54 | 50% | +972 | -4.99 | TOO EARLY |
| R3_orb | 5 | 144 | +16.40 | +11.40 | +1.02 | +0.46 | 52% | +164 | -6.02 | TOO EARLY |
| R7_lead_lag | 5 | 468 | +4.80 | -0.20 | +0.86 | -0.62 | 45% | -9 | +18.31 | TOO EARLY |
| R9_ema_cross | 5 | 390 | +2.32 | -2.68 | +0.62 | -0.33 | 47% | -104 | -3.90 | TOO EARLY |
| R6_periodicity | 5 | 1,330 | +2.32 | -2.68 | +0.42 | -0.49 | 49% | -357 | -4.21 | TOO EARLY |
| R5_xs_momentum | 5 | 350 | +1.54 | -3.46 | +0.20 | -0.45 | 45% | -121 | -3.82 | TOO EARLY |
| C0_spy_long | 5 | 35 | -2.35 | -7.35 | -0.30 | -0.95 | 40% | -26 | -5.10 | TOO EARLY |
| R2_reversal | 5 | 227 | -5.39 | -10.39 | -0.51 | -0.86 | 38% | -236 | -4.43 | TOO EARLY |
| R2L_reversal_long | 5 | 99 | -3.74 | -8.74 | -0.51 | -0.69 | 41% | -87 | n/a | TOO EARLY |
| R8_rsi | 5 | 501 | -21.49 | -26.49 | -0.53 | -0.75 | 42% | -1,327 | -5.20 | TOO EARLY |
| R4_mkt_momentum | 5 | 10 | -16.37 | -21.37 | -1.99 | -2.60 | 20% | -21 | -6.10 | TOO EARLY |

## By day

| Day | Trades | Mean net bps | P&L |
|---|---|---|---|
| 2026-11-04 | 1118 | -2.92 | -327 |
| 2026-11-05 | 1172 | -4.93 | -578 |
| 2026-11-06 | 1008 | +5.58 | +563 |
| 2026-11-09 | 1000 | -8.80 | -880 |
| 2026-11-10 | 790 | +0.88 | +70 |

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
