# Demo week 2026-11-02 → 2026-11-06: rulebook v2.3 on a simulated $100k account

Mechanical rules (see `platform/tagym/demo.py`). Decisions are made on completed daily bars, filled at the next open, 10 bps cost per side.
**One week is far too short to judge the method.** These numbers test the process (execution, discipline, data), not the edge.
Book of record: **internal simulation**.

**Equity 102,004** (+2.00%) vs SPY benchmark 100,969 (+0.97%). Cash 5,180, 13 positions, 1 orders queued for the next open.

| Date | Equity | SPY benchmark | Cash | Positions |
|---|---|---|---|---|
| 2026-10-30 | 100,000 | 100,000 | 100,000 | 0 |
| 2026-11-02 | 99,964 | 99,032 | 24 | 14 |
| 2026-11-03 | 99,428 | 99,328 | 24 | 14 |
| 2026-11-04 | 102,004 | 100,969 | 5,180 | 13 |

## Open positions

| Symbol | Shares | Entry | Entry price | Stop | Trimmed |
|---|---|---|---|---|---|
| NASDAQ:MDLZ | 69 | 2026-11-02 | 65.30 | 61.46 | False |
| NASDAQ:MSFT | 15 | 2026-11-02 | 524.10 | 492.21 | False |
| NYSE:JNJ | 29 | 2026-11-02 | 272.06 | 256.43 | False |
| NYSE:JPM | 23 | 2026-11-02 | 340.94 | 321.20 | False |
| NYSE:KO | 85 | 2026-11-02 | 94.28 | 90.02 | False |
| NYSE:MRK | 43 | 2026-11-02 | 148.82 | 138.02 | False |
| NYSE:NUE | 24 | 2026-11-02 | 277.15 | 253.05 | False |
| NYSE:PG | 49 | 2026-11-02 | 162.24 | 154.02 | False |
| NYSE:TGT | 48 | 2026-11-02 | 155.13 | 144.02 | False |
| NYSE:TMO | 10 | 2026-11-02 | 699.86 | 647.79 | False |
| NYSE:UNH | 18 | 2026-11-02 | 406.00 | 379.57 | False |
| NYSE:V | 19 | 2026-11-02 | 415.51 | 395.53 | False |
| NYSE:WELL | 32 | 2026-11-02 | 234.66 | 219.13 | False |

## Orders queued for the next open

| Symbol | Side | Shares | Rule | Reason |
|---|---|---|---|---|
| NYSE:ABBV | BUY | 17 | D3 | BULLISH, RS6 +40.7 |

## Fills

| Date | Symbol | Side | Shares | Price | Rule | Gap vs prior close | P&L |
|---|---|---|---|---|---|---|---|
| 2026-11-02 | NYSE:PSX | BUY | 20 | 280.33 | D3 | -0.88% |  |
| 2026-11-02 | NYSE:TMO | BUY | 10 | 699.86 | D3 | +0.41% |  |
| 2026-11-02 | NYSE:MRK | BUY | 43 | 148.82 | D3 | -0.47% |  |
| 2026-11-02 | NYSE:V | BUY | 19 | 415.51 | D3 | +0.46% |  |
| 2026-11-02 | NASDAQ:MSFT | BUY | 15 | 524.10 | D3 | +0.42% |  |
| 2026-11-02 | NYSE:TGT | BUY | 48 | 155.13 | D3 | +0.49% |  |
| 2026-11-02 | NYSE:NUE | BUY | 24 | 277.15 | D3 | +1.20% |  |
| 2026-11-02 | NYSE:JNJ | BUY | 29 | 272.06 | D3 | -0.42% |  |
| 2026-11-02 | NYSE:KO | BUY | 85 | 94.28 | D3 | +0.21% |  |
| 2026-11-02 | NYSE:UNH | BUY | 18 | 406.00 | D3 | -0.24% |  |
| 2026-11-02 | NYSE:PG | BUY | 49 | 162.24 | D3 | +0.41% |  |
| 2026-11-02 | NYSE:JPM | BUY | 23 | 340.94 | D3 | +1.16% |  |
| 2026-11-02 | NYSE:WELL | BUY | 32 | 234.66 | D3 | +0.03% |  |
| 2026-11-02 | NASDAQ:MDLZ | BUY | 69 | 65.30 | D3 | +0.55% |  |
| 2026-11-04 | NYSE:PSX | SELL | 20 | 258.04 | STOP |  |  |

