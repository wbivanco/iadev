---
name: aidev-despliegue
description: Verifica que un equipo o servidor de un proyecto IADev esté listo según su guía de despliegue, con el script de chequeo del proyecto (OK, AVISO, ERROR), explica cómo resolver cada problema y ayuda a crear o mantener la guía y el chequeo. Usar antes de abrir producción, después de actualizar un servidor o cambiar el .env o la infraestructura, al preparar el primer despliegue, o cuando una tarea agrega un paso de despliegue.
---

# Despliegue IADev

Objetivo: saber en un minuto si un equipo está como dice la guía, sin
recorrerla a mano. El chequeo **no cambia nada**: sólo informa.

## 0. Contexto

1. Resolvé raíz y `code_root` como indica `aidev-coordinator`.
2. Ubicá en el proyecto la **guía** (por defecto `docs/despliegue.md`) y el
   **chequeo** (por defecto `scripts/chequeo-despliegue.sh`). Si el Perfil
   Tecnológico declara otras rutas, ganan esas.
3. Los dos viven en el proyecto, no en el kit: el chequeo tiene que poder
   correr en el servidor, donde el kit no está.

## 1. Si el proyecto todavía no tiene chequeo

1. Si falta la guía, armala con el usuario: versión del lenguaje, cómo se
   actualiza el código, servicios, variables del `.env` de producción,
   tareas programadas, usuarios y permisos, respaldos y una lista de
   pendientes operativos.
2. Copiá `plantillas/chequeo-despliegue.sh` al proyecto y completá un grupo
   por paso de la guía. Tomá los controles típicos del stack de
   `referencias/` (por ejemplo `laravel.md`).
3. Corrélo en desarrollo: los AVISO esperables ahí (depuración, sin cron) no
   son errores; en producción sí.

## 2. Correr

```bash
./scripts/chequeo-despliegue.sh              # rápido
./scripts/chequeo-despliegue.sh --completo   # además, pruebas lentas
```

`--completo` (si el chequeo lo tiene) prueba la restauración del último
respaldo y los audits. Usalo antes de abrir y después de una actualización
grande. Sale con código 1 si hay algún ERROR.

## 3. Interpretar e informar

- **ERROR**: algo que en ese entorno está mal o impide operar.
- **AVISO**: normal en desarrollo o una decisión pendiente; en producción
  hay que resolverlo o confirmar que es a propósito.

Resumile al usuario el resultado, las líneas de ERROR textuales con el paso
de la guía y el comando que lo resuelve, y qué AVISO son esperables. Sumá lo
que el script no puede ver y está en la guía (por ejemplo, claves guardadas
fuera del servidor o un destino externo de respaldos).

**No corrijas nada sin preguntar**: el chequeo puede correr en un servidor
real. Migrar, rotar claves o restaurar necesitan el ok del usuario.

## 4. Mantener

Cuando una tarea agrega un paso a la guía (una variable obligatoria, un
servicio, una tarea programada, un usuario), agregá su comprobación al
chequeo en el mismo commit, en el grupo del paso. Cada comprobación usa
`ok`, `aviso` o `error`, y no escribe nada.
