# Guía de adopción

## Inicio rápido

1. Copiá la carpeta `ai-system/` en la raíz del proyecto destino.
2. Conservá `workspace/` como ubicación del código o reemplazá esa referencia
   de forma consistente en `AGENTS.md` y la documentación.
3. Editá `memory/project-summary.md` con el objetivo del proyecto destino.
4. Editá `memory/current-state.md` con su fase, estado y próximos pasos.
5. Registrá decisiones iniciales en `memory/decisions.md` y dudas reales en
   `memory/open-questions.md`.
6. Añadí al resumen del proyecto las tecnologías, comandos de validación,
   convenciones y restricciones que sean propias del destino.
7. Ejecutá la [checklist de portabilidad](portability-checklist.md).

## Qué es universal

- Flujo SDD, clasificación de trabajo, trazabilidad de decisiones y cierre.
- Estructura de memoria, specs, templates, skills y roles.
- Criterio de que todo trabajo relevante declare validación.

## Qué se define por proyecto

- Stack, arquitectura, comandos de test, CI/CD y convenciones de código.
- Roles adicionales, skills específicos, permisos y responsables humanos.
- Requisitos funcionales, riesgos de negocio y políticas de despliegue.

## Ciclo de vida documental

| Artefacto | Se crea | Se actualiza | Se cierra o archiva |
| --- | --- | --- | --- |
| Spec | Trabajo no trivial | Si cambia alcance u objetivo | Completada o cancelada |
| Design | El enfoque no es obvio | Si cambia la solución | Aprobado o reemplazado |
| Task | Cada unidad ejecutable | Durante la ejecución | Completada o bloqueada |
| QA | Cuando se requiere evidencia formal | Tras validar | Al aceptar/rechazar |
| Cierre | Al terminar trabajo relevante | Si cambia el resultado | Se conserva como registro |
| Decisión | Cuando cambia un criterio durable | Si se reemplaza | Nunca se borra; se marca reemplazada |

Los documentos terminados que sean útiles como antecedente permanecen en
`specs/`. Los borradores abandonados y registros obsoletos se mueven a
`memory/archive/`, preservando su fecha y motivo.

## Versionado

La versión del kit se declara en `ai-system/README.md`. Se aplica versionado
semántico: cambios incompatibles en reglas o estructura incrementan la versión
mayor; capacidades compatibles, la menor; correcciones documentales, el patch.
