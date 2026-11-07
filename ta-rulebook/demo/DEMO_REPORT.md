# Demo week 2026-11-02 → 2026-11-06: rulebook v2.3 on a simulated $100k account

Mechanical rules (see `platform/tagym/demo.py`). Decisions are made on completed daily bars, filled at the next open, 10 bps cost per side.
**One week is far too short to judge the method.** These numbers test the process (execution, discipline, data), not the edge.
Book of record: **internal simulation**.

**Equity 99,572** (-0.43%) vs SPY benchmark 96,819 (-3.18%). Cash 368, 15 positions, 0 orders queued for the next open.

| Date | Equity | SPY benchmark | Cash | Positions |
|---|---|---|---|---|
| 2026-10-30 | 100,000 | 100,000 | 100,000 | 0 |
| 2026-11-02 | 99,964 | 99,032 | 24 | 14 |
| 2026-11-03 | 99,428 | 99,328 | 24 | 14 |
| 2026-11-04 | 102,004 | 100,969 | 5,180 | 13 |
| 2026-11-05 | 99,369 | 96,517 | 6,163 | 13 |
| 2026-11-06 | 99,572 | 96,819 | 368 | 15 |

## Open positions

| Symbol | Shares | Entry | Entry price | Stop | Trimmed |
|---|---|---|---|---|---|
| NASDAQ:AMGN | 8 | 2026-11-06 | 447.44 | 428.87 | False |
| NASDAQ:MDLZ | 69 | 2026-11-02 | 65.30 | 61.46 | False |
| NASDAQ:MRNA | 9 | 2026-11-06 | 245.58 | 191.02 | False |
| NASDAQ:MSFT | 15 | 2026-11-02 | 524.10 | 492.21 | False |
| NYSE:ABBV | 17 | 2026-11-05 | 298.73 | 277.38 | False |
| NYSE:JNJ | 29 | 2026-11-02 | 272.06 | 256.43 | False |
| NYSE:JPM | 23 | 2026-11-02 | 340.94 | 321.20 | False |
| NYSE:KO | 85 | 2026-11-02 | 94.28 | 90.02 | False |
| NYSE:MRK | 43 | 2026-11-02 | 148.82 | 138.02 | False |
| NYSE:PG | 49 | 2026-11-02 | 162.24 | 154.02 | False |
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
| 2026-11-04 | NYSE:PSX | SELL | 20 | 258.04 | STOP |  | -446 |
| 2026-11-05 | NYSE:ABBV | BUY | 17 | 298.73 | D3 | +1.32% |  |
| 2026-11-05 | NYSE:NUE | SELL | 24 | 253.05 | STOP |  | -579 |
| 2026-11-06 | NASDAQ:MRNA | BUY | 9 | 245.58 | D3 | +1.71% |  |
| 2026-11-06 | NASDAQ:AMGN | BUY | 8 | 447.44 | D3 | -2.79% |  |

Execution: 17 market-on-open fills, mean |gap| vs prior close 0.77% (the backtests charged 0.10% per side and did not assume a favourable gap).

## How often an unfinished-bar read disagreed with the evening verdict

| Run | Reads | Disagreed | Rate |
|---|---|---|---|
| midday | 588 | 28 | 4.8% |
| preclose | 294 | 13 | 4.4% |

## Decision log (latest 40)

| Time (NY) | Run | Symbol | Action | Rule | Detail |
|---|---|---|---|---|---|
| 2026-11-05 18:25 | close | NYSE:MO | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-05 18:25 | close | NYSE:VZ | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-05 18:25 | close | NASDAQ:AMZN | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 12:24 | midday | NASDAQ:MRNA | FILL_BUY | D3 | 9 @ 245.58 |
| 2026-11-06 12:24 | midday | NASDAQ:AMGN | FILL_BUY | D3 | 8 @ 447.44 |
| 2026-11-06 12:24 | midday | - | FLIP_LOG | - | recorded 98 unfinished-bar reads |
| 2026-11-06 12:24 | midday | - | FLIP_LOG | - | recorded 98 unfinished-bar reads |
| 2026-11-06 18:25 | close | NYSE:LLY | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:25 | close | NYSE:MA | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:25 | close | NYSE:CVX | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:25 | close | NYSE:ECL | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:25 | close | NASDAQ:AAPL | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:25 | close | NYSE:PM | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:25 | close | NYSE:PFE | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:25 | close | NYSE:MO | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:25 | close | NYSE:AMT | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:25 | close | NASDAQ:EQIX | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:25 | close | NASDAQ:AMZN | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NYSE:LLY | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NYSE:MA | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NYSE:CVX | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NYSE:ECL | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NASDAQ:AAPL | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NYSE:PM | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NYSE:PFE | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NYSE:MO | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NYSE:AMT | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NASDAQ:EQIX | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NASDAQ:AMZN | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NYSE:LLY | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NYSE:MA | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NYSE:CVX | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NYSE:ECL | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NASDAQ:AAPL | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NYSE:PM | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NYSE:PFE | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NYSE:MO | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NYSE:AMT | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NASDAQ:EQIX | SKIP_ENTRY | max_positions | no free slot |
| 2026-11-06 18:26 | close | NASDAQ:AMZN | SKIP_ENTRY | max_positions | no free slot |
