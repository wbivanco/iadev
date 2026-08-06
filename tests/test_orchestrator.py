from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from aidev.core import Orchestrator, OrchestratorError
from aidev.models import AgentResult
from aidev.provider import Provider


class FakeProvider(Provider):
    def __init__(self, results: list[AgentResult]) -> None:
        self.results = results
        self.calls: list[str] = []

    def run(self, *, role: str, prompt: str, workspace: Path) -> AgentResult:
        self.calls.append(role)
        return self.results.pop(0)


def approve(root: Path, project: str, approval_id: str, decision: str = "approved") -> None:
    path = root / "ai-system" / "specs" / "approvals" / f"{project}-{approval_id}.md"
    content = path.read_text(encoding="utf-8")
    content = content.replace("decision: pending", f"decision: {decision}")
    content = content.replace('approved_by: ""', 'approved_by: "Ana"')
    path.write_text(content, encoding="utf-8")


def fill_intake(root: Path, project: str) -> None:
    brief = root / "ai-system" / "specs" / "intake" / f"{project}-brief.md"
    brief.write_text("""# Brief

## Problema y oportunidad
Demoras operativas.

## Objetivo del producto
Reducir demoras.

## Capacidades requeridas

| ID | Capacidad | Prioridad | Criterio de aceptación |
| --- | --- | --- | --- |
| FR-001 | Registrar pedidos | Must | Se guarda un pedido |

## Criterios de éxito
Se registra un pedido.
""", encoding="utf-8")
    profile = root / "ai-system" / "specs" / "intake" / f"{project}-technology-profile.md"
    profile.write_text("# Perfil\n\n## Stack obligatorio\nPython 3.12\n", encoding="utf-8")


def make_root(path: Path) -> Path:
    system = path / "ai-system"
    (system / "templates").mkdir(parents=True)
    for name in ("project-brief.template.md", "technology-profile.template.md"):
        (system / "templates" / name).write_text("# Template\n", encoding="utf-8")
    (system / "guidance").mkdir()
    (system / "guidance" / "AGENTS.md").write_text("Reglas", encoding="utf-8")
    (system / "docs").mkdir()
    (system / "docs" / "governed-orchestration-v2.md").write_text("Flujo", encoding="utf-8")
    return path


class OrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = make_root(Path(self.temporary.name))

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_intake_requires_content(self) -> None:
        orchestrator = Orchestrator(self.root, FakeProvider([]))
        orchestrator.init_project("demo", "Ana")
        self.assertTrue(orchestrator.validate_intake("demo"))
        fill_intake(self.root, "demo")
        self.assertEqual(orchestrator.validate_intake("demo"), [])

    def test_full_governed_flow(self) -> None:
        provider = FakeProvider([
            AgentResult(status="completed", summary="plan", artifacts=[{"path": "specs/tasks/demo/task-1.md", "content": "---\nvisual_design: not_required\n---\n# Task 1"}]),
            AgentResult(status="completed", summary="implementation", evidence=["tests ok"]),
            AgentResult(status="completed", summary="review"),
            AgentResult(status="completed", summary="commit", evidence=["abc123"]),
            AgentResult(status="completed", summary="closeout"),
        ])
        orchestrator = Orchestrator(self.root, provider)
        state = orchestrator.init_project("demo", "Ana")
        fill_intake(self.root, "demo")
        approve(self.root, "demo", next(iter(state.approvals)))
        self.assertEqual(orchestrator.sync_approvals("demo").stage, "planning")
        state = orchestrator.run_next("demo", "Ana")
        approve(self.root, "demo", next(key for key, value in state.approvals.items() if value["action"] == "approve_plan"))
        self.assertEqual(orchestrator.sync_approvals("demo").stage, "task_ready")
        orchestrator.select_task("demo", "task-1")
        state = orchestrator.run_next("demo", "Ana")
        self.assertEqual(state.stage, "implementation_pending")
        approve(self.root, "demo", next(key for key, value in state.approvals.items() if value["action"] == "start_implementation"))
        self.assertEqual(orchestrator.sync_approvals("demo").stage, "implementation")
        state = orchestrator.run_next("demo", "Ana")
        approve(self.root, "demo", next(key for key, value in state.approvals.items() if value["action"] == "deliver_implementation"))
        self.assertEqual(orchestrator.sync_approvals("demo").stage, "review")
        state = orchestrator.run_next("demo", "Ana")
        approve(self.root, "demo", next(key for key, value in state.approvals.items() if value["action"] == "accept_review"))
        self.assertEqual(orchestrator.sync_approvals("demo").stage, "commit_pending")
        state = orchestrator.run_next("demo", "Ana")
        approve(self.root, "demo", next(key for key, value in state.approvals.items() if value["action"] == "approve_commit"))
        self.assertEqual(orchestrator.sync_approvals("demo").stage, "committing")
        self.assertEqual(orchestrator.run_next("demo", "Ana").stage, "closeout")
        state = orchestrator.run_next("demo", "Ana")
        approve(self.root, "demo", next(key for key, value in state.approvals.items() if value["action"] == "complete_task"))
        self.assertEqual(orchestrator.sync_approvals("demo").stage, "completed")
        self.assertEqual(provider.calls, ["planner", "implementer", "reviewer", "smart_committer", "closeout"])

    def test_cannot_run_while_approval_is_pending(self) -> None:
        orchestrator = Orchestrator(self.root, FakeProvider([]))
        orchestrator.init_project("demo", "Ana")
        with self.assertRaisesRegex(OrchestratorError, "aprobación pendiente"):
            orchestrator.run_next("demo", "Ana")

    def test_high_impact_action_requires_extra_approval(self) -> None:
        provider = FakeProvider([AgentResult(status="completed", summary="plan", high_impact_actions=["install dependency"])])
        orchestrator = Orchestrator(self.root, provider)
        state = orchestrator.init_project("demo", "Ana")
        fill_intake(self.root, "demo")
        approve(self.root, "demo", next(iter(state.approvals)))
        orchestrator.sync_approvals("demo")
        state = orchestrator.run_next("demo", "Ana")
        self.assertEqual(state.stage, "high_impact_pending")
        self.assertTrue(any(item["action"] == "approve_high_impact" for item in state.approvals.values()))

    def test_blocked_task_releases_the_project_for_another_task(self) -> None:
        tasks = self.root / "ai-system" / "specs" / "tasks" / "demo"
        tasks.mkdir(parents=True)
        for task in ("task-1", "task-2"):
            (tasks / f"{task}.md").write_text("---\nvisual_design: not_required\n---\n# Task", encoding="utf-8")
        provider = FakeProvider([AgentResult(status="blocked", summary="waiting for external input")])
        orchestrator = Orchestrator(self.root, provider)
        state = orchestrator.init_project("demo", "Ana")
        state.stage = "task_ready"
        orchestrator._save(state)
        orchestrator.select_task("demo", "task-1")
        state = orchestrator.run_next("demo", "Ana")
        approve(self.root, "demo", next(key for key, value in state.approvals.items() if value["action"] == "start_implementation"))
        self.assertEqual(orchestrator.sync_approvals("demo").stage, "implementation")
        self.assertEqual(orchestrator.run_next("demo", "Ana").stage, "task_ready")
        self.assertEqual(orchestrator.task_status("demo", "task-1"), "blocked")
        self.assertEqual(orchestrator.select_task("demo", "task-2").task_id, "task-2")

    def test_completed_task_returns_to_the_next_task(self) -> None:
        tasks = self.root / "ai-system" / "specs" / "tasks" / "demo"
        tasks.mkdir(parents=True)
        for task in ("task-1", "task-2"):
            (tasks / f"{task}.md").write_text("---\nvisual_design: not_required\n---\n# Task", encoding="utf-8")
        orchestrator = Orchestrator(self.root, FakeProvider([]))
        state = orchestrator.init_project("demo", "Ana")
        state.stage = "closeout_pending"
        state.task_id = "task-1"
        state.task_statuses["task-1"] = "closing"
        orchestrator.create_approval(state, "Ana", "complete_task", "closeout", "Cerrar task")
        approve(self.root, "demo", next(key for key, value in state.approvals.items() if value["action"] == "complete_task"))
        self.assertEqual(orchestrator.sync_approvals("demo").stage, "task_ready")
        self.assertEqual(orchestrator.task_status("demo", "task-1"), "completed")
        self.assertEqual(orchestrator.select_task("demo", "task-2").task_id, "task-2")

    def test_rejected_plan_returns_to_planning(self) -> None:
        orchestrator = Orchestrator(self.root, FakeProvider([]))
        state = orchestrator.init_project("demo", "Ana")
        state.stage = "planner_pending"
        orchestrator.create_approval(state, "Ana", "approve_plan", "planner", "Aceptar plan")
        approve(self.root, "demo", next(key for key, value in state.approvals.items() if value["action"] == "approve_plan"), "rejected")
        self.assertEqual(orchestrator.sync_approvals("demo").stage, "planning")

if __name__ == "__main__":
    unittest.main()
