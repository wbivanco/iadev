#!/usr/bin/env bash
# Siembra un producto nuevo o pasa un repo con la estructura vieja a la nueva.
# No borra la memoria ni pisa archivos de código que ya estén en la raíz.
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

code_root_value() {
  local profile="$TARGET/ai-system/specs/intake/technology-profile.md"
  [[ -f "$profile" ]] || return 0
  grep -E '^[[:space:]]*-[[:space:]]*code_root:' "$profile" | head -1 \
    | sed -E 's/^[[:space:]]*-[[:space:]]*code_root:[[:space:]]*//' \
    | tr -d '[:space:]' || true
}

is_kit_workspace_agents() {
  [[ -f "$1" ]] && grep -q '../ai-system/specs/intake/technology-profile.md' "$1"
}

is_kit_workspace_readme() {
  [[ -f "$1" ]] && grep -q 'Aquí vive el código real del proyecto' "$1"
}

in_git() {
  git -C "$TARGET" rev-parse --is-inside-work-tree >/dev/null 2>&1
}

is_tracked() {
  [[ -n "$(git -C "$TARGET" ls-files -- "$1")" ]]
}

merge_ignore() {
  local src="$1" dest="$2" line
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" ]] && continue
    if ! grep -qxF "$line" "$dest"; then
      printf '\n%s\n' "$line" >> "$dest"
    fi
  done < "$src"
  remove_rel "workspace/$(basename "$src")"
  echo "unido a $(basename "$dest"): workspace/$(basename "$src")"
}

remove_rel() {
  local rel="$1"
  if in_git && is_tracked "$rel"; then
    git -C "$TARGET" rm -r -f -- "$rel" >/dev/null
  elif [[ -e "$TARGET/$rel" || -L "$TARGET/$rel" ]]; then
    rm -rf "$TARGET/$rel"
  fi
}

move_entry() {
  local name="$1"
  local src="$TARGET/workspace/$name"
  if in_git && is_tracked "workspace/$name"; then
    git -C "$TARGET" mv "workspace/$name" "$name"
    echo "git mv: workspace/$name -> $name"
  else
    mv "$src" "$TARGET/$name"
    echo "movido: workspace/$name -> $name"
  fi
  if [[ -e "$src" ]]; then
    echo "quedó sin mover: workspace/$name" >&2
  fi
}

migrate_workspace() {
  [[ -d "$TARGET/workspace" ]] || return 0
  local value name src
  value="$(code_root_value)"
  case "$value" in
    ""|"."|"workspace"|"workspace/") ;;
    *)
      echo "No moví workspace/: code_root es $value."
      return 0
      ;;
  esac

  local -a names=() collisions=()
  shopt -s dotglob nullglob
  for src in "$TARGET/workspace"/*; do
    name="$(basename "$src")"
    if [[ "$name" == "AGENTS.md" ]] && is_kit_workspace_agents "$src"; then
      continue
    fi
    if [[ "$name" == "README.md" ]] && is_kit_workspace_readme "$src"; then
      continue
    fi
    if [[ "$name" == ".gitignore" || "$name" == ".dockerignore" ]] && [[ -f "$TARGET/$name" && -f "$src" ]]; then
      continue
    fi
    if [[ "$name" == "ai-system" && -d "$TARGET/ai-system" && -d "$src" ]]; then
      continue
    fi
    names+=("$name")
    if [[ -e "$TARGET/$name" ]]; then
      collisions+=("$name")
    fi
  done
  shopt -u dotglob nullglob

  if ((${#collisions[@]})); then
    echo "No cambié el repo. Estos nombres de workspace/ ya existen en la raíz: ${collisions[*]}" >&2
    echo "Nada se movió. Resolvé esos nombres y volvé a correr init." >&2
    exit 1
  fi

  local moved=0
  if ((${#names[@]})); then
    for name in "${names[@]}"; do
      move_entry "$name"
      moved=1
    done
  fi

  shopt -s dotglob nullglob
  for src in "$TARGET/workspace"/.gitignore "$TARGET/workspace"/.dockerignore; do
    [[ -f "$src" ]] || continue
    name="$(basename "$src")"
    if [[ -f "$TARGET/$name" ]]; then
      merge_ignore "$src" "$TARGET/$name"
    fi
  done
  if [[ -f "$TARGET/workspace/AGENTS.md" ]] && is_kit_workspace_agents "$TARGET/workspace/AGENTS.md"; then
    remove_rel "workspace/AGENTS.md"
    echo "quitado: workspace/AGENTS.md del kit"
  fi
  if [[ -f "$TARGET/workspace/README.md" ]] && is_kit_workspace_readme "$TARGET/workspace/README.md"; then
    remove_rel "workspace/README.md"
    echo "quitado: workspace/README.md del kit"
  fi
  if [[ -d "$TARGET/workspace/ai-system" && -d "$TARGET/ai-system" ]]; then
    if diff -rq "$TARGET/ai-system" "$TARGET/workspace/ai-system" >/dev/null; then
      remove_rel "workspace/ai-system"
      echo "workspace/ai-system era igual al de la raíz. Quedó el de la raíz."
    elif [[ -e "$TARGET/ai-system.workspace-bak" ]]; then
      echo "No cambié la memoria: ya existe ai-system.workspace-bak y workspace/ai-system es distinta." >&2
      exit 1
    else
      if in_git && is_tracked "workspace/ai-system"; then
        git -C "$TARGET" mv "workspace/ai-system" "ai-system.workspace-bak"
      else
        mv "$TARGET/workspace/ai-system" "$TARGET/ai-system.workspace-bak"
      fi
      echo "La memoria de la raíz se conserva. La copia distinta de workspace/ quedó en ai-system.workspace-bak."
    fi
  fi
  shopt -u dotglob nullglob

  if rmdir "$TARGET/workspace" 2>/dev/null; then
    echo "quitado: workspace/"
  elif [[ -d "$TARGET/workspace" ]]; then
    echo "workspace/ no quedó vacío. Revisá lo que sigue adentro." >&2
  fi
  if [[ "$moved" == 1 ]] && in_git; then
    echo "Git preparó el renombre en el index. No hice commit."
  fi
}

replace_agents() {
  local dest="$TARGET/AGENTS.md" bak="$TARGET/AGENTS.md.iadev-bak"
  if [[ -f "$dest" ]] && cmp -s "$SEED/AGENTS.md" "$dest"; then
    echo "ya está: $dest"
    return
  fi
  if [[ -f "$dest" && ! -e "$bak" ]]; then
    cp "$dest" "$bak"
    echo "resguardo del AGENTS.md anterior: $bak"
  fi
  cp "$SEED/AGENTS.md" "$dest"
  echo "actualizado: $dest"
}

ensure_code_root() {
  local profile="$TARGET/ai-system/specs/intake/technology-profile.md" value
  [[ -f "$profile" ]] || return 0
  value="$(code_root_value)"
  case "$value" in
    ".") return 0 ;;
    ""|"workspace"|"workspace/")
      if [[ -n "$value" ]]; then
        awk '
          /^[[:space:]]*-[[:space:]]*code_root:/ && !done {
            sub(/code_root:.*/, "code_root: .")
            done=1
          }
          { print }
        ' "$profile" > "$profile.tmp"
        mv "$profile.tmp" "$profile"
        echo "code_root pasó a ."
      elif grep -q '^## Decisiones mínimas$' "$profile"; then
        awk '
          { print }
          /^## Decisiones mínimas$/ && !done { print ""; print "- code_root: ."; done=1 }
        ' "$profile" > "$profile.tmp"
        mv "$profile.tmp" "$profile"
        echo "agregado: code_root: ."
      else
        printf '\n## Decisiones mínimas\n\n- code_root: .\n' >> "$profile"
        echo "agregado: code_root: ."
      fi
      ;;
    *)
      echo "code_root se dejó como está: $value"
      ;;
  esac
}

