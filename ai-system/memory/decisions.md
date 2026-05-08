# Decisions

---

## 2026-05-08 - Separar ai-system y workspace

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

---

## 2026-05-08 - Tratar ai-system como producto principal en esta fase

Tipo: alcance  
Estado: vigente  
Tags: prioridad, sistema-base, portabilidad  

### Contexto

El objetivo inmediato no es construir una aplicación dentro de `workspace/`,
sino consolidar una base reusable de trabajo con IA que luego pueda copiarse a
otros proyectos.

### Decisión

Priorizar la calidad y coherencia de `ai-system/` por encima de poblar
`workspace/` con código real en esta etapa.

### Consecuencia

Las siguientes iteraciones deben enfocarse en memoria, reglas, flujo SDD y
templates antes de considerar implementación de producto.
