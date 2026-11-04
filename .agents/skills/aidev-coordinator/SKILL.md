---
name: aidev-coordinator
description: Guía un proyecto IADev entre entrevista, aprobación, planificación, desarrollo y cierre; usar al iniciar o retomar una idea, una tarea o un proyecto.
---

# Coordinador IADev

Resolvé memoria y código antes de leer o editar. Decí al usuario en una frase dónde está cada uno y cuál es el próximo paso.

La raíz de coordinación es la carpeta que contiene `ai-system/`. Buscala así: en el directorio abierto; si no está, en su padre (el chat puede haberse abierto dentro de `workspace/`); si no, subí hasta la raíz del git. Las rutas `ai-system/...` son relativas a esa carpeta, no al directorio del código.

El código sale del Perfil Tecnológico, en `code_root`, también relativo a esa carpeta. Si el perfil no lo declara y existe `workspace/`, el código es `workspace/` y `ai-system/` queda afuera, al lado. Si no hay `code_root` ni `workspace/`, el código es la raíz de coordinación. Si el perfil declara `code_root`, esa ruta gana aunque exista `workspace/`.

Si el repo todavía tiene `workspace/` con el código, o una copia vieja en `.agents/skills/aidev-*` o en `.codex/agents/`, no la uses como motor. Pedí correr `init.sh` del kit en la raíz del producto: mueve el código a la raíz, deja `ai-system/` como está, pone el `AGENTS.md` corto y quita solo la copia de IADev. No hagas esa mudanza a mano en medio de una tarea. Hasta que `init` corra, seguí la resolución de arriba.

Leé `ai-system/memory/status.md`, `context.md` y los documentos aplicables.

1. Si el Brief o Perfil no está aprobado, usá `aidev-interview`.
2. Si el Backlog no está aprobado, usá `aidev-planning` y pedí aprobación.
3. Presentá una sola tarea pendiente: módulo, complejidad, resultado esperado, validación y riesgos. Si el Perfil tiene `Enrutamiento de herramientas`, indicá la herramienta recomendada para esa complejidad. Si no es la que estás usando, avisalo y ofrecé seguir acá o abrir la recomendada y pedir "retomá IADev, tarea X". Es una recomendación: no reemplaza la aprobación. Al aprobarse, anotá en `status.md` `Tarea activa: <ID> (herramienta: X)` para que otra herramienta retome. Si el Perfil no lo define, seguí en la herramienta actual y registralo como decisión diferida.
4. Si el usuario pidió explícitamente diseño, mockup, wireframe, Figma u OpenPencil para la tarea, usá `aidev-design`, esperá la aceptación del diseño y registrá su ruta. Si no lo pidió, no propongas ni exijas diseño.
5. Tras una aprobación explícita de la tarea y, si aplica, del diseño, delegá en `implementer`; no delegues escritores en paralelo.
6. Pedí a `quality-reviewer` una revisión independiente y ejecutá los chequeos del perfil.
7. Mostrá evidencia, riesgos y diff. Sólo con aceptación del usuario marcá la tarea `[x]`, actualizá Backlog, tablero y contexto.
8. Proponé la siguiente tarea, decisión diferida o cierre.

Las aprobaciones se registran en el documento que aprueban con fecha ISO e Historial. Nunca inventes confirmaciones ni hagas commit sin un último sí explícito.
