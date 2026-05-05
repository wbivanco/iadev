# Project Summary

## Objetivo

Crear una arquitectura/template portable para desarrollar software con IA de forma consistente entre herramientas como VS Code, Cursor, OpenCode, Claude Code y Codex.

## Principios

- No depender de una herramienta específica
- Separar planificación de código
- Usar specs como ancla del desarrollo
- Mantener memoria persistente entre sesiones
- Integrar agentes sin perder control humano

## Estructura base

- `ai-system/`: sistema de desarrollo con IA
- `workspace/`: código real del proyecto
