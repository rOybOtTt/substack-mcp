# Intraday forward test (replay) - 9 trading days (2026-11-04 to 2026-11-16)

Rules frozen at RULEBOOK v2.3 plus the forward-only hypothesis R2L. $1,000 per trade, 2.5 bps per side, windows xx:35-xx:55
(hours 9-15). Verdict bars (PLAN_30D.md): CANDIDATE = >= 20 days, gross t >= 2 and net mean > 0; PASS = >= 40 days, net t >= 3
and both halves positive. Fewer than 20 days is TOO EARLY, whatever the numbers look like.

| Rule | Days | Trades | Gross bps | Net bps | t gross | t net | Hit rate | P&L | 60-day backtest net | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| R1_vwap_trend | 9 | 2,872 | +5.34 | +0.34 | +1.67 | +0.19 | 44% | +98 | -4.99 | TOO EARLY |
| R3_orb | 9 | 190 | +14.31 | +9.31 | +1.65 | +0.83 | 52% | +177 | -6.02 | TOO EARLY |
| R7_lead_lag | 8 | 604 | +5.00 | -0.00 | +0.75 | -0.64 | 45% | -0 | +18.31 | TOO EARLY |
| R9_ema_cross | 9 | 678 | +0.19 | -4.81 | +0.26 | -1.41 | 42% | -326 | -3.90 | TOO EARLY |
| C0_spy_long | 9 | 63 | +0.20 | -4.80 | +0.05 | -1.12 | 38% | -30 | -5.10 | TOO EARLY |
| R8_rsi | 9 | 845 | -5.99 | -10.99 | -0.01 | -0.39 | 49% | -929 | -5.20 | TOO EARLY |
| R5_xs_momentum | 9 | 630 | -0.59 | -5.59 | -0.11 | -1.07 | 45% | -352 | -3.82 | TOO EARLY |
| R2_reversal | 9 | 258 | -3.66 | -8.66 | -0.25 | -0.85 | 39% | -223 | -4.43 | TOO EARLY |
| R6_periodicity | 9 | 2,394 | -1.08 | -6.08 | -0.33 | -1.84 | 45% | -1,456 | -4.21 | TOO EARLY |
| R2L_reversal_long | 9 | 116 | -0.83 | -5.83 | -0.34 | -0.67 | 42% | -68 | n/a | TOO EARLY |
| R4_mkt_momentum | 9 | 18 | -16.90 | -21.90 | -3.45 | -4.47 | 11% | -39 | -6.10 | TOO EARLY |

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
