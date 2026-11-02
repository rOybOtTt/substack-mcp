# Demo week 2026-11-02 → 2026-11-06: rulebook v2.2 on a simulated $100k account

Mechanical rules (see `platform/tagym/demo.py`). Decisions are made on completed daily bars, filled at the next open, 10 bps cost per side.
**One week is far too short to judge the method.** These numbers test the process (execution, discipline, data), not the edge.
Book of record: **internal simulation**.

**Equity 100,000** (+0.00%) vs SPY benchmark 100,000 (+0.00%). Cash 100,000, 0 positions, 14 orders queued for the next open.

| Date | Equity | SPY benchmark | Cash | Positions |
|---|---|---|---|---|
| 2026-10-30 | 100,000 | 100,000 | 100,000 | 0 |

## Open positions

| Symbol | Shares | Entry | Entry price | Stop | Trimmed |
|---|---|---|---|---|---|

## Orders queued for the next open

| Symbol | Side | Shares | Rule | Reason |
|---|---|---|---|---|
| NYSE:PSX | BUY | 20 | D3 | BULLISH, RS6 +57.2 |
| NYSE:TMO | BUY | 10 | D3 | BULLISH, RS6 +43.4 |
| NYSE:MRK | BUY | 43 | D3 | BULLISH, RS6 +29.7 |
| NYSE:V | BUY | 19 | D3 | BULLISH, RS6 +21.2 |
| NASDAQ:MSFT | BUY | 15 | D3 | BULLISH, RS6 +21.0 |
| NYSE:TGT | BUY | 48 | D3 | BULLISH, RS6 +16.4 |
| NYSE:NUE | BUY | 24 | D3 | BULLISH, RS6 +16.3 |
| NYSE:JNJ | BUY | 29 | D3 | BULLISH, RS6 +16.1 |
| NYSE:KO | BUY | 85 | D3 | BULLISH, RS6 +15.8 |
| NYSE:UNH | BUY | 18 | D3 | BULLISH, RS6 +6.3 |
| NYSE:PG | BUY | 49 | D3 | BULLISH, RS6 +5.9 |
| NYSE:JPM | BUY | 23 | D3 | BULLISH, RS6 +3.5 |
| NYSE:WELL | BUY | 32 | D3 | BULLISH, RS6 +3.5 |
| NASDAQ:MDLZ | BUY | 73 | D3 | BULLISH, RS6 +2.3 |

## Decision log (latest 40)

| Time (NY) | Run | Symbol | Action | Rule | Detail |
|---|---|---|---|---|---|
| 2026-11-01 09:01 | close | NASDAQ:AAPL | SKIP_ENTRY | E1 | BULLISH but earnings within 10 trading days |
| 2026-11-01 09:01 | close | NASDAQ:MRNA | SKIP_ENTRY | E1 | BULLISH but earnings within 10 trading days |
| 2026-11-01 09:01 | close | NYSE:BRK.B | SKIP_ENTRY | E1 | BULLISH but earnings within 10 trading days |
| 2026-11-01 09:01 | close | NYSE:MPC | SKIP_ENTRY | E1 | BULLISH but earnings within 10 trading days |
| 2026-11-01 09:01 | close | NYSE:PFE | SKIP_ENTRY | E1 | BULLISH but earnings within 10 trading days |
| 2026-11-01 09:01 | close | NYSE:WMB | SKIP_ENTRY | E1 | BULLISH but earnings within 10 trading days |
| 2026-11-01 09:01 | close | NYSE:OXY | SKIP_ENTRY | E1 | BULLISH but earnings within 10 trading days |
| 2026-11-01 09:01 | close | NYSE:PSX | QUEUE_BUY | D3 | 20 sh, stop 258.04 (2.5xATR) |
| 2026-11-01 09:01 | close | NYSE:TMO | QUEUE_BUY | D3 | 10 sh, stop 647.79 (2.5xATR) |
| 2026-11-01 09:01 | close | NYSE:MRK | QUEUE_BUY | D3 | 43 sh, stop 138.02 (2.5xATR) |
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
