# Contexto activo

## Estado

Brief, Perfil Tecnológico y Backlog aprobados. Las tareas 1.1 (contenido demo), 1.2 (estructura semántica), 2.1 (presentación principal) y 2.2 (ofertas destacadas) fueron aceptadas; la siguiente tarea pendiente es 2.3, sector de marcas comercializadas.

## Decisiones vigentes

- IADev se coordina desde Codex mediante documentos Markdown versionados.
- Alias de agentes: Ada (`planner`), Nicola (`implementer`), Leonardo (`quality-reviewer`) y Alan (`researcher`); se pueden invocar por alias o por nombre técnico.
- El código vive en `workspace/`; el contexto y backlog en `ai-system/`.
- La landing será estática, sin framework, con HTML, CSS y JavaScript sin dependencias; no usará base de datos ni panel de administración.
- Se autorizó contenido ficticio exclusivamente para una demo. Debe reemplazarse y verificarse antes de cualquier publicación, incluido el enlace real de WhatsApp.
- La presentación principal usa un recurso visual CSS local y el menú incorpora estilos responsive, estados de interacción y foco visible; no se usan activos externos.
- Las ofertas se presentan como tres tarjetas responsive con visuales CSS decorativos y CTAs de demostración deshabilitados; sus textos comerciales reproducen la fuente demo aprobada.

## Pendientes y próximo paso

- Implementar el sector de marcas comercializadas tras aprobación explícita de la tarea 2.3.
- Definir hosting y sustituir los contenidos demo por datos comerciales aprobados antes de publicar.
- Realizar la comprobación visual manual de la landing en viewports móvil y escritorio cuando haya navegador disponible.
