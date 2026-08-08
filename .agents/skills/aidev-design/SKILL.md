---
name: aidev-design
description: Diseña wireframes, mockups, pantallas, dashboards y sistemas de componentes opcionales con OpenPencil para tareas o productos de IADev. Usar sólo cuando el usuario pida explícitamente diseño, mockup, wireframe, Figma o OpenPencil; nunca como requisito implícito para implementar.
---

# Diseño opcional IADev

Leé el Brief, Perfil, Backlog y la tarea visual solicitada. No reemplaces la entrevista, planificación ni aprobación de tareas. No modifiques código, `ai-system/`, Backlog, memoria, aprobaciones ni commits.

1. Confirmá que OpenPencil está disponible antes de modificar un diseño. Si el MCP o el software no responde, informá que el diseño queda pendiente; no crees archivos ni bloquees el flujo normal de IADev.
2. Acordá el alcance visual y usá una página nueva del documento llamada `IADev — <tarea>` para no alterar un diseño existente sin autorización.
3. Creá el borrador mediante `render` o las herramientas de nodos de OpenPencil. Podés producir wireframes, mockups, landing pages, dashboards, componentes y variables de diseño.
4. Exportá una vista previa para revisión. No guardes un `.fig` en el repositorio ni generes código antes de la aceptación explícita del usuario.
5. Tras la aceptación, guardá el artefacto en `design/<slug-de-tarea>.fig`. Si aportan valor, obtené tokens y un mapa de componentes para acompañar la implementación; no los trates como código generado automáticamente.
6. Devolvé al Coordinador la ruta del diseño, la vista previa, los componentes/tokens relevantes y las decisiones visuales. El Coordinador registra el diseño aprobado en la tarea del Backlog antes de delegar implementación.

El archivo `.fig` es una referencia visual aprobable. Si no existe o no puede abrirse, el implementador continúa con el Brief, Perfil y tarea aprobada; no inventes un diseño ni marques la tarea bloqueada.
