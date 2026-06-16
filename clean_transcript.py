"""Clean SRT subtitles (YouTube auto-captions) into a readable transcript.

YouTube auto-captions use a rolling window: each block repeats the tail of the
previous one plus adds new words. This script removes that overlap, joins the
text, and splits it into paragraphs.

Usage:
    python clean_transcript.py \\
        --srt video.ru.srt \\
        --out transcript.md \\
        --title "Title" --source "https://..." --channel "Channel" --duration "12 min"

Frontmatter is added automatically. If no metadata is passed, only the cleaned
text is written (no frontmatter) — handy for debugging.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path


def parse_srt_blocks(raw: str) -> list[str]:
    """Return the text line of each SRT block (without index and timing)."""
    lines: list[str] = []
    for block in re.split(r"\r?\n\r?\n", raw):
        parts = block.strip().split("\n")
        # Block: [index, timing, text...]. Take everything after the timing line.
        if len(parts) < 3:
            continue
        text = " ".join(parts[2:]).strip()
        text = html.unescape(text)
        if text:
            lines.append(text)
    return lines


def dedup_rolling(lines: list[str]) -> str:
    """Remove rolling-caption overlap: for each line, drop leading words that
    already appear at the end of the previous line."""
    kept_words: list[str] = []
    prev_words: list[str] = []
    for line in lines:
        words = line.split()
        if not words:
            continue
        # Largest k where prev[-k:] == words[:k]
        max_k = min(len(prev_words), len(words))
        overlap = 0
        for k in range(max_k, 0, -1):
            if " ".join(prev_words[-k:]).lower() == " ".join(words[:k]).lower():
                overlap = k
                break
        new_words = words[overlap:]
        if new_words:
            kept_words.extend(new_words)
            prev_words = words

    text = " ".join(kept_words)
    text = re.sub(r"\s+", " ", text).strip()
    # Fix punctuation spacing.
    for sep in (",", ".", "!", "?", ";", ":", ")"):
        text = text.replace(f" {sep}", sep)
    text = text.replace(" (", "(")
    return text


def to_paragraphs(text: str, sentences_per_para: int = 5) -> str:
    """Split text into paragraphs by sentence."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    paragraphs: list[str] = []
    buf: list[str] = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        buf.append(s)
        if len(buf) >= sentences_per_para:
            paragraphs.append(" ".join(buf))
            buf = []
    if buf:
        paragraphs.append(" ".join(buf))
    return "\n\n".join(paragraphs)


FRONTMATTER = """---
type: source
created: {today}
tags: [video-transcript]
source: {source}
channel: {channel}
title: "{title}"
duration: "{duration}"
language: {language}
transcript_method: youtube auto-captions (yt-dlp), deduplicated
---

# {title} — {channel}

> Full transcript. Auto-generated captions — names and terms may be misrecognized.

"""


def build_frontmatter(meta: dict) -> str:
    import datetime

    today = meta.get("today") or datetime.date.today().isoformat()
    return FRONTMATTER.format(
        today=today,
        source=meta.get("source", ""),
        channel=meta.get("channel", ""),
        title=(meta.get("title") or "Video").replace('"', '\\"'),
        duration=meta.get("duration", ""),
        language=meta.get("language", "ru"),
    )


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--srt", required=True, help="Path to the .srt subtitle file")
    p.add_argument("--out", help="Where to write the result (.md). If omitted, stdout")
    p.add_argument("--title", help="Video title (for frontmatter)")
    p.add_argument("--source", help="Source URL (for frontmatter)")
    p.add_argument("--channel", help="Channel (for frontmatter)")
    p.add_argument("--duration", help='Duration, e.g. "12 min" (for frontmatter)')
    p.add_argument("--language", default="ru", help="Language (for frontmatter)")
    p.add_argument(
        "--no-frontmatter", action="store_true", help="Write text only, no frontmatter"
    )
    args = p.parse_args()

    srt_path = Path(args.srt)
    if not srt_path.exists():
        print(f"Error: {srt_path} not found", file=sys.stderr)
        return 1

    raw = srt_path.read_text(encoding="utf-8", errors="replace")
    lines = parse_srt_blocks(raw)
    if not lines:
        print("Error: no text blocks found in SRT", file=sys.stderr)
        return 1

    cleaned = dedup_rolling(lines)
    body = to_paragraphs(cleaned)

    meta = {
        "today": None,
        "source": args.source or "",
        "channel": args.channel or "",
        "title": args.title or "",
        "duration": args.duration or "",
        "language": args.language,
    }
    output = body if args.no_frontmatter else build_frontmatter(meta) + body + "\n"

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        words = len(cleaned.split())
        print(f"Written: {out_path} ({words} words)")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
