# Laravel

Plantilla: `--iniciar laravel` (grupos `php` en `app/`, `blade` en
`resources/views`, `js_css` en `resources/js` y `resources/css`).

## Qué mide además de la duplicación

- **Clases sin uso** en `app/` que nadie nombra. Quedan afuera controladores,
  comandos, Form Requests, middleware y providers, que se cargan por
  convención.
- **Vistas sin uso**: vistas no nombradas desde `app/`, rutas u otras vistas;
  componentes `<x-…>` no usados.
- **Variables sin uso** de `.env.example` que nada lee. Las que lee Laravel por
  su cuenta van en `laravel.env_del_framework`; carpetas extra donde se leen
  (por ejemplo un `docker/` al lado del código) en `laravel.env_otras_carpetas`.
- **Deprecadas**: patrones de `deprecadas` (por ejemplo `dd(`, `dump(`,
  `imagedestroy(`), en las carpetas de `deprecadas_carpetas`.

## Chequeos habituales del Perfil

```bash
php artisan test --compact --parallel
vendor/bin/pint --test
vendor/bin/phpstan analyse
composer audit
```

Si las vistas fallan después de quitar paquetes: `php artisan view:clear`.

## Formas de reutilizar en Laravel

- Lógica repetida de controladores: trait en `Http/Controllers/Concerns`.
- Reglas repetidas: el Request de edición hereda del de alta; trait en
  `Http/Requests/Concerns` para lo que cambia (por ejemplo el `unique` que
  ignora el id en edición).
- Consultas y cálculos: clases en `app/Support` o `app/Actions`, o métodos en
  el modelo o el enum dueño del dato.
- Vistas: componentes Blade (`resources/views/components`) con props y slots;
  layouts para estructuras de página repetidas.
- Permisos: un helper que registra los Gates de una sección en vez de uno por
  línea.
