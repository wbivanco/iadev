# Decisions

---

## YYYY-MM-DD — Separar ai-system y workspace

Tipo: arquitectura  
Estado: vigente  
Tags: estructura, agentes, memoria  

### Contexto

Se necesita separar la planificación, memoria y reglas del código real del proyecto.

### Decisión

Usar dos carpetas principales:

- `ai-system/`: sistema de trabajo con IA
- `workspace/`: código desarrollado

### Consecuencia

El sistema queda portable y puede aplicarse a distintos tipos de proyectos.
