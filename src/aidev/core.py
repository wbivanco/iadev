"""Núcleo del flujo gobernado: estados, aprobaciones, contexto y ejecuciones."""

from __future__ import annotations

import json
import re
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .models import AgentResult, ProjectState
from .provider import Provider

APPROVAL_TRANSITIONS = {
    "approve_intake": "planning",
    "approve_plan": "task_ready",
    "approve_visual_design": "implementation_ready",
    "start_implementation": "implementation",
    "deliver_implementation": "review",
    "accept_review": "commit_pending",
    "approve_commit": "committing",
    "complete_task": "task_ready",
}
ROLE_BY_STAGE = {"planning": "planner", "visual_design": "visual_designer", "implementation": "implementer", "review": "reviewer", "committing": "smart_committer", "closeout": "closeout"}
HIGH_IMPACT_WORDS = ("dependency", "dependencia", "migration", "migración", "deploy", "desplieg", "network", "red", "secret", "credencial", "shared configuration", "configuración compartida")


class OrchestratorError(RuntimeError):
    """Indica una transición inválida o un artefacto requerido ausente."""

    pass


class Orchestrator:
    """Coordina el ciclo de vida de un proyecto con gates humanos explícitos."""

    def __init__(self, root: Path, provider: Provider) -> None:
        """Inicializa rutas del repositorio y el proveedor que ejecuta los roles."""
        self.root = root.resolve()
        self.provider = provider
        self.system = self.root / "ai-system"
        self.state_root = self.root / ".aidev" / "state"
        self.intake_root = self.system / "specs" / "intake"
        self.approvals_root = self.system / "specs" / "approvals"
        self.workspace = self.root / "workspace"
        self.guidance = self.system / "guidance"

    def init_project(self, project: str, responsible: str) -> ProjectState:
        """Crea intake, estado inicial y la aprobación necesaria para planificar."""
        self._validate_project(project)
        project_dir = self._project_dir(project)
        if (project_dir / "project.json").exists():
            raise OrchestratorError(f"El proyecto {project} ya existe")
        for directory in (project_dir / "runs", self.intake_root, self.approvals_root):
            directory.mkdir(parents=True, exist_ok=True)
        self.workspace.mkdir(parents=True, exist_ok=True)
        self._copy_template("project-brief.template.md", self.intake_root / f"{project}-brief.md")
        self._copy_template("technology-profile.template.md", self.intake_root / f"{project}-technology-profile.md")
        state = ProjectState(project=project)
        self._save(state)
        self._event(project, "initialized", {"responsible": responsible})
        self.create_approval(state, responsible, "approve_intake", "Coordinator", "Aprobar el intake para iniciar la planificación.")
        return self.load(project)

    def load(self, project: str) -> ProjectState:
        """Recupera el estado persistido de un proyecto inicializado."""
        path = self._project_dir(project) / "project.json"
        if not path.exists():
            raise OrchestratorError(f"No existe el proyecto {project}")
        return ProjectState.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def validate_intake(self, project: str) -> list[str]:
        """Devuelve los campos obligatorios que faltan en el intake del proyecto."""
        required = ("## Problema y oportunidad", "## Objetivo del producto", "## Capacidades requeridas", "## Criterios de éxito")
        brief = self.intake_root / f"{project}-brief.md"
        profile = self.intake_root / f"{project}-technology-profile.md"
        issues = []
        for file in (brief, profile):
            if not file.exists():
                issues.append(f"Falta {file.relative_to(self.system)}")
            elif not file.read_text(encoding="utf-8").strip():
                issues.append(f"Está vacío {file.relative_to(self.system)}")
        if brief.exists():
            content = brief.read_text(encoding="utf-8")
            for heading in required:
                if not self._section_has_content(content, heading):
                    issues.append(f"Falta contenido en {heading}")
        if profile.exists() and not self._section_has_content(profile.read_text(encoding="utf-8"), "## Stack obligatorio"):
            issues.append("Falta contenido en ## Stack obligatorio")
        return issues

    def list_tasks(self, project: str) -> list[str]:
        """Lista las tasks individuales disponibles para el proyecto."""
        directory = self.system / "specs" / "tasks" / project
        return sorted(path.stem for path in directory.glob("*.md")) if directory.exists() else []

    def task_status(self, project: str, task_id: str) -> str:
        """Devuelve el estado operativo de una task, incluyendo las aún no iniciadas."""
        state = self.load(project)
        return state.task_statuses.get(task_id, "pending")

    def select_task(self, project: str, task_id: str) -> ProjectState:
        """Selecciona la task que se ejecutará en el siguiente tramo del flujo."""
        state = self.load(project)
        path = self.system / "specs" / "tasks" / project / f"{task_id}.md"
        if state.stage != "task_ready" or not path.exists():
            raise OrchestratorError("La task no existe o el proyecto no está listo para seleccionarla")
        if self.task_status(project, task_id) in {"completed", "cancelled"}:
            raise OrchestratorError("La task ya está cerrada y no puede volver a seleccionarse")
        state.task_id = task_id
        self._set_task_status(state, "selected")
        self._save(state)
        self._event(project, "task_selected", {"task_id": task_id})
        return state

    def create_approval(self, state: ProjectState, responsible: str, action: str, role: str, proposal: str) -> str:
        """Crea una solicitud Markdown y la registra como aprobación pendiente."""
        approval_id = f"AP-{len(state.approvals) + 1:03d}-{action}"
        path = self.approvals_root / f"{state.project}-{approval_id}.md"
        text = f'''---
id: {approval_id}
action: {action}
status: pending
responsible: {responsible}
role: {role}
created_at: {datetime.now(UTC).isoformat()}
decision: pending
approved_by: ""
decided_at: ""
---

# Solicitud de aprobación

## Decisión solicitada

{proposal}

## Acción final propuesta

{action}

## Alcance y artefactos afectados

- Proyecto: {state.project}
- Etapa actual: {state.stage}

## Opciones y recomendación

Aprobar, rechazar o aprobar con condiciones explícitas.

## Impacto, riesgos y validación prevista

La transición queda bloqueada hasta contar con una decisión explícita.

## Respuesta humana

- Decisión: pending
- Condiciones o cambios solicitados:
- Fecha y responsable:
'''
        path.write_text(text, encoding="utf-8")
        state.approvals[approval_id] = {"action": action, "path": str(path.relative_to(self.system)), "status": "pending"}
        self._save(state)
        self._event(state.project, "approval_requested", {"id": approval_id, "action": action})
        return approval_id

    def sync_approvals(self, project: str) -> ProjectState:
        """Aplica al estado las decisiones humanas registradas en los Markdown."""
        state = self.load(project)
        for approval_id, approval in state.approvals.items():
            if approval["status"] != "pending":
                continue
            path = self.system / approval["path"]
            metadata = self._front_matter(path.read_text(encoding="utf-8"))
            decision = metadata.get("decision", "pending").lower()
            approved_by = metadata.get("approved_by", "").strip()
            if decision not in {"approved", "rejected", "conditional"}:
                continue
            if not approved_by:
                raise OrchestratorError(f"La aprobación {approval_id} no identifica a quien decidió")
            approval["status"] = decision
            approval["decided_by"] = approved_by
            self._event(project, "approval_synced", {"id": approval_id, "decision": decision, "by": approved_by})
            action = approval["action"]
            if decision == "approved":
                if action == "approve_high_impact":
                    state.stage = state.high_impact_return_stage or "implementation"
                    state.high_impact_return_stage = None
                else:
                    state.stage = APPROVAL_TRANSITIONS[action]
                    self._apply_approved_task_transition(state, action)
            else:
                self._return_from_unapproved_decision(state, action, decision)
        self._save(state)
        return state

    def run_next(self, project: str, responsible: str) -> ProjectState:
        """Ejecuta el siguiente rol habilitado o crea el gate previo correspondiente."""
        state = self.load(project)
        if state.stage == "commit_pending":
            self.create_approval(state, responsible, "approve_commit", "Smart Committer", "Autorizar el commit de los cambios revisados de la task aprobada.")
            state.stage = "commit_approval_pending"
            self._save(state)
            return state
        if state.stage.endswith("pending") or state.stage == "blocked":
            raise OrchestratorError(f"No se puede ejecutar en estado {state.stage}; sincronizá o resolvé la aprobación pendiente")
        if state.stage == "task_ready":
            if not self.list_tasks(project):
                raise OrchestratorError("El plan no contiene tasks seleccionables")
            if not state.task_id:
                raise OrchestratorError("Seleccioná una task con `aidev task select <proyecto> <task-id>` antes de continuar")
            if state.task_id and self._task_requires_visual_design(project, state.task_id):
                state.stage = "visual_design"
                self._save(state)
                return state
            self.create_approval(state, responsible, "start_implementation", "Coordinator", "Autorizar el inicio de la implementación de la task aprobada.")
            state.stage = "implementation_pending"
            self._save(state)
            return state
        if state.stage == "implementation_ready":
            self.create_approval(state, responsible, "start_implementation", "Coordinator", "Autorizar el inicio de la implementación de la task aprobada.")
            state.stage = "implementation_pending"
            self._save(state)
            return state
        role = ROLE_BY_STAGE.get(state.stage)
        if not role:
            raise OrchestratorError(f"No hay una acción ejecutable para el estado {state.stage}")
        if role == "visual_designer" and getattr(self.provider, "requires_installed_skills", False):
            from .codex import open_pencil_is_available
            if not open_pencil_is_available(getattr(self.provider, "executable", "codex")):
                raise OrchestratorError("La task requiere OpenPencil, pero el MCP `open-pencil` no está disponible en Codex")
        if getattr(self.provider, "requires_installed_skills", False):
            from .codex import codex_setup_is_ready
            if not codex_setup_is_ready(self.root, role):
                raise OrchestratorError("Faltan los skills de Codex; ejecutá `aidev setup codex` antes de continuar")
        state.active_role = role
        self._save(state)
        result = self.provider.run(role=role, prompt=self._prompt(state, role), workspace=self.workspace)
        self._record_run(state, role, result)
        state.active_role = None
        if result.high_impact_actions:
            state.high_impact_return_stage = state.stage
            self.create_approval(state, responsible, "approve_high_impact", role, "Autorizar estas acciones de alto impacto: " + "; ".join(result.high_impact_actions))
            state.stage = "high_impact_pending"
            self._save(state)
            return state
        if state.stage == "visual_design" and not self._design_path(state).exists():
            self._set_task_status(state, "blocked")
            state.task_id = None
            state.stage = "task_ready"
            self._save(state)
            return state
        for artifact in result.artifacts:
            self._write_artifact(artifact)
        if result.status != "completed":
            self._set_task_status(state, "blocked")
            state.task_id = None
            state.stage = "task_ready"
            self._save(state)
            return state
        if role == "smart_committer":
            state.stage = "closeout"
            self._set_task_status(state, "closing")
            self._save(state)
            return state
        action = {"planning": "approve_plan", "visual_design": "approve_visual_design", "implementation": "deliver_implementation", "review": "accept_review", "closeout": "complete_task"}[state.stage]
        self.create_approval(state, responsible, action, role, f"Aceptar el resultado entregado por {role}.")
        state.stage = f"{role}_pending"
        self._save(state)
        return state

    def _prompt(self, state: ProjectState, role: str) -> str:
        context_files = [
            self.guidance / "AGENTS.md",
            self.system / "memory" / "MEMORY.md",
            self.system / "memory" / "project-summary.md",
            self.system / "memory" / "current-state.md",
            self.system / "memory" / "decisions.md",
            self.system / "memory" / "open-questions.md",
            self.system / "docs" / "governed-orchestration-v2.md",
        ]
        if state.stage == "planning":
            context_files += [self.intake_root / f"{state.project}-brief.md", self.intake_root / f"{state.project}-technology-profile.md"]
        if state.task_id:
            context_files.append(self.system / "specs" / "tasks" / state.project / f"{state.task_id}.md")
        context = "\n\n".join(f"## {file.relative_to(self.root)}\n{file.read_text(encoding='utf-8')}" for file in context_files if file.exists())
        visual_instruction = "" if role != "visual_designer" else f"Usá el MCP open-pencil y creá exclusivamente workspace/design/{state.task_id}.fig."
        commit_instruction = "" if role != "smart_committer" else "Podés usar git status, git diff, git add con rutas explícitas y git commit exclusivamente para la task activa ya autorizada; no hagas push ni reescribas historial."
        return f"""Actuás como {role} dentro de un flujo gobernado.\n{context}\n\nSólo podés editar el workspace. {visual_instruction} {commit_instruction} No instales dependencias, no ejecutes migraciones, no uses red, no despliegues ni modifiques configuración compartida. Si alguna acción es necesaria, listala en high_impact_actions y no la ejecutes. Devolvé únicamente JSON conforme al schema. Para artifacts de planificación, devolvé path relativo a ai-system y content; no intentes escribirlos."""

    def _record_run(self, state: ProjectState, role: str, result: AgentResult) -> None:
        run_id = f"run-{len(state.runs) + 1:03d}"
        path = self._project_dir(state.project) / "runs" / f"{run_id}.json"
        path.write_text(json.dumps({"id": run_id, "role": role, "result": result.to_dict(), "at": datetime.now(UTC).isoformat()}, indent=2), encoding="utf-8")
        state.runs.append(str(path.relative_to(self.root)))
        self._event(state.project, "role_finished", {"run": run_id, "role": role, "status": result.status})

    def _set_task_status(self, state: ProjectState, status: str) -> None:
        """Actualiza el estado de la task activa sin perder las demás tasks del plan."""
        if state.task_id:
            state.task_statuses[state.task_id] = status

    def _apply_approved_task_transition(self, state: ProjectState, action: str) -> None:
        """Mantiene el estado por task alineado con una aprobación concedida."""
        statuses = {
            "start_implementation": "in_progress",
            "deliver_implementation": "in_review",
            "accept_review": "commit_pending",
            "approve_commit": "committing",
        }
        if action == "complete_task":
            self._set_task_status(state, "completed")
            state.task_id = None
            if self._all_tasks_closed(state):
                state.stage = "completed"
                self._event(state.project, "project_completed", {})
            return
        if action in statuses:
            self._set_task_status(state, statuses[action])

    def _return_from_unapproved_decision(self, state: ProjectState, action: str, decision: str) -> None:
        """Devuelve una propuesta rechazada o condicionada a la etapa donde puede corregirse."""
        returns = {
            "approve_intake": "intake_pending",
            "approve_plan": "planning",
            "approve_visual_design": "visual_design",
            "start_implementation": "task_ready",
            "deliver_implementation": "implementation",
            "accept_review": "implementation",
            "approve_commit": "implementation",
            "complete_task": "closeout",
        }
        if action == "approve_high_impact":
            state.stage = state.high_impact_return_stage or "implementation"
            state.high_impact_return_stage = None
        else:
            state.stage = returns.get(action, "planning")
        if action == "start_implementation":
            self._set_task_status(state, "pending")
            state.task_id = None
        elif state.task_id:
            self._set_task_status(state, "needs_changes" if decision == "conditional" else "rework_required")
        self._event(state.project, "approval_returned", {"action": action, "decision": decision, "stage": state.stage})

    def _all_tasks_closed(self, state: ProjectState) -> bool:
        tasks = self.list_tasks(state.project)
        return bool(tasks) and all(state.task_statuses.get(task) in {"completed", "cancelled"} for task in tasks)

    def _write_artifact(self, artifact: dict[str, str]) -> None:
        path = (self.system / artifact["path"]).resolve()
        if self.system not in path.parents or path.suffix != ".md":
            raise OrchestratorError("Un artefacto debe ser un Markdown dentro de ai-system")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(artifact["content"], encoding="utf-8")

    def _copy_template(self, template: str, destination: Path) -> None:
        source = self.system / "templates" / template
        if not source.exists():
            raise OrchestratorError(f"No existe la plantilla {template}")
        shutil.copyfile(source, destination)

    def _project_dir(self, project: str) -> Path:
        return self.state_root / project

    def _task_requires_visual_design(self, project: str, task_id: str) -> bool:
        path = self.system / "specs" / "tasks" / project / f"{task_id}.md"
        metadata = self._front_matter(path.read_text(encoding="utf-8"))
        return metadata.get("visual_design", "not_required").lower() == "required"

    def _design_path(self, state: ProjectState) -> Path:
        return self.workspace / "design" / f"{state.task_id}.fig"

    def _save(self, state: ProjectState) -> None:
        path = self._project_dir(state.project) / "project.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(state.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")

    def _event(self, project: str, event: str, data: dict[str, Any]) -> None:
        path = self._project_dir(project) / "events.jsonl"
        with path.open("a", encoding="utf-8") as file:
            file.write(json.dumps({"at": datetime.now(UTC).isoformat(), "event": event, "data": data}, ensure_ascii=False) + "\n")


    
    
    @staticmethod
    def _section_has_content(content: str, heading: str) -> bool:
        match = re.search(r"^" + re.escape(heading) + r"\n(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL)
        if not match:
            return False
        value = re.sub(r"[|\-:# ]", "", match.group(1))
        return bool(value.strip())

    
    
    @staticmethod
    def _front_matter(content: str) -> dict[str, str]:
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not match:
            raise OrchestratorError("La aprobación no tiene front matter válido")
        return {key.strip(): value.strip().strip('"') for key, _, value in (line.partition(":") for line in match.group(1).splitlines()) if key and _}

    @staticmethod
    def _validate_project(project: str) -> None:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", project):
            raise OrchestratorError("El proyecto debe usar minúsculas, números y guiones")
