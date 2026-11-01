# Round 3 agent feedback (rulebook v2.1.1)

Totals: 17 BULLISH (D3), 10 BEARISH (D2), 23 NO_SIGNAL (5 D4, 2 D5, 16 D6, 0 D1). No case received the PULLBACK label.

Two ambiguities could flip a signal. Both come from rounding in the supplied data, not from the rule text. The other four affect only secondary fields.

## Could flip the signal

1. **round3-016: `close_vs_sma200_pct` is printed as `-0.0`.** B1 needs C < SMA200 strictly. I read the minus sign as "below", which gives B1 → BROKEN → D2 BEARISH. If C were exactly equal to or above SMA200, the case would be NEUTRAL → D6 NO_SIGNAL. Confidence is low either way.
   *Suggested wording (§1.2):* "When a supplied value rounds to 0.0, its sign decides any strict comparison (−0.0 means below). Data providers should supply at least two decimals, or explicit booleans such as `close_above_sma200`."

2. **round3-046: `bollinger_pctb` is printed as `1.0` (two-decimal rounding).** EXTENDED (b) needs %B > 1 strictly. I treated 1.0 as not crossing, so the stock is not EXTENDED → D3 BULLISH. A true value of 1.004 would give D4 NO_SIGNAL.
   *Suggested wording (§4):* "A printed value equal to a strict cut-off counts as not crossing it." Alternatively, supply a `close_above_upper_band` boolean.

## Secondary fields only

3. **Scope of `near_threshold`.** The §9 schema describes it as "inputs within a hair of a cut-off". The confidence rule says "List those inputs", meaning only the four exhaustive confidence inputs. I kept `near_threshold` to those four, so it is non-empty exactly when confidence is low. I put other near-misses under `warnings`:
   - round3-003: RS percentile 89, one below the A1 cut, with SPY under its 10-month SMA.
   - round3-030: ATR percentile 66, one below 67. In RISK_OFF, a value of 67 would make risk_flag HIGH.
   - round3-026: ATR percentile exactly 67, so high-vol.
   - round3-006: up_streak 4.
   - round3-012: pct_from_60d_high −6.8.

   *Suggested wording (§9):* "`near_threshold` lists only the four confidence inputs. Near-misses on other cut-offs may go under `warnings` and never change confidence."

4. **±1 band boundary (round3-000, pct_from_52w_high exactly −9.0).** I treated it as inside the band (|x − (−10)| = 1.0), following "inclusive as written".
   *Suggested wording:* "within ±1 pt means |x − cut| ≤ 1."

5. **A3 on a D3 row (round3-008, 039, 046, each closing at a new 52-week high, pct_from_52w_high = 0.0).** The rulebook says not to buy the breakout bar, but it does not say whether to attach a warning. I attached an A3 warning and left the output unchanged.
   *Suggested wording (§7):* "If today's close is the 52-week closing high, attach an A3 warning to a D3 output. The output is unchanged."

6. **D4 when the regime is not RISK_ON (round3-049: HEALTHY, EXTENDED, RISK_OFF, top-decile RS).** First match gives D4. Its RISK_OFF calibration (11.1%) is lower than D5's (12.3%). The D4 text does not mention the bad market.
   *Suggested wording (D4):* "If regime ≠ RISK_ON, also say 'healthy stock in an unhealthy market' and check A1." I attached A1 and mentioned D5 in the warnings.

Nothing else in the rulebook was ambiguous. No case triggered D1: all have at least 260 bars, a close of $5 or more, and $vol20 of at least $5M (lowest: 6.6M). Every supplied ATR and RS percentile was used in place of the raw thresholds (round3-001, 035 and 037 have ATR% ≥ 3 but are not high-vol).
