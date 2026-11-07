---
name: aidev-seguridad
description: Revisa la seguridad de una aplicación IADev (control de acceso, datos de otro cliente o sucursal, inyección, XSS, archivos subidos, sesión, límites de pedidos, configuración, secretos y dependencias) con búsquedas automáticas por stack y revisión guiada, y reporta hallazgos verificados. Usar antes de abrir a producción, al cerrar tareas que tocan rutas, formularios, permisos, archivos o endpoints públicos, o cuando el usuario pida una revisión de seguridad.
---

# Seguridad IADev

Objetivo: encontrar fallas reales y demostrables, no una lista de buenas
prácticas. Cada hallazgo tiene evidencia, gravedad y arreglo propuesto.

## 0. Contexto

1. Resolvé raíz y `code_root` como indica `aidev-coordinator`.
2. Leé `ai-system/specs/seguridad.md`. Si no existe, armalo antes de revisar
   (plantilla abajo): proponé un borrador leyendo rutas, roles y modelos, y
   confirmá con el usuario lo público a propósito y las reglas de acceso.
3. Detectá el stack y leé su guía en `referencias/`:
   `artisan` + `composer.json` → `laravel.md`. Si no hay guía para el stack,
   seguí sólo con el método de abajo y decíselo al usuario; al terminar,
   proponé agregar la guía al kit.
4. Elegí el alcance: **completo** (toda la app: antes de abrir o a pedido) o
   **cambio** (sólo lo que toca la tarea: `git diff` contra la rama base).

## 1. Búsqueda automática

Si la guía del stack tiene script, corrélo (no cambia nada) y guardá su
salida para el informe. Sus líneas son pistas, no hallazgos: cada una se
confirma o se descarta en el paso 2.

## 2. Revisión guiada

Recorré en este orden, primero lo de mayor impacto:

1. **Control de acceso.** Toda ruta no pública exige sesión y permiso. Lo
   que pertenece a otro usuario, cliente, sucursal o empresa no se puede ver
   ni cambiar cambiando un id en la URL o en el formulario (IDOR). Las reglas
   salen de `seguridad.md`.
2. **Entradas.** Validación del lado del servidor; asignación masiva;
   consultas armadas con texto del usuario; salida sin escapar (XSS);
   redirecciones a URL externas; rutas de archivo con datos del usuario.
3. **Archivos subidos.** Tipo real (no sólo extensión), tamaño, nombre,
   dónde se guardan y si se pueden ejecutar o listar.
4. **Sesión y autenticación.** Cookies seguras, CSRF, límite de intentos en
   el ingreso y en formularios públicos, cambio de sesión al ingresar,
   recuperación de clave.
5. **Lógica pública.** Lo que manda el navegador no define precios, totales,
   stock ni estados. Códigos de seguimiento o enlaces no adivinables.
   Enumeración de datos (emails, pedidos).
6. **Configuración.** Modo depuración, cabeceras de seguridad, CORS, proxy
   (por ejemplo Cloudflare: IP real del cliente), errores que muestran datos.
7. **Secretos y dependencias.** Nada sensible en git ni en el historial;
   audits de dependencias; claves con el mínimo privilegio.

## 3. Verificar

Un hallazgo es **CONFIRMADO** sólo con evidencia: un test que falla, un
pedido HTTP reproducido en desarrollo o el código exacto que lo permite sin
camino que lo frene. Si falta la prueba, es **PLAUSIBLE**. No pruebes contra
producción ni contra servicios de terceros sin permiso explícito, y nunca
con datos reales que se modifiquen.

## 4. Informar

Tabla ordenada por gravedad: **crítica** (acceso o cambio de datos ajenos sin
permiso, ejecución de código), **alta**, **media**, **baja**. Por hallazgo:
dónde (`archivo:línea` o ruta), cómo se reproduce, impacto, arreglo propuesto
y estado (CONFIRMADO/PLAUSIBLE). Agregá lo revisado sin problemas, en una
línea por categoría, para que se sepa qué se cubrió.

No arregles sin aprobación. Los arreglos se planifican como tareas del
Backlog; cada uno lleva un test que reproduce la falla y pasa con el arreglo.
Registrá la fecha, el alcance y el resultado en el Historial de
`seguridad.md`. Lo que se acepta como riesgo, con su motivo.

## Plantilla de `ai-system/specs/seguridad.md`

```markdown
# Seguridad

## Público a propósito
Rutas o pantallas sin sesión y por qué (tienda, ficha pública, webhooks…).

## Reglas de acceso
Quién ve y cambia qué: roles, y separación por cliente/sucursal/empresa.

## Datos sensibles
Claves, certificados, datos personales o bancarios, y dónde se guardan.

## Integraciones
Servicios externos y cómo se autentican.

## Riesgos aceptados
Qué se decidió no corregir, con fecha y motivo.

## Historial
- AAAA-MM-DD: revisión (completa/cambio), resultado.
```
