#!/usr/bin/env bash
#
# Verifica que un equipo o servidor esté listo según docs/despliegue.md.
# No cambia nada: sólo informa. Cada línea es OK, AVISO o ERROR.
# Plantilla de la skill aidev-despliegue: un grupo por paso de la guía.
#
# Uso (desde la raíz del repositorio):
#   ./scripts/chequeo-despliegue.sh              # chequeo rápido
#   ./scripts/chequeo-despliegue.sh --completo   # además, pruebas lentas
#
# Sale con código 1 si hay algún ERROR. Los AVISO no cortan.

set -uo pipefail

raiz="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
app="$raiz"                      # carpeta del código (code_root)
env_file="$app/.env"
completo="no"
[[ "${1:-}" == "--completo" ]] && completo="si"

errores=0
avisos=0

ok() { printf '  OK     %s\n' "$1"; }
aviso() { printf '  AVISO  %s\n' "$1"; avisos=$((avisos + 1)); }
error() { printf '  ERROR  %s\n' "$1"; errores=$((errores + 1)); }
titulo() { printf '\n%s\n' "$1"; }

leer_env() {
    grep -E "^$1=" "$env_file" 2>/dev/null | tail -1 | cut -d= -f2- | sed -e 's/^"//' -e 's/"$//'
}

# Producción: algunos AVISO pasan a ERROR.
produccion="no"
[[ "$(leer_env APP_ENV)" == "production" ]] && produccion="si"
segun_entorno() { [[ "$produccion" == "si" ]] && error "$1" || aviso "$1"; }

# ---------------------------------------------------------------- paso 0
titulo "Versión del lenguaje (paso 0)"
# Ejemplo: comparar la versión instalada con la mínima de la guía.

# ---------------------------------------------------------------- paso 1
titulo ".env y configuración (paso 1)"
[[ -f "$env_file" ]] && ok ".env presente." || { error "Falta el .env."; exit 1; }
permisos="$(stat -f '%Lp' "$env_file" 2>/dev/null || stat -c '%a' "$env_file")"
[[ "$permisos" == "600" || "$permisos" == "400" ]] && ok "Permisos del .env: $permisos." || aviso "Permisos del .env: $permisos (chmod 600)."

# ---------------------------------------------------------------- paso 2
titulo "Servicios (paso 2)"
# Ejemplo: base de datos, almacenamiento, colas; un comando del proyecto que
# los pruebe sin escribir datos.

# ---------------------------------------------------------------- paso 3
titulo "Tareas programadas (paso 3)"
if (crontab -l 2>/dev/null; cat /etc/crontab /etc/cron.d/* 2>/dev/null) | grep -q 'COMANDO-DEL-PLANIFICADOR'; then
    ok "Hay una línea de cron del planificador."
else
    segun_entorno "No encuentro la línea de cron del planificador."
fi

# ---------------------------------------------------------------- respaldos
titulo "Respaldos"
if [[ "$completo" == "si" ]]; then
    : # Ejemplo: probar la restauración del último respaldo en una base aparte.
fi

# ---------------------------------------------------------------- resumen
printf '\nResultado: %d error(es), %d aviso(s).\n' "$errores" "$avisos"
[[ "$errores" -eq 0 ]]
