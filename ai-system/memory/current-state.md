# Current State

## Estado general

- Proyecto en fase: V1.2 - Runtime gobernado con integración visual opcional
- Módulo activo: Documentación, pruebas y adopción piloto del flujo completo
- Producto objetivo: `ai-system/` como asistente de programación para crear software desde especificaciones
- Última actualización: 2026-08-06

## Completado

- Separación entre `ai-system/` y `workspace/`.
- Memoria persistente, reglas para agentes y flujo SDD v1.
- Templates para spec, design, task, decisión, sesión, cierre y skill.
- Guía de adopción, ciclo de vida documental y checklist de portabilidad.
- Roles temporales, contrato de handoff y skills genéricos.
- Orquestación gobernada: Coordinador, entradas estructuradas y aprobación humana por transición material.
- Runtime v1: CLI Python `aidev`, estado JSON/JSONL versionable y adaptador a Codex CLI con sandbox de workspace.
- Refactor de runtime: código Python en `src/aidev`, configuración y estado efímero en `.aidev/`, y conocimiento portable en `ai-system/`.
- Instalación nativa para Codex que integra `workspace/AGENTS.md` sin sobrescribir reglas ajenas y genera skills `aidev-*`.
- Selección explícita de tasks mediante `aidev task list` y `aidev task select`.
- Flujo opcional de diseño visual: el rol Visual Designer usa el MCP local `open-pencil`, genera `workspace/design/<task-id>.fig` y requiere aprobación antes de implementar.
- Escenarios ficticios de referencia de punta a punta.

## Próximo paso

1. Ejecutar un proyecto piloto con `aidev`, completar el intake, seleccionar tasks y validar el ciclo de aprobaciones con Codex CLI.
2. Probar al menos una task UI con OpenPencil configurado localmente y revisar el artefacto `.fig`.
3. Registrar fricciones y decidir la siguiente evolución a partir del uso real.

## Contexto importante

- El objetivo de este repositorio es desarrollar `ai-system/`, un producto documental portable e independiente de stack.
- Contiene planificación, memoria, contexto, specs, reglas, skills y coordinación de agentes para operar como asistente de programación.
- Debe poder copiarse a cualquier proyecto.
- `workspace/` no es el producto principal; es el destino del código que el asistente ayude a crear, modificar o mantener.
