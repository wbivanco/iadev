# Checklist de portabilidad

Usá esta lista después de copiar o actualizar el kit.

## Integridad del kit

- [ ] Existen `AGENTS.md`, `README.md`, `PLAN.md`, `docs/`, `memory/`,
  `specs/`, `templates/`, `skills/` y `orchestration/`.
- [ ] Existen los templates de spec, design, task, decisión, sesión, cierre y
  skill.
- [ ] Los enlaces desde `AGENTS.md`, `README.md` y esta guía resuelven.

## Inicialización del destino

- [ ] `project-summary.md` describe el proyecto destino, no esta plantilla.
- [ ] `current-state.md` tiene estado y próximos pasos reales.
- [ ] Están documentados stack, comandos de validación y restricciones locales.
- [ ] Las decisiones iniciales y dudas abiertas están registradas.
- [ ] Se definieron los responsables humanos y roles de agentes permitidos.

## Operación

- [ ] Una tarea normal tiene spec, task y validación declarada.
- [ ] Un trabajo ambiguo tiene además design.
- [ ] Se seleccionó un rol y, cuando aplica, un skill para la tarea.
- [ ] El cierre actualiza `current-state.md`, decisiones, dudas y sesión.
