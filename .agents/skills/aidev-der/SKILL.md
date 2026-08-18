---
name: aidev-der
description: Mantiene diagramas entidad-relación de proyectos IADev en Mermaid y Markdown. Usar al crear o actualizar un DER, al contrastar migraciones con un esquema de base de datos disponible, o antes de cerrar un cambio de esquema para producir sus SVG y PNG.
---

# DER IADev

Mantené el DER como un artefacto versionado y editable. Antes de actualizarlo,
revisá las migraciones accesibles del proyecto: son la fuente primaria para
entidades, campos y relaciones. Contrastá el esquema de base de datos sólo si
ya hay un acceso autorizado y de sólo lectura; ese contraste es opcional y no
reemplaza a las migraciones.

## Contrato de artefactos

- Guardá cada DER en `ai-system/docs/der/<nombre>.md` y
  `ai-system/docs/der/<nombre>.mmd`.
- Creá o actualizá `ai-system/docs/der/<nombre>.svg` y
  `ai-system/docs/der/<nombre>.png` sólo si el entorno ya cuenta con un
  renderizador que pueda usarse, sin instalarlo ni configurarlo.
- Usá enlaces relativos desde el Markdown hacia Mermaid, SVG y PNG.
- Conservá los nombres existentes salvo que el usuario apruebe su cambio.
- Si falta una fuente, una credencial o el renderizador, no sustituyas ni
  elimines Markdown, Mermaid, SVG o PNG existentes.

## Fuentes y contraste

1. Localizá y leé las migraciones accesibles; registralas como fuente primaria.
2. Si existe una conexión o una extracción de esquema que ya esté disponible,
   consultala sólo en modo lectura y contrastala con las migraciones.
3. Comunicá las diferencias encontradas para decisión humana. Si se actualiza
   el Markdown del DER, registralas en una tabla con: objeto, diferencia, fuente
   de migraciones, fuente de base de datos y decisión pendiente.
4. No modifiques migraciones, la base de datos ni el DER para reconciliar una
   diferencia sin una decisión humana explícita.
5. Si falta una fuente o credencial, informá el límite. Podés conservar un
   Mermaid existente como continuidad, pero no inventes entidades, campos o
   relaciones.

## Validación

- Cuando haya un renderizador disponible, usalo para validar el Mermaid antes
  de reemplazar SVG o PNG. Si la validación falla, informá el error y preservá
  las exportaciones previas.
- Después de agregar enlaces relativos desde el Markdown, comprobá que cada uno
  resuelva desde la ubicación del documento. Informá los enlaces rotos sin
  inventar archivos de destino.

## Secuencia para cambios de esquema aceptados

Esta secuencia se aplica únicamente cuando una tarea ya aceptada modifica el
esquema. No la impongas a tareas sin cambios de esquema.

1. Ejecutá este skill primero: actualizá o contrastá el DER según las fuentes
   disponibles y validá los artefactos que el entorno pueda validar.
2. Después ejecutá `aidev-documentation` para actualizar la guía técnica con
   enlaces relativos a los artefactos del DER que existan.
3. Antes de solicitar el último sí para el commit, revisá los enlaces de la
   sección actualizada y comunicá las validaciones realizadas, sus resultados y
   cualquier bloqueo.

Un contraste pendiente, una diferencia sin decisión, un enlace roto o la
indisponibilidad de una fuente, credencial o herramienta requiere comunicación
y decisión humana; no lo resuelvas de forma implícita ni automatices el cierre.

## Portabilidad

- Usá sólo las capacidades y herramientas ya disponibles en el entorno del
  proyecto consumidor. No agregues scripts, automatizaciones, adaptadores por
  motor, runtimes ni dependencias al repositorio para generar o inspeccionar el
  DER.
- Si no hay renderizador disponible, informá que SVG y PNG no se actualizaron y
  preservá los artefactos previos; no intentes instalar herramientas.
- Mantené el skill agnóstico de motor: no prescribas comandos ni mecanismos
  específicos para leer migraciones o esquemas.
