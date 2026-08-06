"""Instalación y verificación de la integración nativa de IADev con Codex."""

from __future__ import annotations

import hashlib
import json
import subprocess
import re
from dataclasses import dataclass
from pathlib import Path


ROLE_SKILLS = {
    "planner": "aidev-planning",
    "implementer": "aidev-implementation",
    "reviewer": "aidev-review",
    "closeout": "aidev-closeout",
    "coordinator": "aidev-coordinator",
    "visual_designer": "aidev-visual-design",
    "smart_committer": "aidev-smart-commit",
}
SKILL_SOURCES = {
    "planner": "planning.md",
    "implementer": "implementation.md",
    "reviewer": "review.md",
    "closeout": "closeout.md",
    "coordinator": "coordinator.md",
    "visual_designer": "visual-design.md",
    "smart_committer": "smart-commit.md",
}
START_MARKER = "<!-- aidev:codex:start -->"
END_MARKER = "<!-- aidev:codex:end -->"
SKILL_MARKER = "<!-- aidev:codex:skill digest="


@dataclass(frozen=True)
class SetupResult:
    """Resume los archivos creados o actualizados durante una instalación."""

    created: list[Path]
    updated: list[Path]


def _error(message: str) -> Exception:
    from .core import OrchestratorError
    return OrchestratorError(message)


def skill_for_role(role: str) -> str | None:
    """Devuelve el skill de Codex asociado a un rol del flujo."""
    return ROLE_SKILLS.get(role)


def setup_codex(root: Path, *, force: bool = False) -> SetupResult:
    """Instala reglas y skills en workspace sin sobrescribir contenido ajeno."""
    root = root.resolve()
    system = root / "ai-system"
    workspace = root / "workspace"
    template = system / "targets" / "codex" / "AGENTS.md.template"
    if not template.exists():
        raise _error(f"No existe el template de Codex: {template.relative_to(root)}")

    created: list[Path] = []
    updated: list[Path] = []
    workspace.mkdir(parents=True, exist_ok=True)
    _install_agents_block(workspace / "AGENTS.md", template.read_text(encoding="utf-8"), created, updated)
    for role, skill_name in ROLE_SKILLS.items():
        source = system / "guidance" / "skills" / SKILL_SOURCES[role]
        if not source.exists():
            raise _error(f"No existe el skill canónico: {source.relative_to(root)}")
        destination = workspace / ".agents" / "skills" / skill_name / "SKILL.md"
        _install_skill(destination, skill_name, source.read_text(encoding="utf-8"), force, created, updated)
    return SetupResult(created=created, updated=updated)


def codex_setup_is_ready(root: Path, role: str) -> bool:
    """Comprueba que el skill requerido por el rol esté instalado."""
    skill_name = skill_for_role(role)
    if not skill_name:
        return True
    path = root / "workspace" / ".agents" / "skills" / skill_name / "SKILL.md"
    return path.exists() and SKILL_MARKER in path.read_text(encoding="utf-8")


def open_pencil_is_available(executable: str = "codex") -> bool:
    """Comprueba que Codex tenga configurado el MCP local open-pencil."""
    completed = subprocess.run([executable, "mcp", "list", "--json"], text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        return False
    try:
        servers = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return False
    return any(server.get("name") == "open-pencil" and server.get("enabled") is True for server in servers if isinstance(server, dict))


def _install_agents_block(path: Path, template: str, created: list[Path], updated: list[Path]) -> None:
    block = f"{START_MARKER}\n{template.strip()}\n{END_MARKER}\n"
    if not path.exists():
        path.write_text(block, encoding="utf-8")
        created.append(path)
        return
    content = path.read_text(encoding="utf-8")
    start = content.find(START_MARKER)
    end = content.find(END_MARKER)
    if start == -1 and end == -1:
        separator = "" if not content.strip() else "\n\n"
        path.write_text(content.rstrip() + separator + block, encoding="utf-8")
        updated.append(path)
        return
    if start == -1 or end == -1 or end < start:
        raise _error(f"Los marcadores IADev de {path} están incompletos")
    end += len(END_MARKER)
    suffix = content[end:].lstrip("\n")
    path.write_text(content[:start] + block + suffix, encoding="utf-8")
    updated.append(path)


def _install_skill(path: Path, name: str, source: str, force: bool, created: list[Path], updated: list[Path]) -> None:
    rendered = _render_skill(name, source)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
        created.append(path)
        return
    existing = path.read_text(encoding="utf-8")
    if SKILL_MARKER not in existing:
        raise _error(f"Conflicto: {path} no fue generado por IADev")
    if not _is_unmodified_skill(existing) and not force:
        raise _error(f"Conflicto: {path} fue modificado; usá --force para restaurar el skill de IADev")
    path.write_text(rendered, encoding="utf-8")
    updated.append(path)


def _render_skill(name: str, source: str) -> str:
    descriptions = {
        "aidev-planning": "Planificar trabajo aprobado de IADev mediante spec, design y tasks verificables.",
        "aidev-implementation": "Implementar únicamente una task aprobada dentro del flujo gobernado de IADev.",
        "aidev-review": "Revisar cambios y evidencia dentro del flujo gobernado de IADev.",
        "aidev-closeout": "Preparar el cierre trazable de un trabajo revisado de IADev.",
        "aidev-coordinator": "Coordinar intake, aprobaciones y transiciones del flujo IADev sin tomar decisiones humanas.",
        "aidev-visual-design": "Crear y documentar diseños visuales aprobables mediante OpenPencil.",
        "aidev-smart-commit": "Crear un commit acotado y trazable para una task revisada de IADev.",
    }
    core = f"---\nname: {name}\ndescription: {descriptions[name]}\n---\n\n{source.strip()}\n"
    digest = hashlib.sha256(core.encode("utf-8")).hexdigest()
    return core.replace("---\n\n", f"---\n{SKILL_MARKER}{digest} -->\n\n", 1)


def _is_unmodified_skill(content: str) -> bool:
    match = re.search(r"<!-- aidev:codex:skill digest=([a-f0-9]{64}) -->\n", content)
    if not match:
        return False
    without_marker = content[:match.start()] + content[match.end():]
    return hashlib.sha256(without_marker.encode("utf-8")).hexdigest() == match.group(1)
