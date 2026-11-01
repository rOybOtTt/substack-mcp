# Agent feedback: blind test round 2 (rulebook v2.1)

Result: 15 BULLISH (D3), 14 BEARISH (D2), 11 NO_SIGNAL (2 D4, 2 D5, 7 D6, 0 D1).

For signal, decision row, regime, health and timing the rulebook gave one answer for **all 40 cases**. Every Q1/Q2/Q3 boundary used here (strict SMA200 sign, the −10% / −40% / −25% cuts, the EXTENDED tests, the PULLBACK tests, the D1 liquidity floor) was clear. The ambiguities left are in the secondary fields (risk_flag, confidence, warnings) and in how the output is formatted.

## 1. High-vol definition: is it "OR", or does the percentile override? (changes risk_flag)
§1.2: "High-vol if ATR% ≥ 3.0% … or, when available, an ATR percentile ≥ 67."
- **round2-032**: ATR% 2.22 (not high-vol), percentile 74 (high-vol). It is D3, so the reading decides `LOW` vs `NORMAL`. I applied the literal OR and gave `NORMAL`.
- **round2-005**: ATR% 3.02 (high-vol), percentile 45 (not). No effect here (MIXED, NEUTRAL), but in RISK_OFF it would decide HIGH vs NORMAL.
- round2-000 and round2-010 (ATR% < 3, percentile ≥ 67) have the same conflict, with no effect.
- Suggested wording: "High-vol = `atr_pct_percentile_vs_universe ≥ 67` when that field exists; only when it is missing, use ATR% ≥ 3.0%." Or, if OR is intended: "High-vol if **either** test is true."
- RS top-decile ("RS6 > +25 pts (or an RS percentile ≥ 90 when available)") has the same OR-vs-override wording. It had no effect here, because only the percentile is supplied.

## 2. Confidence: does "any *deciding* input" mean an input that actually changed the result?
§9 says "Downgrade to low if any **deciding** input is within its hair-trigger band". But the §10 example (18% off the high, slope −0.05%) gives low confidence even though the slope could not change the result there.
- **round2-037**: pct_from_52w_high −9.9 is in the −10 band, but health is already NEUTRAL because SMA200 is falling. I gave `low`, following the §10 example.
- **round2-005**: the slope (−0.05) does decide the outcome. Close +0.8% from SMA200 is in its band but does not decide it (B1 needs C < SMA200 **and** a falling slope; the stock is above SMA200). I gave `low`.
- **round2-015**: close −0.1% from SMA200 truly decides B1. I gave `low` (no ambiguity here).
- Suggested wording: "Downgrade to low if any listed input is within its band, whether or not it changed the output." Or, the opposite: "…only if moving that input across its threshold would change signal, health or timing."

## 3. The hair-trigger list leaves out several thresholds that decide results
None of these changed confidence under the current list, but an agent cannot tell whether leaving them out is deliberate:
- B3's −25% cut: round2-029 (−25.4) and round2-020 (−25.9). Both cases are also B1, so the result does not change.
- PULLBACK cuts (−7% / −15%, vol10 0.70, RSI10 30): round2-011 (pct60 −6.8), round2-031 (vol10 0.75), round2-032 (RSI10 34.9).
- Slope band edge: round2-017 (−0.11) and round2-036 (−0.15) sit just outside the 0.1% band.
- High-vol cuts: round2-005 (ATR 3.02), round2-035 (ATR 3.00, exactly at the inclusive cut), round2-024 (percentile 66, one below 67, which decides LOW vs NORMAL).
- D1 floor: round2-036 ($vol20 5.3M vs the $5M floor).
- Suggested wording: add "The list is exhaustive; other thresholds never lower confidence." Or add bands such as ±1 pt for −25%, ±0.2 pt for ATR%, ±2 for the ATR percentile, and ±0.05 for vol10.

## 4. A1 trigger: "SPY below its 10-month SMA (RISK_OFF or MIXED)" covers two different sets of cases
A MIXED regime can have SPY **above** its 10-month SMA, with only SMA50 < SMA200. That was true for round2-013 and round2-030. So "below 10-month SMA" and "RISK_OFF or MIXED" pick out different cases.
- It had no effect this round: the only top-decile RS cases (003, 018, 024, 039) are all RISK_ON, and 030 has RS percentile 83.
- Suggested wording: "A1 applies when `market_index_above_10m_sma` is false and RS is top-decile." Or, if the regime is meant: "…when regime ≠ RISK_ON…".

## 5. risk_flag in a MIXED regime
"HIGH if BROKEN, or if high-vol in RISK_OFF" leaves a high-vol non-BROKEN stock in a MIXED regime at NORMAL (round2-005). That is probably intended, but saying "MIXED high-vol → NORMAL" explicitly would remove the doubt.

## 6. Output schema mismatch (the test, not the rulebook)
The answer schema for this test has no `near_threshold` or `invalidation` fields, which §9 requires. I put near-threshold items in `warnings`, prefixed "near_threshold:" (005, 015, 037). Suggestion: add `near_threshold` to the test schema, or say where these items should go.

## Clear this round (no change needed)
- Regime mapping.
- B1/B2/B3 order.
- D-row order: D4 before D5, and D2 before any timing check.
- EXTENDED is checked for every stock (009 BROKEN + EXTENDED, 037 NEUTRAL + EXTENDED), with no effect on the signal.
- PULLBACK is checked only for HEALTHY stocks (019 and 023 would otherwise qualify).
- ret5 test (c) is one-sided.
- Calibration lookup per row and regime.
- D1 thresholds: all 40 cases passed.
