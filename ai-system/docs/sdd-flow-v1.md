# SDD Flow v1

## Objetivo

Definir un flujo mínimo, portable y repetible para trabajar con IA desde una
idea hasta el cierre del trabajo sin depender de una herramienta específica.

Este flujo está pensado para ser lo bastante liviano para proyectos pequeños y
lo bastante claro para coordinar agentes o sesiones futuras.

## Flujo base

`idea -> spec -> design -> tasks -> implementacion -> validacion -> cierre -> memoria`

## Etapas

### 1. Idea

Propósito:

- capturar el problema, cambio o necesidad
- decidir si el trabajo amerita formalización

Entrada mínima:

- pedido del usuario, issue o necesidad detectada

Salida mínima:

- decisión de continuar o no
- alcance resumido en una spec nueva o existente

Regla:

- si el cambio es trivial y de bajo riesgo, puede saltarse una idea explícita
  siempre que la spec o task deje claro el objetivo

### 2. Spec

Propósito:

- describir qué se quiere lograr y por qué

Documento sugerido:

- `ai-system/specs/product/` o `ai-system/specs/requirements/`

Debe responder:

- problema
- objetivo
- alcance
- restricciones
- criterio de éxito

Entrada mínima:

- idea aprobada o necesidad concreta

Salida mínima:

- una spec entendible por otro agente sin contexto adicional

Regla:

- no implementar cambios medianos o grandes sin una spec explícita

### 3. Design

Propósito:

- definir cómo se va a resolver

Documento sugerido:

- `ai-system/specs/design/`

Debe responder:

- enfoque técnico o documental
- componentes afectados
- decisiones relevantes
- riesgos y tradeoffs

Entrada mínima:

- spec suficientemente clara

Salida mínima:

- estrategia concreta que reduzca ambigüedad antes de ejecutar

Regla:

- puede omitirse en trabajos simples si la task ya contiene un enfoque claro

### 4. Tasks

Propósito:

- dividir el trabajo en unidades ejecutables

Documento sugerido:

- `ai-system/specs/tasks/`

Debe responder:

- qué se hace
- en qué orden
- cómo se valida
- qué queda fuera

Entrada mínima:

- spec y, si aplica, design

Salida mínima:

- lista de tareas verificables

Regla:

- si hay más de una sesión o más de un agente, las tasks son obligatorias

### 5. Implementación

Propósito:

- ejecutar cambios en `workspace/` o en `ai-system/`, según corresponda

Entrada mínima:

- task activa
- contexto cargado desde memoria

Salida mínima:

- cambios concretos y revisables

Reglas:

- no modificar `workspace/` sin revisar memoria y reglas
- si falta contexto crítico, detenerse y registrar la ambigüedad

### 6. Validación

Propósito:

- comprobar que el trabajo cumple el objetivo

Documento sugerido:

- `ai-system/specs/qa/` si hace falta dejar evidencia más formal

Validaciones posibles:

- tests
- revisión manual
- checklist documental
- verificación contra criterios de éxito

Entrada mínima:

- implementación terminada

Salida mínima:

- evidencia suficiente para afirmar si el trabajo quedó aceptable o no

Regla:

- toda task debe declarar al menos una forma de validación

### 7. Cierre

Propósito:

- resumir qué cambió, qué se decidió y qué queda pendiente

Documento sugerido:

- `ai-system/specs/releases/` o template de cierre

Debe responder:

- resultado
- validaciones ejecutadas
- riesgos restantes
- próximos pasos

Entrada mínima:

- implementación y validación completadas

Salida mínima:

- estado comunicable a otra persona o agente

### 8. Memoria

Propósito:

- persistir el contexto operativo del proyecto

Archivos mínimos:

- `ai-system/memory/current-state.md`
- `ai-system/memory/decisions.md`
- `ai-system/memory/open-questions.md`
- `ai-system/memory/session-log.md`

Regla:

- actualizar memoria después de todo trabajo relevante

## Criterios de entrada y salida por tipo de trabajo

### Trabajo trivial

Ejemplos:

- corrección menor de texto
- ajuste puntual sin impacto estructural

Requiere:

- memoria
- task breve o contexto equivalente
- validación básica

Puede omitir:

- design formal
- spec extensa

### Trabajo normal

Ejemplos:

- cambio funcional acotado
- refactor mediano
- mejora documental relevante

Requiere:

- spec
- task
- validación explícita
- actualización de memoria

### Trabajo grande o ambiguo

Ejemplos:

- nueva capacidad del sistema
- cambio arquitectónico
- trabajo multiagente

Requiere:

- spec
- design
- task descompuesta
- cierre más formal
- actualización de decisiones si cambió el enfoque del sistema

## Reglas para agentes

- Si no existe spec y el trabajo no es trivial, crearla antes de implementar.
- Si la spec existe pero el cómo no está claro, crear design antes de avanzar.
- Si hay ambigüedad no resoluble con el repo, registrar la duda en
  `open-questions.md`.
- Si una decisión afecta el modo de trabajo del sistema, registrarla en
  `decisions.md`.
- Si no se pudo validar, dejarlo explícito en el cierre y en la sesión.

## Definición de mínimo operable

El flujo se considera operativo cuando un agente puede:

1. leer memoria
2. ubicar la spec aplicable
3. ejecutar una task concreta
4. validar el resultado
5. actualizar memoria sin instrucciones extra
