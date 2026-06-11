#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
#  make_preview.sh — WebM → анимированный WebP (большой + thumb)
#
#  Зависимости: ffmpeg, img2webp (brew install webp)
#
#  Использование:
#    ./make_preview.sh site/infographics/Tank_01.webm
#    ./make_preview.sh site/infographics/*.webm        # батч
#
#  Результат рядом с исходником:
#    Tank_01_preview.webp   (1200px, полная длительность, 15 fps)
#    Tank_01_thumb.webp     (400px,  первые 4 сек,        10 fps)
#
#  Деплой: git add site/infographics && git commit && git push
# ─────────────────────────────────────────────────────────────────

set -euo pipefail

# ── настройки ────────────────────────────────────────────────────
PREVIEW_W=1200      # ширина большого превью (px)
PREVIEW_FPS=15      # fps большого превью
PREVIEW_Q=80        # качество WebP (0–100)

THUMB_W=400         # ширина миниатюры (px)
THUMB_FPS=10        # fps миниатюры
THUMB_DUR=4         # длительность миниатюры (сек)
THUMB_Q=75          # качество WebP миниатюры
# ─────────────────────────────────────────────────────────────────

require() { command -v "$1" &>/dev/null || { echo "❌ Нужен $1 (brew install ${2:-$1})"; exit 1; }; }
require ffmpeg
require img2webp webp

build_webp() {
  local INPUT="$1"
  local OUTPUT="$2"
  local W="$3"
  local FPS="$4"
  local Q="$5"
  local EXTRA_FF="${6:-}"   # доп. аргументы ffmpeg (например, -t 4)

  local TMPDIR
  TMPDIR=$(mktemp -d)
  trap "rm -rf '$TMPDIR'" RETURN

  # 1) ffmpeg → PNG-фреймы
  ffmpeg -y -i "$INPUT" $EXTRA_FF \
    -vf "fps=${FPS},scale=${W}:-1:flags=lanczos" \
    "${TMPDIR}/f%05d.png" 2>/dev/null

  local FRAMES=("${TMPDIR}"/f*.png)
  if [ ${#FRAMES[@]} -eq 0 ]; then
    echo "     ⚠️  Нет фреймов, пропускаем"
    return 1
  fi

  # Длительность одного кадра в мс
  local FRAME_MS=$(( 1000 / FPS ))

  # 2) img2webp → анимированный WebP
  # Строим аргументы: -d <ms> -q <q> frame.png  для каждого файла
  local ARGS=()
  for F in "${FRAMES[@]}"; do
    ARGS+=( -d "${FRAME_MS}" -q "${Q}" "${F}" )
  done

  img2webp -loop 0 "${ARGS[@]}" -o "$OUTPUT" 2>/dev/null
}

# ─────────────────────────────────────────────────────────────────

if [ $# -eq 0 ]; then
  echo "Использование: $0 <file.webm> [file2.webm ...]"
  exit 1
fi

for INPUT in "$@"; do
  if [ ! -f "$INPUT" ]; then
    echo "⚠️  Файл не найден: $INPUT"
    continue
  fi

  DIR="$(dirname "$INPUT")"
  BASE="$(basename "$INPUT" .webm)"
  PREVIEW="${DIR}/${BASE}_preview.webp"
  THUMB="${DIR}/${BASE}_thumb.webp"

  DURATION=$(ffprobe -v quiet -show_entries format=duration \
             -of csv=p=0 "$INPUT" 2>/dev/null || echo "?")

  echo "──────────────────────────────────────────"
  echo "📽  $BASE.webm  (${DURATION}s)"

  echo "  → preview: ${PREVIEW_W}px · ${PREVIEW_FPS}fps · полное"
  build_webp "$INPUT" "$PREVIEW" "$PREVIEW_W" "$PREVIEW_FPS" "$PREVIEW_Q"
  echo "     ✅ $(du -sh "$PREVIEW" | cut -f1)  →  $PREVIEW"

  echo "  → thumb:   ${THUMB_W}px · ${THUMB_FPS}fps · ${THUMB_DUR}s"
  build_webp "$INPUT" "$THUMB" "$THUMB_W" "$THUMB_FPS" "$THUMB_Q" "-t ${THUMB_DUR}"
  echo "     ✅ $(du -sh "$THUMB" | cut -f1)  →  $THUMB"
done

echo ""
echo "Деплой:"
echo "  cd $(dirname "$0")/site"
echo "  git add infographics && git commit -m 'add webp previews' && git push"