remove_old_motor() {
  local dir name removed=0
  shopt -s nullglob
  for dir in "$TARGET/.agents/skills"/aidev-*; do
    [[ -d "$dir" || -L "$dir" ]] || continue
    remove_rel "${dir#"$TARGET/"}"
    echo "quitado: $dir"
    removed=1
  done
  shopt -u nullglob
  for name in designer implementer planner quality-reviewer researcher; do
    dir="$TARGET/.codex/agents/$name.toml"
    if [[ -e "$dir" ]]; then
      remove_rel "${dir#"$TARGET/"}"
      echo "quitado: $dir"
      removed=1
    fi
  done
  if [[ -f "$TARGET/.codex/config.toml" && -f "$ROOT/.codex/config.toml" ]] \
    && cmp -s "$TARGET/.codex/config.toml" "$ROOT/.codex/config.toml"; then
    remove_rel ".codex/config.toml"
    echo "quitado: $TARGET/.codex/config.toml"
  fi
  rmdir "$TARGET/.agents/skills" "$TARGET/.agents" "$TARGET/.codex/agents" "$TARGET/.codex" 2>/dev/null || true
  if [[ "$removed" == 1 ]]; then
    echo "El motor queda en el kit. Los skills propios del proyecto, si había, siguen en .agents/skills/."
  fi
}

migrate_workspace

copy_if_missing "$SEED/project-brief.md" "$TARGET/ai-system/specs/intake/project-brief.md"
copy_if_missing "$SEED/technology-profile.md" "$TARGET/ai-system/specs/intake/technology-profile.md"
copy_if_missing "$SEED/backlog.md" "$TARGET/ai-system/specs/backlog.md"
copy_if_missing "$SEED/status.md" "$TARGET/ai-system/memory/status.md"
copy_if_missing "$SEED/context.md" "$TARGET/ai-system/memory/context.md"
copy_if_missing "$SEED/ai-system-readme.md" "$TARGET/ai-system/README.md"
replace_agents
copy_if_missing "$SEED/CLAUDE.md" "$TARGET/CLAUDE.md"
ensure_code_root
remove_old_motor

MARKER="# iadev-deploy-exclude"
DOCKERIGNORE="$TARGET/.dockerignore"
if [[ -f "$DOCKERIGNORE" ]] && grep -qF "$MARKER" "$DOCKERIGNORE"; then
  echo "ya presente: $DOCKERIGNORE"
else
  {
    if [[ -s "$DOCKERIGNORE" ]]; then
      printf '\n'
    fi
    printf '%s\n' "$MARKER" "ai-system" "AGENTS.md" "CLAUDE.md"
  } >> "$DOCKERIGNORE"
  echo "actualizado: $DOCKERIGNORE"
fi

echo "Listo en $TARGET."
echo "El código queda en la raíz y la memoria en ai-system/. No hice commit."
echo "Si el deploy no usa Docker, excluí ai-system/, AGENTS.md y CLAUDE.md en la herramienta que publica. Si solo publicás la salida del build, no hace falta otro ignore."
