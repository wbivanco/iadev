# Guía de puesta en marcha de IADev

## Inicio rápido

1. Copiá `ai-system/`, `src/`, `tests/` y `pyproject.toml` en la raíz del proyecto destino.
2. Conservá `workspace/` como código ejecutable o adaptá esa ruta de forma consistente.
3. Instalá el comando local: `python -m pip install -e .`.
4. Instalá la integración nativa de Codex: `aidev setup codex`.
5. Inicializá el proyecto: `aidev init <proyecto> --responsible "<persona>"`.
6. Completá `specs/intake/<proyecto>-brief.md` y `<proyecto>-technology-profile.md`.
7. Ejecutá `aidev intake validate <proyecto>`.
8. Aprobá el intake editando su Markdown y aplicá la decisión con `aidev approvals sync <proyecto>`.
9. Después del plan aprobado, listá y seleccioná la task: `aidev task list <proyecto>` y `aidev task select <proyecto> <task-id>`.
10. Para una task UI con diseño requerido, ejecutá el paso de diseño visual, aprobá el `.fig` y recién entonces autorizá la implementación.
11. Tras la revisión aceptada, autorizá el commit local de la task y ejecutá el rol `smart-commit`; luego aprobá su cierre.
12. Repetí selección de task, ejecución y aprobaciones hasta que no queden tasks abiertas.

La referencia operativa de comandos, estados y archivos es la [guía de uso de
AIDev CLI](orchestrator-cli.md).

## Practicar antes de un proyecto real

Los [escenarios de referencia](reference-scenarios.md) muestran recorridos
completos para una corrección pequeña, un cambio amplio y una task visual. Son
opcionales, pero sirven para aprender o validar manualmente el flujo antes de
aplicarlo a un producto real.

## Qué es universal

- Flujo SDD, trazabilidad de decisiones, cierre y memoria persistente.
- Estructura de specs, templates, skills, roles y gates de aprobación.
- CLI Python local, estado JSON/JSONL versionable y contratos de proveedor.
- Criterio de que todo trabajo relevante declare validación y reciba aprobación humana.

## Qué se define por proyecto

- Stack, arquitectura, comandos de test, CI/CD y convenciones de código.
- Responsable humano, roles permitidos, modelo y configuración local de Codex.
- MCPs locales requeridos por el proyecto, sin comandos, rutas, variables ni secretos en archivos versionados.
- Requisitos funcionales, riesgos de negocio y políticas de despliegue.

Nunca incluir secretos en Brief, Technology Profile, estado o archivos de
configuración versionados.

## Aplicabilidad, escala y arquitectura

IADev es un sistema de trabajo para pasar de una necesidad a un backlog
ejecutable y trazable: produce brief, spec, diseño y tasks, y ayuda a
implementar, validar, revisar y cerrar cada unidad aprobada. No sustituye la
definición de producto, la arquitectura ni la responsabilidad de una persona;
tampoco crea y opera de forma autónoma un sistema completo en una sola corrida.

Puede adoptarse en proyectos pequeños, medianos o grandes. En un proyecto
grande, evitá tratar todo el producto como una sola spec o task: dividilo en
hitos o capacidades, luego en specs y tasks pequeñas, ordenadas por
dependencias y con una validación verificable. La escalabilidad práctica del
flujo depende de conservar decisiones y contexto, controlar cambios de alcance,
mantener contratos entre componentes y ejecutar pruebas unitarias, de contrato
e integración apropiadas.

El kit no impone arquitectura. Es aplicable a monolitos, monolitos modulares,
frontends y backends separados, y microservicios. Los microservicios requieren
más diseño y operación; antes de planificar su implementación, documentá como
mínimo en el Technology Profile y el diseño:

- responsabilidad y límites de cada servicio;
- propiedad de datos y consistencia entre servicios;
- contratos de APIs, eventos, versionado y compatibilidad;
- autenticación, autorización, observabilidad y manejo de fallas;
- pruebas de contrato e integración, CI/CD y estrategia de despliegue.

Elegir microservicios no es un objetivo en sí mismo. Cuando el dominio, el
equipo y el despliegue todavía son simples, un monolito modular suele reducir
la coordinación y acelerar el aprendizaje. La división en servicios cobra
sentido si hay límites de negocio claros, ciclos de despliegue independientes o
requisitos operativos y de escalado que lo justifiquen.

Finalmente, los límites operativos del runtime se mantienen incluso si el
proyecto es grande: no instala dependencias, ejecuta migraciones, accede a la
red ni despliega automáticamente. Esas acciones y toda decisión que afecte
arquitectura, seguridad, costo o entornos compartidos deben pasar por
aprobación humana explícita.

## Integración nativa de Codex

`aidev setup codex` instala un bloque administrado por IADev en
`workspace/AGENTS.md` y los skills nativos en `workspace/.agents/skills/`.
Las reglas existentes se conservan: sólo se actualiza el bloque delimitado por
marcadores IADev. Los skills pueden usarse manualmente en Codex o los invoca
explícitamente `aidev run` para cada rol. Si un skill generado fue modificado,
la instalación pide `--force` antes de restaurarlo.

## Diseño visual con OpenPencil

Una task que declara `visual_design: required` necesita el MCP local `open-pencil` disponible en Codex. IADev sólo declara esa dependencia en `integrations/open-pencil.toml`: cada usuario administra su instalación y configuración local. El rol Visual Designer crea `workspace/design/<task-id>.fig`; el archivo se revisa y aprueba antes de habilitar al Implementer. Las tasks que no lo requieren continúan directamente al gate de inicio.

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
