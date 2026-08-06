# Orquestador técnico v1

`aidev` ejecuta localmente el flujo gobernado. Usa Python 3.12 y Codex CLI
como primer proveedor de agentes. No requiere servidor ni base de datos.

## Instalación

Desde la raíz del repositorio:

```bash
python -m pip install -e .
aidev --help
```

`aidev init` crea `.aidev/config.toml` si no existe. El
proveedor usa el ejecutable `codex` y la sesión local ya autenticada; el modelo
puede configurarse en ese archivo. No guardar claves ni secretos en el repo.

Antes de ejecutar roles con Codex, instalá la integración nativa:

```bash
aidev setup codex
```

Esto crea o actualiza sólo el bloque IADev de `workspace/AGENTS.md` y genera
los skills `aidev-*` en `workspace/.agents/skills/`. Las reglas existentes no
se sobrescriben.


## Inicio de un proyecto

```bash
aidev init mi-proyecto --responsible "Nombre Apellido"
aidev intake validate mi-proyecto
```

El primer comando crea:

- `specs/intake/mi-proyecto-brief.md`
- `specs/intake/mi-proyecto-technology-profile.md`
- una solicitud de aprobación de intake en `specs/approvals/`
- estado y auditoría en `.aidev/state/mi-proyecto/`

Completar el Brief y el Technology Profile antes de aprobar el intake.

## Aprobar y continuar

1. Abrir la aprobación pendiente en `ai-system/specs/approvals/`.
2. En el front matter, cambiar `decision: pending` por `approved`, `rejected`
   o `conditional`; completar `approved_by` y `decided_at`.
3. Aplicar la decisión y ejecutar el siguiente paso permitido:

```bash
aidev approvals sync mi-proyecto
aidev run mi-proyecto --responsible "Nombre Apellido"
```

Una decisión `rejected` bloquea el proyecto. Una decisión `conditional` lo
vuelve a planificación. El silencio nunca habilita una transición.

## Comandos

| Comando | Efecto |
| --- | --- |
| `aidev init <proyecto> --responsible <persona>` | Inicializa intake, estado y aprobación inicial. |
| `aidev setup codex` | Instala reglas y skills nativos de Codex en `workspace/`. |
| `aidev intake validate <proyecto>` | Comprueba contenido mínimo del Brief y del stack. |
| `aidev approvals sync <proyecto>` | Lee y valida decisiones humanas en Markdown. |
| `aidev run <proyecto> --responsible <persona>` | Ejecuta el siguiente rol o crea su gate de inicio. |
| `aidev resume <proyecto> --responsible <persona>` | Equivale a `run`; continúa sólo si no falta aprobación. |
| `aidev status <proyecto>` | Muestra etapa, rol activo, aprobaciones y ejecuciones. |
| `aidev audit <proyecto>` | Imprime el registro JSONL de eventos. |

## Máquina de estados

```text
intake_pending
  -- aprobar intake --> planning
  -- planner --> planner_pending
  -- aprobar plan --> task_ready
  -- autorizar inicio --> implementation_pending
  -- aprobar inicio --> implementation
  -- implementer --> implementer_pending
  -- aprobar entrega --> review
  -- reviewer --> reviewer_pending
  -- aceptar revisión --> closeout
  -- closeout --> closeout_pending
  -- aprobar cierre --> completed
```

Una ejecución que devuelve `blocked` bloquea el proyecto. Una acción de alto
impacto crea `high_impact_pending`; tras aprobarla, el orquestador vuelve a la
etapa que la solicitó.

## Archivos de estado y evidencia

Todo es legible y versionable:

- `state/<proyecto>/project.json`: etapa, rol, aprobaciones y ejecuciones.
- `state/<proyecto>/runs/run-*.json`: resultado estructurado de cada agente.
- `state/<proyecto>/events.jsonl`: auditoría append-only de transiciones.
- `specs/approvals/*.md`: solicitud y decisión humana.

## Límites de seguridad

Codex se invoca con raíz en `workspace/` y sandbox `workspace-write`. El
contexto de `ai-system/` se entrega en el prompt; el agente no debe modificarlo
directamente. El prompt prohíbe instalaciones, migraciones, red, despliegues y
configuración compartida. Si son necesarias, el agente debe declararlas como
`high_impact_actions`; el coordinador crea un gate adicional y no continúa sin
aprobación explícita.
