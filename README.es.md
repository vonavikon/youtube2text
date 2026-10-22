# youtube2text

[EN](README.md) · [RU](README.ru.md) · [中文](README.zh.md) · **Español** · [Français](README.fr.md)

Un skill de Claude Code que convierte un vídeo de YouTube en una transcripción limpia y un resumen estructurado de sus puntos clave.

## Qué hace

- Descarga los subtítulos del vídeo con [yt-dlp](https://github.com/yt-dlp/yt-dlp): los manuales si existen, y si no, los generados automáticamente.
- Limpia la transcripción: elimina los duplicados que produce la ventana deslizante de los subtítulos automáticos de YouTube, une el texto y lo redistribuye en párrafos.
- Escribe la transcripción completa y un resumen (tesis, no paráfrasis) uno junto al otro.

## Por qué

Los subtítulos automáticos son ruidosos y están llenos de repeticiones. Esto te da una transcripción legible y un resumen aprovechable, con la deduplicación hecha de forma determinista por un script y no estimada por el modelo.

## Requisitos

- [yt-dlp](https://github.com/yt-dlp/yt-dlp): `pip install yt-dlp`
- [Claude Code](https://claude.com/claude-code)

## Instalación

Copia esta carpeta en tu directorio de skills:

- **A nivel de proyecto:** `.claude/skills/youtube2text/`
- **A nivel de usuario:** `~/.claude/skills/youtube2text/`

Luego invócalo en Claude Code:

```
/youtube2text https://www.youtube.com/watch?v=...
```

## Qué obtienes

```
digested/<slug>/
  conspectus.md              ← key points, grouped by theme
  attachments/transcript.md  ← full cleaned transcript
```

El skill propone un slug corto a partir del título y, tras tu confirmación, genera ambos archivos.

## Directorio de salida

Por defecto es `./digested`. Apúntalo a donde encaje en tu proyecto: dile al skill la ruta, o edita `OUT_DIR` en `SKILL.md`.

## `clean_transcript.py`

El paso de limpieza es un script independiente, utilizable sin Claude:

```bash
python clean_transcript.py \
  --srt video.ru.srt \
  --out transcript.md \
  --title "Title" --source "url" --channel "Channel" --duration "12 min"
```

Ejecuta `python clean_transcript.py --help` para ver todas las opciones.

## Limitaciones

- La calidad está limitada por los subtítulos automáticos de YouTube. Nombres propios, números y términos pueden reconocerse mal (p. ej. "Бафет" en vez de "Баффет"). El script limpia la estructura; no puede corregir los errores de reconocimiento.
- Si un vídeo no tiene subtítulos en absoluto, el skill no puede transcribirlo: no ejecuta reconocimiento de voz sobre el audio.

## Licencia

MIT
