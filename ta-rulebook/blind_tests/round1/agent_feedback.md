# Agent feedback on RULEBOOK v2.0, blind test round 1 (40 cases)

Result: BULLISH 18 (all D3), BEARISH 10 (all D2), NO_SIGNAL 12 (D4 ×2, D5 ×1, D6 ×9, D1 ×0).

Below, each item lists the problem, the cases where it mattered (or came close), the reading I used, and suggested wording. Items are roughly ordered by impact.

---

## 1. PULLBACK volume test is undefined (which volume, which average)
- **Problem.** §4 says "a 7-15% pullback from the 60-day high on volume ≤ 0.7× average". It does not say whether that is today's volume or the volume during the pullback, and it does not say how long the average is. The snapshot has two candidates: `volume_today_vs_50d` and `volume_5d_vs_prior_50d`.
- **Cases.** **round1-007**: about a 7.0% pullback, today 0.51× (passes), 5-day 0.77× (fails), so the label is PULLBACK or NORMAL depending on the reading. round1-012 and round1-022 pass both measures. round1-020 (HEALTHY, D5) fails both.
- **What I did.** I used `volume_5d_vs_prior_50d`, i.e. volume during the pullback. So 007 is NORMAL.
- **Suggested wording.** "...and the 5-day average volume ≤ 0.7× the prior 50-day average volume (`volume_5d_vs_prior_50d ≤ 0.70`)."

## 2. The "60-day high" has no formula and no field
- **Problem.** §1 defines `pct_from_52w_high` on closes but has no 60-day equivalent. The snapshot has no `pct_from_60d_high`. The only way to get it is from the weekly bars (about 12 weeks), where weekly closes understate daily closes and weekly highs are intraday. It is also unclear whether the 7% and 15% bounds are inclusive.
- **Cases.** **round1-007**: close basis 7.0%, intraday-high basis 10.3%. **round1-012**: weekly-close estimate 6.6%. The 52-week close-high (implied from `pct_from_52w_high` = −7.0) falls inside the last 60 days, so the close-based pullback is 7.0%, exactly on the bound. The intraday-high basis gives 9.0%. round1-009: 6.6% on closes but 7.6% on highs (volume fails anyway).
- **What I did.** Close basis, bounds inclusive. Where the 52-week high is inside the 60-day window, I took the pullback as `pct_from_52w_high`. 012 is PULLBACK, a boundary call.
- **Suggested wording.** "`pct_from_60d_high` = C / max(C over last 60 bars) − 1; PULLBACK if −15% ≤ pct_from_60d_high ≤ −7%." Also add that field to the snapshot.

## 3. "RSI14 just crossed above 70" says nothing about RSI that is already above 70
- **Problem.** The test is an event (a cross today). A stock whose RSI14 crossed 70 a few days ago and is still above it is not EXTENDED by the letter of the rule, although most readers would call it overbought. The micro-example in §10 also combines a cross with a +11% week, so it does not settle this.
- **Cases.** **round1-021**: RSI14 72.3, yesterday 73.0, at the 52-week high, RISK_ON. By the letter it is not EXTENDED, so D3 BULLISH (I gave it low confidence). If "RSI14 ≥ 70" alone counted, it would be D4 NO_SIGNAL. round1-018 (a cross today, 67.2 → 70.8) is clear.
- **Suggested wording.** Pick one. Either "EXTENDED only on the day RSI14 crosses from < 70 to ≥ 70; RSI14 staying above 70 afterwards is NOT extended", or "RSI14 crossed above 70 within the last 5 sessions and is still ≥ 70".

## 4. Two conflicting thresholds for "5-day return in top decile", and an unclear "/"
- **Problem.** §1 gives "top-decile ≈ ret5 > +8% for a typical stock" and also "ret5 > 2.2·ATR%·√5 ≈ extreme". These disagree a lot: about 6% for a 1.2% ATR stock against about 25% for a 5% ATR stock. §4 writes "5-day return in top decile / ≥5 straight up closes". The "/" reads as OR, but it could be read as "i.e.". It is also not stated whether today's close counts toward the up-close streak.
- **Cases.** **round1-001**: 5 straight up closes, ret5 7.9% (below 8% and below the scaled 15.8%). It is EXTENDED only because I read "/" as OR, and that turns D3 into D4. round1-031: ret5 8.7% is above 8% but below the scaled 24.7% (NEUTRAL, so the signal does not change, but the timing label does).
- **What I did.** I used the ATR-scaled threshold as the test harness instructed, read "/" as OR, and used `consecutive_up_closes ≥ 5`.
- **Suggested wording.** "EXTENDED if ANY of: (a) RSI14 crossed ≥ 70 today; (b) close > upper Bollinger band (%B > 1); (c) ret5 > 2.2 × ATR% × √5; (d) ≥ 5 consecutive higher closes including today." Delete the "+8%" aside, or label it as illustration only.

