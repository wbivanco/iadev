# AI Development System v1.1.0

Kit portable para planificar, ejecutar y cerrar trabajo asistido por IA. Incluye
memoria persistente, desarrollo guiado por especificaciones, templates, skills,
roles y un orquestador técnico local gobernado por aprobación humana.

## Empezar

Leé la [guía de adopción](docs/adoption-guide.md), personalizá `memory/` y
completá el Project Brief y Technology Profile. Para usar el runtime, instalá el
paquete desde la raíz del repositorio y seguí la [guía del orquestador](orchestrator/README.md).

El código real del proyecto vive por convención en `../workspace`.

## Alcance

La v1.1 incluye el CLI `aidev`, una máquina de estados, aprobaciones en
Markdown, auditoría JSONL y un adaptador a Codex CLI con sandbox de workspace.
El orquestador ejecuta roles sólo cuando su gate correspondiente fue aprobado;
no despliega, migra ni hace operaciones de red de forma autónoma.

## Referencias

- [Flujo de orquestación gobernada](docs/governed-orchestration-v2.md)
- [Guía del orquestador](orchestrator/README.md)
- [Roles y handoffs](orchestration/roles.md)
- [Skills incluidos](skills/)
