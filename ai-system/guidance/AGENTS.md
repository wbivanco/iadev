# AGENTS.md

## Objetivo

Operar un desarrollo asistido por IA de forma portable, trazable y gobernada por una persona responsable.

## Lectura obligatoria

Antes de trabajar, leer en este orden:

1. `ai-system/memory/MEMORY.md` y los archivos de memoria enlazados.
2. `ai-system/docs/sdd-flow-v1.md`.
3. `ai-system/docs/governed-orchestration-v2.md`.
4. El Project Brief, Technology Profile, spec, design y task aplicables.
5. La solicitud de aprobación vigente.

## Separación de responsabilidades

- `ai-system/`: planificación, memoria, specs, reglas, skills y orquestación.
- `workspace/`: código real del proyecto.

Declarar el rol de `guidance/roles.md`. Aplicar el skill correspondiente de `guidance/skills/`. El Coordinador administra el flujo; el responsable humano decide las transiciones materiales.

## Flujo operativo

1. Recibir el Project Brief y Technology Profile.
2. El Coordinador verifica completitud y obtiene aprobación del intake.
3. El Planner genera spec, design y tasks; solicita aprobación del plan.
4. Si la task requiere diseño visual, el Visual Designer usa `open-pencil`, registra `workspace/design/<task-id>.fig` y obtiene su aprobación.
5. El Coordinador solicita autorización para iniciar cada task.
6. El Implementer ejecuta sólo la task aprobada y solicita autorización para entregarla a revisión.
7. El Reviewer emite dictamen y solicita autorización para aceptar o corregir.
8. El Closeout prepara el cierre y solicita autorización para completar.
9. Registrar la respuesta y actualizar memoria tras cada transición.

## Regla de aprobación humana

Antes de una acción material, crear una solicitud usando `templates/approval-request.template.md` y esperar una respuesta explícita. No avanzar por silencio ni por una aprobación ambigua. Si cambian alcance, arquitectura, costo, seguridad, fechas o riesgos, volver al Coordinador.

Son acciones materiales: aprobar/publicar artefactos, iniciar implementación, ampliar una task, instalar dependencias, migrar, desplegar, modificar configuración compartida, comunicar externamente y cerrar trabajo.

## Validación y cierre

Toda task declara validación. No declarar éxito sin evidencia. Después de trabajo relevante, actualizar `current-state.md`, `decisions.md` cuando corresponda, `open-questions.md`, `session-log.md` y `agent-handoffs.md`.
