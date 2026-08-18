# Contexto activo

## Estado

Brief, Perfil Tecnológico y Backlog aprobados. DER-01, DOC-01 y FLOW-01 fueron
aceptadas el 2026-08-18.

## Decisiones vigentes

- Los DER se versionan en `ai-system/docs/der/` como Markdown, Mermaid, SVG y
  PNG.
- Las migraciones son la fuente primaria; la base de datos se usa sólo para
  contraste y las diferencias requieren decisión humana.
- SVG y PNG se generan sólo con un renderizador ya disponible en el entorno,
  sin incorporar scripts propios ni dependencias persistentes.
- La actualización de DER y guía técnica ocurre después de aceptar un cambio de
  esquema y antes de solicitar el último sí de commit.

## Hallazgo de revisión

- `aidev-der` fue validado por revisión independiente y aceptado por el usuario.
- `aidev-documentation` fue validado por revisión independiente y aceptado por el usuario.
- FLOW-01 fue validada por revisión independiente y aceptada por el usuario.
- No quedan tareas pendientes en el backlog aprobado.

## Pendientes y próximo paso

- Cierre preparado: esperar el último sí explícito del usuario antes de cualquier
  commit local.
