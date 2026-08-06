"""Contratos y adaptador para ejecutar roles de IADev mediante Codex CLI."""

from __future__ import annotations

import json
import subprocess
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from .codex import skill_for_role
from .models import AgentResult


class Provider(ABC):
    """Contrato mínimo para un proveedor capaz de ejecutar un rol de IADev."""

    requires_installed_skills = False

    @abstractmethod
    def run(self, *, role: str, prompt: str, workspace: Path) -> AgentResult:
        """Ejecuta un rol con el contexto dado y devuelve su resultado estructurado."""
        raise NotImplementedError


class CodexCliProvider(Provider):
    """Ejecuta un rol mediante la CLI local autenticada de Codex."""

    requires_installed_skills = True

    def __init__(self, executable: str = "codex", model: str | None = None) -> None:
        self.executable = executable
        self.model = model

    def run(self, *, role: str, prompt: str, workspace: Path) -> AgentResult:
        """Invoca Codex en el workspace y convierte su salida JSON al contrato IADev."""
        schema = {
            "type": "object",
            "required": ["status", "summary", "evidence", "risks", "artifacts", "high_impact_actions"],
            "properties": {
                "status": {"type": "string", "enum": ["completed", "blocked", "needs_approval"]},
                "summary": {"type": "string"},
                "evidence": {"type": "array", "items": {"type": "string"}},
                "risks": {"type": "array", "items": {"type": "string"}},
                "artifacts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["path", "content"],
                        "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                    },
                },
                "high_impact_actions": {"type": "array", "items": {"type": "string"}},
            },
        }
        skill_name = skill_for_role(role)
        if skill_name:
            prompt = f"Usá explícitamente el skill ${skill_name} para esta tarea\n\n{prompt}"
        with tempfile.TemporaryDirectory(prefix="aidev-") as directory:
            schema_path = Path(directory) / "result-schema.json"
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            command = [
                self.executable, "exec", "--json", "--ephemeral", "--sandbox", "workspace-write",
                "-C", str(workspace), "--output-schema", str(schema_path), prompt,
            ]
            if self.model:
                command[2:2] = ["--model", self.model]
            completed = subprocess.run(command, text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            return AgentResult(status="blocked", summary=completed.stderr.strip() or "Codex execution failed")
        final_message = ""
        for line in completed.stdout.splitlines():
            try:
                event: dict[str, Any] = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "item.completed":
                item = event.get("item", {})
                if item.get("type") == "agent_message":
                    final_message = str(item.get("text", ""))
        try:
            return AgentResult.from_dict(json.loads(final_message))
        except json.JSONDecodeError:
            return AgentResult(status="blocked", summary="Codex did not return a valid structured result")
