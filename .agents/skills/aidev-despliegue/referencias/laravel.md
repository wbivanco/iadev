# Laravel

Controles habituales para el chequeo de un proyecto Laravel. Ejemplo completo
y probado: `scripts/chequeo-despliegue.sh` de Podio.

- **PHP**: versión mínima de la guía (`php -r 'echo PHP_VERSION;'` y
  `version_compare`); PHP-FPM puede tener otra versión que la consola.
- **Configuración efectiva**: una sola llamada a
  `php artisan tinker --execute='echo json_encode([...]);'` con
  `app()->environment()`, `config("app.debug")`, `config("app.url")`,
  `config("app.timezone")` y `app()->configurationIsCached()`. En producción:
  `APP_DEBUG=false` (ERROR), `APP_URL` sin localhost (ERROR), configuración
  cacheada con `php artisan optimize` (AVISO).
- **Servicios**: un comando propio que pruebe base y almacenamiento sin
  escribir (por ejemplo `system:check`) y convertir su salida en OK/ERROR.
- **Migraciones**: `php artisan migrate:status | grep -c Pending` en 0.
- **Assets**: `public/build/manifest.json` (Vite) presente.
- **Permisos**: `storage/` y `bootstrap/cache/` con escritura.
- **Planificador**: `php artisan schedule:list` contiene las tareas
  esperadas y hay cron con `schedule:run`. Si hay colas, un worker activo
  (`supervisorctl status` o `systemctl`).
- **Usuarios con privilegios mínimos**: la base no se usa con superusuario
  (`SELECT rolsuper FROM pg_roles WHERE rolname = current_user` en
  PostgreSQL); las claves del almacenamiento no son las maestras.
- **Respaldos** (`--completo`): restaurar el último en una base aparte,
  comparar tablas y borrarla.
- **Dependencias** (`--completo`): `composer audit` y `npm audit --omit=dev`.
