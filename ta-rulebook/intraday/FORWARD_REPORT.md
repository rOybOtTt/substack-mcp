# Intraday forward test (replay) - 3 trading days (2026-11-04 to 2026-11-06)

Rules frozen at RULEBOOK v2.3 plus the forward-only hypothesis R2L. $1,000 per trade, 2.5 bps per side, windows xx:35-xx:55
(hours 9-15). Verdict bars (PLAN_30D.md): CANDIDATE = >= 20 days, gross t >= 2 and net mean > 0; PASS = >= 40 days, net t >= 3
and both halves positive. Fewer than 20 days is TOO EARLY, whatever the numbers look like.

| Rule | Days | Trades | Gross bps | Net bps | t gross | t net | Hit rate | P&L | 60-day backtest net | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| R7_lead_lag | 3 | 358 | +7.93 | +2.93 | +10.27 | +4.13 | 49% | +105 | +18.31 | TOO EARLY |
| R1_vwap_trend | 3 | 928 | +15.11 | +10.11 | +2.54 | +1.60 | 52% | +939 | -4.99 | TOO EARLY |
| R3_orb | 3 | 107 | +22.24 | +17.24 | +1.06 | +0.72 | 58% | +185 | -6.02 | TOO EARLY |
| R9_ema_cross | 3 | 241 | +4.01 | -0.99 | +0.63 | +0.08 | 51% | -24 | -3.90 | TOO EARLY |
| R5_xs_momentum | 3 | 210 | +5.59 | +0.59 | +0.43 | +0.04 | 47% | +12 | -3.82 | TOO EARLY |
| R6_periodicity | 3 | 798 | +2.61 | -2.39 | +0.27 | -0.25 | 50% | -191 | -4.21 | TOO EARLY |
| R2L_reversal_long | 3 | 88 | -5.28 | -10.28 | +0.06 | -0.09 | 41% | -90 | n/a | TOO EARLY |
| R2_reversal | 3 | 213 | -6.30 | -11.30 | -0.12 | -0.41 | 38% | -241 | -4.43 | TOO EARLY |
| R8_rsi | 3 | 328 | -25.44 | -30.44 | -0.36 | -0.49 | 41% | -998 | -5.20 | TOO EARLY |
| C0_spy_long | 3 | 21 | -5.81 | -10.81 | -0.48 | -0.89 | 33% | -23 | -5.10 | TOO EARLY |
| R4_mkt_momentum | 3 | 6 | -21.31 | -26.31 | -1.77 | -2.18 | 17% | -16 | -6.10 | TOO EARLY |

## By day

| Day | Trades | Mean net bps | P&L |
|---|---|---|---|
| 2026-11-04 | 1118 | -2.92 | -327 |
| 2026-11-05 | 1172 | -4.93 | -578 |
| 2026-11-06 | 1008 | +5.58 | +563 |

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
