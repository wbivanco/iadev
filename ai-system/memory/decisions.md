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

---

## 2026-05-20 - Formalizar flujo SDD v1 antes de expandir skills u orquestación

Tipo: proceso  
Estado: vigente  
Tags: sdd, flujo, agentes, templates  

### Contexto

El sistema ya tenía memoria y reglas básicas, pero faltaba un flujo repetible
que indicara cuándo crear spec, design, task, validación y cierre. Sin ese
flujo, `AGENTS.md` y los templates quedaban subdefinidos.

### Decisión

Definir primero un flujo `SDD v1` mínimo en `ai-system/docs/sdd-flow-v1.md`,
derivar de ahí `AGENTS.md` v2 y crear sólo los templates esenciales.

### Consecuencia

El siguiente trabajo del proyecto ya no es diseñar más estructura, sino probar
el flujo con un caso real y ajustar fricciones observadas.
