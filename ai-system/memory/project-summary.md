# Project Summary

## Objetivo

Crear un asistente portable de desarrollo con IA que ayude a crear software de
cualquier tipo a partir de una especificacion.

El asistente debe manejar memoria, contexto, skills y agentes cuando sean
necesarios para convertir una especificacion en plan, implementacion,
validacion y cierre.

## Enfoque

El repositorio no esta centrado en construir una aplicacion especifica dentro
de `workspace/`. El producto principal es `ai-system/`, que actua como sistema
operativo reusable para guiar a agentes de IA en la construccion de software.

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