## 5. The `risk_flag` formula contradicts §8.2 for high-volatility BULLISH stocks
- **Problem.** §9 says `risk_flag` is LOW whenever the row is D3. §8.2 says "A BULLISH stock with top-tercile ATR% still has crash risk comparable to a NEUTRAL low-vol stock", which would be NORMAL.
- **Cases.** round1-012 (ATR percentile 78), round1-017 (83), round1-022 (77). All are D3 with top-tercile ATR.
- **What I did.** I followed §9 (LOW) and mentioned the volatility in the reason text.
- **Suggested wording.** "risk_flag = LOW if D3 and ATR% not in top tercile; NORMAL if D3 with top-tercile ATR%."

## 6. "Top tercile" ATR and how MIXED regimes count for risk
- **Problem.** The rulebook does not say which ATR% field or cutoff defines "top tercile". I used `atr_pct_percentile_vs_universe ≥ 66.7`. The HIGH clause fires only in RISK_OFF, so very-high-volatility NEUTRAL stocks in a MIXED market get NORMAL.
- **Cases.** round1-033: percentile 70, RISK_OFF, so a NO_SIGNAL case is flagged HIGH. round1-002: 65, just under the cutoff, but RISK_ON so it does not matter. round1-000: 96 with MIXED gives NORMAL. round1-031: 90 with MIXED gives NORMAL.
- **Suggested wording.** "Top tercile = `atr_pct_percentile_vs_universe ≥ 67` (cross-section on the same date). HIGH also applies when regime = MIXED and the index is below its 10-month SMA" (if that is what you intend).

## 7. Confidence is specified only for D2
- **Problem.** D2 says "medium (stronger if RISK_OFF)", but confidence can never be "high", so "stronger" cannot be expressed. Nothing is said about D1, D3, D4, D5 or D6, so I had to make up a convention.
- **What I did.** I used medium by default and low where the row depends on a near-threshold value or an ambiguous mapping: round1-001 (item 4), round1-016 (close only 0.5% above a falling SMA200, so 0.5% from flipping to D2 BEARISH) and round1-021 (item 3).
- **Suggested wording.** Add a table: "D2/D3: medium; D4/D5/D6: medium; any row: downgrade to low if one input is within ±1 pt (or ±0.1%/month for slopes) of its threshold." Either drop "stronger if RISK_OFF" or put it in `evidence`.

## 8. "SMA200 flat" is used but never defined
- **Problem.** §1 makes "rising" a strict sign test, so "falling" by implication is also a strict sign test. Micro-example 4 in §10 talks about a "flat" SMA200, which has no definition. A −0.15%/month slope counts as "falling" for BROKEN purposes, which is a knife-edge.
- **Cases.** round1-035 (slope −0.15; it stays NEUTRAL because the close is above the SMA200 and the regime is MIXED). round1-016 (−0.54 with the close only 0.5% above). round1-026, 036 and 005 are BROKEN with slopes of only −0.29, −0.35 and −0.39%/month.
- **Suggested wording.** Add a dead-band if intended: "flat if |sma200_slope_1m_pct| < 0.10; flat counts as neither rising nor falling." Otherwise state that any negative slope counts as falling.

## 9. Rule A1 uses a different RISK_OFF definition than §2, and the D5 text doesn't say what to apply in MIXED
- **Problem.** A1 says "when the market is RISK_OFF" but its evidence is "SPY < 10-month SMA". That is a MIXED regime when SMA50 > SMA200. D5 covers MIXED and only says "Apply Rule A1". "Top-decile 6-month RS" also needs a field mapping, which I took as `rs_6m_percentile_vs_universe ≥ 90`. Row order is also a factor: HEALTHY + EXTENDED + RISK_OFF hits D4 before D5, so the A1 warning would be skipped.
- **Cases.** round1-020 (MIXED with the index below its 10-month SMA; RS 55, so no A1 warning). round1-031 (same market state, RS 79, NEUTRAL). In this round, no RS ≥ 90 case was outside RISK_ON (001, 012 and 018 were all RISK_ON).
- **Suggested wording.** "A1 applies whenever the index is below its 10-month SMA (RISK_OFF or MIXED) and `rs_6m_percentile_vs_universe ≥ 90`. Attach the A1 warning on D4 and D5 alike."

## 10. The price < $5 test cannot be run
- **Problem.** The bars are rebased to 100 and there is no raw price field, so the price part of D1 cannot be evaluated in any case.
- **Cases.** All 40 cases. I treated price as unknown and assumed it passes.
- **Suggested wording.** Add `last_close_usd` to the snapshot, or state "if raw price is unavailable, skip the price test".

