---
name: aidev-quality
description: Valida formato, lint, pruebas, convenciones y riesgos técnicos de una tarea IADev antes de cerrarla.
---

# Calidad IADev

Leé el Perfil Tecnológico para encontrar formato, lint y tests. Ejecutá sólo los comandos aplicables y reportá resultados sin ocultar fallos. Para cambios no triviales, pedí una revisión independiente a `quality-reviewer`.

Si la tarea toca rutas, formularios, permisos, archivos subidos, endpoints públicos o configuración de sesión, corré `aidev-seguridad` con alcance **cambio**; un hallazgo CONFIRMADO de gravedad alta o crítica devuelve la tarea a implementación.

Priorizá regresiones, seguridad, deuda técnica concreta y pruebas ausentes. Si hay problemas, devolvé la tarea a implementación; no la marques realizada ni hagas commit. Si todo está conforme, entregá evidencia clara al Coordinador.
