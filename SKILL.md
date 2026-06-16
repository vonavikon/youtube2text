---
name: youtube2text
description: "Turn a YouTube video into a clean transcript and a structured conspectus of its key points. Downloads captions with yt-dlp, removes auto-caption duplication, and writes the transcript plus a conspectus. Triggers: digest this video, make a conspectus of this video, transcribe this video, summarize this youtube video, digest youtube."
---

# youtube2text: YouTube video → transcript + conspectus

Takes a YouTube URL, pulls and cleans the captions into a readable transcript, then writes a conspectus of the video's main points.

**Requirements:** `yt-dlp` (`pip install yt-dlp`) and the bundled `clean_transcript.py` (in this skill's folder).

---

## Output

```
<OUT_DIR>/<slug>/
  conspectus.md              ← conspectus (key points)
  attachments/transcript.md  ← full cleaned transcript
```

- **`<slug>`** — kebab-case, the gist of the title (3-4 words, not the full title, not the channel). Confirmed with the user; renaming later breaks links.
- **`<OUT_DIR>`** — defaults to `./digested`. Point it wherever fits the user's project (`notes/`, `wiki/`, `docs/`, …). On the first run, if the project layout isn't obvious, ask the user where transcripts should live.

Write the conspectus in the video's language.

---

## Stage 1: Probe + slug

Input: a YouTube URL.

```bash
# Metadata
yt-dlp --no-update --skip-download \
  --print "%(title)s ||| %(duration)s ||| %(language)s ||| %(uploader)s" "<URL>"

# What captions exist (manual vs auto)
yt-dlp --no-update --list-subs "<URL>" 2>&1 | grep -iE "available (automatic )?captions|subtitles|^ru|^en|language" | head
```

`duration` is in seconds — convert to minutes for the frontmatter.

**Slug.** Propose a kebab-case slug from the gist of the title. Show the metadata and the proposed slug; confirm with one question. This is the one decision worth pausing for.

---

## Stage 2: Transcript

1. **Download captions.** If manual subtitles exist for the video's language, use them (`--write-subs`); otherwise auto-captions (`--write-auto-subs`). Prefer the original-language caption (e.g. `ru-orig`) over a translated one.

```bash
# auto-captions (usual case)
yt-dlp --no-update --skip-download --write-auto-subs \
  --sub-langs "<lang>" --sub-format srt \
  -o "<OUT_DIR>/<slug>.%(ext)s" "<URL>"
```

(For manual subs, replace `--write-auto-subs` with `--write-subs`.)

2. **Clean** with the bundled script. Adjust the path to your install location — project skills live under `.claude/skills/youtube2text/`, user skills under `~/.claude/skills/youtube2text/`:

```bash
python <skill-dir>/clean_transcript.py \
  --srt "<OUT_DIR>/<slug>.<lang>.srt" \
  --out "<OUT_DIR>/<slug>/attachments/transcript.md" \
  --title "<Title>" \
  --source "<URL>" \
  --channel "<Channel>" \
  --duration "<NN min>" \
  --language "<lang>"
```

The script removes rolling-caption overlap, joins the text, splits it into paragraphs, and adds frontmatter.

---

## Stage 3: Conspectus

Read `attachments/transcript.md` in full. Write the key points to `<OUT_DIR>/<slug>/conspectus.md`.

Structure:

```markdown
---
type: source
created: YYYY-MM-DD
tags: [<domain>, <topic>, video-conspectus]
source: <URL>
channel: <Channel>
title: "<Title>"
duration: "<NN min>"
---

# <Title> — <Channel>

One or two sentences on what the source is about. Full transcript: [transcript.md](./attachments/transcript.md).

## Main idea
...

## <Themed sections>
... group by the source's logic, not chronology. Specifics (names, numbers, experiments) are required.

## Conclusion
...

## See also
- [Full transcript](./attachments/transcript.md)
```

Principles:
- Theses, not retelling. What the source **claims**, with the key evidence/examples.
- Be concrete: names, numbers, named experiments — not generalities.
- Be fair to the source: if the author hedges or is uncertain, say so; flag opinion/commentary vs. fact.
- Size to the video: a short video needs fewer sections. Don't pad.

---

## Stage 4: Report (+ optional index)

Report what was created (paths, word count). If the user's project keeps an index or catalog of notes, offer to add a line pointing at the new conspectus — don't assume one exists, and don't invent structure.

---

## Cleanup

Remove the temporary SRT:
```bash
rm "<OUT_DIR>/<slug>.<lang>.srt"
```

---

## Don't

- **Don't store the raw SRT** — only the cleaned transcript in `attachments/`.
- **Don't duplicate the transcript in the conspectus** — the conspectus is theses; the full transcript lives next to it.
- **Don't skip slug confirmation** — renaming later breaks links.
- If yt-dlp warns about a missing JS runtime (deno) — it doesn't affect captions; ignore it for Stage 2. If extraction fails entirely, update yt-dlp (`pip install -U yt-dlp`).
- If the video has no captions at all, say so and stop — this skill doesn't transcribe audio.