## 11. Dollar-volume window and boundary not stated
- **Problem.** D1 says "median daily $-volume < $5M" without giving the lookback window. The snapshot provides a 20-day median, which I used.
- **Cases.** round1-005 ($5.3M, which passes narrowly and is the D2 case nearest the D1 floor), round1-022 ($7.0M), round1-002 ($7.4M), round1-027 ($7.7M).
- **Suggested wording.** "median of (close × volume) over the last 20 sessions < $5M (strict)."

## 12. Market-regime inputs: month-end vs live, and fields that are noise
- **Problem.** §2 says "SPY **last month-end** close > its 10-month SMA". The snapshot field `market_index_above_10m_sma` does not say whether it is the month-end value or the live value. `market_index_above_200d_sma`, `market_breadth_pct_above_200d` and `market_index_pct_from_52w_high` are also provided but not used. They conflict with the 10-month flag in round1-000 (above 10m SMA but below 200d SMA, breadth 25%), round1-033 (below 10m but above 200d) and round1-035/020/031 (below 10m, SMA50 > SMA200).
- **Suggested wording.** "`market_index_above_10m_sma` = last completed month-end close vs mean of last 10 month-end closes. The daily 200-day flag and breadth are NOT regime inputs (§2 evidence: daily rules whipsaw)."

## 13. Timing labels for non-HEALTHY stocks, and what wins if EXTENDED and PULLBACK both fire
- **Problem.** PULLBACK is defined "in a HEALTHY stock". The rulebook does not say whether EXTENDED is evaluated for NEUTRAL or BROKEN stocks, or which label wins when both conditions are true. One example is a 7-15% pullback with ≥5 up closes, or %B > 1 after a sharp drop.
- **Cases.** In round1-002, 014, 026 and 027 (BROKEN), a 7-15% pullback from the 60-day high exists, but PULLBACK is not allowed. No case had both labels firing this round.
- **What I did.** I evaluated EXTENDED for every stock and PULLBACK only for HEALTHY, non-EXTENDED stocks. Otherwise the label is NORMAL.
- **Suggested wording.** State that order explicitly.

## 14. `pct_from_52w_high`: closes or intraday highs, and are boundaries inclusive?
- **Problem.** §1 defines it on closes, but the snapshot field is not documented. HEALTHY uses "≥ −10%" and BROKEN uses "≤ −40%" on a value rounded to 0.1.
- **Cases.** round1-019 (exactly −10.0; NEUTRAL anyway because the close is below the SMA200), round1-022 (−9.3, HEALTHY by 0.7 pt), round1-032 (−42.0, BROKEN on both clauses).
- **Suggested wording.** "Snapshot `pct_from_52w_high` is close-based; thresholds are inclusive as written."

## 15. A NEUTRAL case that looks broken
- **Problem.** round1-000 closes 11.3% below its SMA200, with SMA50 < SMA200, a 3-month return of −23% and ATR in the 96th percentile. It is still NEUTRAL because the slow SMA200 is still rising (+1.44%/month). If that is intended, say so: "BROKEN deliberately requires a falling SMA200; a fresh breakdown under a rising SMA200 is NEUTRAL." If it is not, consider "or (C < SMA200 and SMA50 < SMA200 and pct_from_52w_high ≤ −25%)".

## 16. Prime directive #1 vs D3 hit rate
- **Problem.** "The default answer is NO_SIGNAL", yet D3 fired on 18 of 40 cases (45%) because many stocks are HEALTHY in a RISK_ON tape. An agent that takes directive #1 literally might suppress D3.
- **Suggested wording.** Add to §0.1: "BULLISH (D3) is a low-risk *class* label and may legitimately apply to a large share of stocks in a bull market; directive #1 refers to return-forecasting signals."

## 17. Minor items
- **Weekly bars.** It is not stated whether the last weekly bar is a partial week ending on the decision day. That matters when estimating 60-day highs from 12 weekly bars.
- **Missing 'leader of the leading group' data.** A4 cannot be applied because there is no industry-group field. round1-001, 012 and 018 are RS ≥ 90, but there is no group data. Either supply it or mark A4 "context only".
- **A1 'top decile' bound.** It is not said whether "top decile" means `≥ 90` or `> 90`. round1-012 and 018 sit exactly at 90 (no effect this round because the regime was RISK_ON).
- **SMA200 slope horizon.** §1 compares to 21 bars ago, and the field is named `_1m_pct`. That looks consistent, but a one-line mapping in the rulebook would remove the guesswork.
