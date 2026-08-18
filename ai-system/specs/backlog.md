---
status: approved
updated_at: "2026-08-18"
---

# Backlog

Este backlog fue aprobado por el usuario el 2026-08-18. Cada tarea requiere
aprobación explícita antes de implementarse.

Los skills deben ser livianos y portables: orientan las acciones de un agente
con las herramientas ya disponibles en cada proyecto. No incluyen scripts
propios, adaptadores por motor ni dependencias persistentes.

## Módulo 1 — Skill `aidev-der`

### [x] DER-01 — Revisar y completar las instrucciones del DER

**Alcance**

- Revisar `.agents/skills/aidev-der/SKILL.md` contra el Brief y este criterio
  de portabilidad.
- Completar sólo las instrucciones necesarias para que el agente priorice las
  migraciones, contraste de forma opcional y de sólo lectura un esquema ya
  accesible, y exponga las diferencias para decisión humana.
- Mantener el contrato de artefactos versionados en `ai-system/docs/der/` y la
  preservación de artefactos previos ante fuentes o herramientas ausentes.
- Indicar que la creación o actualización de Mermaid, Markdown, SVG y PNG se
  realiza con las capacidades disponibles en el entorno, sin incorporar
  automatizaciones ni dependencias al repositorio.

**Aceptación**

- El `SKILL.md` deja claro qué evidencia revisar, qué artefactos mantener y qué
  límites comunicar, sin prescribir scripts ni adaptadores específicos.
- Las diferencias entre migraciones y esquema no habilitan modificaciones
  automáticas de ninguna de las dos fuentes.

**Validación**

- Revisión manual del `SKILL.md` frente al Brief, Perfil y esta tarea.
- Búsqueda de referencias a scripts propios, adaptadores por motor o archivos
  de dependencias persistentes: no deben formar parte del alcance del skill.

**Dependencias**

- Brief y Perfil Tecnológico aprobados.

**Cierre (2026-08-18)**

- Validación: revisión manual, `git diff --check` y revisión independiente aprobada.
- Riesgo residual: sin renderizador o fuentes accesibles no se regeneran los artefactos; el skill conserva lo existente e informa el límite.

## Módulo 2 — Skill `aidev-documentation`

### [x] DOC-01 — Revisar y completar las instrucciones de guía técnica

**Alcance**

- Revisar `.agents/skills/aidev-documentation/SKILL.md` para que guíe al agente
  a localizar una guía existente, actualizarla de forma acotada o proponer una
  nueva ruta cuando no exista una convención clara.
- Mantener enlaces relativos únicamente a DER y documentos que existan;
  informar ausencias o enlaces rotos sin inventar referencias.
- Asegurar que las instrucciones no requieran generadores, scripts ni
  dependencias persistentes.

**Aceptación**

- El `SKILL.md` establece un criterio portable para preservar contenido ajeno,
  enlazar artefactos existentes y comunicar límites.
- La guía resultante puede verificarse mediante enlaces relativos resolubles en
  un clon normal del repositorio.

**Validación**

- Revisión manual del `SKILL.md` con los casos de guía existente, guía ausente y
  DER ausente.
- Comprobación de que el alcance no incorpora automatizaciones ni archivos de
  dependencias persistentes.

**Dependencias**

- DER-01, para fijar las rutas y los límites de los artefactos que se enlazan.

**Cierre (2026-08-18)**

- Validación: revisión de los casos de guía existente, guía ausente y DER ausente; revisión independiente aprobada.
- Riesgo residual: no hay una guía ni DER reales en este repositorio para resolver enlaces; el skill exige comprobarlos al aplicarse.

## Módulo 3 — Integración documental

### [x] FLOW-01 — Documentar la secuencia de uso de ambos skills

**Alcance**

- Alinear en los dos `SKILL.md` la secuencia documental para un cambio de
  esquema aceptado: DER, guía técnica, revisión de enlaces y comunicación de
  riesgos antes de solicitar el último sí de commit.
- Documentar que un contraste pendiente, un enlace roto o la indisponibilidad
  de una herramienta se informa al usuario; no se resuelve de forma implícita.
- Mantener fuera de alcance cualquier automatización del cierre, integración de
  scripts o adaptación por motor.

**Aceptación**

- Ambos skills describen el mismo orden, sus condiciones de salida y los
  bloqueos que requieren decisión humana.
- El flujo para tareas sin cambios de esquema no impone pasos documentales
  innecesarios.

**Validación**

- Lectura cruzada de ambos `SKILL.md` para confirmar orden, rutas y tratamiento
  coherente de bloqueos.
- Revisión de un escenario de cambio de esquema y otro sin cambio de esquema,
  verificando que las instrucciones diferencien ambos casos.

**Dependencias**

- DER-01 y DOC-01.

**Cierre (2026-08-18)**

- Validación: lectura cruzada de ambos skills, `git diff --check` y revisión independiente aprobada.
- Riesgo residual: la detección concreta de cambios de esquema queda a criterio del proyecto consumidor.

## Orden de ejecución propuesto

1. DER-01 — Instrucciones portables para el DER.
2. DOC-01 — Instrucciones portables para la guía técnica.
3. FLOW-01 — Secuencia documental compartida.

## Riesgos de planificación
- Sin un renderizador ya disponible, SVG y PNG no pueden garantizarse de manera
  portable. El agente debe informar el límite y preservar lo existente.
- Sin una convención documental del proyecto consumidor, elegir la ruta de una
  guía nueva requiere decisión humana.

## Historial

- 2026-08-08: creado como esqueleto genérico para una nueva planificación.
- 2026-08-14: backlog original aprobado por el usuario.
- 2026-08-18: backlog simplificado aprobado por el usuario; los skills son portables, sin scripts propios ni dependencias persistentes, y SVG/PNG se generan sólo si el entorno ya puede renderizarlos.
- 2026-08-18: DER-01 aceptada por el usuario tras revisión independiente; el skill `aidev-der` quedó validado como instrucción portable.
- 2026-08-18: DOC-01 aceptada por el usuario tras revisión independiente; el skill `aidev-documentation` quedó validado como instrucción portable.
- 2026-08-18: FLOW-01 aceptada por el usuario tras revisión independiente; ambos skills comparten la secuencia documental para cambios de esquema.
