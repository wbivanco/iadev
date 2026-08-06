# MEMORY.md

## Cómo usar esta memoria

Antes de trabajar en el proyecto, leer `context.md`. Es la única memoria
operativa que el runtime carga automáticamente en cada ejecución.

Mantener `context.md` por debajo de 12.000 caracteres. Debe contener sólo el
resumen vigente, estado actual, decisiones activas, dudas abiertas y próximo
paso. El detalle cerrado se conserva en `archive/` y se consulta sólo cuando
una task lo requiere.

## Estructura

- `context.md`: memoria activa y acotada que recibe Codex.
- `archive/`: decisiones, sesiones y cierres históricos fuera del contexto
  automático.
- `project-summary.md`, `current-state.md`, `decisions.md`,
  `open-questions.md`, `session-log.md` y `agent-handoffs.md`: fuentes de
  trabajo o histórico que deben consolidarse en `context.md`, no crecer sin
  límite.

## Regla clave

Esta carpeta es la fuente de verdad del contexto del proyecto. No confiar
únicamente en el contexto del chat o del agente.
