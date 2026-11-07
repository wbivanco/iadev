---
name: aidev-deuda-tecnica
description: Mide la deuda técnica de un proyecto IADev (código duplicado, clases, vistas y variables sin uso, funciones deprecadas) contra una línea base, y guía qué reutilizar o unificar para que ninguna tarea la aumente. Usar antes de cerrar una tarea de código, cuando el usuario pida revisar deuda técnica, optimización o código duplicado, o al planificar un refactor.
---

# Deuda técnica IADev

Objetivo: que ninguna tarea deje deuda nueva y que la existente baje. La
medición es automática; decidir qué unificar no lo es.

## 0. Contexto

1. Resolvé la raíz (la carpeta con `ai-system/`) y `code_root` como indica
   `aidev-coordinator`.
2. Leé `ai-system/specs/deuda-tecnica.md` si existe: mapa de piezas para
   reutilizar y duplicaciones que se decidió dejar.
3. La configuración y la base están en `ai-system/specs/deuda-tecnica.json`.
   Si no existe, creala y mostrale al usuario las carpetas elegidas:

   ```bash
   python3 <skill>/scripts/deuda-tecnica.py <raiz> --iniciar laravel   # o generico
   python3 <skill>/scripts/deuda-tecnica.py <raiz> --actualizar-base
   ```

   `<skill>` es la carpeta de este archivo. Si el stack no tiene plantilla,
   usá `generico` y ajustá carpetas y extensiones; al terminar, proponé
   agregar el stack al kit (plantilla y controles de "sin uso").

## 1. Medir

```bash
python3 <skill>/scripts/deuda-tecnica.py <raiz> --detalle
```

Cuenta bloques de 8 líneas iguales por grupo (por ejemplo PHP, vistas,
JS/CSS), elementos sin uso según el stack y patrones deprecados o de
depuración. Sale con código 1 si algo empeoró respecto de la base. Además,
corré los chequeos del Perfil Tecnológico (tests, lint, análisis estático,
audit de dependencias); los tests tienen que pasar también en paralelo si el
stack lo permite. Guía por stack en `referencias/`.

## 2. Interpretar

- **Si la tarea empeoró la medición**, no se cierra: primero se reutiliza lo
  que ya existe (mapa de `deuda-tecnica.md`) y después se escribe código nuevo.
- **Unificar sólo la misma regla de negocio.** Dos bloques que hoy coinciden
  pero representan reglas que pueden cambiar por separado se dejan y se anota
  por qué en `deuda-tecnica.md`. Llegar a cero no es el objetivo.
- **Si al unificar aparece una diferencia de comportamiento** entre copias,
  no se elige en silencio: se conserva y se pregunta al usuario cuál vale.
- Audit con avisos: proponer la actualización dentro de las versiones
  actuales; subir de versión mayor se consulta.

## 3. Informar y actualizar

Mostrá la medición antes y después, los pares más duplicados y lo que se
decidió no unificar. Si la medición **mejoró** y el usuario aprueba los
cambios, guardá la base en el mismo commit:

```bash
python3 <skill>/scripts/deuda-tecnica.py <raiz> --actualizar-base
```

Nunca actualices la base para tapar un empeoramiento. Si se crea una pieza
reutilizable nueva, sumala al mapa de `deuda-tecnica.md`.

## Plantilla de `ai-system/specs/deuda-tecnica.md`

```markdown
# Deuda técnica

## Piezas para reutilizar
Clases, componentes o helpers que hay que usar antes de escribir algo nuevo.

## Duplicación aceptada
Qué se dejó repetido a propósito y por qué.

## Historial
- AAAA-MM-DD: medición (grupos y valores), qué cambió.
```
