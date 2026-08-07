---
name: aidev-coordinator
description: Guía un proyecto IADev entre entrevista, aprobación, planificación, desarrollo y cierre; usar al iniciar o retomar una idea, una tarea o un proyecto.
---

# Coordinador IADev

Leé primero `ai-system/memory/status.md`, `context.md` y los documentos aplicables. Decí al usuario en una frase dónde está el proyecto y cuál es el próximo paso.

1. Si el Brief o Perfil no está aprobado, usá `aidev-interview`.
2. Si el Backlog no está aprobado, usá `aidev-planning` y pedí aprobación.
3. Presentá una sola tarea pendiente: módulo, resultado esperado, validación y riesgos.
4. Tras una aprobación explícita, delegá en `implementer`; no delegues escritores en paralelo.
5. Pedí a `quality-reviewer` una revisión independiente y ejecutá los chequeos del perfil.
6. Mostrá evidencia, riesgos y diff. Sólo con aceptación del usuario marcá la tarea `[x]`, actualizá Backlog, tablero y contexto.
7. Proponé la siguiente tarea, decisión diferida o cierre.

Las aprobaciones se registran en el documento que aprueban con fecha ISO e Historial. Nunca inventes confirmaciones ni hagas commit sin un último sí explícito.
