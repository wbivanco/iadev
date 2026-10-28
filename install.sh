#!/usr/bin/env bash
# Publica el motor de IADev en el home del usuario. No modifica repos de producto.
set -euo pipefail

SOURCE="${BASH_SOURCE[0]}"
while [[ -L "$SOURCE" ]]; do
  DIR="$(cd "$(dirname "$SOURCE")" && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [[ "$SOURCE" != /* ]] && SOURCE="$DIR/$SOURCE"
done
ROOT="$(cd "$(dirname "$SOURCE")" && pwd)"

SKILLS_SRC="$ROOT/.agents/skills"
AGENTS_SRC="$ROOT/.codex/agents"
SKILLS_DST="${HOME}/.agents/skills"
CLAUDE_DST="${HOME}/.claude/skills"
CODEX_DST="${HOME}/.codex/agents"

if [[ ! -d "$SKILLS_SRC" ]]; then
  echo "No está la carpeta de skills: $SKILLS_SRC" >&2
  exit 1
fi

mkdir -p "$SKILLS_DST" "$CLAUDE_DST" "$CODEX_DST"

link_one() {
  local src="$1" dst="$2"
  if [[ -e "$dst" && ! -L "$dst" ]]; then
    echo "omitido (ya existe y no es un enlace): $dst" >&2
    return
  fi
  ln -sfn "$src" "$dst"
  echo "enlazado: $dst -> $src"
}

for dir in "$SKILLS_SRC"/*; do
  [[ -d "$dir" ]] || continue
  name="$(basename "$dir")"
  link_one "$dir" "$SKILLS_DST/$name"
  link_one "$dir" "$CLAUDE_DST/$name"
done

if [[ -d "$AGENTS_SRC" ]]; then
  for file in "$AGENTS_SRC"/*.toml; do
    [[ -f "$file" ]] || continue
    link_one "$file" "$CODEX_DST/$(basename "$file")"
  done
fi

echo "Listo. Skills en $SKILLS_DST y $CLAUDE_DST. Agentes de Codex en $CODEX_DST."
echo "En cada producto, desde su raíz: $ROOT/init.sh"
echo "Un skill o agente nuevo requiere correr este script otra vez. Un cambio en uno ya enlazado se ve con git pull."
