# Intraday forward test: 20-minute windows every market hour

Every pre-registered rule from `tagym/intraday_bt.py` is traded on paper in each window (xx:35-xx:55 New York),
one $1,000 unit per trade, 2.5 bps cost per side, flat at xx:55. None of the rules passed the 60-day backtest,
so this measures forward returns and execution; it is not expected to make money.

Sessions: 2 (2026-11-02 → 2026-11-02), trades: 235, P&L +67.67 on $1,000 units, equity 100,067.67.

| Session | Trades | Unfilled | Mean gross (bps) | Mean net (bps) | P&L | Started late (s) |
|---|---|---|---|---|---|---|
| 2026-11-02 13:35 | 105 | 1 | 12.68 | 7.68 | +80.58 | 20.0 |
| 2026-11-02 14:35 | 130 | 0 | 4.01 | -0.99 | -12.91 | 20.0 |

## By rule: forward vs backtest

| Rule | Trades | Fwd gross | Fwd net | Hit rate | Backtest gross | Backtest net | Shortfall vs backtest price |
|---|---|---|---|---|---|---|---|
| C0_spy_long | 2 | -8.14 | -13.14 | 0% | -0.10 | -5.10 | -0.56 |
| R1_vwap_trend | 86 | +14.26 | +9.26 | 67% | +0.01 | -4.99 | +0.75 |
| R2_reversal | 2 | -2.39 | -7.38 | 0% | +0.57 | -4.43 | +1.66 |
| R3_orb | 8 | +2.26 | -2.74 | 38% | -1.02 | -6.02 | +0.70 |
| R5_xs_momentum | 20 | +21.57 | +16.57 | 65% | +1.18 | -3.82 | +2.01 |
| R6_periodicity | 76 | +4.79 | -0.21 | 53% | +0.79 | -4.21 | +0.23 |
| R8_rsi | 24 | -7.91 | -12.91 | 25% | -0.20 | -5.20 | -2.44 |
| R9_ema_cross | 17 | +1.39 | -3.61 | 41% | +1.10 | -3.90 | -1.35 |

Shortfall = return at the backtest's assumed entry (the 5-minute bar's open) minus the return at the live fill (the next 1-minute bar after the decision). Positive = the live delay cost money.

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
