#!/usr/bin/env bash
#
# Búsqueda automática de pistas de seguridad en una app Laravel (aidev-seguridad).
# No cambia nada. Cada línea REVISAR es una pista a confirmar o descartar a mano.
#
# Uso: laravel.sh <code_root> [url]
#   code_root  carpeta con artisan
#   url        opcional: app corriendo (http://localhost:8000) para ver
#              cabeceras y cookies de una respuesta real

set -uo pipefail

raiz="${1:?Uso: laravel.sh <code_root> [url]}"
url="${2:-}"
cd "$raiz" || exit 1

if [[ ! -f artisan ]]; then
    echo "No hay artisan en $raiz: no es una app Laravel." >&2
    exit 1
fi

pistas=0
titulo() { printf '\n== %s\n' "$1"; }
ok() { printf '  OK       %s\n' "$1"; }
revisar() { printf '  REVISAR  %s\n' "$1"; pistas=$((pistas + 1)); }

# Busca un patrón (regex extendida) en las carpetas dadas y lista archivo:línea.
buscar() {
    local descripcion="$1" patron="$2"
    shift 2
    local hallado
    hallado="$(grep -rEn --include='*.php' --include='*.blade.php' --include='*.js' --include='*.vue' "$patron" "$@" 2>/dev/null | grep -v '/vendor/' | head -40)"
    if [[ -n "$hallado" ]]; then
        revisar "$descripcion:"
        printf '%s\n' "$hallado" | sed 's/^/             /' | cut -c1-200
    else
        ok "Sin $descripcion."
    fi
}

dirs_php=(app routes bootstrap config)
dirs_vistas=(resources)

# ---------------------------------------------------------------- 1. acceso
titulo "1. Control de acceso (rutas)"
rutas="$(php artisan route:list --json --except-vendor 2>/dev/null)"
if [[ -z "$rutas" ]]; then
    revisar "No se pudo leer php artisan route:list."
else
    printf '%s' "$rutas" | php -r '
        $rutas = json_decode(stream_get_contents(STDIN), true) ?? [];
        $tiene = function (array $mw, array $prefijos): bool {
            foreach ($mw as $m) {
                foreach ($prefijos as $p) {
                    if ($m === $p || str_starts_with($m, $p.":") || str_contains($m, $p === "auth" ? "Authenticate" : "ThrottleRequests")) {
                        return true;
                    }
                }
            }
            return false;
        };
        $publicas = $sinPermiso = $sinLimite = [];
        foreach ($rutas as $r) {
            $mw = (array) $r["middleware"];
            $linea = str_pad($r["method"], 10)." /".ltrim($r["uri"], "/")."  (".($r["name"] ?? "sin nombre").")";
            $escribe = (bool) preg_match("/POST|PUT|PATCH|DELETE/", $r["method"]);
            if (! $tiene($mw, ["auth"])) {
                $publicas[] = $linea;
                if ($escribe && ! $tiene($mw, ["throttle"])) {
                    $sinLimite[] = $linea;
                }
            } elseif (! preg_grep("/^can:/", $mw)) {
                $sinPermiso[] = $linea;
            }
        }
        $imprimir = function (string $titulo, array $lista, string $siVacia) {
            if ($lista === []) { echo "  OK       $siVacia\n"; return 0; }
            echo "  REVISAR  $titulo (".count($lista)."):\n";
            foreach ($lista as $l) { echo "             $l\n"; }
            return 1;
        };
        $n = $imprimir("Rutas sin sesión: confirmar que cada una es pública a propósito (seguridad.md)", $publicas, "Todas las rutas exigen sesión.");
        $n += $imprimir("Rutas públicas que escriben sin límite de pedidos (throttle)", $sinLimite, "Las rutas públicas que escriben tienen límite de pedidos.");
        $n += $imprimir("Rutas con sesión sin can: en la ruta: confirmar que el controlador autoriza", $sinPermiso, "Todas las rutas con sesión tienen can: en la ruta.");
        exit($n);
    '
    pistas=$((pistas + $?))
