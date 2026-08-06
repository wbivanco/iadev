# AI Development System

Kit portable para planificar, ejecutar y cerrar trabajo asistido por IA. Incluye
memoria persistente, desarrollo guiado por especificaciones, templates, skills,
roles y un orquestador técnico local gobernado por aprobación humana.

## Empezar

Leé la [guía de adopción](docs/adoption-guide.md), personalizá `memory/` y
completá el Project Brief y Technology Profile. Para usar el runtime, instalá el
paquete desde la raíz del repositorio y seguí la [guía del orquestador](docs/orchestrator-cli.md).

El código real del proyecto vive por convención en `../workspace`.

## Alcance

El estado actual incluye el CLI `aidev`, una máquina de estados, aprobaciones en
Markdown, auditoría JSONL, selección explícita de tasks y un adaptador a Codex
CLI con sandbox de workspace.
El orquestador ejecuta roles sólo cuando su gate correspondiente fue aprobado;
no despliega, migra ni hace operaciones de red de forma autónoma. Las tasks de
interfaz pueden requerir un diseño visual aprobado: se ejecutan con el MCP
local `open-pencil` y dejan un artefacto `.fig` en `workspace/design/` antes de
habilitar la implementación.

## Tamaño, arquitectura y límites

IADev puede acompañar la creación, evolución y mantenimiento de software a
partir de una necesidad: la convierte en brief, spec, diseño y tasks de un
backlog; luego ejecuta cada task aprobada, con validación, revisión y cierre.
No pretende generar ni operar un producto completo sin intervención humana en
una única ejecución.

No hay un límite conceptual de tamaño ni una arquitectura obligatoria. Puede
usarse con un monolito, un monolito modular, frontend y backend separados o
microservicios. Para iniciativas grandes, el trabajo debe organizarse en
hitos, specs y tasks pequeñas con dependencias y criterios de aceptación
explícitos. El límite práctico está en la calidad de esa descomposición, el
contexto disponible, las pruebas de integración y la revisión humana.

Los microservicios no son un requisito ni una preferencia del kit. Si se eligen,
el Technology Profile y el diseño deben definir los límites de cada servicio,
contratos de API o eventos, datos y propiedad, autenticación, observabilidad,
versionado, pruebas integradas y estrategia de despliegue. Para un dominio
pequeño o todavía cambiante suele ser más simple comenzar con un monolito
modular y separar servicios sólo cuando haya límites de negocio u operación
claros.

El orquestador no instala dependencias, ejecuta migraciones, usa red ni
despliega por cuenta propia. Esas operaciones, como cualquier cambio de costo,
seguridad, arquitectura o entorno compartido, requieren una decisión humana
explícita y pueden ejecutarse fuera del runtime según las políticas del
proyecto.

## Referencias

- [Flujo de orquestación gobernada](docs/governed-orchestration-v2.md)
- [Guía del orquestador](docs/orchestrator-cli.md)
- [Roles y handoffs](guidance/roles.md)
- [Skills incluidos](guidance/skills/)
- [Integración OpenPencil](integrations/open-pencil.toml)
