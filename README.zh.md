# youtube2text

[EN](README.md) · [RU](README.ru.md) · **中文** · [Español](README.es.md) · [Français](README.fr.md)
[![VirusTotal](https://img.shields.io/badge/VirusTotal-0%2F75_clean-brightgreen)](https://www.virustotal.com/gui/file/a31c0ee972ddd386b0ffeaa104d93269a91980ffe7de99fe1038691fbc5a33ff)


一个 Claude Code 技能：把 YouTube 视频转成干净的逐字稿，并整理出结构化的要点摘要。

## 功能

- 用 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 下载视频字幕——有手动字幕就用手动字幕，否则用自动生成的。
- 清理逐字稿：去掉 YouTube 自动字幕因滚动窗口产生的重复，再拼接文本、重新划分段落。
- 把完整逐字稿和摘要（提炼要点，不是复述）一起写出。

## 为什么做

自动字幕噪音多、重复多。这个技能给你一份能读的逐字稿和一份能直接用的要点摘要；去重由脚本按确定性规则完成，而不是让模型猜。

## 依赖

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)：`pip install yt-dlp`
- [Claude Code](https://claude.com/claude-code)

## 安装

把这个文件夹复制到你的技能目录：

- **项目级：**`.claude/skills/youtube2text/`
- **用户级：**`~/.claude/skills/youtube2text/`

然后在 Claude Code 里调用：

```
/youtube2text https://www.youtube.com/watch?v=...
```

## 你会得到

```
digested/<slug>/
  conspectus.md              ← key points, grouped by theme
  attachments/transcript.md  ← full cleaned transcript
```

技能会根据视频标题提议一个简短的 slug，经你确认后生成这两个文件。

## 输出目录

默认是 `./digested`。可以指到项目里任何合适的位置——直接告诉技能路径，或者修改 `SKILL.md` 里的 `OUT_DIR`。

## `clean_transcript.py`

清理这一步是独立脚本，不用 Claude 也能跑：

```bash
python clean_transcript.py \
  --srt video.ru.srt \
  --out transcript.md \
  --title "Title" --source "url" --channel "Channel" --duration "12 min"
```

运行 `python clean_transcript.py --help` 查看全部选项。

## 局限

- 质量受 YouTube 自动字幕水平限制。专有名词、数字、术语可能识别错（比如 “Бафет” 而不是 “Баффет”）。脚本清理的是结构，识别错误修不了。
- 视频完全没有字幕时，技能无法转录——它不对音频做语音转文字。

## 许可证

MIT
