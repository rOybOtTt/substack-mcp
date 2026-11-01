"""Concept frequency + rule-phrase extraction over downloaded transcripts.

Counts, per video and view-weighted across the corpus, how often each TA
concept is taught, and pulls sentences that state rules ("buy when", "stop
loss", "never", "only trade") so they can be compared with the rulebook's
tested verdicts (RULEBOOK.md Section 6).
"""
import re
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
CONCEPTS = {
    "support_resistance": r"support|resistance",
    "trend": r"\btrend",
    "candlestick": r"candle|engulfing|doji|hammer|pin bar",
    "chart_pattern": r"head and shoulders|double (top|bottom)|triangle|wedge|flag|pennant|cup and handle",
    "moving_average": r"moving average|\bema\b|\bsma\b",
    "rsi": r"\brsi\b",
    "macd": r"macd",
    "volume": r"volume",
    "fibonacci": r"fibonacci|\bfib\b|golden ratio|0\.618|61\.8",
    "liquidity_smc": r"liquidity|order block|fair value gap|smart money|stop hunt",
    "risk_reward": r"risk (to|reward)|risk-reward|\br ?: ?r\b|reward",
    "stop_loss": r"stop ?loss",
    "win_rate": r"win ?rate|percent of the time|accuracy",
    "timeframe": r"time ?frame",
    "breakout": r"breakout|break out|fake ?out",
    "psychology": r"psycholog|emotion|discipline|patience",
}
RULE = re.compile(r"[^.?!]*\b(buy when|sell when|enter when|only (trade|buy|enter)|never|always|stop loss (goes|at|below|above)|take profit)\b[^.?!]*[.?!]", re.I)

vids = pd.read_csv(HERE / "top300_ta_videos.csv").set_index("id")
rows, rules = [], []
for f in sorted((HERE / "transcripts").glob("*.txt")):
    vid = f.stem
    txt = f.read_text(errors="ignore").lower()
    words = max(1, len(txt.split()))
    r = {"id": vid, "words": words, "views": vids.views.get(vid, 0)}
    for k, pat in CONCEPTS.items():
        r[k] = len(re.findall(pat, txt)) / words * 1000  # mentions per 1000 words
    rows.append(r)
    for m in RULE.finditer(txt):
        rules.append({"id": vid, "sentence": m.group(0).strip()[:300]})
df = pd.DataFrame(rows)
if len(df):
    w = df.views / df.views.sum()
    summary = pd.DataFrame({"mentions_per_1000_words_viewweighted": {k: (df[k] * w).sum() for k in CONCEPTS},
                            "share_of_videos_mentioning": {k: (df[k] > 0).mean() for k in CONCEPTS}})
    summary.sort_values("mentions_per_1000_words_viewweighted", ascending=False).to_csv(HERE / "transcript_concepts.csv")
    pd.DataFrame(rules).to_csv(HERE / "transcript_rule_sentences.csv", index=False)
    print(summary.sort_values("mentions_per_1000_words_viewweighted", ascending=False).round(3))
else:
    print("no transcripts found - run fetch_transcripts_locally.py first")
