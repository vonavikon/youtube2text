# youtube2text

[EN](README.md) · **RU** · [中文](README.zh.md) · [Español](README.es.md) · [Français](README.fr.md)
[![VirusTotal](https://img.shields.io/badge/VirusTotal-0%2F75_clean-brightgreen)](https://www.virustotal.com/gui/file/a31c0ee972ddd386b0ffeaa104d93269a91980ffe7de99fe1038691fbc5a33ff)


Скилл Claude Code: превращает видео с YouTube в чистый транскрипт и структурированный конспект его ключевых тезисов.

## Что делает

- Скачивает субтитры видео через [yt-dlp](https://github.com/yt-dlp/yt-dlp) — ручные, если они есть, иначе автоматически сгенерированные.
- Чистит транскрипт: убирает повторы от «скользящего окна», которые дают автосубтитры YouTube, потом склеивает текст и заново расставляет абзацы.
- Записывает полный транскрипт и конспект (тезисы, а не пересказ) рядом друг с другом.

## Зачем

Автосубтитры шумные и полны повторов. Скилл даёт читаемый транскрипт и выжимку, с которой можно работать, причём дедупликацию детерминированно делает скрипт, а не угадывает модель.

## Требования

- [yt-dlp](https://github.com/yt-dlp/yt-dlp): `pip install yt-dlp`
- [Claude Code](https://claude.com/claude-code)

## Установка

Скопируйте эту папку в каталог скиллов:

- **На уровне проекта:** `.claude/skills/youtube2text/`
- **На уровне пользователя:** `~/.claude/skills/youtube2text/`

Затем вызовите его в Claude Code:

```
/youtube2text https://www.youtube.com/watch?v=...
```

## Что получится

```
digested/<slug>/
  conspectus.md              ← key points, grouped by theme
  attachments/transcript.md  ← full cleaned transcript
```

Скилл предлагает короткий slug из названия видео и после вашего подтверждения создаёт оба файла.

## Каталог вывода

По умолчанию `./digested`. Укажите любой путь под ваш проект: скажите скиллу, где хранить, или поменяйте `OUT_DIR` в `SKILL.md`.

## `clean_transcript.py`

Очистка — отдельный скрипт, работает и без Claude:

```bash
python clean_transcript.py \
  --srt video.ru.srt \
  --out transcript.md \
  --title "Title" --source "url" --channel "Channel" --duration "12 min"
```

Все опции — `python clean_transcript.py --help`.

## Ограничения

- Качество ограничено автосубтитрами YouTube. Имена собственные, числа и термины могут быть распознаны с ошибками (например, «Бафет» вместо «Баффет»). Скрипт чистит структуру; исправить ошибки распознавания он не может.
- Если у видео вообще нет субтитров, скилл не сможет его расшифровать — он не запускает распознавание речи по аудио.

## Лицензия

MIT
