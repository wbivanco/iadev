from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

from .core import Orchestrator, OrchestratorError
from .provider import CodexCliProvider


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="aidev", description="Orquestador local de desarrollo asistido por IA")
    root.add_argument("--root", type=Path, default=Path.cwd(), help="Raíz del repositorio")
    sub = root.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="Inicializa un proyecto")
    init.add_argument("project")
    init.add_argument("--responsible", required=True)
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
    return root


def provider_for(root: Path) -> CodexCliProvider:
    config_path = root / "ai-system" / "orchestrator" / "config.toml"
    if not config_path.exists():
        return CodexCliProvider()
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    codex = config.get("providers", {}).get("codex", {})
    return CodexCliProvider(executable=codex.get("executable", "codex"), model=codex.get("model"))


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = args.root.resolve()
    orchestrator = Orchestrator(root, provider_for(root))
    try:
        if args.command == "init":
            state = orchestrator.init_project(args.project, args.responsible)
            _ensure_config(root)
            print(f"Proyecto {state.project} inicializado; estado: {state.stage}")
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
            path = root / "ai-system" / "orchestrator" / "state" / args.project / "events.jsonl"
            print(path.read_text(encoding="utf-8") if path.exists() else "Sin eventos")
    except OrchestratorError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    return 0


def _ensure_config(root: Path) -> None:
    path = root / "ai-system" / "orchestrator" / "config.toml"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('[providers.codex]\nexecutable = "codex"\n# model = "gpt-5.6-codex"\n', encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
