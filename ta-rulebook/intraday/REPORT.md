# Intraday forward test: 20-minute windows every market hour

Every pre-registered rule from `tagym/intraday_bt.py` is traded on paper in each window (xx:35-xx:55 New York),
one $1,000 unit per trade, 2.5 bps cost per side, flat at xx:55. None of the rules passed the 60-day backtest,
so this measures forward returns and execution; it is not expected to make money.

Sessions: 3 (2026-11-02 → 2026-11-02), trades: 425, P&L -24.64 on $1,000 units, equity 99,975.36.

| Session | Trades | Unfilled | Mean gross (bps) | Mean net (bps) | P&L | Started late (s) |
|---|---|---|---|---|---|---|
| 2026-11-02 13:35 | 105 | 1 | 12.68 | 7.68 | +80.58 | 20.0 |
| 2026-11-02 14:35 | 130 | 0 | 4.01 | -0.99 | -12.91 | 20.0 |
| 2026-11-02 15:35 | 190 | 0 | 0.14 | -4.86 | -92.31 | 20.0 |

## By rule: forward vs backtest

| Rule | Trades | Fwd gross | Fwd net | Hit rate | Backtest gross | Backtest net | Shortfall vs backtest price |
|---|---|---|---|---|---|---|---|
| C0_spy_long | 3 | -6.09 | -11.09 | 0% | -0.10 | -5.10 | -0.92 |
| R1_vwap_trend | 134 | +7.16 | +2.16 | 59% | +0.01 | -4.99 | +2.24 |
| R2_reversal | 23 | +4.41 | -0.59 | 52% | +0.57 | -4.43 | -1.79 |
| R3_orb | 13 | +4.96 | -0.04 | 54% | -1.02 | -6.02 | +2.09 |
| R4_mkt_momentum | 2 | +0.88 | -4.12 | 0% | -1.10 | -6.10 | -3.80 |
| R5_xs_momentum | 30 | +6.27 | +1.27 | 57% | +1.18 | -3.82 | +5.96 |
| R6_periodicity | 114 | +6.02 | +1.02 | 52% | +0.79 | -4.21 | +0.12 |
| R7_lead_lag | 54 | -0.88 | -5.88 | 41% | +23.31 | +18.31 | -2.21 |
| R8_rsi | 26 | -7.62 | -12.62 | 27% | -0.20 | -5.20 | -2.53 |
| R9_ema_cross | 26 | +5.47 | +0.47 | 46% | +1.10 | -3.90 | -1.68 |

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
