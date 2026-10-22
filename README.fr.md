# youtube2text

[EN](README.md) · [RU](README.ru.md) · [中文](README.zh.md) · [Español](README.es.md) · **Français**

Un skill Claude Code qui transforme une vidéo YouTube en transcription propre et en résumé structuré de ses points clés.

## Ce qu'il fait

- Télécharge les sous-titres de la vidéo avec [yt-dlp](https://github.com/yt-dlp/yt-dlp) — les manuels s'ils existent, sinon les auto-générés.
- Nettoie la transcription : supprime les doublons issus de la fenêtre glissante des sous-titres automatiques de YouTube, puis rejoint le texte et le redécoupe en paragraphes.
- Écrit la transcription complète et un résumé (des thèses, pas un récit) côte à côte.

## Pourquoi

Les sous-titres automatiques sont bruités et pleins de répétitions. Vous obtenez ici une transcription lisible et un résumé exploitable, avec une déduplication faite de façon déterministe par un script plutôt qu'estimée par le modèle.

## Prérequis

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) : `pip install yt-dlp`
- [Claude Code](https://claude.com/claude-code)

## Installation

Copiez ce dossier dans votre répertoire de skills :

- **Au niveau du projet :** `.claude/skills/youtube2text/`
- **Au niveau de l'utilisateur :** `~/.claude/skills/youtube2text/`

Puis appelez-le dans Claude Code :

```
/youtube2text https://www.youtube.com/watch?v=...
```

## Ce que vous obtenez

```
digested/<slug>/
  conspectus.md              ← key points, grouped by theme
  attachments/transcript.md  ← full cleaned transcript
```

Le skill propose un slug court à partir du titre et, après votre confirmation, produit les deux fichiers.

## Répertoire de sortie

Par défaut, `./digested`. Pointez-le où vous voulez dans votre projet — indiquez le chemin au skill, ou modifiez `OUT_DIR` dans `SKILL.md`.

## `clean_transcript.py`

L'étape de nettoyage est un script autonome, utilisable sans Claude :

```bash
python clean_transcript.py \
  --srt video.ru.srt \
  --out transcript.md \
  --title "Title" --source "url" --channel "Channel" --duration "12 min"
```

Lancez `python clean_transcript.py --help` pour voir toutes les options.

## Limites

- La qualité est plafonnée par les sous-titres automatiques de YouTube. Noms propres, chiffres et termes peuvent être mal reconnus (p. ex. « Бафет » au lieu de « Баффет »). Le script nettoie la structure ; il ne peut pas corriger les erreurs de reconnaissance.
- Si une vidéo n'a aucun sous-titre, le skill ne peut pas la transcrire : il ne fait pas de reconnaissance vocale de l'audio.

## Licence

MIT
