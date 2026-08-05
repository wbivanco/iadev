# Guía de adopción

## Inicio rápido

1. Copiá `ai-system/`, `src/`, `tests/` y `pyproject.toml` en la raíz del proyecto destino.
2. Conservá `workspace/` como código ejecutable o adaptá esa ruta de forma consistente.
3. Instalá el comando local: `python -m pip install -e .`.
4. Inicializá el proyecto: `aidev init <proyecto> --responsible "<persona>"`.
5. Completá `specs/intake/<proyecto>-brief.md` y `<proyecto>-technology-profile.md`.
6. Ejecutá `aidev intake validate <proyecto>`.
7. Aprobá el intake editando su Markdown y aplicá la decisión con `aidev approvals sync <proyecto>`.
8. Repetí `aidev run`, aprobación y `aidev approvals sync` hasta completar el ciclo.

La referencia operativa de comandos, estados y archivos es la [guía del
orquestador](../orchestrator/README.md).

## Qué es universal

- Flujo SDD, trazabilidad de decisiones, cierre y memoria persistente.
- Estructura de specs, templates, skills, roles y gates de aprobación.
- CLI Python local, estado JSON/JSONL versionable y contratos de proveedor.
- Criterio de que todo trabajo relevante declare validación y reciba aprobación humana.

## Qué se define por proyecto

- Stack, arquitectura, comandos de test, CI/CD y convenciones de código.
- Responsable humano, roles permitidos, modelo y configuración local de Codex.
- Requisitos funcionales, riesgos de negocio y políticas de despliegue.

Nunca incluir secretos en Brief, Technology Profile, estado o archivos de
configuración versionados.

## Ciclo de vida documental

| Artefacto | Se crea | Se actualiza | Se cierra o archiva |
| --- | --- | --- | --- |
| Brief y perfil tecnológico | Al iniciar proyecto | Si cambia el contexto | Reemplazado al cambiar el proyecto |
| Aprobación | Antes de cada transición material | Al decidir | Se conserva como auditoría |
| Spec, Design y Task | Durante planificación | Si cambia alcance o enfoque | Completada o cancelada |
| Run y evidencia | Al ejecutar un rol | Nunca; es evidencia | Se conserva en estado |
| Cierre | Tras revisión aceptable | Si cambian condiciones | Se conserva como registro |
| Decisión | Cuando cambia un criterio durable | Si se reemplaza | Nunca se borra; se marca reemplazada |

## Operación segura

El implementador recibe `workspace/` como raíz escribible. No debe instalar
dependencias, ejecutar migraciones, usar red, desplegar ni cambiar configuración
compartida. Si detecta una de esas necesidades, devuelve una acción de alto
impacto; el orquestador crea una aprobación adicional y espera decisión humana.
