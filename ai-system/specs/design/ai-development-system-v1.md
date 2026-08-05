# Design: AI Development System v1.0

## Enfoque

La v1 conserva Markdown como formato universal y no introduce dependencias ni
automatización. Se organiza en cuatro capas: gobierno del trabajo, adopción,
capacidades reutilizables y evidencia.

## Componentes

| Capa | Responsabilidad |
| --- | --- |
| Núcleo | Reglas, flujo SDD, templates y ciclo de vida documental. |
| Adopción | Instrucciones para copiar, personalizar y verificar la base. |
| Skills y roles | Procedimientos reutilizables y contratos humanos/agente. |
| Referencias | Escenarios completos que sirven como ejemplo y prueba manual. |

## Decisiones

- Los skills son documentos declarativos y no prompts dependientes de una
  plataforma.
- Los agentes son roles temporales; no son procesos persistentes ni requieren
  una herramienta de orquestación.
- El estado activo vive en `memory/`; los artefactos terminados se mantienen en
  `specs/` o se archivan según su valor como referencia.
- La validación de portabilidad es una checklist Markdown para que funcione en
  cualquier entorno.

## Riesgos y mitigación

- Demasiada burocracia: se conserva la clasificación trivial/normal/grande y
  el flujo permite omitir design en trabajo simple.
- Duplicación entre roles y skills: los roles indican responsabilidad; los
  skills indican cómo realizar una actividad.
