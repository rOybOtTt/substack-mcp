# Paper-trading scoreboard (rulebook v2.3)

Journal: 1274 verdicts, 13 trading days (2026-10-30 → 2026-11-17), 98 symbols. Updated 2026-11-17 23:25 UTC.

Each call is graded once its window has passed (entry = next open). 'Expected' is the rulebook's
stated probability; 'calibrated?' tests realized vs expected at 95% (binomial). The test treats calls as
independent, but calls from one date share one market path: a verdict rests on 20+ distinct call
dates, and fewer than that is shown as 'provisional'.

## ≥20% drawdown within 60 days

| Class | matured calls | call dates | realized | expected | calibrated? | mean excess vs SPY |
|---|---|---|---|---|---|---|
| BULLISH | 0 | 0 | – | – | – | – |
| NO_SIGNAL | 0 | 0 | – | – | – | – |
| BEARISH | 0 | 0 | – | – | – | – |

## ≥10% drop within 10 days

| Class | matured calls | call dates | realized | expected | calibrated? | mean excess vs SPY |
|---|---|---|---|---|---|---|
| BULLISH | 74 | 3 | 13.5% | 4.4% | NO (provisional, 3 dates) | +1.46% |
| NO_SIGNAL | 125 | 3 | 20.0% | 7.5% | NO (provisional, 3 dates) | +0.85% |
| BEARISH | 95 | 3 | 27.4% | 13.0% | NO (provisional, 3 dates) | +1.19% |

## Latest verdicts (2026-11-17)

| Symbol | Signal | Row | Health | Timing | Risk | Earnings ≤10d | Warnings |
|---|---|---|---|---|---|---|---|
| NASDAQ:APP | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NASDAQ:AVGO | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:BKNG | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NASDAQ:CEG | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NASDAQ:COIN | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NASDAQ:DASH | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NASDAQ:GOOGL | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NASDAQ:HOOD | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NASDAQ:INTC | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:META | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:MRVL | BEARISH | D2 | BROKEN | NORMAL | HIGH | True | E1: earnings in 10 trading days - short-term crash risk ~2-3x higher (P(>=10% drop in 10d) |
| NASDAQ:MU | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:NFLX | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:PEP | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NASDAQ:SNDK | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NASDAQ:TMUS | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NASDAQ:TSLA | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:BA | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:BAC | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:BE | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NYSE:CAT | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:CBRE | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NYSE:CRH | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NYSE:GEV | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:GS | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:MCD | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NYSE:MLM | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NYSE:NEM | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NYSE:NKE | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:PCG | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NYSE:T | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:TJX | BEARISH | D2 | BROKEN | NORMAL | HIGH | True | E1: earnings in 1 trading days - short-term crash risk ~2-3x higher (P(>=10% drop in 10d)  |
| NYSE:UBER | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:VRT | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NYSE:VST | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NASDAQ:AAPL | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NASDAQ:AMGN | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NASDAQ:AMZN | BULLISH | D3 | HEALTHY | NORMAL | NORMAL | nan |  |
| NASDAQ:MDLZ | BULLISH | D3 | HEALTHY | NORMAL | LOW | nan |  |
| NASDAQ:MSFT | BULLISH | D3 | HEALTHY | NORMAL | NORMAL | False |  |
| NYSE:ABBV | BULLISH | D3 | HEALTHY | NORMAL | LOW | nan |  |
| NYSE:AMT | BULLISH | D3 | HEALTHY | NORMAL | LOW | nan |  |
| NYSE:COP | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:CVX | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:DIS | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:ECL | BULLISH | D3 | HEALTHY | NORMAL | LOW | nan |  |
| NYSE:JNJ | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:JPM | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:KO | BULLISH | D3 | HEALTHY | NORMAL | LOW | nan |  |
| NYSE:LLY | BULLISH | D3 | HEALTHY | NORMAL | NORMAL | nan |  |
| NYSE:MA | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:MO | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:MRK | BULLISH | D3 | HEALTHY | NORMAL | LOW | nan |  |
| NYSE:NUE | BULLISH | D3 | HEALTHY | NORMAL | NORMAL | False |  |
| NYSE:PFE | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:PG | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:PM | BULLISH | D3 | HEALTHY | NORMAL | LOW | nan |  |
| NYSE:TGT | BULLISH | D3 | HEALTHY | NORMAL | NORMAL | True | E1: earnings in 1 trading days - short-term crash risk ~2-3x higher (P(>=10% drop in 10d)  |
| NYSE:TMO | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:V | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:WELL | BULLISH | D3 | HEALTHY | NORMAL | LOW | nan |  |
| NASDAQ:AEP | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NASDAQ:AMD | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NASDAQ:COST | NO_SIGNAL | D6 | NEUTRAL | EXTENDED | NORMAL | False |  |
| NASDAQ:EQIX | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NASDAQ:EXC | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NASDAQ:LIN | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NASDAQ:MRNA | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NASDAQ:NVDA | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NASDAQ:WMT | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | True | E1: earnings in 2 trading days - short-term crash risk ~2-3x higher (P(>=10% drop in 10d)  |
| NASDAQ:XEL | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NYSE:AZO | NO_SIGNAL | D6 | NEUTRAL | EXTENDED | NORMAL | False |  |
| NYSE:BRK.B | NO_SIGNAL | D4 | HEALTHY | EXTENDED | NORMAL | nan |  |
| NYSE:C | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:CF | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NYSE:DLR | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NYSE:DUK | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NYSE:ETN | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:FCX | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:GE | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:HD | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:MPC | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:NEE | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:O | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NYSE:OXY | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NYSE:PLD | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:PSX | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NYSE:RTX | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:SHW | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:SLB | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:SO | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NYSE:UNH | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:VLO | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:VMRK | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NYSE:VTR | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NYSE:VZ | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:WMB | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NYSE:XOM | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |

## Data integrity (TradingView cross-checks): 8 checks, max |diff| 0.000%, last 2026-10-30
