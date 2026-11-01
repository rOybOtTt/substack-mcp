"""Select the 300 most-viewed technical-analysis videos and profile what they teach."""
import re
import sys
from pathlib import Path

import pandas as pd

d = pd.read_csv("all_videos.csv")
TA = re.compile(r"technical analysis|chart|candlestick|candle|indicator|\brsi\b|macd|moving average|\bema\b|\bsma\b|"
                r"support|resistance|price action|pattern|fibonacci|fib\b|elliott|wyckoff|dow theory|breakout|"
                r"volume|vwap|bollinger|ichimoku|stochastic|trend ?line|trend following|swing trad|day trad|scalp|"
                r"smart money|\bict\b|supply (and|&) demand|order block|liquidity|market structure|divergence|"
                r"head and shoulders|double (top|bottom)|cup and handle|flag|triangle|wedge|trading strategy|"
                r"strategy|backtest|stage analysis|vcp|minervini|can ?slim|o'?neil|atr|stop loss|gap", re.I)
NOT = re.compile(r"how does the stock market work|make \$|millions|passive income|dividend|real estate|budget|"
                 r"retire|index fund|roth|401k|credit", re.I)
d["title"] = d["title"].fillna("")
d = d[d.title.str.contains(TA) & ~d.title.str.contains(NOT)].copy()
d = d.sort_values("views", ascending=False).reset_index(drop=True)
top = d.head(300).copy()
top["rank"] = range(1, len(top) + 1)

TOPICS = {
    "candlesticks": r"candle|engulfing|doji|hammer|pin bar",
    "chart_patterns": r"pattern|head and shoulders|double (top|bottom)|triangle|wedge|flag|pennant|cup and handle",
    "support_resistance": r"support|resistance|key level|zones?\b",
    "trend_lines": r"trend ?line|channel",
    "moving_averages": r"moving average|\bema\b|\bsma\b|200 day|golden cross|death cross",
    "rsi": r"\brsi\b|relative strength index",
    "macd": r"macd",
    "bollinger": r"bollinger",
    "stochastic": r"stochastic",
    "volume_vwap": r"volume|vwap|order flow",
    "fibonacci": r"fibonacci|\bfib\b",
    "elliott_wave": r"elliott",
    "wyckoff": r"wyckoff",
    "dow_theory": r"dow theory",
    "ichimoku": r"ichimoku",
    "smart_money_ict": r"smart money|\bict\b|order block|liquidity|fair value gap|\bfvg\b|market structure",
    "supply_demand": r"supply (and|&) demand",
    "price_action": r"price action",
    "breakouts": r"breakout|false breakout|fakeout",
    "divergence": r"divergence",
    "day_trading_scalping": r"day trad|scalp|intraday|\b1 ?min|\b5 ?min",
    "swing_trading": r"swing",
    "full_course": r"full course|complete|masterclass|ultimate|beginner to (advanced|pro)|everything",
    "win_rate_claims": r"win rate|\d+% |never lose|profitable|backtest|tested",
    "risk_management": r"risk|stop loss|position siz",
    "momentum_growth": r"minervini|vcp|can ?slim|o'?neil|momentum|stage analysis",
    "multi_timeframe": r"time ?frame",
}
for t, pat in TOPICS.items():
    top[t] = top.title.str.contains(pat, case=False, regex=True)

rows = []
total_views = top.views.sum()
for t in TOPICS:
    m = top[t]
    rows.append({"topic": t, "videos": int(m.sum()), "views_share": top.views[m].sum() / total_views})
prof = pd.DataFrame(rows).sort_values("views_share", ascending=False)

ch = top.groupby("channel").agg(videos=("id", "count"), views=("views", "sum")).sort_values("views", ascending=False)

top.drop(columns=list(TOPICS)).to_csv("top300_ta_videos.csv", index=False)
prof.to_csv("topic_profile.csv", index=False)
ch.to_csv("channel_profile.csv")

print("videos:", len(top), "total views:", f"{total_views:,}", "median views:", f"{top.views.median():,.0f}",
      "total hours:", round(top.duration_s.sum() / 3600, 1))
print(prof.to_string(index=False))
print(ch.head(30).to_string())
