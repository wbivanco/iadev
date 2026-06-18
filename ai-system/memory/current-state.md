# Current State

## Estado general

- Proyecto en fase: V1.0 - Kit portable completado
- Módulo activo: Validación posterior mediante adopción en proyectos reales
- Producto objetivo: `ai-system/` como asistente de programación para crear software desde especificaciones
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

- El objetivo de este repositorio es desarrollar `ai-system/`, un producto documental portable e independiente de stack.
- Contiene planificación, memoria, contexto, specs, reglas, skills y coordinación de agentes para operar como asistente de programación.
- Debe poder copiarse a cualquier proyecto.
- `workspace/` no es el producto principal; es el destino del código que el asistente ayude a crear, modificar o mantener.
