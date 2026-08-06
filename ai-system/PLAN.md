# PLAN.md

## Propósito

Este repositorio existe para construir un asistente portable de desarrollo con
IA capaz de ayudar a crear software de cualquier tipo a partir de una
especificacion.

La idea es que `ai-system/` pueda copiarse a cualquier proyecto y sirva como
capa de planificacion, memoria, contexto, reglas, skills y coordinacion de
agentes.

`workspace/` no representa el producto principal. Puede permanecer vacio o
minimo hasta que el sistema base este lo bastante maduro como para generar,
acompanar o modificar proyectos reales.

## Objetivo del sistema

Lograr una forma de trabajo portable entre herramientas. El núcleo documental y el runtime Python no dependen de una plataforma; cada integración nativa se implementa como un target. Codex es el primer target operativo.

El objetivo funcional es que el asistente pueda recibir una especificacion,
mantener memoria y contexto del trabajo, decidir que skills o agentes necesita
usar, producir un plan ejecutable, implementar cambios, validarlos y dejar
registro persistente del estado alcanzado.

El sistema busca separar por completo:

- `ai-system/`: inteligencia operativa del proyecto
- `workspace/`: código ejecutable del proyecto

## Estado actual

Fase actual: `V1.2 - Orquestación gobernada operativa con target Codex`

Estado resumido:

- El sistema ya es usable como base manual de trabajo con IA.
- La memoria persistente ya funciona.
- Ya existe una versión operativa de reglas para agentes.
- Ya existe un flujo SDD mínimo formalizado.
- La orquestación gobernada se ejecuta mediante el CLI `aidev`: mantiene estado JSON/JSONL, crea gates y llama roles de Codex de forma acotada.
- El target Codex instala reglas y skills nativos sin sobrescribir instrucciones existentes.
- El runtime permite seleccionar una task explícitamente y, si la task UI lo requiere, ejecutar un diseño visual con OpenPencil y aprobar su `.fig` antes de implementar.

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

La base documental v1.0 está cerrada; el runtime gobernado y el target Codex constituyen la evolución v1.2. El uso en proyectos reales permitirá medir fricciones y priorizar la siguiente versión.

### Prioridad alta

- Aplicar la guía y checklist al adoptar el kit en un proyecto real.
- Ejecutar y documentar un piloto completo, incluida una task UI con OpenPencil si aplica.
- Registrar fricciones de los roles, skills, templates y handoffs.

### Prioridad media

- Ajustar `AGENTS.md` y templates según evidencia de uso.
- Agregar skills específicos sólo cuando sean reutilizables entre proyectos.

### Prioridad baja

- Automatización adicional de memoria y capacidades no gobernadas.
- Búsqueda avanzada con SQLite o FTS.
- Nuevos targets nativos para otras herramientas e integraciones MCP adicionales.

## Criterio de éxito de v1

La v1 se considera cerrada cuando:

- `ai-system/` puede copiarse sin depender de este repositorio.
- Un agente puede iniciar leyendo memoria y reglas sin contexto adicional.
- Existe un flujo repetible desde idea hasta cierre, con templates, skills y roles.
- La guía, checklist y escenarios permiten adoptar y entender la base sin un proyecto real.
