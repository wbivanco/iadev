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

Fase actual: `V1.1 - Orquestación gobernada documentada`

Estado resumido:

- El sistema ya es usable como base manual de trabajo con IA.
- La memoria persistente ya funciona.
- Ya existe una versión operativa de reglas para agentes.
- Ya existe un flujo SDD mínimo formalizado.
- La orquestación gobernada agrega coordinación y aprobación humana documentadas; la automatización ejecutable de agentes sigue siendo una evolución posterior.

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

## Evolución posterior

La v1.0 está cerrada como base documental portable. El uso en proyectos reales permitirá medir fricciones y priorizar una v1.1 o v2.

### Prioridad alta

- Aplicar la guía y checklist al adoptar el kit en un proyecto real.
- Registrar fricciones de los roles, skills, templates y handoffs.

### Prioridad media

- Ajustar `AGENTS.md` y templates según evidencia de uso.
- Agregar skills específicos sólo cuando sean reutilizables entre proyectos.

### Prioridad baja

- Automatización de memoria y orquestación autónoma.
- Búsqueda avanzada con SQLite o FTS.
- Integraciones con IDE, Git, MCPs u otras herramientas.

## Criterio de éxito de v1

La v1 se considera cerrada cuando:

- `ai-system/` puede copiarse sin depender de este repositorio.
- Un agente puede iniciar leyendo memoria y reglas sin contexto adicional.
- Existe un flujo repetible desde idea hasta cierre, con templates, skills y roles.
- La guía, checklist y escenarios permiten adoptar y entender la base sin un proyecto real.
