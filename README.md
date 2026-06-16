# youtube2text

A Claude Code skill that turns a YouTube video into a clean transcript and a structured conspectus of its key points.

## What it does

- Downloads the video's captions with [yt-dlp](https://github.com/yt-dlp/yt-dlp) — manual subtitles if available, otherwise auto-generated.
- Cleans the transcript: removes the rolling-window duplication YouTube auto-captions produce, then joins and re-paragraphs the text.
- Writes the full transcript and a conspectus (theses, not a retelling) side by side.

## Why

Auto-captions are noisy and full of repetition. This gives you a readable transcript and a digest you can act on, with deduplication done deterministically by a script rather than guessed at by the model.

## Requirements

- [yt-dlp](https://github.com/yt-dlp/yt-dlp): `pip install yt-dlp`
- [Claude Code](https://claude.com/claude-code)

## Install

Copy this folder into your skills directory:

- **Project-level:** `.claude/skills/youtube2text/`
- **User-level:** `~/.claude/skills/youtube2text/`

Then invoke it in Claude Code:

```
/youtube2text https://www.youtube.com/watch?v=...
```

## What you get

```
digested/<slug>/
  conspectus.md              ← key points, grouped by theme
  attachments/transcript.md  ← full cleaned transcript
```

The skill proposes a short slug from the title and, on your confirmation, produces both files.

## Output directory

Defaults to `./digested`. Point it anywhere that fits your project — tell the skill where, or edit `OUT_DIR` in `SKILL.md`.

## `clean_transcript.py`

The cleaning step is a standalone script — usable without Claude:

```bash
python clean_transcript.py \
  --srt video.ru.srt \
  --out transcript.md \
  --title "Title" --source "url" --channel "Channel" --duration "12 min"
```

Run `python clean_transcript.py --help` for all options.

## Limitations

- Quality is bounded by YouTube's auto-captions. Proper names, numbers, and terms may be misrecognized (e.g. "Бафет" instead of "Баффет"). The script cleans structure; it cannot fix recognition errors.
- If a video has no captions at all, the skill cannot transcribe it — it does not run speech-to-text on the audio.

## License

MIT
