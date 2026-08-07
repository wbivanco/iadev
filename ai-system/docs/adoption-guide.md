# Guía de adopción

## Requisitos

- Git y Codex instalados y autenticados.
- Este kit copiado o clonado en la raíz del repositorio.
- Las herramientas del stack elegido disponibles cuando se llegue a implementación.

## Estructura

- `.codex/agents/`: agentes especializados de Codex, versionados por proyecto.
- `.agents/skills/`: workflows que Codex activa para IADev.
- `AGENTS.md`: regla principal que convierte el chat en Coordinador.
- `ai-system/`: Brief, Perfil, Backlog, memoria y tablero.
- `workspace/`: código real del producto.

## Inicio

Abrí Codex desde la raíz del repositorio. Escribí una idea normal, por ejemplo: `Quiero iniciar un proyecto para administrar turnos de una clínica.`

El Coordinador detecta que no hay Brief aprobado, inicia la entrevista y crea o completa los documentos. No hay comandos de inicialización, aprobaciones por archivo ni estados locales que administrar.

## Ciclo diario

1. Codex lee `status.md` y `context.md`, y explica el estado.
2. Guía Brief, Perfil y Backlog hasta sus aprobaciones conversacionales.
3. Presenta y pide aprobación de una tarea antes de desarrollarla.
4. Implementa, valida y revisa; vos aceptás o pedís correcciones.
5. Actualiza tablero y memoria, propone lo siguiente y solicita una confirmación final antes de cada commit local.

Para retomar en otra computadora, cloná el repositorio, abrilo con Codex desde su raíz y pedí continuar. Git contiene todo el contexto útil; no guardar secretos en estos documentos.

## Agentes

El chat principal es el Coordinador. Puede delegar a `planner`, `implementer`, `quality-reviewer` y `researcher`, definidos en `.codex/agents/`. La planificación y revisión pueden delegarse; las escrituras de una tarea se hacen en secuencia para evitar conflictos.
