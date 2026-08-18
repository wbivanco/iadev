---
status: approved
updated_at: "2026-08-14"
---

# Brief del proyecto

## Idea inicial

Incorporar al kit IADev dos skills: uno para mantener diagramas de entidad-relación y
sus exportaciones, y otro para crear o actualizar la documentación técnica del
proyecto con enlaces a esos artefactos.

## Problema y oportunidad (obligatorio)

Evitar que el modelo de datos y la documentación técnica queden desactualizados
respecto de los cambios confirmados por el equipo.

## Objetivo y usuarios (obligatorio)

Mantener para el equipo de desarrollo una fuente de documentación técnica y un
modelo de datos actuales, fáciles de consultar y vinculados entre sí.

## Capacidades y alcance (obligatorio)

- Crear un skill agnóstico de motor de base de datos que genere y mantenga el DER
  en Mermaid/Markdown.
- Determinar el DER leyendo primero las migraciones del proyecto y luego la
  estructura de la base de datos cuando esté disponible; informar diferencias
  para que el equipo decida cómo resolverlas, sin sobrescribir ninguna fuente
  automáticamente.
- Exportar cada DER a SVG y PNG en calidad suficiente para consultar nombres de
  entidades y campos; el SVG debe conservar la posibilidad de zoom sin pérdida.
- Guardar los archivos del DER dentro de `ai-system/docs/der/`.
- Crear un skill que detecte una guía de documentación técnica existente y la
  actualice; si no existe, debe crearla e incluir enlaces relativos al DER y a
  los documentos necesarios para desarrollo.

## Criterios de éxito (obligatorio)

- Todo cambio de esquema confirmado deja DER y guía técnica actualizados antes
  del commit.
- Los enlaces de la guía a los artefactos del DER son válidos.
- Los diagramas permiten consultar con claridad entidades y campos al ampliarlos.

## Restricciones y fuera de alcance (opcional)

- Las skills se ejecutan tras la aceptación de un cambio y antes de solicitar el
  último sí para el commit local.

## Historial

- 2026-08-08: creado como esqueleto genérico para una nueva entrevista.
- 2026-08-14: se registró el alcance inicial de skills para DER y documentación.
- 2026-08-14: aprobado por el usuario.
