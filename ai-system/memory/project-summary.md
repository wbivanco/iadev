# Project Summary

## Objetivo

Crear un asistente portable de programacion con IA que ayude a crear software
de cualquier tipo a partir de una especificacion.

El asistente debe manejar memoria, contexto, skills y agentes cuando sean
necesarios para convertir una especificacion en plan, implementacion,
validacion y cierre.

## Enfoque

El repositorio no esta centrado en construir una aplicacion especifica dentro
de `workspace/`. El producto principal es `ai-system/`, y el objetivo del
proyecto es desarrollar todo lo que vive dentro de esa carpeta.

`workspace/` es solo el destino donde iria el codigo del proyecto que el
asistente ayude a crear, modificar o mantener. Ese codigo no es el foco de este
repositorio salvo cuando se use como caso de prueba para validar el sistema.

## Principios

- No depender de una herramienta específica
- Separar planificación de código
- Usar specs como ancla del desarrollo
- Mantener memoria persistente entre sesiones
- Integrar agentes sin perder control humano
- Priorizar portabilidad y claridad documental

## Estructura base

- `ai-system/`: asistente de programacion con IA y sistema operativo reusable
- `workspace/`: codigo real del proyecto concreto cuando exista
