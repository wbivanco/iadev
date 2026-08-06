# Escenarios de referencia

Estos escenarios no requieren un producto real. Sirven para comprobar que una persona o agente puede recorrer el sistema de punta a punta.

## Escenario 1: corrección normal — mensaje de error ambiguo

| Etapa | Artefacto y resultado esperado |
| --- | --- |
| Idea | Se informa que un formulario muestra “falló” sin orientar al usuario. |
| Spec | Problema: el mensaje no permite corregir la entrada. Objetivo: mostrar una causa accionable. Fuera de alcance: rediseñar el formulario. Éxito: el error identifica el campo o acción a corregir. |
| Design | Se reutiliza el mecanismo de mensajes del proyecto; no se cambia la API. |
| Task | Localizar la conversión de error, ajustar el mensaje y ejecutar la prueba afectada. |
| Implementación | El implementer documenta el cambio y el resultado de la prueba. |
| Review | Se confirma que no expone detalles internos y que el alcance no se amplió. |
| Cierre | Se registra validación, riesgo restante y estado en memoria. |

Roles: planner → implementer → reviewer → closeout. Skills: planning, implementation, review y closeout.

## Escenario 2: cambio grande — exportación de datos

| Etapa | Artefacto y resultado esperado |
| --- | --- |
| Idea | Usuarios necesitan descargar sus resultados para analizarlos. |
| Spec | Define qué datos incluye, roles autorizados, formato esperado y criterios de privacidad. |
| Design | Establece el flujo de autorización, generación, almacenamiento temporal y auditoría; identifica riesgos de datos personales. |
| Tasks | Divide backend, interfaz, pruebas de autorización, documentación y cierre. Cada task declara su validación. |
| Implementación | Cada implementer entrega evidencia por task y registra dependencias o bloqueos. |
| QA/review | Verifica campos, permisos, formato, fallas y ausencia de datos no autorizados. |
| Cierre | Resume resultado, validaciones, riesgo residual, decisión de retención y próximos pasos. |

Este escenario exige design, tasks descompuestas, evidencia formal de QA y handoffs registrados. Muestra cuándo el flujo grande agrega rigor sin depender de una tecnología particular.

## Escenario 3: cambio UI — panel de filtros

| Etapa | Artefacto y resultado esperado |
| --- | --- |
| Spec y task | Se define el objetivo del panel y la task declara `visual_design: required`. |
| Selección | El Coordinador selecciona la task con `aidev task select <proyecto> <task-id>`. |
| Diseño visual | El Visual Designer usa el MCP local `open-pencil` y crea `workspace/design/<task-id>.fig`. |
| Aprobación | La persona responsable revisa y aprueba el `.fig`; sin esta decisión no se habilita implementación. |
| Implementación | El Implementer traduce el diseño aprobado a código y ejecuta las validaciones declaradas. |
| Cierre | Se conserva la evidencia del diseño, los cambios y la validación. |

Este escenario requiere que `open-pencil` esté habilitado localmente en Codex.
La configuración del MCP no se copia ni se versiona en IADev.
