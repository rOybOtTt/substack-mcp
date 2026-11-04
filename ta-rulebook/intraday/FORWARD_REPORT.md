# Intraday forward test (replay) - 1 trading days (2026-11-04 to 2026-11-04)

Rules frozen at RULEBOOK v2.3 plus the forward-only hypothesis R2L. $1,000 per trade, 2.5 bps per side, windows xx:35-xx:55
(hours 9-15). Verdict bars (PLAN_30D.md): CANDIDATE = >= 20 days, gross t >= 2 and net mean > 0; PASS = >= 40 days, net t >= 3
and both halves positive. Fewer than 20 days is TOO EARLY, whatever the numbers look like.

| Rule | Days | Trades | Gross bps | Net bps | t gross | t net | Hit rate | P&L | 60-day backtest net | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| C0_spy_long | 1 | 7 | +7.77 | +2.77 | +nan | +nan | 43% | +2 | -5.10 | TOO EARLY |
| R1_vwap_trend | 1 | 310 | +11.50 | +6.50 | +nan | +nan | 53% | +201 | -4.99 | TOO EARLY |
| R2L_reversal_long | 1 | 37 | -31.49 | -36.49 | +nan | +nan | 30% | -135 | n/a | TOO EARLY |
| R2_reversal | 1 | 95 | -30.89 | -35.89 | +nan | +nan | 24% | -341 | -4.43 | TOO EARLY |
| R3_orb | 1 | 51 | +33.19 | +28.19 | +nan | +nan | 69% | +144 | -6.02 | TOO EARLY |
| R4_mkt_momentum | 1 | 2 | -28.25 | -33.25 | +nan | +nan | 0% | -7 | -6.10 | TOO EARLY |
| R5_xs_momentum | 1 | 70 | -9.42 | -14.42 | +nan | +nan | 40% | -101 | -3.82 | TOO EARLY |
| R6_periodicity | 1 | 266 | +12.88 | +7.88 | +nan | +nan | 57% | +210 | -4.21 | TOO EARLY |
| R7_lead_lag | 1 | 59 | +9.89 | +4.89 | +nan | +nan | 59% | +29 | +18.31 | TOO EARLY |
| R8_rsi | 1 | 156 | -12.80 | -17.80 | +nan | +nan | 37% | -278 | -5.20 | TOO EARLY |
| R9_ema_cross | 1 | 65 | -2.84 | -7.84 | +nan | +nan | 45% | -51 | -3.90 | TOO EARLY |

## By day

| Day | Trades | Mean net bps | P&L |
|---|---|---|---|
| 2026-11-04 | 1118 | -2.92 | -327 |

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
