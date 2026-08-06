"""Punto de entrada de la CLI para operar IADev desde la terminal."""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

from .codex import setup_codex
from .core import Orchestrator, OrchestratorError
from .provider import CodexCliProvider


def parser() -> argparse.ArgumentParser:
    """Construye el parser y los subcomandos públicos de `aidev`."""
    root = argparse.ArgumentParser(prog="aidev", description="Orquestador local de desarrollo asistido por IA")
    root.add_argument("--root", type=Path, default=Path.cwd(), help="Raíz del repositorio")
    sub = root.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="Inicializa un proyecto")
    init.add_argument("project")
    init.add_argument("--responsible", required=True)
    doctor = sub.add_parser("doctor", help="Verifica el kit y el estado opcional de un proyecto")
    doctor.add_argument("project", nargs="?")
    intake = sub.add_parser("intake", help="Opera documentos de entrada")
    intake_sub = intake.add_subparsers(dest="intake_command", required=True)
    validate = intake_sub.add_parser("validate", help="Valida el intake")
    validate.add_argument("project")
    for name, help_text in (("run", "Ejecuta el siguiente rol permitido"), ("status", "Muestra el estado"), ("resume", "Reanuda el siguiente rol permitido")):
        command = sub.add_parser(name, help=help_text)
        command.add_argument("project")
        if name in {"run", "resume"}:
            command.add_argument("--responsible", required=True)
    approvals = sub.add_parser("approvals", help="Sincroniza aprobaciones humanas")
    approval_sub = approvals.add_subparsers(dest="approval_command", required=True)
    sync = approval_sub.add_parser("sync", help="Lee decisiones Markdown")
    sync.add_argument("project")
    audit = sub.add_parser("audit", help="Muestra la auditoría")
    audit.add_argument("project")
    task = sub.add_parser("task", help="Selecciona o lista tasks del proyecto")
    task_sub = task.add_subparsers(dest="task_command", required=True)
    task_list = task_sub.add_parser("list", help="Lista tasks disponibles")
    task_list.add_argument("project")
    task_select = task_sub.add_parser("select", help="Selecciona una task")
    task_select.add_argument("project")
    task_select.add_argument("task_id")
    setup = sub.add_parser("setup", help="Instala una integración nativa de IADev")
    setup.add_argument("target", choices=["codex"])
    setup.add_argument("--force", action="store_true", help="Restaura skills IADev modificados")
    return root


def provider_for(root: Path) -> CodexCliProvider:
    """Crea el proveedor Codex usando la configuración local si existe."""
    config_path = root / ".aidev" / "config.toml"
    if not config_path.exists():
        return CodexCliProvider()
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    codex = config.get("providers", {}).get("codex", {})
    return CodexCliProvider(executable=codex.get("executable", "codex"), model=codex.get("model"))


def main(argv: list[str] | None = None) -> int:
    """Procesa un comando de IADev y devuelve un código de salida de consola."""
    args = parser().parse_args(argv)
    root = args.root.resolve()
    orchestrator = Orchestrator(root, provider_for(root))
    try:
        if args.command == "init":
            state = orchestrator.init_project(args.project, args.responsible)
            _ensure_config(root)
            print(f"Proyecto {state.project} inicializado; estado: {state.stage}")
            _print_doctor(orchestrator.doctor())
        elif args.command == "doctor":
            checks = orchestrator.doctor(args.project)
            _print_doctor(checks)
            return 1 if any(not passed for passed, _ in checks) else 0
        elif args.command == "intake":
            issues = orchestrator.validate_intake(args.project)
            if issues:
                print("Intake inválido:\n" + "\n".join(f"- {issue}" for issue in issues))
                return 1
            print("Intake válido")
        elif args.command == "approvals":
            state = orchestrator.sync_approvals(args.project)
            print(f"Aprobaciones sincronizadas; estado: {state.stage}")
        elif args.command in {"run", "resume"}:
            state = orchestrator.run_next(args.project, args.responsible)
            print(f"Siguiente estado: {state.stage}")
        elif args.command == "status":
            state = orchestrator.load(args.project)
            print(f"Proyecto: {state.project}\nEtapa: {state.stage}\nRol: {state.active_role or '-'}\nAprobaciones: {len(state.approvals)}\nEjecuciones: {len(state.runs)}")
        elif args.command == "audit":
            path = root / ".aidev" / "state" / args.project / "events.jsonl"
            print(path.read_text(encoding="utf-8") if path.exists() else "Sin eventos")
        elif args.command == "task":
            if args.task_command == "list":
                print("\n".join(f"{task}\t{orchestrator.task_status(args.project, task)}" for task in orchestrator.list_tasks(args.project)))
            else:
                state = orchestrator.select_task(args.project, args.task_id)
                print(f"Task seleccionada: {state.task_id}")
        elif args.command == "setup":
            result = setup_codex(root, force=args.force)
            for path in result.created:
                print(f"Creado: {path.relative_to(root)}")
            for path in result.updated:
                print(f"Actualizado: {path.relative_to(root)}")
    except OrchestratorError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    return 0


def _ensure_config(root: Path) -> None:
    path = root / ".aidev" / "config.toml"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('[providers.codex]\nexecutable = "codex"\n# model = "gpt-5.6-codex"\n', encoding="utf-8")


def _print_doctor(checks: list[tuple[bool, str]]) -> None:
    """Muestra el resultado de las verificaciones sin ocultar los puntos fallidos."""
    for passed, message in checks:
        print(f"[{'OK' if passed else 'ERROR'}] {message}")


if __name__ == "__main__":
    raise SystemExit(main())
