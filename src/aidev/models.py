"""Modelos serializables que intercambian el orquestador y los proveedores."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class AgentResult:
    """Resultado estructurado devuelto por la ejecución de un rol de IA."""

    status: str
    summary: str
    evidence: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    artifacts: list[dict[str, str]] = field(default_factory=list)
    high_impact_actions: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AgentResult":
        """Construye un resultado seguro a partir de datos JSON no confiables."""
        return cls(
            status=str(data.get("status", "blocked")),
            summary=str(data.get("summary", "")),
            evidence=[str(item) for item in data.get("evidence", [])],
            risks=[str(item) for item in data.get("risks", [])],
            artifacts=[item for item in data.get("artifacts", []) if isinstance(item, dict)],
            high_impact_actions=[str(item) for item in data.get("high_impact_actions", [])],
        )

    def to_dict(self) -> dict[str, Any]:
        """Devuelve una representación apta para persistir como JSON."""
        return asdict(self)


@dataclass
class ProjectState:
    """Estado persistente de un proyecto y de sus transiciones gobernadas."""

    project: str
    stage: str = "intake_pending"
    active_role: str | None = None
    task_id: str | None = None
    task_statuses: dict[str, str] = field(default_factory=dict)
    approvals: dict[str, dict[str, Any]] = field(default_factory=dict)
    artifacts: list[str] = field(default_factory=list)
    runs: list[str] = field(default_factory=list)
    high_impact_return_stage: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProjectState":
        """Reconstruye el estado guardado en disco."""
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        """Actualiza la marca temporal y serializa el estado para guardarlo."""
        self.updated_at = datetime.now(UTC).isoformat()
        return asdict(self)
