# PLAN.md

## Propósito

Este repositorio existe para construir un `AI Development System` portable.
La idea es que `ai-system/` pueda copiarse a cualquier proyecto y sirva como
capa de planificación, memoria, reglas y coordinación de agentes.

`workspace/` no es el foco actual. Puede permanecer vacío o mínimo hasta que el
sistema base esté lo bastante maduro como para usarse en un proyecto real.

## Objetivo del sistema

Lograr una forma de trabajo consistente entre herramientas como VS Code,
Cursor, OpenCode, Claude Code y Codex, sin depender de una sola plataforma.

El sistema busca separar por completo:

- `ai-system/`: inteligencia operativa del proyecto
- `workspace/`: código ejecutable del proyecto

## Estado actual

Fase actual: `Fase 1 - Sistema base operativo`

Estado resumido:

- El sistema ya es usable como base manual de trabajo con IA.
- La memoria persistente ya funciona.
- Ya existe una primera versión de reglas para agentes.
- El sistema todavía no está formalizado como flujo completo de desarrollo.

## Qué ya está resuelto

### 1. Separación estructural

La división principal ya está definida:

```text
mi-proyecto/
├── ai-system/
└── workspace/
```

Esto permite:

- portabilidad entre proyectos
- independencia respecto de una herramienta concreta
- separación clara entre planificación y ejecución

### 2. Sistema de memoria v1

Ubicación:

`ai-system/memory/`

Archivos actuales:

- `MEMORY.md`: entrypoint para leer la memoria
- `project-summary.md`: visión general del sistema
- `current-state.md`: estado actual del proyecto
- `decisions.md`: decisiones persistentes
- `open-questions.md`: dudas y pendientes abiertos
- `session-log.md`: historial de sesiones
- `agent-handoffs.md`: coordinación entre agentes

Capacidades ya presentes:

- persistencia entre sesiones
- continuidad de contexto más allá del chat
- base operativa para trabajo con agentes
- formato portable y simple basado en Markdown

### 3. Filosofía base

Los principios ya definidos son:

- independencia de herramientas
- separación entre planificación y código
- desarrollo guiado por specs
- memoria persistente como fuente de verdad contextual
- IA como ejecutor asistido, no como única fuente de verdad

### 4. Flujo mínimo ya operativo

Hoy el sistema permite trabajar así:

1. leer memoria
2. entender estado y contexto
3. revisar o crear spec
4. ejecutar trabajo
5. validar
6. actualizar memoria

Este flujo funciona, pero todavía no está completamente formalizado.

### 5. Reglas base para agentes

`AGENTS.md` ya define una primera operación mínima:

- lectura obligatoria de memoria
- separación entre `ai-system/` y `workspace/`
- pasos mínimos de ejecución
- regla de cierre con actualización de memoria

## Qué está incompleto

### 1. Flujo SDD formal

Existe la intención, pero no la formalización completa.

Flujo objetivo:

`idea -> spec -> design -> tasks -> implementacion -> testing -> PR -> memoria`

Falta definir:

- documentos mínimos por etapa
- criterios de entrada y salida
- enforcement para agentes
- integración con revisión y validación

### 2. AGENTS.md v2

La próxima versión debería cubrir:

- comportamiento según tipo de tarea
- uso obligatorio de specs
- manejo de errores y ambigüedad
- criterios de calidad
- relación con testing, revisión y cierre

### 3. Templates base

Todavía no existen, pero son parte del siguiente salto de madurez.

Templates sugeridos:

- `spec.template.md`
- `task.template.md`
- `decision.template.md`
- `session-log.template.md`
- template de PR o cierre de trabajo

### 4. Skills y orquestación

Más adelante el sistema debería incorporar:

- skills modulares por tipo de tarea
- contratos de entrada y salida para agentes
- handoffs más formales
- soporte real para trabajo multiagente

## Prioridades

### Alta

- ordenar y estabilizar la documentación base
- definir `AGENTS.md` v2
- formalizar el flujo SDD mínimo
- crear templates esenciales

### Media

- estructurar `skills/`
- estructurar `orchestration/`
- mejorar handoffs entre agentes

### Baja

- automatización de memoria
- búsqueda avanzada con SQLite o FTS
- integraciones con IDE y Git
- utilidades o MCPs específicos del sistema

## Estado real resumido

Completado:

- arquitectura base
- separación `ai-system/` / `workspace/`
- memoria v1 funcional
- `AGENTS.md` base
- flujo mínimo operativo

Pendiente:

- flujo SDD formal
- `AGENTS.md` avanzado
- templates
- skills
- orquestación

## Criterio de éxito de esta fase

Esta fase se considera cerrada cuando:

- `ai-system/` pueda copiarse a otro proyecto sin depender de este repositorio
- un agente pueda arrancar leyendo memoria y reglas sin contexto adicional
- exista un flujo mínimo repetible desde idea hasta cierre
- la estructura documental esté limpia, consistente y mantenible
