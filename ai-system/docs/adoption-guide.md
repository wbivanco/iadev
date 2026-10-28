# Guía de adopción

La instalación del motor y el `init` de cada producto están en el [README de la raíz](../../README.md). Esta guía describe el ciclo después de inicializar.

## Requisitos

- Git instalado.
- El kit instalado en la máquina con `install.sh`.
- Cursor, Codex o Claude Code abiertos en la raíz del producto, donde está el `AGENTS.md` corto.
- Las herramientas del stack elegido, cuando se llegue a implementación.
- OpenPencil y su MCP sólo si se desean usar diseños opcionales; el kit funciona sin ellos.

## Estructura de un producto

- `AGENTS.md`: arranque del coordinador. Apunta a los skills instalados en el home.
- `ai-system/`: Brief, Perfil, Backlog, memoria y tablero. Se versiona y no se despliega.
- Código en `code_root` del Perfil Tecnológico. En un producto nuevo es la raíz del repo.

El motor (`.agents/skills/` y `.codex/agents/`) permanece en el repo del kit. Cursor usa los skills. Codex, además, usa los agentes `.toml`.

## Inicio

Abrí el editor en la raíz del producto. Escribí una idea normal, por ejemplo: `Quiero iniciar un proyecto para administrar turnos de una clínica.`

El Coordinador detecta que no hay Brief aprobado, inicia la entrevista y completa los documentos. No hay aprobaciones por archivo ni estados locales que administrar.

## Ciclo diario

1. El editor lee `status.md` y `context.md`, y el coordinador explica el estado.
2. Guía Brief, Perfil y Backlog hasta sus aprobaciones conversacionales.
3. Presenta y pide aprobación de una tarea antes de desarrollarla.
4. Implementa dentro de `code_root`, valida y revisa; vos aceptás o pedís correcciones.
5. Actualiza tablero y memoria, propone lo siguiente y solicita una confirmación final antes de cada commit local.

### Diseño opcional

Cuando pidas explícitamente un diseño, mockup, wireframe, Figma u OpenPencil, IADev puede preparar un borrador visual antes de implementar. Si lo aceptás, guarda el `.fig` en `design/` y lo usa como referencia para la tarea. Si OpenPencil no está disponible, el diseño se registra como pendiente y el ciclo normal continúa sin bloquearse.

Para retomar en otra computadora, instalá el kit, cloná el producto y pedí continuar. Git del producto contiene el contexto útil; no guardar secretos en estos documentos.

## Agentes

El chat principal es el Coordinador, guiado por el skill `aidev-coordinator`. Puede delegar a `planner` (Ada) para backlog, `implementer` (Nicola) para código, `quality-reviewer` (Leonardo) para una revisión independiente, `researcher` (Alan) para incertidumbres técnicas y `designer` (Isaac, sólo para diseño explícitamente solicitado). En Codex esos roles están en `.codex/agents/`. En Cursor el mismo chat sigue el skill correspondiente. Los alias y los nombres técnicos son equivalentes al pedir una delegación; internamente se usa el nombre técnico. La planificación y revisión pueden delegarse; las escrituras de una tarea se hacen en secuencia para evitar conflictos.
