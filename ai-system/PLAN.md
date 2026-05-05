# PLAN.md

## 📌 Estado general del proyecto

Este proyecto tiene como objetivo construir un **sistema portable de desarrollo con IA** (AI Development System) que permita trabajar de forma consistente entre herramientas como VS Code, Cursor, OpenCode, Claude Code y Codex.

Se busca separar completamente:

- la **planificación, memoria y reglas** (`ai-system/`)
- del **código real del proyecto** (`workspace/`)

---

# 🧭 Fase actual

## Fase 1 — Fundación del sistema (EN PROGRESO)

Estamos construyendo la base estructural del sistema.

---

# ✅ Lo que ya está hecho

## 1. Estructura del proyecto

Se definió y creó:

```text
mi-proyecto/
├── ai-system/
└── workspace/




Estado actual del proyecto
Fase actual
🟡 Fase 1 — Sistema base operativo (EN PROGRESO AVANZADO)

El sistema ya:

✔ Es usable
✔ Permite retomar contexto
✔ Funciona con agentes

Pero aún no:

❌ Está completamente formalizado
❌ Tiene flujo SDD completo
❌ Está optimizado para equipos

🧱 Arquitectura definida
mi-proyecto/
├── ai-system/
│   ├── AGENTS.md
│   ├── plan.md
│   ├── memory/
│   ├── specs/
│   ├── skills/
│   ├── orchestration/
│   ├── templates/
│   └── docs/
│
└── workspace/
✅ Lo que YA está hecho
1. Separación estructural del sistema

✔ ai-system/ como capa de inteligencia
✔ workspace/ como código ejecutable
✔ Independencia de herramientas

👉 Esto permite portabilidad total

2. Sistema de memoria completo (v1 funcional)

Ubicación:

ai-system/memory/

Archivos:

MEMORY.md → entrypoint del sistema
current-state.md → estado actual del proyecto
project-summary.md → visión general
decisions.md → decisiones persistentes
open-questions.md → incertidumbre activa
session-log.md → historial de trabajo
agent-handoffs.md → coordinación entre agentes
Capacidades

✔ Persistencia entre sesiones
✔ Reemplazo del contexto de chat
✔ Base para multi-agente
✔ Portable entre herramientas

👉 Esta es una de las piezas más maduras del sistema

3. Filosofía del sistema

Se definieron principios clave:

Spec Anchored Development
Separación planificación / ejecución
IA como ejecutor, no como fuente de verdad
Memoria persistente como núcleo del sistema
Independencia total de herramientas

👉 Esto define el comportamiento global

4. Flujo de trabajo mínimo (operativo)

Actualmente el sistema permite:

leer memoria
→ entender estado
→ implementar
→ actualizar memoria

✔ Funciona en práctica
❌ No está formalizado completamente

5. AGENTS.md (versión base funcional)

Define:

lectura obligatoria de memoria
separación ai-system / workspace
flujo mínimo de ejecución
reglas de cierre

✔ Permite usar agentes reales
❌ Aún es limitado

6. Modelo de memoria avanzada (conceptual)

Diseñado:

Markdown como fuente de verdad
SQLite/FTS como optimización futura
memoria por capas (estado, decisiones, histórico)

✔ Escalable
✔ Portable
✔ independiente de tecnología

🚧 Lo que está parcialmente hecho
1. Flujo SDD (incompleto)

Existe de forma implícita:

idea → spec → implementación → memoria

Pero falta:

formalización completa
enforcement
integración con agentes
❌ Lo que falta (para completar el sistema)
🔴 PRIORIDAD ALTA
1. AGENTS.md v2 (CRÍTICO)

Debe incluir:

flujo SDD completo
comportamiento por tipo de tarea
integración con specs
manejo de errores
reglas de calidad
integración con testing / PR

👉 Esto convierte el sistema en consistente

2. Flujo SDD completo

Formalizar:

idea
→ spec
→ design
→ tasks
→ implementación
→ testing
→ PR
→ memoria

👉 Esto convierte el sistema en profesional

3. Templates base

Ubicación:

ai-system/templates/

Necesarios:

spec.template.md
task.template.md
decision.template.md
PR template

👉 Reduce fricción
👉 Asegura consistencia

🟡 PRIORIDAD MEDIA
4. Skills modulares

Ubicación:

ai-system/skills/

Ejemplos:

spec-writing
implementation
debugging
testing
review

👉 Permite escalar conocimiento sin romper contexto

5. Orquestación mínima

Ubicación:

ai-system/orchestration/

Definir:

roles de agentes
handoffs
contratos de salida

👉 Habilita multi-agente real

🟢 PRIORIDAD BAJA (futuro)
6. Automatización de memoria
búsqueda avanzada (SQLite / FTS)
scripts de indexación
MCP server
7. Integraciones IDE
VS Code tasks
hooks de Git
comandos automáticos
🎯 Estado real resumido
[✔] Arquitectura del sistema
[✔] Separación código / planificación
[✔] Sistema de memoria completo
[✔] AGENTS.md base funcional
[✔] Flujo mínimo operativo

[ ] Flujo SDD formal
[ ] AGENTS.md avanzado
[ ] Templates
[ ] Skills
[ ] Orquestación
🧠 Nivel del sistema
Estructura:       100%
Memoria:          90%
Flujo:            60%
Automatización:   20%
Escalabilidad:    50%
🚀 Próximo paso estratégico

👉 Enfocar en:

AGENTS.md v2 + Flujo SDD completo

Porque:

define cómo trabaja todo el sistema
elimina ambigüedad
permite consistencia entre herramientas
habilita multi-agente real
📌 Regla del proyecto

No agregar complejidad hasta cerrar el flujo base.

🏁 Objetivo de esta fase

Pasar de:

👉 sistema estructurado

a:

👉 sistema operativo completo

🔥 Insight clave

Este proyecto no busca mejorar un IDE.

Busca crear:

👉 una capa superior que gobierne cómo se desarrolla software con IA