#!/usr/bin/env bash
# Siembra la memoria de IADev en el directorio actual. No copia el motor.
set -euo pipefail

SOURCE="${BASH_SOURCE[0]}"
while [[ -L "$SOURCE" ]]; do
  DIR="$(cd "$(dirname "$SOURCE")" && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [[ "$SOURCE" != /* ]] && SOURCE="$DIR/$SOURCE"
done
ROOT="$(cd "$(dirname "$SOURCE")" && pwd)"
TARGET="$(pwd)"
SEED="$ROOT/ai-system/templates/product"

if [[ "$TARGET" == "$ROOT" ]]; then
  echo "Corré init en la raíz del producto, no dentro del kit." >&2
  exit 1
fi

if [[ ! -d "$SEED" ]]; then
  echo "No están las plantillas: $SEED" >&2
  exit 1
fi

copy_if_missing() {
  local src="$1" dst="$2"
  if [[ -e "$dst" ]]; then
    echo "ya existe: $dst"
    return
  fi
  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
  echo "creado: $dst"
}

copy_if_missing "$SEED/AGENTS.md" "$TARGET/AGENTS.md"
copy_if_missing "$SEED/project-brief.md" "$TARGET/ai-system/specs/intake/project-brief.md"
copy_if_missing "$SEED/technology-profile.md" "$TARGET/ai-system/specs/intake/technology-profile.md"
copy_if_missing "$SEED/backlog.md" "$TARGET/ai-system/specs/backlog.md"
copy_if_missing "$SEED/status.md" "$TARGET/ai-system/memory/status.md"
copy_if_missing "$SEED/context.md" "$TARGET/ai-system/memory/context.md"
copy_if_missing "$SEED/ai-system-readme.md" "$TARGET/ai-system/README.md"

MARKER="# iadev-deploy-exclude"
DOCKERIGNORE="$TARGET/.dockerignore"
if [[ -f "$DOCKERIGNORE" ]] && grep -qF "$MARKER" "$DOCKERIGNORE"; then
  echo "ya presente: $DOCKERIGNORE"
else
  {
    if [[ -s "$DOCKERIGNORE" ]]; then
      printf '\n'
    fi
    printf '%s\n' "$MARKER" "ai-system" "AGENTS.md"
  } >> "$DOCKERIGNORE"
  echo "actualizado: $DOCKERIGNORE"
fi

echo "Listo en $TARGET."
echo "Commiteá AGENTS.md y ai-system/. El motor queda en el kit; no se copia a este repo."
echo "Si el deploy no usa Docker, excluí esas mismas rutas en la herramienta que publica. Si solo publicás la salida del build, no hace falta otro ignore."
