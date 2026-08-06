# AI Development System

Kit portable para planificar, ejecutar y cerrar trabajo asistido por IA. Incluye
memoria persistente, desarrollo guiado por especificaciones, templates, skills,
roles y un orquestador técnico local gobernado por aprobación humana.

## Empezar

Leé la [guía de adopción](docs/adoption-guide.md), personalizá `memory/` y
completá el Project Brief y Technology Profile. Para usar el runtime, instalá el
paquete desde la raíz del repositorio y seguí la [guía del orquestador](docs/orchestrator-cli.md).

El código real del proyecto vive por convención en `../workspace`.

## Alcance

El estado actual incluye el CLI `aidev`, una máquina de estados, aprobaciones en
Markdown, auditoría JSONL, selección explícita de tasks y un adaptador a Codex
CLI con sandbox de workspace.
El orquestador ejecuta roles sólo cuando su gate correspondiente fue aprobado;
no despliega, migra ni hace operaciones de red de forma autónoma. Las tasks de
interfaz pueden requerir un diseño visual aprobado: se ejecutan con el MCP
local `open-pencil` y dejan un artefacto `.fig` en `workspace/design/` antes de
habilitar la implementación.

## Referencias

- [Flujo de orquestación gobernada](docs/governed-orchestration-v2.md)
- [Guía del orquestador](docs/orchestrator-cli.md)
- [Roles y handoffs](guidance/roles.md)
- [Skills incluidos](guidance/skills/)
- [Integración OpenPencil](integrations/open-pencil.toml)