Execution: 14 market-on-open fills, mean |gap| vs prior close 0.52% (the backtests charged 0.10% per side and did not assume a favourable gap).

## How often an unfinished-bar read disagreed with the evening verdict

| Run | Reads | Disagreed | Rate |
|---|---|---|---|
| midday | 294 | 16 | 5.4% |
| preclose | 294 | 13 | 4.4% |

## Decision log (latest 40)

| Time (NY) | Run | Symbol | Action | Rule | Detail |
|---|---|---|---|---|---|
| 2026-11-03 18:24 | close | NYSE:ABBV | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-03 18:24 | close | NYSE:MA | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-03 18:24 | close | NYSE:PM | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-03 18:24 | close | NYSE:CVX | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-03 18:24 | close | NYSE:ECL | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-03 18:24 | close | NYSE:COP | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-03 18:24 | close | NYSE:PFE | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-03 18:24 | close | NASDAQ:AAPL | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-03 18:24 | close | NYSE:XOM | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-03 18:24 | close | NYSE:MO | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-03 18:24 | close | NYSE:AMT | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-03 18:24 | close | NYSE:OXY | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-03 18:24 | close | NYSE:WMB | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-03 18:24 | close | NASDAQ:EQIX | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-04 08:24 | preopen | NYSE:PSX | HOLD_CHECK | §8.1 | stop 258.04 |
| 2026-11-04 08:24 | preopen | NYSE:TMO | HOLD_CHECK | §8.1 | stop 647.79 |
| 2026-11-04 08:24 | preopen | NYSE:MRK | HOLD_CHECK | §8.1 | stop 138.02 |
| 2026-11-04 08:24 | preopen | NYSE:V | HOLD_CHECK | §8.1 | stop 395.53 |
| 2026-11-04 08:24 | preopen | NASDAQ:MSFT | HOLD_CHECK | §8.1 | stop 492.21 |
| 2026-11-04 08:24 | preopen | NYSE:TGT | HOLD_CHECK | §8.1 | stop 144.02 |
| 2026-11-04 08:24 | preopen | NYSE:NUE | HOLD_CHECK | §8.1 | stop 253.05 |
| 2026-11-04 08:24 | preopen | NYSE:JNJ | HOLD_CHECK | §8.1 | stop 256.43 |
| 2026-11-04 08:24 | preopen | NYSE:KO | HOLD_CHECK | §8.1 | stop 90.02 |
| 2026-11-04 08:24 | preopen | NYSE:UNH | HOLD_CHECK | §8.1 | stop 379.57 |
| 2026-11-04 08:24 | preopen | NYSE:PG | HOLD_CHECK | §8.1 | stop 154.02 |
| 2026-11-04 08:24 | preopen | NYSE:JPM | HOLD_CHECK | §8.1 | stop 321.20 |
| 2026-11-04 08:24 | preopen | NYSE:WELL | HOLD_CHECK | §8.1 | stop 219.13 |
| 2026-11-04 08:24 | preopen | NASDAQ:MDLZ | HOLD_CHECK | §8.1 | stop 61.46 |
| 2026-11-04 08:24 | preopen | - | SUMMARY | - | 0 orders queued for the open, 14 positions |
| 2026-11-04 12:24 | midday | NYSE:PSX | STOP_FILLED | §8.1 stop | 20 @ 258.04 |
| 2026-11-04 12:24 | midday | NYSE:PSX | FILL_SELL | STOP | 20 @ 258.04 |
| 2026-11-04 12:24 | midday | - | FLIP_LOG | - | recorded 98 unfinished-bar reads |
| 2026-11-04 15:24 | preclose | - | FLIP_LOG | - | recorded 98 unfinished-bar reads |
| 2026-11-04 18:24 | close | NYSE:ABBV | QUEUE_BUY | D3 | 17 sh, stop 277.38 (2.5xATR) |
| 2026-11-04 18:24 | close | NASDAQ:AAPL | SKIP_ENTRY | cash | no budget left |
| 2026-11-04 18:24 | close | NYSE:PFE | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-04 18:24 | close | NYSE:CVX | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-04 18:24 | close | NYSE:XOM | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-04 18:24 | close | NYSE:MO | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-04 18:24 | close | NASDAQ:AMZN | SKIP_ENTRY | max_positions | no free slot |
