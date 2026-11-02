# Demo week 2026-11-02 → 2026-11-06: rulebook v2.2 on a simulated $100k account

Mechanical rules (see `platform/tagym/demo.py`). Decisions are made on completed daily bars, filled at the next open, 10 bps cost per side.
**One week is far too short to judge the method.** These numbers test the process (execution, discipline, data), not the edge.
Book of record: **internal simulation**.

**Equity 99,964** (-0.04%) vs SPY benchmark 99,032 (-0.97%). Cash 24, 14 positions, 0 orders queued for the next open.

| Date | Equity | SPY benchmark | Cash | Positions |
|---|---|---|---|---|
| 2026-10-30 | 100,000 | 100,000 | 100,000 | 0 |
| 2026-11-02 | 99,964 | 99,032 | 24 | 14 |

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
| NYSE:PSX | 20 | 2026-11-02 | 280.33 | 258.04 | False |
| NYSE:TGT | 48 | 2026-11-02 | 155.13 | 144.02 | False |
| NYSE:TMO | 10 | 2026-11-02 | 699.86 | 647.79 | False |
| NYSE:UNH | 18 | 2026-11-02 | 406.00 | 379.57 | False |
| NYSE:V | 19 | 2026-11-02 | 415.51 | 395.53 | False |
| NYSE:WELL | 32 | 2026-11-02 | 234.66 | 219.13 | False |

## Orders queued for the next open

| Symbol | Side | Shares | Rule | Reason |
|---|---|---|---|---|

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

Execution: 14 market-on-open fills, mean |gap| vs prior close 0.52% (the backtests charged 0.10% per side and did not assume a favourable gap).

## How often an unfinished-bar read disagreed with the evening verdict

| Run | Reads | Disagreed | Rate |
|---|---|---|---|
| midday | 98 | 5 | 5.1% |
| preclose | 98 | 5 | 5.1% |

## Decision log (latest 40)

| Time (NY) | Run | Symbol | Action | Rule | Detail |
|---|---|---|---|---|---|
| 2026-11-01 09:01 | close | NYSE:V | QUEUE_BUY | D3 | 19 sh, stop 395.53 (2.5xATR) |
| 2026-11-01 09:01 | close | NASDAQ:MSFT | QUEUE_BUY | D3 | 15 sh, stop 492.21 (2.5xATR) |
| 2026-11-01 09:01 | close | NYSE:TGT | QUEUE_BUY | D3 | 48 sh, stop 144.02 (2.5xATR) |
| 2026-11-01 09:01 | close | NYSE:NUE | QUEUE_BUY | D3 | 24 sh, stop 253.05 (2.5xATR) |
| 2026-11-01 09:01 | close | NYSE:JNJ | QUEUE_BUY | D3 | 29 sh, stop 256.43 (2.5xATR) |
| 2026-11-01 09:01 | close | NYSE:KO | QUEUE_BUY | D3 | 85 sh, stop 90.02 (2.5xATR) |
| 2026-11-01 09:01 | close | NYSE:UNH | QUEUE_BUY | D3 | 18 sh, stop 379.57 (2.5xATR) |
| 2026-11-01 09:01 | close | NYSE:PG | QUEUE_BUY | D3 | 49 sh, stop 154.02 (2.5xATR) |
| 2026-11-01 09:01 | close | NYSE:JPM | QUEUE_BUY | D3 | 23 sh, stop 321.20 (2.5xATR) |
| 2026-11-01 09:01 | close | NYSE:WELL | QUEUE_BUY | D3 | 32 sh, stop 219.13 (2.5xATR) |
| 2026-11-01 09:01 | close | NASDAQ:MDLZ | QUEUE_BUY | D3 | 73 sh, stop 61.46 (2.5xATR) |
| 2026-11-01 09:01 | close | NYSE:AMT | SKIP_ENTRY | cash | no budget left |
| 2026-11-01 09:01 | close | NASDAQ:EQIX | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-02 08:27 | preopen | - | SUMMARY | - | 14 orders queued for the open, 0 positions |
| 2026-11-02 12:31 | midday | NYSE:PSX | FILL_BUY | D3 | 20 @ 280.33 |
| 2026-11-02 12:31 | midday | NYSE:TMO | FILL_BUY | D3 | 10 @ 699.86 |
| 2026-11-02 12:31 | midday | NYSE:MRK | FILL_BUY | D3 | 43 @ 148.82 |
| 2026-11-02 12:31 | midday | NYSE:V | FILL_BUY | D3 | 19 @ 415.51 |
| 2026-11-02 12:31 | midday | NASDAQ:MSFT | FILL_BUY | D3 | 15 @ 524.10 |
| 2026-11-02 12:31 | midday | NYSE:TGT | FILL_BUY | D3 | 48 @ 155.13 |
| 2026-11-02 12:31 | midday | NYSE:NUE | FILL_BUY | D3 | 24 @ 277.15 |
| 2026-11-02 12:31 | midday | NYSE:JNJ | FILL_BUY | D3 | 29 @ 272.06 |
| 2026-11-02 12:31 | midday | NYSE:KO | FILL_BUY | D3 | 85 @ 94.28 |
| 2026-11-02 12:31 | midday | NYSE:UNH | FILL_BUY | D3 | 18 @ 406.00 |
| 2026-11-02 12:31 | midday | NYSE:PG | FILL_BUY | D3 | 49 @ 162.24 |
| 2026-11-02 12:31 | midday | NYSE:JPM | FILL_BUY | D3 | 23 @ 340.94 |
| 2026-11-02 12:31 | midday | NYSE:WELL | FILL_BUY | D3 | 32 @ 234.66 |
| 2026-11-02 12:31 | midday | NASDAQ:MDLZ | FILL_BUY | D3 | 69 @ 65.30 |
| 2026-11-02 12:31 | midday | - | FLIP_LOG | - | recorded 98 unfinished-bar reads |
| 2026-11-02 15:24 | preclose | - | FLIP_LOG | - | recorded 98 unfinished-bar reads |
| 2026-11-02 18:25 | close | NYSE:ABBV | SKIP_ENTRY | cash | no budget left |
| 2026-11-02 18:25 | close | NYSE:PM | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-02 18:25 | close | NASDAQ:AAPL | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-02 18:25 | close | NYSE:CVX | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-02 18:25 | close | NYSE:PFE | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-02 18:25 | close | NYSE:COP | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-02 18:25 | close | NYSE:XOM | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-02 18:25 | close | NYSE:MO | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-02 18:25 | close | NYSE:AMT | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-02 18:25 | close | NYSE:OXY | SKIP_ENTRY | max_positions | no free slot |
