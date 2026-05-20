# AGENTS.md

## Objetivo

Este archivo define cómo debe operar un agente dentro de este repositorio.

El objetivo no es sólo producir cambios, sino hacerlo de forma portable,
repetible y compatible con memoria persistente.

## Lectura obligatoria

Antes de trabajar, leer primero:

1. `ai-system/memory/MEMORY.md`
2. `ai-system/memory/current-state.md`
3. `ai-system/memory/decisions.md`
4. `ai-system/memory/open-questions.md`
5. `ai-system/docs/sdd-flow-v1.md`

## Separación de responsabilidades

- `ai-system/`: planificación, memoria, specs, reglas, skills y orquestación.
- `workspace/`: código real del proyecto.

## Flujo operativo

Seguir este flujo:

1. Entender la tarea.
2. Revisar memoria.
3. Determinar si el trabajo es trivial, normal o grande.
4. Revisar o crear la `spec` correspondiente.
5. Revisar o crear `design` si el cómo no está claro.
6. Revisar o crear `task` antes de ejecutar.
7. Implementar.
8. Validar.
9. Cerrar el trabajo.
10. Actualizar memoria.

## Regla de specs

- No implementar cambios medianos o grandes sin `spec`.
- Si la tarea abarca más de una sesión o más de un agente, crear `task`
  explícita.
- Si el enfoque tiene ambigüedad técnica o documental, crear `design` antes de
  ejecutar.

## Clasificación del trabajo

### Trabajo trivial

- Ajuste pequeño y de bajo riesgo.
- Puede resolverse con contexto breve y validación simple.

### Trabajo normal

- Requiere `spec`, validación explícita y actualización de memoria.

### Trabajo grande o ambiguo

- Requiere `spec`, `design`, `task` descompuesta y cierre más formal.

## Comportamiento ante ambigüedad o falta de contexto

- Si falta contexto resoluble, buscarlo en el repo antes de avanzar.
- Si falta contexto crítico no resoluble, detener implementación y registrar la
  duda en `ai-system/memory/open-questions.md`.
- Si una decisión cambia la forma de trabajar del sistema, registrarla en
  `ai-system/memory/decisions.md`.

## Validación mínima

- Toda tarea debe declarar cómo se valida.
- Si no se pudo validar, dejarlo explícito en el cierre y en la memoria.
- No dar por terminado un trabajo relevante sin algún tipo de evidencia.

## Regla de cierre

Después de cada trabajo relevante, actualizar:

- `current-state.md`
- `decisions.md` si hubo decisiones nuevas
- `open-questions.md` si quedaron dudas
- `session-log.md`

## Plantillas base

Usar cuando aplique:

- `ai-system/templates/spec.template.md`
- `ai-system/templates/task.template.md`
- `ai-system/templates/decision.template.md`
- `ai-system/templates/session-log.template.md`
- `ai-system/templates/work-closeout.template.md`
