# AI Development System v1.0

## Estado

Completado

## Contexto

El repositorio ya define una memoria, un flujo SDD y reglas mínimas, pero no
puede adoptarse de forma autosuficiente: faltan convenciones de ciclo de vida,
guía de inicio, skills, roles y evidencia completa de uso.

## Problema

Una persona o agente que copie `ai-system/` debe inferir qué personalizar,
dónde crear documentos, cómo transferir trabajo y cómo verificar que la base
quedó lista.

## Objetivo

Entregar una v1.0 portable, independiente de herramientas, que permita
inicializar y gobernar trabajo asistido por IA desde una idea hasta el cierre.

## Alcance

- Convenciones para specs, diseños, tareas, QA, cierres y archivo.
- Guía de adopción y checklist de portabilidad.
- Templates de design y skill.
- Cuatro skills genéricos y cuatro roles de agentes con handoffs mínimos.
- Dos escenarios ficticios de referencia de punta a punta.
- Versionado y documentación del alcance de v1.

## Fuera de alcance

- Implementar una aplicación en `workspace/`.
- Automatizar la orquestación, integrar IDEs o MCPs.
- Ejecutar agentes de manera autónoma o imponer tecnologías.

## Criterios de éxito

- Se puede copiar `ai-system/` e inicializarlo siguiendo una guía única.
- Cada tipo de documento tiene ubicación, template y estado definido.
- Un agente puede asumir un rol, seleccionar un skill y producir un handoff
  verificable.
- Los escenarios permiten entender el flujo sin un proyecto real.
- La checklist permite verificar manualmente la integridad del paquete.
