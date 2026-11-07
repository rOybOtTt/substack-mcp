# Demo week summary (2026-11-02 → 2026-11-06)

Simulated $100k long-only account run mechanically by rulebook v2.2/v2.3 daily logic (`platform/tagym/demo.py`). **Book of record: internal simulation** (no Alpaca keys were present in the scheduled environment, so no order was sent to a broker). One week is statistically meaningless; this checks the process, not the edge.

## Result (not evidence of anything)

| | Equity | Return |
|---|---|---|
| Demo account (Fri close) | $99,572 | −0.43% |
| SPY bought at the first open | $96,819 | −3.18% |

15 positions held at the end (the maximum), cash $368. Realized loss from the two stop-outs: −$1,024. With 5 days and one correlated book, the gap to SPY has no usable t-statistic.

## Execution

- 17 buys filled at the open: mean gap vs the prior close +0.21%, mean absolute gap 0.77%, largest 2.79% (the backtests charged 10 bps per side and assumed no favourable gap).
- 2 stop-outs, both filled at the stop price because the day's low breached it: PSX on Nov 4 (258.04, −$446) and NUE on Nov 5 (253.05, −$579). The simulation assumes a fill at the stop, never worse; a real gap through the stop would fill lower.

## Rule adherence (every logged action traced to a rule id)

| Action | Rule | Count |
|---|---|---|
| Buy queued and filled | D3 | 17 / 17 |
| Stop-loss sale | §8.1 | 2 |
| Entry skipped, earnings within 10 trading days | E1 | 7 |
| Entry skipped, no free slot | max_positions | 93 |
| Entry skipped, no cash | cash | 4 |
| D2 (verdict turned BEARISH) exits, §8.5 earnings trims | – | 0 |

No SUBMIT_FAILED, STOP_FAILED or RECONCILE_WARN entries (no broker was used).

## Do unfinished-bar reads hold up?

Disagreement between the mid-day / pre-close read and that evening's final verdict: mid-day 4.8% of 588 reads, pre-close 4.4% of 294 reads. By day (mid-day): 5.1%, 2.0%, 9.2%, 3.1%, 4.6%. Reads are mostly stable, but about one in twenty names changes class between mid-day and the close. Trading only on completed bars (as the rules do) avoids acting on those.

## Missed or failed runs, and a bug

- Of 20 scheduled runs, 4 left no trace in the decision log: Nov 3 pre-open, Nov 5 pre-close, Nov 6 pre-open and Nov 6 pre-close. I cannot tell from the data whether they did not fire or failed. No trade depended on them: orders queue after the close and fill at the next executed run's open.
- **Bug (fixed Nov 7, log #80):** from the first stop-loss sale (Nov 4), `trades.csv` was written with shifted columns. The demo report was stale from Nov 4 and the dashboard's demo exports failed from Nov 5. Trading, state and `equity.csv` were unaffected. File repaired (19 rows = 19 fills), writer fixed, regression test added, report and dashboard rebuilt.
- The scheduled task reported success despite these errors; the weekly review now checks each run's own output.

## Takeaways for the next demo

1. Add keys in the environment settings before the pre-open run if a broker book is wanted; otherwise the week stays simulated.
2. Give each scheduled run a non-zero exit on any exception, so a failed report or export cannot look like success.
3. The 15-position cap blocked 93 candidate entries; the cap, not signal scarcity, set the portfolio.