fi

# ---------------------------------------------------------------- 2. entradas
titulo "2. Entradas"
buscar "asignación masiva abierta (\$guarded = [])" '\$guarded\s*=\s*\[\s*\]' app
buscar "create/update/fill con \$request->all()" '(create|update|fill|forceFill)\(\s*\$request->(all|input)\(\)' app
buscar "SQL crudo (revisar si lleva datos del usuario)" '(DB::raw|whereRaw|selectRaw|orderByRaw|havingRaw|groupByRaw|DB::(select|statement|unprepared))\(' "${dirs_php[@]}"
buscar "salida sin escapar ({!! !!}, v-html, innerHTML con contenido)" "\{!!|v-html|\.innerHTML\s*=\s*[^'\" ]|\.innerHTML\s*=\s*['\"][^'\"]" "${dirs_vistas[@]}"
buscar "redirección con datos de la petición" 'redirect(\(\)->away|\(\)->to)?\(\s*\$request' app
buscar "ejecución de comandos o código" '\b(exec|shell_exec|system|passthru|proc_open|popen|eval|unserialize)\(' app

# ---------------------------------------------------------------- 3. archivos
titulo "3. Archivos"
buscar "lectura o descarga con ruta tomada de la petición" '(Storage::[a-z]+\(\)?->?(get|download|response|readStream)|response\(\)->(download|file))\(\s*\$request' app
sin_max=""
while IFS= read -r archivo; do
    grep -Eq "max:|->max\(|::max\(" "$archivo" || sin_max+="$archivo"$'\n'
done < <(grep -rlE "'(file|image)'|mimes:|mimetypes:|File::" app/Http 2>/dev/null | grep -i request)
if [[ -n "$sin_max" ]]; then
    revisar "Form Requests con reglas de archivo y sin tamaño máximo (max: o ->max()):"
    printf '%s' "$sin_max" | sed 's/^/             /'
else
    ok "Los Form Requests con archivos fijan un tamaño máximo (confirmar el tipo real: mimetypes)."
fi
if find public -type f \( -name '*.php' ! -name 'index.php' \) 2>/dev/null | grep -q .; then
    revisar "Hay archivos .php en public/ además de index.php: $(find public -type f -name '*.php' ! -name 'index.php' | head -5 | tr '\n' ' ')"
else
    ok "Sin .php ejecutables en public/ (salvo index.php)."
fi

# ---------------------------------------------------------------- 4. sesión
titulo "4. Sesión, CSRF y configuración"
# Una línea por control: estado|mensaje (estado 1 = OK, 0 = revisar).
while IFS='|' read -r estado mensaje; do
    [[ -z "$mensaje" ]] && continue
    [[ "$estado" == "1" ]] && ok "$mensaje" || revisar "$mensaje"
