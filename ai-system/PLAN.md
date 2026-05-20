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
- Ya existe una versión operativa de reglas para agentes.
- Ya existe un flujo SDD mínimo formalizado.
- La siguiente etapa es probar el sistema con casos reales y ajustar fricciones.

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
4. revisar o crear design y task si hace falta
5. ejecutar trabajo
6. validar
7. actualizar memoria

Este flujo ya fue formalizado en:

`ai-system/docs/sdd-flow-v1.md`

### 5. Reglas base para agentes

`AGENTS.md` ya define una operación v2 más clara:

- lectura obligatoria de memoria
- separación entre `ai-system/` y `workspace/`
- uso de spec, design y task según complejidad
- manejo de ambigüedad y validación mínima
- regla de cierre con actualización de memoria

## Qué está incompleto

### 1. Validación del flujo en casos reales

Flujo definido:

`idea -> spec -> design -> tasks -> implementacion -> testing -> PR -> memoria`

Falta comprobar:

- si el flujo es lo bastante liviano para trabajo real
- qué fricciones aparecen en sesiones reales
- qué partes necesitan simplificación o más detalle

### 2. Ajuste fino de AGENTS.md

La base ya existe, pero debería refinarse después de uso real:

- excepciones prácticas
- comportamiento multiagente
- relación más precisa con revisión y cierre

### 3. Templates base

Ya existen templates mínimos en `ai-system/templates/`.

Templates actuales:

- `spec.template.md`
- `task.template.md`
- `decision.template.md`
- `session-log.template.md`
- template de PR o cierre de trabajo

Falta validar:

- si alcanzan para trabajo real
- si sobran o faltan campos
- si conviene agregar un template de design

### 4. Skills y orquestación

Más adelante el sistema debería incorporar:

- skills modulares por tipo de tarea
- contratos de entrada y salida para agentes
- handoffs más formales
- soporte real para trabajo multiagente

## Prioridades

### Alta

- ordenar y estabilizar la documentación base
- probar el flujo SDD mínimo con un caso real
- ajustar `AGENTS.md` según uso
- validar templates esenciales

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
- `AGENTS.md` operativo
- flujo SDD v1 formalizado
- templates mínimos

Pendiente:

- prueba de punta a punta con un caso real
- refinamiento de `AGENTS.md`
- refinamiento de templates
- skills
- orquestación

## Criterio de éxito de esta fase

Esta fase se considera cerrada cuando:

- `ai-system/` pueda copiarse a otro proyecto sin depender de este repositorio
- un agente pueda arrancar leyendo memoria y reglas sin contexto adicional
- exista un flujo mínimo repetible desde idea hasta cierre
- la estructura documental esté limpia, consistente y mantenible
