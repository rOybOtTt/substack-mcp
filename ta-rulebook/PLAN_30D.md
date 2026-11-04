# 30-day improvement program (2026-11-04 → 2026-12-04)

Written on 2026-11-04 **before any forward data exists**. Anything not in this file, or decided after seeing forward
data, is exploratory and is labelled so. The rulebook (v2.3) changes only through the gates below.

## 1. What is frozen

| Layer | Frozen at | What runs for 30 days |
|---|---|---|
| Daily rules (RULEBOOK §1–§11) | v2.2 logic, v2.3 text | `paper` journal each evening (98 stocks) + automatic scoring; demo week Nov 2–6 |
| Intraday rules (RULEBOOK §12) | the 10 rules of `tagym/intraday_bt.py` | nightly **replay** of every window (hours 9–15, xx:35–xx:55) on that day's 5-minute bars, appended to `intraday/forward_events.csv.gz` |
| One forward-only hypothesis | **R2L**: R2 restricted to its long side (buy sharp relative drops) | same replay. It came from looking at the 60-day backtest, so it counts only on days after Nov 3 |

Costs: 2.5 bps per side, $1,000 per trade. Forward days start 2026-11-04 (the live test of Nov 2–3 stays reported as live, separately).

## 2. Why a replay

The live process lost 2 of 10 windows to a worker restart and needed this session awake. A nightly replay cannot miss a window. It uses the same signal code. Checked on the 8 live windows (Nov 2–3):

- direction agreed on 100% of matched trades;
- price-only rules (R2, R5, R6, R8, R9) matched 93–100% of trades; the two **volume-based** rules (R1 VWAP, R3 opening range) matched only 49% and 34%, because Yahoo's newest-bar volume is still provisional 20 s after the bar closes, which moves VWAP and relative volume;
- mean gross return per trade over the same windows: replay +2.7 bps, live +2.3 bps. The earlier "126 of 126 identical" check was the same code on final data, which shows less than it seemed to.

Consequence: R1 and R3 forward numbers are with final volume, an optimistic read of what an agent sees in real time. Their verdicts can only be harsher live.

## 3. Verdict bars (fixed now)

Date-clustered t-statistics (one observation per day), costs included, 11 rules (10 + R2L).

| Days of forward data | Possible verdicts |
|---|---|
| < 20 | TOO EARLY, whatever the numbers look like |
| ≥ 20 | **CANDIDATE** if gross t ≥ 2 and net mean > 0; otherwise **NO EDGE** |
| ≥ 40 | **PASS** if net t ≥ 3 and net mean > 0 in both halves |

Dec 4 gives about **22 trading days** (Thanksgiving closed; Nov 27 is a half day). So this program **can reject or shortlist, it cannot pass anything**. A CANDIDATE continues to 40 days (about Jan 5) before the rulebook changes. With 11 rules, one CANDIDATE by luck is expected about once in 5 samples, which is why PASS needs t ≥ 3 and 40 days.

A PASS would move that rule into RULEBOOK §12 as a *tested but small* edge, with its measured net bps, not a recommendation to trade it.

## 4. Weekly review (Fridays after the close)

Each review does the same things, in this order:

1. Read `intraday/FORWARD_REPORT.md`, `paper/SCOREBOARD.md`, `demo/DEMO_REPORT.md`, run logs. Note missed runs or data failures.
2. Add one row to `experiments/ITERATION_LOG.md` (Phase N) with the numbers and the verdict class; no narrative beyond the numbers.
3. Check calibration of the daily rulebook: realized vs stated crash odds (matures from mid-November: 10-day calls first, 60-day calls late January, so only the 10-day part can be judged in this program).
4. Improvement work, only of these kinds:
   - **bug or data fixes** (anything that makes a measurement wrong): free to fix, logged as a correction;
   - **new hypotheses**: written into section 6 below *with the date*, run as shadow rules from that date forward, never judged on days before they were written;
   - **no change** to a frozen rule's definition. A changed rule is a new rule with a new start date.
5. Report to the user in a few lines: what ran, what the data says, what (if anything) changed.

## 5. Gates for editing the rulebook

- Text corrections and measured numbers: any time, noted in the changelog.
- A new signal or a changed threshold: only after its pre-registered bar in section 3, version bump, changelog.
- A rule that fails its bar is recorded as NOT-a-signal; nothing is deleted from the logs.

## 6. Hypotheses added during the program (append only, with date)

| Added | Hypothesis | Shadow start | Notes |
|---|---|---|---|
| 2026-11-04 | R2L: buy sharp relative drops (R2 long side) | 2026-11-04 | from the 60-day backtest (+3.2 bps gross vs −3.1 short side); forward-only |

## 7. Honest limits

- 22 days of 5-minute data is a small sample; a rule with a true +1 bp net edge would not be detectable.
- All windows share market regimes: results are correlated across rules and across trades within a day, which the day-clustered t partly accounts for.
- Yahoo data is free and sometimes revised; the ledger keeps the first computed value of each trade.
- Large-cap US stocks only. Spreads on liquid names are below 2.5 bps per side; slippage on larger size would be higher.
