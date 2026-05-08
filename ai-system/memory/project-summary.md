# Project Summary

## Objetivo

Crear un sistema portable de desarrollo con IA que pueda copiarse entre
proyectos y funcionar de forma consistente en distintas herramientas.

## Enfoque

El repositorio no está centrado todavía en construir una aplicación dentro de
`workspace/`. El activo principal es `ai-system/`, que actúa como plantilla
operativa reusable para memoria, planificación, reglas y agentes.

## Principios

- No depender de una herramienta específica
- Separar planificación de código
- Usar specs como ancla del desarrollo
- Mantener memoria persistente entre sesiones
- Integrar agentes sin perder control humano
- Priorizar portabilidad y claridad documental

## Estructura base

- `ai-system/`: sistema de desarrollo con IA
- `workspace/`: código real del proyecto cuando exista
