"""Collect metadata for the most-viewed technical-analysis videos on YouTube.

Uses yt-dlp's search (metadata only; no downloads). Ranks by view count,
deduplicates, and writes top_videos.csv.

Usage:  python collect_youtube_corpus.py [out_dir]
"""
import csv
import json
import subprocess
import sys
import time
from pathlib import Path

QUERIES = [
    "technical analysis full course", "technical analysis for beginners",
    "how to read stock charts", "stock chart patterns", "candlestick patterns",
    "support and resistance trading", "price action trading", "trend lines trading",
    "moving average trading strategy", "200 day moving average", "golden cross death cross",
    "RSI indicator strategy", "MACD indicator strategy", "bollinger bands strategy",
    "volume analysis trading", "VWAP trading strategy", "fibonacci retracement trading",
    "elliott wave theory", "wyckoff method", "dow theory", "head and shoulders pattern",
    "double top double bottom", "cup and handle pattern", "breakout trading strategy",
    "swing trading strategy", "day trading strategy", "market structure trading",
    "smart money concepts", "ICT trading concepts", "supply and demand trading",
    "stochastic indicator", "ichimoku cloud", "divergence trading", "best trading indicator",
    "trading strategy backtest", "stage analysis weinstein", "minervini VCP",
    "CAN SLIM william oneil", "multiple time frame analysis", "trend following trading",
    "mean reversion trading strategy", "chart patterns cheat sheet", "how to trade stocks",
    "ATR stop loss", "relative strength stocks", "gap trading strategy",
    "technical analysis does it work", "is technical analysis real",
]
PER_QUERY = 60


def search(q: str, n: int):
    cmd = ["yt-dlp", "--flat-playlist", "-J", f"ytsearch{n}:{q}"]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if out.returncode != 0:
        print("ERR", q, out.stderr[-300:], file=sys.stderr)
        return []
    data = json.loads(out.stdout)
    rows = []
    for e in data.get("entries") or []:
        rows.append({
            "id": e.get("id"),
            "title": e.get("title"),
            "channel": e.get("channel") or e.get("uploader"),
            "views": e.get("view_count") or 0,
            "duration_s": e.get("duration") or 0,
            "description": (e.get("description") or "").replace("\n", " ")[:500],
            "query": q,
        })
    return rows


def main():
    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    allrows = {}
    for q in QUERIES:
        rows = search(q, PER_QUERY)
        for r in rows:
            if r["id"] and (r["id"] not in allrows or r["views"] > allrows[r["id"]]["views"]):
                prev_q = allrows.get(r["id"], {}).get("queries", "")
                r["queries"] = (prev_q + ";" if prev_q else "") + q
                allrows[r["id"]] = r
        print(f"{q!r}: {len(rows)} results, total unique {len(allrows)}", flush=True)
        time.sleep(2)
    ranked = sorted(allrows.values(), key=lambda r: -r["views"])
    with open(out_dir / "all_videos.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["rank", "id", "title", "channel", "views", "duration_s", "queries", "description"])
        w.writeheader()
        for i, r in enumerate(ranked, 1):
            r = dict(r); r["rank"] = i; r.pop("query", None)
            w.writerow(r)
    print("wrote", len(ranked))


if __name__ == "__main__":
    main()
