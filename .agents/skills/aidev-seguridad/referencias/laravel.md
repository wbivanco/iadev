# Laravel

Script: `scripts/laravel.sh <code_root> [url]` (desde la carpeta de la skill o
con su ruta completa). Con `url` (por ejemplo `http://localhost:8000`) revisa
además cabeceras y cookies de una respuesta real. No cambia nada.

## Dónde mirar, por categoría

1. **Control de acceso**
   - `php artisan route:list --json`: rutas sin `auth` que no figuran como
     públicas en `seguridad.md`; rutas con `auth` sin `can:` (confirmar que
     el controlador autoriza con `authorize`, `Gate` o Policy).
   - IDOR: con route model binding (`{venta}`), comprobar que el controlador
     o la consulta filtra por el dueño (usuario, sucursal, empresa). Buscar
     `findOrFail($request->...)` y `whereKey` sin ese filtro.
   - Probarlo con un test de Pest/PHPUnit: dos usuarios de distinto dueño;
     el segundo pide el recurso del primero y debe recibir 403 o 404.
2. **Entradas**
   - Asignación masiva: `$guarded = []`, `forceFill`, `create($request->all())`
     o `->update($request->all())` en lugar de `validated()`.
   - SQL: `DB::raw`, `whereRaw`, `selectRaw`, `orderByRaw`, `havingRaw`,
     `DB::select/statement` con variables concatenadas.
   - XSS: `{!! !!}` en Blade, `v-html`, `innerHTML` con datos del usuario.
   - Redirecciones: `redirect($request->...)`, `redirect()->to(` con datos
     del usuario; preferir `intended()` o rutas con nombre.
   - Procesos: `exec`, `shell_exec`, `system`, `Process::run` con string
     armado; `unserialize`, `eval`.
3. **Archivos**: reglas `file|mimes|mimetypes|max` en los Form Requests;
   `store()` con nombre generado; nada subido bajo `public/` ejecutable;
   descargas con ruta armada desde la petición (`Storage::get($request->…)`).
4. **Sesión y autenticación**: `config/session.php` (`secure` en producción,
   `http_only`, `same_site`); excepciones de CSRF
   (`validateCsrfTokens(except:)` en `bootstrap/app.php`); `throttle` o
   `RateLimiter` en login, recuperación de clave y formularios públicos;
   `session()->regenerate()` al ingresar.
5. **Lógica pública**: controladores de la tienda o la API pública
   recalculan precio, total y stock en el servidor; códigos de seguimiento
   con `Str::random` largo y comparación junto con otro dato (email).
6. **Configuración**: `APP_DEBUG=false` en producción; cabeceras
   (`X-Frame-Options` o CSP `frame-ancestors`, `X-Content-Type-Options`,
   `Referrer-Policy`, HSTS detrás de HTTPS); detrás de Cloudflare o un proxy,
   `trustProxies` para la IP real (si no, el límite de intentos es por IP del
   proxy); CORS en `config/cors.php`.
7. **Secretos y dependencias**: `composer audit`, `npm audit`; `.env`,
   volcados, `.pem` o `.key` en el historial de git; `APP_KEY` usada para
   cifrar datos guardados (rotarla los vuelve ilegibles).
