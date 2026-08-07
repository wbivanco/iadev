---
status: approved
approved_at: "2026-08-07"
updated_at: "2026-08-07"
---

# Backlog — Landing de casa de deportes

## Alcance planificado

Landing estática de una página para presentar la casa de deportes, destacar ofertas y marcas, informar ubicación, horarios y contacto, y dirigir consultas a WhatsApp. La implementación prevista usa HTML, CSS y JavaScript sin dependencias ni backend.

## Módulo 1 — Contenido comercial y base de la página

### [x] 1.1 Relevar y normalizar el contenido público definitivo

- **Alcance:** reunir logo, nombre comercial, textos de presentación, ofertas destacadas, marcas, dirección, horarios, teléfono y enlace/número de WhatsApp; definir qué contenido puede usarse como reemplazo temporal si falta algún dato.
- **Aceptación:** existe una fuente de contenido aprobable con todos los textos y enlaces que verá la persona usuaria; cada oferta indica al menos título, descripción breve e imagen o alternativa visual. Para esta demo se acepta un enlace de WhatsApp no operativo, siempre que esté claramente identificado como ficticio y no apto para producción; antes de publicar, deberá sustituirse por un destino verificable.
- **Validación:** revisión manual contra la fuente entregada. En esta demo se verifica el formato y la señalización del enlace ficticio; antes de producción se deberá probar su apertura en navegador con el número real aprobado.
- **Dependencias:** ninguna.
- **Decisiones diferidas:** identidad visual final; cantidad definitiva de ofertas y marcas; autorización y formato de las imágenes.
- **Cierre:** aceptada por el usuario el 2026-08-07. Validación: revisión independiente aprobada y comprobación de formato/señalización de la fuente de demo; `git diff --check` sin errores. Riesgo residual: todos los datos ficticios, incluido WhatsApp, deben sustituirse y verificarse antes de publicar. Hash: pendiente de commit.

### [ ] 1.2 Crear la estructura semántica de la landing

- **Alcance:** construir el documento base de una sola página con encabezado, navegación, contenido principal por secciones y pie; establecer anclas para las secciones públicas.
- **Aceptación:** están representadas las secciones de presentación, ofertas, marcas, ubicación, horarios y contacto; la jerarquía de encabezados es coherente y la navegación apunta a secciones existentes.
- **Validación:** inspección del HTML y recorrido con los enlaces internos en escritorio y móvil.
- **Dependencias:** 1.1 para los textos y nombres definitivos; puede iniciar con contenido temporal señalado.
- **Decisiones diferidas:** nombres finales de anclas y etiquetas de navegación si cambian los textos comerciales.

## Módulo 2 — Identidad y secciones comerciales

### [ ] 2.1 Definir e implementar la presentación principal

- **Alcance:** componer la sección inicial con propuesta de valor, identidad disponible y CTA principal a WhatsApp; contemplar un recurso visual local o una alternativa sin imagen.
- **Aceptación:** al cargar la página se identifica qué ofrece el comercio y se ve un CTA de consulta a WhatsApp sin desplazarse; la ausencia de un activo definitivo no rompe la composición.
- **Validación:** comprobación visual inicial en viewport móvil y de escritorio; prueba funcional del CTA.
- **Dependencias:** 1.1 y 1.2.
- **Decisiones diferidas:** imagen hero definitiva, mensaje comercial final y posible CTA secundario.

### [ ] 2.2 Incorporar el sector de ofertas destacadas

- **Alcance:** mostrar las ofertas provistas como elementos visuales legibles, con título, descripción breve y, si se entrega, imagen; incluir una salida clara para consultar por WhatsApp.
- **Aceptación:** todas las ofertas aprobadas se distinguen entre sí, no muestran precios ni condiciones no provistos y el CTA permite iniciar una consulta; el diseño soporta la cantidad acordada de ofertas sin desbordes.
- **Validación:** comparación con el contenido normalizado, inspección visual en móvil/escritorio y prueba del CTA.
- **Dependencias:** 1.1 y 1.2.
- **Decisiones diferidas:** precios, vigencia, condiciones promocionales y necesidad de enlaces individuales por oferta.

### [ ] 2.3 Incorporar el sector de marcas comercializadas

- **Alcance:** presentar las marcas aprobadas mediante logotipos autorizados o texto como alternativa accesible.
- **Aceptación:** cada marca se reconoce sin depender exclusivamente de una imagen; los logotipos mantienen proporción y no se usan activos sin autorización.
- **Validación:** revisión de lista de marcas, textos alternativos y comportamiento visual en distintos anchos.
- **Dependencias:** 1.1 y 1.2.
- **Decisiones diferidas:** activos de marca definitivos, orden de prioridad y si alguna marca enlazará a un sitio externo.

## Módulo 3 — Información del local y conversión

### [ ] 3.1 Publicar ubicación, horarios y datos de contacto

