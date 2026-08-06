# Contexto activo

## Resumen vigente

IADev es un kit portable para planificar, implementar, validar y cerrar
software asistido por IA, con aprobación humana por transición material.

## Estado actual

- Fase: V1.2, adopción piloto del runtime gobernado.
- Próximo objetivo: ejecutar un proyecto piloto completo y registrar las
  fricciones observadas.

## Decisiones activas

- Separar el sistema de trabajo en `ai-system/` del código en `workspace/`.
- Mantener el flujo SDD y la aprobación humana como controles centrales.
- Usar roles temporales y skills genéricos; no agentes persistentes.

## Dudas abiertas

- Evaluar automatización adicional sólo después de adopciones reales.
- Evaluar búsqueda de memoria bajo demanda si el archivo histórico crece.

## Próximo paso verificable

Ejecutar un proyecto piloto con `aidev`, completar el intake y recorrer el
flujo de planificación, implementación, revisión y cierre.
