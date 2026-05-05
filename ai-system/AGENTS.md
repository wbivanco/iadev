# AGENTS.md

## Regla principal

Antes de modificar código en `workspace/`, leer primero:

1. `ai-system/memory/MEMORY.md`
2. `ai-system/memory/current-state.md`
3. `ai-system/memory/decisions.md`
4. `ai-system/memory/open-questions.md`

## Separación de responsabilidades

- `ai-system/`: planificación, memoria, specs, reglas, skills y orquestación.
- `workspace/`: código real del proyecto.

## Flujo mínimo

1. Entender la tarea.
2. Revisar memoria.
3. Revisar o crear spec.
4. Proponer plan.
5. Implementar en `workspace/`.
6. Ejecutar validaciones.
7. Actualizar memoria.

## Regla de cierre

Después de cada trabajo relevante, actualizar:

- `current-state.md`
- `decisions.md` si hubo decisiones nuevas
- `open-questions.md` si quedaron dudas
- `session-log.md`
