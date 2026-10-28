---
status: approved
updated_at: "2026-10-28"
---

# Perfil tecnológico

## Decisiones mínimas

- Lenguaje: Markdown y Mermaid. El agente usa las herramientas ya disponibles
  en el proyecto consumidor. Los skills no incorporan scripts propios ni runtimes persistentes.
- code_root: .
- Este repo es el kit. `install.sh` publica el motor en el home. `init.sh` siembra cada producto y no se copia a su repo. El código de una aplicación vive en el repo de esa aplicación.
- Framework: no aplica; los skills deben ser agnósticos del proyecto consumidor.
- Base de datos: cualquier motor. Las migraciones son la fuente prioritaria y la
  base disponible permite contrastar el esquema real.

## Arquitectura (opcional)

- Los skills residen en `.agents/skills/`; los DER y sus exportaciones residen
  en `ai-system/docs/der/`.
- SVG y PNG se generan sólo si el entorno ya cuenta con un renderizador
  disponible. No se agrega `package.json`, lockfile ni `node_modules` al repositorio.
- Ante diferencias entre migraciones y base de datos, se informa el contraste
  para decisión humana; no se modifica automáticamente ninguna fuente.

## Calidad y convenciones (opcional hasta que haya código)

- Formato: Mermaid válido, Markdown con enlaces relativos y artefactos SVG/PNG.
- Lint: validar Mermaid mediante el renderizador disponible, cuando exista, y
  comprobar los enlaces Markdown pertinentes.
- Tests: no aplican a los `SKILL.md`; la validación es revisión de instrucciones, enlaces y artefactos disponibles.
- Convenciones del proyecto: ejecutar los skills después de aceptar un cambio de
  esquema y antes de pedir el último sí para el commit local.

## Decisiones diferidas

- Los adaptadores concretos para inspeccionar cada motor de base de datos se
  agregan según los motores que use cada proyecto consumidor.
- Si no hay un renderizador disponible, el skill debe informar el límite sin
  alterar los artefactos existentes.

## Historial

- 2026-08-08: creado como esqueleto genérico para una nueva entrevista.
- 2026-08-14: se definió un renderizado efímero con Mermaid CLI vía npx, sin
  dependencias persistentes en el repositorio.
- 2026-08-14: aprobado por el usuario.
- 2026-08-18: ajustado por aprobación del usuario al enfoque liviano y portable: sin scripts propios ni dependencias persistentes; SVG/PNG sólo cuando el entorno ya puede renderizarlos.
- 2026-10-28: el usuario aprobó instalar el motor una vez por máquina y sembrar cada producto con `init.sh`. Los skills siguen sin scripts propios. Se elimina `workspace/` como carpeta de código.
