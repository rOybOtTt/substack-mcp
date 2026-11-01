"""Run this on YOUR OWN computer (normal home/office internet connection) to
download the transcripts of the 300 most-viewed technical-analysis videos.

YouTube blocks transcript requests from cloud servers, which is why the cloud
research run could only use titles/descriptions plus the creators' written
material. With transcripts in hand, `analyze_transcripts.py` re-scores which
concepts the top creators actually teach and how they phrase entry/exit rules.

    pip install youtube-transcript-api pandas
    python fetch_transcripts_locally.py            # writes transcripts/<video_id>.txt
    python analyze_transcripts.py                  # writes transcript_concepts.csv

Be polite: the script sleeps between requests and skips videos already saved.
"""
import time
from pathlib import Path

import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi

HERE = Path(__file__).parent
OUT = HERE / "transcripts"
OUT.mkdir(exist_ok=True)

api = YouTubeTranscriptApi()
vids = pd.read_csv(HERE / "top300_ta_videos.csv")
for i, row in vids.iterrows():
    f = OUT / f"{row['id']}.txt"
    if f.exists():
        continue
    try:
        tr = api.fetch(row["id"], languages=["en", "en-US", "en-GB", "hi", "ur"])
        f.write_text(" ".join(s.text for s in tr.snippets))
        print(f"[{i+1}/{len(vids)}] ok  {row['title'][:70]}")
    except Exception as e:  # no captions, private, region-blocked...
        print(f"[{i+1}/{len(vids)}] skip {row['id']}: {type(e).__name__}")
    time.sleep(2.0)