done < <(php artisan tinker --execute='
$s = config("session");
$sameSite = strtolower((string) ($s["same_site"] ?? ""));
$controles = [
    [(bool) ($s["http_only"] ?? false), "session.http_only activo.", "session.http_only está apagado."],
    [in_array($sameSite, ["lax", "strict"], true), "session.same_site=$sameSite.", "session.same_site=\"$sameSite\" (usar lax o strict)."],
    [(bool) ($s["secure"] ?? false), "session.secure activo.", "session.secure apagado: en producción con HTTPS tiene que estar activo (SESSION_SECURE_COOKIE=true)."],
    [! config("app.debug"), "APP_DEBUG=false.", "APP_DEBUG=true (en producción tiene que ser false)."],
    [! (config("cors.allowed_origins") === ["*"] && config("cors.supports_credentials")), "CORS sin origen * con credenciales.", "CORS abierto a cualquier origen con credenciales."],
];
foreach ($controles as [$bien, $si, $no]) { echo ($bien ? "1|$si" : "0|$no"), PHP_EOL; }
' 2>/dev/null)

excepciones="$(grep -rEn 'validateCsrfTokens\(|VerifyCsrfToken|\$except\s*=' bootstrap app/Http 2>/dev/null | head)"
[[ -n "$excepciones" ]] && { revisar "Excepciones de CSRF (confirmar que cada ruta exceptuada se autentica de otra forma):"; printf '%s\n' "$excepciones" | sed 's/^/             /'; } || ok "Sin excepciones de CSRF."

grep -rEq 'trustProxies|TrustProxies' bootstrap app 2>/dev/null \
    && ok "Hay configuración de proxies de confianza (verificar que incluya el proxy real, por ejemplo Cloudflare)." \
    || revisar "Sin trustProxies: detrás de Cloudflare o un proxy, la IP del cliente (y el límite de intentos) sería la del proxy."

grep -rEq 'regenerate\(\)' app 2>/dev/null && ok "Se regenera la sesión en algún punto (confirmar que sea al ingresar)." || revisar "No se encontró session()->regenerate(): confirmar que el ingreso cambia la sesión."

# ---------------------------------------------------------------- 5. cabeceras
if [[ -n "$url" ]]; then
    titulo "5. Cabeceras y cookies de $url"
    cabeceras="$(curl -sS -D - -o /dev/null --max-time 10 "$url" 2>/dev/null | tr -d '\r')"
    if [[ -z "$cabeceras" ]]; then
        revisar "No respondió $url."
    else
        for h in 'x-frame-options|content-security-policy:.*frame-ancestors' 'x-content-type-options' 'referrer-policy' 'strict-transport-security'; do
            grep -Eqi "^($h)" <<<"$cabeceras" && ok "Cabecera presente: ${h%%|*}." || revisar "Falta la cabecera ${h%%|*}$([[ $h == strict* ]] && echo ' (sólo aplica con HTTPS)')."
        done
        grep -Ei '^x-powered-by|^server:.*[0-9]' <<<"$cabeceras" | sed 's/^/  REVISAR  Expone versión: /' && pistas=$((pistas + 1))
        while IFS= read -r c; do
            nombre="$(sed -E 's/^set-cookie: ([^=]+)=.*/\1/I' <<<"$c")"
            faltan=""
            grep -qi 'httponly' <<<"$c" || [[ "$nombre" == XSRF-TOKEN ]] || faltan+=" HttpOnly"
            grep -qi 'samesite' <<<"$c" || faltan+=" SameSite"
            grep -qi 'secure' <<<"$c" || faltan+=" Secure"
            [[ -z "$faltan" ]] && ok "Cookie $nombre con sus atributos." || revisar "Cookie $nombre sin:$faltan."
        done < <(grep -i '^set-cookie:' <<<"$cabeceras")
    fi
fi

# ---------------------------------------------------------------- 6. secretos
titulo "6. Secretos y dependencias"
sensibles="$(git log --all --name-only --format= 2>/dev/null \
    | grep -Ei '(^|/)\.env$|\.env\.(prod|production|backup)$|\.(pem|key|p12|pfx|dump|sql|bak)$|(^|/)[^/]*backup[^/]*$' \
    | grep -Evi '\.(sh|php|py|js|ts|md|json|ya?ml|blade\.php)$' | sort -u | head -20)"
[[ -n "$sensibles" ]] && { revisar "Archivos sensibles en el historial de git (aunque ya no estén):"; printf '%s\n' "$sensibles" | sed 's/^/             /'; } || ok "Sin .env, claves ni volcados en el historial de git."

if command -v composer >/dev/null; then
    composer audit --no-interaction >/dev/null 2>&1 && ok "composer audit sin avisos." || revisar "composer audit con avisos (o sin conexión): composer audit."
fi
if [[ -f package.json ]] && command -v npm >/dev/null; then
    npm audit --omit=dev >/dev/null 2>&1 && ok "npm audit sin avisos." || revisar "npm audit con avisos (o sin conexión): npm audit."
fi

printf '\nPistas para revisar: %d. Ninguna es un hallazgo hasta confirmarla (paso 3 de la skill).\n' "$pistas"
