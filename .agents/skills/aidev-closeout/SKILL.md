---
name: aidev-closeout
description: Cierra una tarea IADev aceptada, actualiza memoria y tablero, y prepara un commit local confirmado por el usuario.
---

# Cierre IADev

Usalo sólo después de que calidad haya pasado y el usuario haya aceptado el resultado.

1. En la tarea del Backlog, registrá estado `[x]`, fecha, validación, riesgos residuales y hash si existe.
2. Actualizá `memory/status.md` y `memory/context.md` con módulo, avance, decisiones vigentes y próximo paso.
3. Mostrá diff y proponé commit local atómico con mensaje Conventional Commit en castellano y rutas incluidas.
4. Esperá un último sí explícito. Recién entonces hacé `git add` sólo de esas rutas y `git commit`; no hagas push, amend, reset ni incluyas cambios ajenos.
5. Después de confirmar el commit, leé y mostrá `memory/status.md` como estado del plan: tareas completadas, pendientes y próximo paso. No ocultes tareas pendientes ni las marques como realizadas sin aceptación registrada.
