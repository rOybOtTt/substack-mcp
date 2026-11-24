# Paper-trading scoreboard (rulebook v2.3)

Journal: 1763 verdicts, 18 trading days (2026-10-30 → 2026-11-24), 98 symbols. Updated 2026-11-24 23:24 UTC.

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
| BULLISH | 190 | 8 | 11.6% | 4.1% | NO (provisional, 8 dates) | +1.35% |
| NO_SIGNAL | 338 | 8 | 17.2% | 7.3% | NO (provisional, 8 dates) | +0.91% |
| BEARISH | 254 | 8 | 35.8% | 12.7% | NO (provisional, 8 dates) | -0.36% |

## Latest verdicts (2026-11-24)

| Symbol | Signal | Row | Health | Timing | Risk | Earnings ≤10d | Warnings |
|---|---|---|---|---|---|---|---|
| NASDAQ:APP | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:AVGO | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:BKNG | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NASDAQ:CEG | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NASDAQ:COIN | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:DASH | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:GOOGL | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:HOOD | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:INTC | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:META | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:MRVL | BEARISH | D2 | BROKEN | NORMAL | HIGH | True | E1: earnings in 5 trading days - short-term crash risk ~2-3x higher (P(>=10% drop in 10d)  |
| NASDAQ:MU | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:NFLX | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:NVDA | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NASDAQ:PEP | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:SNDK | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NASDAQ:TMUS | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:BA | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:BAC | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:BE | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:CAT | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:CBRE | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:CRH | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:ETN | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:FCX | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:GEV | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:GS | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:MLM | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:NEM | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:NKE | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:O | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:PCG | BEARISH | D2 | BROKEN | EXTENDED | HIGH | False |  |
| NYSE:PLD | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:T | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:TJX | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NYSE:UBER | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:VRT | BEARISH | D2 | BROKEN | NORMAL | HIGH | False |  |
| NYSE:VST | BEARISH | D2 | BROKEN | NORMAL | HIGH | nan |  |
| NASDAQ:AAPL | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NASDAQ:AMGN | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NASDAQ:COST | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NASDAQ:LIN | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NASDAQ:MDLZ | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:AMT | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:BRK.B | BULLISH | D3 | HEALTHY | NORMAL | LOW | nan |  |
| NYSE:DIS | BULLISH | D3 | HEALTHY | NORMAL | LOW | False | A3: close is the 52-week closing high - prefer a pullback entry over buying the breakout b |
| NYSE:ECL | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:JNJ | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:KO | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:LLY | BULLISH | D3 | HEALTHY | NORMAL | NORMAL | False |  |
| NYSE:MA | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:MO | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:MRK | BULLISH | D3 | HEALTHY | NORMAL | NORMAL | False |  |
| NYSE:PFE | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:PG | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:TMO | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:V | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NYSE:WELL | BULLISH | D3 | HEALTHY | NORMAL | LOW | False |  |
| NASDAQ:AEP | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NASDAQ:AMD | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NASDAQ:AMZN | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NASDAQ:EQIX | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NASDAQ:EXC | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NASDAQ:MRNA | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NASDAQ:MSFT | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NASDAQ:TSLA | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NASDAQ:WMT | NO_SIGNAL | D6 | NEUTRAL | EXTENDED | NORMAL | False |  |
| NASDAQ:XEL | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:ABBV | NO_SIGNAL | D4 | HEALTHY | EXTENDED | NORMAL | False |  |
| NYSE:AZO | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | True | E1: earnings in 10 trading days - short-term crash risk ~2-3x higher (P(>=10% drop in 10d) |
| NYSE:C | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:CF | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:COP | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:CVX | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:DLR | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:DUK | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:GE | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:HD | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:JPM | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:MCD | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:MPC | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:NEE | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:NUE | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:OXY | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:PM | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:PSX | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:RTX | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:SHW | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:SLB | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:SO | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | nan |  |
| NYSE:TGT | NO_SIGNAL | D4 | HEALTHY | EXTENDED | NORMAL | nan |  |
| NYSE:UNH | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:VLO | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:VMRK | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:VTR | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:VZ | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:WMB | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |
| NYSE:XOM | NO_SIGNAL | D6 | NEUTRAL | NORMAL | NORMAL | False |  |

## Data integrity (TradingView cross-checks): 8 checks, max |diff| 0.000%, last 2026-10-30
