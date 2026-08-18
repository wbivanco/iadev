---
name: aidev-documentation
description: Crea o actualiza la guía técnica de proyectos IADev y enlaza documentación de desarrollo con DER en Mermaid, SVG y PNG. Usar después de actualizar un DER, al crear documentación para desarrolladores o antes de cerrar un cambio de esquema.
---

# Documentación IADev

Mantené una guía técnica que permita a una persona desarrolladora ubicar el
modelo de datos y los documentos de trabajo relevantes sin duplicar información.

## Descubrimiento y ubicación de la guía

1. Localizá primero la guía técnica que el proyecto ya use. Considerá sólo
   documentación de desarrollo pertinente, por ejemplo la que describe
   arquitectura, ejecución, validación o decisiones.
2. Si existe una guía apropiada, actualizala de forma acotada: agregá o ajustá
   sólo la referencia necesaria al modelo de datos y preservá el contenido
   ajeno al DER, su estructura y sus enlaces existentes.
3. Si no hay una guía técnica ni una convención documental clara, proponé la
   ruta `ai-system/docs/technical-guide.md` y pedí confirmación explícita antes
   de crear el archivo. No reemplaces ni reconviertas arbitrariamente un
   `README.md` u otro documento existente.

## Enlaces y ausencias

1. Para cada artefacto disponible en
   `ai-system/docs/der/<nombre>.md`, `ai-system/docs/der/<nombre>.mmd`,
   `ai-system/docs/der/<nombre>.svg` y `ai-system/docs/der/<nombre>.png`,
   calculá el `href` relativo desde el directorio de la guía. No copies la ruta
   de almacenamiento como destino del enlace.
2. Enlazá sólo documentos de desarrollo que existan y sean pertinentes, como
   arquitectura, ejecución, validación o decisiones. Informá las ausencias en
   vez de crear enlaces ficticios.
3. Si falta un artefacto del DER, indicá cuál es y no agregues un enlace a ese
   destino. Si encontrás un enlace roto relacionado con el DER o con la sección
   que actualizaste, informá su texto, el destino relativo resuelto y la
   ausencia; no inventes el archivo ni una referencia alternativa.
4. No copies el contenido del DER ni de los documentos vinculados: la guía debe
   servir para encontrarlos y explicar brevemente por qué son relevantes.

## Validación de enlaces

Para cada enlace agregado o modificado, y para los enlaces al DER de la sección
actualizada, verificá manualmente lo siguiente antes de informar el resultado:

1. El destino es una ruta relativa desde el directorio de la guía; no usa una
   ruta absoluta ni una referencia local a la máquina.
2. Al resolver `.` y `..` desde esa ubicación, el destino corresponde a un
   archivo existente en el repositorio.
3. El archivo de destino es el artefacto o documento que el texto del enlace
   describe. Si no se cumple alguno de estos puntos, conservá la evidencia de
   la ausencia o del enlace roto y comunicala sin crear archivos ni enlaces de
   reemplazo.

## Integración con cambios de esquema

Esta secuencia se aplica únicamente cuando una tarea ya aceptada modifica el
esquema. No la impongas a tareas sin cambios de esquema.

1. Ejecutá primero `aidev-der`: actualizá o contrastá el DER según las fuentes
   disponibles y validá los artefactos que el entorno pueda validar.
2. Después ejecutá este skill para actualizar la guía técnica con enlaces
   relativos a los artefactos del DER que existan.
3. Antes de solicitar el último sí para el commit, revisá los enlaces de la
   sección actualizada y comunicá las validaciones realizadas, sus resultados y
   cualquier bloqueo.

Un contraste pendiente, una diferencia sin decisión, un enlace roto o la
indisponibilidad de una fuente, credencial o herramienta requiere comunicación
y decisión humana; no lo resuelvas de forma implícita ni automatices el cierre.

## Portabilidad

No introduzcas scripts, generadores, automatizaciones, adaptadores, runtimes ni
dependencias persistentes para actualizar Markdown. La guía y sus enlaces deben
seguir siendo navegables en un clon normal del repositorio.
