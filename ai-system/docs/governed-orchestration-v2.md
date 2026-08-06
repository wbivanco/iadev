# Orquestación gobernada v2

## Objetivo

Transformar un `Project Brief` y un `Technology Profile` aprobados en trabajo planificado, implementado y validado, manteniendo a una persona responsable como autorizador de cada resultado final de etapa.

## Regla principal

Un agente puede investigar, proponer, redactar borradores y ejecutar pasos reversibles definidos en una task aprobada. No puede declarar terminada una etapa, avanzar a la siguiente ni realizar una acción material no autorizada sin una solicitud de aprobación respondida por el responsable humano.

Una acción material incluye: aprobar o publicar un artefacto, comenzar implementación, modificar código o esquema fuera de una task aprobada, instalar dependencias, ejecutar migraciones, desplegar, enviar comunicaciones externas y cambiar configuración de entornos compartidos.

## Entradas obligatorias

1. `specs/intake/<proyecto>-brief.md`, creado desde `project-brief.template.md`.
2. `specs/intake/<proyecto>-technology-profile.md`, creado desde `technology-profile.template.md`.
3. Responsable humano identificado en ambos documentos.

El coordinador valida campos obligatorios, registra dudas y solicita aprobación del intake. No planifica ni asigna trabajo hasta que ambos documentos estén `Aprobados`.

## Estados y transiciones

```text
Borrador -> Pendiente de aprobación -> Aprobado -> En trabajo
                                      |              |
                                      v              v
                                  Rechazado   Pendiente de aprobación
                                                     |
                                                     v
                                               Completado | Bloqueado
```

Cada transición hacia `Aprobado`, `En trabajo`, `Completado` o `Bloqueado` requiere una solicitud registrada en `specs/approvals/`. Una respuesta de chat puede servir, pero el coordinador debe copiar la decisión y sus condiciones al registro antes de continuar. Un rechazo o una decisión condicional devuelve el artefacto a la etapa corregible correspondiente; por ejemplo, una revisión no aceptada vuelve a implementación. No bloquea todo el proyecto salvo que exista un impedimento real.

## Flujo de agentes

1. **Coordinador** recibe el intake, verifica completitud, abre dudas y pide aprobación humana.
2. **Planner** convierte el intake aprobado en spec, design y tasks; antes de consolidar el plan pide aprobación humana.
3. **Coordinador** selecciona una task aprobada y propone la asignación. Si la task declara `visual_design: required`, la deriva primero al diseño visual.
4. **Visual Designer** usa el MCP local `open-pencil` para crear `workspace/design/<task-id>.fig`; pide aprobación humana del artefacto antes de habilitar la implementación. Las tasks no visuales omiten este rol.
5. **Coordinador** solicita autorización para iniciar la implementación una vez aprobada la task y, cuando aplica, su diseño visual.
6. **Implementer** ejecuta exclusivamente esa task; ante cualquier ampliación de alcance vuelve al coordinador. Al finalizar pide aprobación para entregar el resultado a revisión.
7. **Reviewer** contrasta cambios y evidencia con los criterios. Pide aprobación humana para aceptar el resultado o abrir correcciones.
8. **Smart Committer** prepara y crea un commit local, atómico y limitado a la task sólo después de que el responsable humano apruebe explícitamente ese commit.
9. **Closeout** prepara cierre y actualización de memoria de la task. Tras aprobarlo, el Coordinador vuelve a `task_ready` para seleccionar la siguiente; sólo marca el proyecto completado cuando todas las tasks están completadas o canceladas.

El coordinador es el único agente que enruta trabajo y cambia la etapa activa. No implementa, revisa ni reemplaza la decisión humana.

## Responsabilidad humana

La persona responsable puede aprobar, rechazar o aprobar con condiciones. Un rechazo o una condición que cambie alcance, arquitectura, costo, seguridad o fecha devuelve el flujo a Planner y se registra como decisión persistente.

La ausencia de respuesta mantiene el trabajo en `Pendiente de aprobación`; no se infiere aprobación por silencio.

## Handoff mínimo

Todo handoff debe incluir enlaces al brief, perfil tecnológico, spec, design, task, evidencia y solicitud de aprobación aplicable. Debe indicar el próximo paso verificable y el estado de la aprobación.

## Runtime técnico

El protocolo se ejecuta con `aidev`. El estado canónico para la máquina es
`.aidev/state/<proyecto>/project.json`; `runs/*.json` conserva resultados
de roles y `events.jsonl` mantiene la auditoría. Las solicitudes en
`ai-system/specs/approvals/` son el registro editable por la persona responsable.

Para aprobar mediante el runtime, editar el front matter con `decision:
approved`, `rejected` o `conditional`, identificar `approved_by` y ejecutar
`aidev approvals sync <proyecto>`. Una aprobación por chat puede registrarse en
el Markdown, pero no habilita el CLI hasta ser sincronizada.

El primer proveedor es Codex CLI y se ejecuta en `workspace/` con sandbox de escritura. `aidev setup codex` instala los skills nativos requeridos, incluido `aidev-visual-design`. Para un diseño visual el runtime exige que Codex tenga habilitado el MCP `open-pencil`; la configuración concreta del MCP pertenece al entorno local del usuario y no al repositorio y devuelve un resultado JSON estructurado. El proveedor no puede
cambiar el estado del orquestador: sólo el Coordinador aplica resultados,
registra evidencia y crea la siguiente solicitud de aprobación.
