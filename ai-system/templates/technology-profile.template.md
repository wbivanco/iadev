# Technology Profile Template

> Usar este documento como checklist del contexto técnico. Las secciones
> **obligatorias** deben estar completas para aprobar el intake. Las
> **recomendadas** agregan el detalle que permite planificar y ejecutar con
> menos supuestos. Las secciones **condicionales** son obligatorias cuando se
> cumple su condición. Cuando una sección no aplique, indicarlo explícitamente
> con `No aplica` y el motivo. Nunca incluir secretos.

## Checklist de completitud

- [ ] Obligatoria: Identificación.
- [ ] Obligatoria: Stack obligatorio.
- [ ] Obligatoria: Arquitectura y convenciones.
- [ ] Obligatoria: Integraciones, credenciales y entornos.
- [ ] Obligatoria: Calidad y entrega.
- [ ] Obligatoria: Restricciones técnicas y de seguridad.
- [ ] Obligatoria: Decisiones pendientes.
- [ ] Recomendada: Roles habilitados del catálogo y responsable operativo.
- [ ] Recomendada: Modelo y configuración local de Codex.
- [ ] Recomendada: MCPs requeridos.
- [ ] Condicional: Arquitectura distribuida, si se usan microservicios o servicios independientes.

## Identificación

- Proyecto:
- Responsable humano:
- Fecha:
- Estado: Borrador | Pendiente de aprobación | Aprobado | Reemplazado

## Stack obligatorio

| Capa | Tecnología | Versión | Motivo o restricción |
| --- | --- | --- | --- |
| Frontend |  |  |  |
| Backend |  |  |  |
| Base de datos |  |  |  |
| Infraestructura |  |  |  |

## Arquitectura y convenciones

- Patrón arquitectónico:
- Estructura de repositorio:
- Convenciones de código:
- Gestión de dependencias:

## Roles habilitados del catálogo y responsable operativo — Recomendada

Elegí cuáles de los roles ya definidos en `guidance/roles.md` pueden
participar en este proyecto. No es necesario crear roles nuevos. Esta sección
documenta la configuración operativa del proyecto y actualmente no bloquea la
ejecución del runtime.

- Responsable operativo:
- Roles humanos o de agentes habilitados (del catálogo):
- Separación de responsabilidades requerida:

## Modelo y configuración local de Codex — Recomendada

- Modelo o política de selección de modelo:
- Configuración local relevante (sin rutas, variables ni secretos):
- Restricciones de uso o sandbox:

## Integraciones, credenciales y entornos

No incluir secretos. Referenciar el mecanismo seguro para configurarlos.

### MCPs requeridos

| MCP | Uso | Configuración |
| --- | --- | --- |
| open-pencil | Diseño visual de tasks UI | Instalación local del usuario; no versionar rutas ni secretos |

## Arquitectura distribuida — Condicional

Completar si se usan microservicios o servicios con despliegue independiente.

- Servicios, responsabilidad y límites:
- Propiedad de datos y consistencia entre servicios:
- Contratos de APIs o eventos, versionado y compatibilidad:
- Autenticación, autorización, observabilidad y manejo de fallas:
- Pruebas de contrato e integración:
- CI/CD y estrategia de despliegue por servicio:

## Calidad y entrega

- Comandos de instalación:
- Comandos de test:
- Linter, formateador y análisis estático:
- CI/CD:
- Estrategia de despliegue:

## Restricciones técnicas y de seguridad

## Decisiones pendientes