- **Alcance:** incorporar dirección, horarios, teléfono u otros canales entregados, y un acceso a indicaciones de llegada si se aprueba un destino de mapa.
- **Aceptación:** la información del local es completa, legible y consistente con la fuente comercial; teléfono y mapa sólo son interactivos cuando sus destinos fueron confirmados.
- **Validación:** revisión contra la fuente, prueba de enlaces de teléfono/mapa cuando existan y lectura en móvil.
- **Dependencias:** 1.1 y 1.2.
- **Decisiones diferidas:** proveedor y URL de mapa; inclusión de redes sociales u otros canales.

### [ ] 3.2 Unificar los puntos de conversión a WhatsApp

- **Alcance:** configurar el CTA principal y los accesos complementarios de la página para abrir el mismo canal de consulta, con mensajes precompletados sólo si se aprueban.
- **Aceptación:** los CTAs visibles funcionan y conducen al número correcto; ningún enlace contiene un número de prueba ni revela datos no aprobados; la acción conserva un nombre accesible.
- **Validación:** prueba manual de cada CTA en navegador y emulación móvil, verificando URL, número y texto precompletado.
- **Dependencias:** 1.1, 2.1 y 2.2.
- **Decisiones diferidas:** texto precompletado por contexto, horario de respuesta y política de atención fuera de horario.

## Módulo 4 — Experiencia responsive, accesibilidad y entrega

### [ ] 4.1 Aplicar estilos responsive y consistencia visual

- **Alcance:** definir estilos proporcionales para tipografía, espaciados, grillas, navegación y CTAs en la landing, priorizando la experiencia móvil.
- **Aceptación:** no hay desplazamiento horizontal no intencional; contenido, ofertas y CTAs se leen y accionan correctamente en móvil y escritorio; el diseño mantiene jerarquía visual entre secciones.
- **Validación:** comprobación manual en un viewport móvil aproximado de 320 px, uno intermedio y uno de escritorio; inspección de estados de foco y enlaces.
- **Dependencias:** 2.1, 2.2, 2.3 y 3.1.
- **Decisiones diferidas:** paleta, tipografías y lineamientos de marca finales si no se entregan en 1.1.

### [ ] 4.2 Revisar accesibilidad básica y comportamiento sin JavaScript

- **Alcance:** verificar semántica, contraste, textos alternativos, foco visible, orden de teclado y funcionamiento de los contenidos/enlaces esenciales sin requerir JavaScript.
- **Aceptación:** la navegación por teclado alcanza enlaces y CTAs; las imágenes informativas tienen alternativa textual; no se depende de JavaScript para consultar por WhatsApp ni para leer la información del local.
- **Validación:** recorrido sólo con teclado, revisión manual de contraste y desactivación de JavaScript en navegador para los flujos esenciales.
- **Dependencias:** 1.2, 2.1, 2.2, 2.3, 3.1, 3.2 y 4.1.
- **Decisiones diferidas:** nivel formal de conformidad de accesibilidad y herramienta automática de auditoría, si se requieren.

### [ ] 4.3 Ejecutar la validación manual de la versión inicial

- **Alcance:** realizar la lista de comprobación final de secciones, enlaces, CTA, responsive y contenido antes de entregar la landing.
- **Aceptación:** todas las secciones del Brief están presentes; los enlaces internos y externos definidos funcionan; los defectos encontrados quedan corregidos o registrados como riesgo explícito.
- **Validación:** recorrido manual en móvil y escritorio, prueba de CTAs, enlaces internos, teléfono/mapa si aplican, y contraste con criterios de éxito del Brief.
- **Dependencias:** 4.2.
- **Decisiones diferidas:** URL pública y controles posteriores al despliegue, sujetos a decidir hosting.

## Dependencias transversales

- El contenido y los activos comerciales definitivos (1.1) desbloquean la versión pública final de las secciones y CTAs.
- La decisión de hosting no bloquea la construcción local, pero sí la URL pública y la validación posterior al despliegue.
- No se planifican backend, panel de administración, base de datos, analítica ni integración de pagos en esta versión.

## Riesgos y decisiones necesarias antes de la implementación

- **Contenido crítico pendiente:** faltan logo, ofertas, marcas, dirección, horarios y número/enlace de WhatsApp definitivos. Sin ellos sólo podrá desarrollarse una maqueta con contenido temporal identificado.
- **Ofertas:** definir si comunicarán precios, vigencia y condiciones; publicarlos sin confirmación puede generar información comercial incorrecta.
- **Activos:** confirmar licencias/autorizaciones de fotografías y logotipos, o acordar alternativas tipográficas/visuales locales.
- **Mapa y contacto:** decidir si habrá enlace externo de indicaciones y qué canales complementarios se publicarán.
- **Identidad:** acordar paleta, tipografías y tono de los textos si no hay manual de marca.
- **Despliegue:** elegir hosting y dominio antes de solicitar una URL pública o añadir analítica.

## Historial

- Sin planificación todavía.
- 2026-08-07: backlog generado en borrador a partir del Brief y Perfil aprobados.
- 2026-08-07: Backlog aprobado por el usuario.
- 2026-08-07: el usuario autorizó que la tarea 1.1 use contenido ficticio para una demo; se adecuaron sus criterios de aceptación y validación para admitir un WhatsApp no operativo, con verificación real diferida a producción.
- 2026-08-07: tarea 1.1 aceptada por el usuario tras revisión de calidad independiente.
