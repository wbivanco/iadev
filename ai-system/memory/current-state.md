# Current State

## Estado general

- Proyecto en fase: V1.0 - Kit portable completado
- Módulo activo: Validación posterior mediante adopción en proyectos reales
- Última actualización: 2026-08-05

## Completado

- Separación entre `ai-system/` y `workspace/`.
- Memoria persistente, reglas para agentes y flujo SDD v1.
- Templates para spec, design, task, decisión, sesión, cierre y skill.
- Guía de adopción, ciclo de vida documental y checklist de portabilidad.
- Roles temporales, contrato de handoff y skills genéricos.
- Orquestación gobernada: Coordinador, entradas estructuradas y aprobación humana por transición material.
- Runtime v1: CLI Python `aidev`, estado JSON/JSONL versionable y adaptador a Codex CLI con sandbox de workspace.
- Escenarios ficticios de referencia de punta a punta.

## Próximo paso

1. Ejecutar un proyecto piloto con `aidev`, completar el intake y validar el ciclo de aprobaciones con Codex CLI.
2. Registrar fricciones y decidir cambios para v1.1 o v2.
3. Evaluar automatización, búsqueda avanzada e integración con herramientas sólo si el uso real lo justifica.

## Contexto importante

- `ai-system/` es un producto documental portable e independiente de stack.
- `workspace/` contiene el código real cuando exista; no es requisito para cerrar la v1.
