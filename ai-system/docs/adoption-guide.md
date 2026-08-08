# Guía de adopción

## Requisitos

- Git y Codex instalados y autenticados.
- Este kit copiado o clonado en la raíz del repositorio.
- Las herramientas del stack elegido disponibles cuando se llegue a implementación.
- OpenPencil y su MCP sólo si se desean usar diseños opcionales; el kit funciona sin ellos.

## Estructura

- `.codex/agents/`: agentes especializados de Codex, versionados por proyecto.
- `.agents/skills/`: workflows que Codex activa para IADev.
- `AGENTS.md`: regla principal que convierte el chat en Coordinador.
- `ai-system/`: Brief, Perfil, Backlog, memoria y tablero.
- `workspace/`: código real del producto.

## Instalación

El kit se instala en la raíz del repositorio donde se trabajará, nunca dentro de `workspace/`. Al clonar este repositorio, Git descarga también las carpetas ocultas versionadas: `.codex/` y `.agents/`.

Para incorporarlo a un repositorio existente, copiá a su raíz estos elementos: `AGENTS.md`, `.codex/`, `.agents/` y `ai-system/`. Conservá `workspace/` como la ubicación del código real de la aplicación.

Abrí Codex desde la raíz que contiene `AGENTS.md`; así detectará la configuración, los agentes y los documentos de coordinación.

## Inicio

Abrí Codex desde la raíz del repositorio. Escribí una idea normal, por ejemplo: `Quiero iniciar un proyecto para administrar turnos de una clínica.`

El Coordinador detecta que no hay Brief aprobado, inicia la entrevista y crea o completa los documentos. No hay comandos de inicialización, aprobaciones por archivo ni estados locales que administrar.

## Ciclo diario

1. Codex lee `status.md` y `context.md`, y explica el estado.
2. Guía Brief, Perfil y Backlog hasta sus aprobaciones conversacionales.
3. Presenta y pide aprobación de una tarea antes de desarrollarla.
4. Implementa, valida y revisa; vos aceptás o pedís correcciones.
5. Actualiza tablero y memoria, propone lo siguiente y solicita una confirmación final antes de cada commit local.

### Diseño opcional

Cuando pidas explícitamente un diseño, mockup, wireframe, Figma u OpenPencil, IADev puede preparar un borrador visual antes de implementar. Si lo aceptás, guarda el `.fig` en `design/` y lo usa como referencia para la tarea. Si OpenPencil no está disponible, el diseño se registra como pendiente y el ciclo normal continúa sin bloquearse.

Para retomar en otra computadora, cloná el repositorio, abrilo con Codex desde su raíz y pedí continuar. Git contiene todo el contexto útil; no guardar secretos en estos documentos.

## Agentes

El chat principal es el Coordinador. Puede delegar a `planner` (Ada), `implementer` (Nicola), `quality-reviewer` (Leonardo), `researcher` (Alan) y `designer` (Isaac, sólo para diseño explícitamente solicitado), definidos en `.codex/agents/`. Los alias y los nombres técnicos son equivalentes al pedir una delegación; internamente se usa el nombre técnico. La planificación y revisión pueden delegarse; las escrituras de una tarea se hacen en secuencia para evitar conflictos.
