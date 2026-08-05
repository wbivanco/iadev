# Roles y handoffs v1

Los roles son responsabilidades temporales. Una misma persona o agente puede
cubrir varios roles, pero debe declarar cuál está ejerciendo en cada task.

| Rol | Entrada | Salida | Responsabilidad |
| --- | --- | --- | --- |
| Planner | Idea y memoria | Spec y task | Aclarar objetivo, alcance y éxito. |
| Implementer | Task aprobada | Cambios y evidencia | Ejecutar el trabajo dentro del alcance. |
| Reviewer | Cambios y criterios | Revisión o hallazgos | Verificar calidad, alcance y riesgos. |
| Closeout | Resultado validado | Cierre y memoria actualizada | Registrar resultado y próximos pasos. |

## Contrato de handoff

Todo traspaso se registra en `memory/agent-handoffs.md` e incluye:

- rol emisor y receptor;
- objetivo y estado actual;
- enlaces a spec, design, task y evidencia aplicable;
- decisiones, riesgos, bloqueos y próximo paso verificable.

Un receptor no inicia implementación si faltan objetivo, alcance, validación o
un bloqueo crítico sin registrar.
