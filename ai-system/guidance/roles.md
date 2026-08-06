# Roles y handoffs v2

Los roles son responsabilidades temporales. Una misma persona o agente puede cubrir varios, salvo que el responsable humano establezca segregación de funciones. Todo rol queda sujeto a la aprobación humana definida en `docs/governed-orchestration-v2.md`.

| Rol | Entrada | Salida | Responsabilidad | Límite |
| --- | --- | --- | --- | --- |
| Coordinador | Brief, perfil tecnológico y memoria | Asignación, handoff y estado | Validar entradas, enrutar trabajo, administrar aprobaciones y bloqueos. | No implementa, revisa ni reemplaza decisiones humanas. |
| Planner | Intake aprobado y memoria | Spec, design y tasks | Aclarar objetivo, alcance, solución y éxito. | No consolida el plan sin aprobación. |
| Visual Designer | Task UI aprobada | Artefacto `.fig` y evidencia | Crear el diseño visual con el MCP local requerido y solicitar su aprobación. | No implementa producto ni reemplaza la revisión humana. |
| Implementer | Task aprobada | Cambios y evidencia | Ejecutar sólo la unidad aprobada. | No amplía alcance ni entrega a revisión sin aprobación. |
| Reviewer | Cambios, criterios y evidencia | Dictamen o correcciones | Verificar calidad, alcance y riesgos. | No acepta ni rechaza definitivamente sin aprobación humana. |
| Smart Committer | Task revisada y aprobación de commit | Commit local y evidencia | Crear un commit atómico limitado a la task. | No hace push, no reescribe historial ni incluye cambios ajenos. |
| Closeout | Resultado revisado y commit | Cierre y memoria actualizada | Registrar resultado, pendientes y siguiente paso. | No marca completado sin aprobación. |
| Responsable humano | Solicitudes de aprobación | Decisión registrada | Aprobar, rechazar o condicionar las transiciones materiales. | No delegar su decisión por silencio. |

## Contrato de handoff

Todo traspaso se registra en `memory/agent-handoffs.md` e incluye:

- rol emisor y receptor;
- objetivo y estado actual;
- enlaces al brief, perfil tecnológico, spec, design, task y evidencia;
- solicitud de aprobación vigente y su estado;
- decisiones, riesgos, bloqueos y próximo paso verificable.

Un receptor no inicia una acción material si falta una aprobación aplicable. Si el trabajo se bloquea, el coordinador crea una solicitud de decisión para el responsable humano.
