#!/usr/bin/env python3
"""Mide la deuda técnica de un proyecto IADev y la compara con su línea base.

Uso:
    python3 deuda-tecnica.py <raiz>                    # mide y compara
    python3 deuda-tecnica.py <raiz> --detalle          # además, pares más duplicados
    python3 deuda-tecnica.py <raiz> --actualizar-base  # guarda la medición como base
    python3 deuda-tecnica.py <raiz> --iniciar <stack>  # crea la configuración (laravel|generico)

<raiz> es la carpeta que contiene ai-system/. La configuración y la base están en
ai-system/specs/deuda-tecnica.json. Sale con código 1 si algo empeoró: más bloques
duplicados, o elementos sin uso o deprecados nuevos.
"""

from __future__ import annotations

import collections
import json
import os
import re
import sys
from pathlib import Path

VENTANA_POR_DEFECTO = 8

TRIVIALES = {
    "{", "}", "});", "];", ")", "*/", "/**", "*", "</div>", "@endif", "@endforeach",
    "@else", "</li>", "</ul>", "</span>", "</a>", "</td>", "</tr>", "</p>", "</label>",
    "</button>", "</section>", "</form>", "</table>", "</thead>", "</tbody>", "end", "pass",
}

# Líneas que no cuentan para duplicados (imports y comentarios). Se ajustan por stack.
PREFIJOS_POR_DEFECTO = ["//", "* ", "#", "import ", "from "]

PLANTILLAS = {
    "laravel": {
        "code_root": ".",
        "stack": "laravel",
        "ignorar_prefijos": ["use ", "//", "* ", "namespace"],
        "duplicacion": {
            "php": {"carpetas": ["app"], "extensiones": [".php"]},
            "blade": {"carpetas": ["resources/views"], "extensiones": [".blade.php"]},
            "js_css": {"carpetas": ["resources/js", "resources/css"], "extensiones": [".js", ".css"]},
        },
        "deprecadas": {
            r"\bimagedestroy\(": "imagedestroy() está deprecado en PHP 8.5",
            r"\butf8_(en|de)code\(": "utf8_encode/decode están deprecados",
            r"\bdd\(|\bdump\(|\bray\(": "llamada de depuración olvidada",
        },
        "deprecadas_carpetas": ["app", "tests"],
        "laravel": {"env_otras_carpetas": [], "env_del_framework": [
            "APP_MAINTENANCE_DRIVER", "APP_MAINTENANCE_STORE", "PHP_CLI_SERVER_WORKERS",
        ]},
        "base": None,
    },
    "generico": {
        "code_root": ".",
        "stack": "generico",
        "duplicacion": {"codigo": {"carpetas": ["src"], "extensiones": [".py", ".js", ".ts"]}},
        "deprecadas": {},
        "deprecadas_carpetas": ["src"],
        "base": None,
    },
}


class Proyecto:
    def __init__(self, raiz: Path):
        self.raiz = raiz
        self.archivo = raiz / "ai-system" / "specs" / "deuda-tecnica.json"
        if not self.archivo.exists():
            sys.exit(f"No existe {self.archivo}. Crealo con: --iniciar laravel|generico")
        self.config = json.loads(self.archivo.read_text())
        self.codigo = (raiz / self.config.get("code_root", ".")).resolve()

    def archivos(self, carpeta: str, extensiones: tuple[str, ...]) -> list[Path]:
        base = (self.codigo / carpeta).resolve()
        if not base.exists():
            return []
        return sorted(
            p for p in base.rglob("*")
            if p.is_file() and p.name.endswith(extensiones)
            and not any(parte in ("vendor", "node_modules", ".git") for parte in p.parts)
        )

    def relativo(self, p: Path) -> str:
        try:
            return str(p.relative_to(self.codigo))
        except ValueError:
            return str(p)

    def texto_de(self, carpetas: list[str], extensiones=(".php", ".js", ".json", ".yml", ".yaml")) -> str:
        return "\n".join(
            r.read_text(errors="ignore") for c in carpetas for r in self.archivos(c, extensiones)
        )

    def guardar_base(self, medicion: dict) -> None:
        self.config["base"] = medicion
        self.archivo.write_text(json.dumps(self.config, indent=2, ensure_ascii=False) + "\n")


def duplicacion(proyecto: Proyecto, rutas: list[Path], ventana: int) -> tuple[int, list]:
    prefijos = tuple(proyecto.config.get("ignorar_prefijos", PREFIJOS_POR_DEFECTO))
    bloques: dict[str, list[Path]] = collections.defaultdict(list)
    for ruta in rutas:
        lineas = [re.sub(r"\s+", " ", l.strip()) for l in ruta.read_text(errors="ignore").split("\n")]
        utiles = [l for l in lineas if len(l) > 3 and l not in TRIVIALES and not l.startswith(prefijos)]
        for i in range(len(utiles) - ventana):
            bloques["\n".join(utiles[i:i + ventana])].append(ruta)

    total = 0
    pares: collections.Counter = collections.Counter()
    for rutas_bloque in bloques.values():
        total += len(rutas_bloque) - 1
        distintas = sorted({proyecto.relativo(r) for r in rutas_bloque})
        for i, a in enumerate(distintas):
            for b in distintas[i + 1:]:
                pares[(a, b)] += 1
    return total, [(n, a, b) for (a, b), n in pares.most_common(10)]


def deprecadas(proyecto: Proyecto) -> list[str]:
    patrones = proyecto.config.get("deprecadas", {})
    if not patrones:
        return []
    extensiones = tuple({e for g in proyecto.config["duplicacion"].values() for e in g["extensiones"]} | {".php"})
    hallazgos = []
    for carpeta in proyecto.config.get("deprecadas_carpetas", []):
        for ruta in proyecto.archivos(carpeta, extensiones):
            for n, linea in enumerate(ruta.read_text(errors="ignore").split("\n"), 1):
                if linea.strip().startswith(("//", "*", "#")):
                    continue
                for patron, motivo in patrones.items():
                    if re.search(patron, linea):
                        hallazgos.append(f"{proyecto.relativo(ruta)}:{n} {motivo}")
    return hallazgos


# ------------------------------------------------------------------ Laravel

def laravel_clases_sin_uso(p: Proyecto) -> list[str]:
    """Clases de app/ que nadie nombra. Controladores, comandos, requests,
    middleware y providers se cargan por convención y quedan afuera."""
    excluidas = ("Http/Controllers", "Console/Commands", "Http/Requests", "Http/Middleware", "Providers")
    fuentes = {r: r.read_text(errors="ignore") for r in p.archivos("app", (".php",))}
    resto = p.texto_de(["routes", "resources", "config", "database", "bootstrap"])
    sin_uso = []
    for ruta in fuentes:
        nombre = p.relativo(ruta)
        if any(e in nombre for e in excluidas):
            continue
        patron = re.compile(r"\b" + re.escape(ruta.stem) + r"\b")
        if patron.search(resto):
            continue
        if not any(patron.search(texto) for otra, texto in fuentes.items() if otra != ruta):
            sin_uso.append(nombre)
    return sin_uso


def laravel_vistas_sin_uso(p: Proyecto) -> list[str]:
    vistas = p.codigo / "resources" / "views"
    referencias = p.texto_de(["app", "routes"]) + "\n".join(
        r.read_text(errors="ignore") for r in p.archivos("resources/views", (".php",))
    )
    sin_uso = []
    for ruta in p.archivos("resources/views", (".blade.php",)):
        nombre = str(ruta.relative_to(vistas))[: -len(".blade.php")]
        punto = nombre.replace(os.sep, ".")
        if nombre.startswith("components" + os.sep):
            if re.search(r"<x-" + re.escape(punto[len("components."):]) + r"[\s/>]", referencias):
                continue
        elif punto in referencias or nombre.startswith("vendor"):
            continue
        sin_uso.append(nombre)
    return sin_uso


def laravel_env_sin_uso(p: Proyecto) -> list[str]:
    ejemplo = p.codigo / ".env.example"
    if not ejemplo.exists():
        return []
    opciones = p.config.get("laravel", {})
    claves = re.findall(r"^([A-Z][A-Z0-9_]*)=", ejemplo.read_text(), re.M)
    codigo = p.texto_de(["config", "app", "bootstrap", "routes", "resources", "database"])
    vite = p.codigo / "vite.config.js"
    codigo += vite.read_text(errors="ignore") if vite.exists() else ""
    codigo += p.texto_de(opciones.get("env_otras_carpetas", []))
    del_framework = set(opciones.get("env_del_framework", []))
    return [
        k for k in claves
        if k not in del_framework and not re.search(r"['\"${]" + k + r"\b|\b" + k + r"['\"}]", codigo)
    ]


SIN_USO = {
    "laravel": {
        "clases_sin_uso": laravel_clases_sin_uso,
        "vistas_sin_uso": laravel_vistas_sin_uso,
        "env_sin_uso": laravel_env_sin_uso,
    },
}

# ------------------------------------------------------------------ medición


def medir(p: Proyecto) -> tuple[dict, dict]:
    ventana = int(p.config.get("ventana", VENTANA_POR_DEFECTO))
    medicion, pares = {}, {}
    for grupo, definicion in p.config["duplicacion"].items():
        rutas = [r for c in definicion["carpetas"] for r in p.archivos(c, tuple(definicion["extensiones"]))]
        medicion[f"duplicacion_{grupo}"], pares[grupo] = duplicacion(p, rutas, ventana)
    for clave, funcion in SIN_USO.get(p.config.get("stack", ""), {}).items():
        medicion[clave] = funcion(p)
    medicion["deprecadas"] = deprecadas(p)
    return medicion, pares


def iniciar(raiz: Path, stack: str) -> int:
    destino = raiz / "ai-system" / "specs" / "deuda-tecnica.json"
    if destino.exists():
        print(f"Ya existe {destino}; no se pisa.")
        return 1
    if stack not in PLANTILLAS:
        print(f"Stack sin plantilla: {stack}. Opciones: {', '.join(PLANTILLAS)}.")
        return 1
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(PLANTILLAS[stack], indent=2, ensure_ascii=False) + "\n")
    print(f"Creada {destino}. Revisá code_root y carpetas, y corré --actualizar-base.")
    return 0


def main() -> int:
    argumentos = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not argumentos:
        print(__doc__)
        return 2
    raiz = Path(argumentos[0]).resolve()

    if "--iniciar" in sys.argv:
        return iniciar(raiz, argumentos[1] if len(argumentos) > 1 else "laravel")

    p = Proyecto(raiz)
    actual, pares = medir(p)

    if "--actualizar-base" in sys.argv:
        p.guardar_base(actual)
        print(f"Línea base guardada en {p.archivo.relative_to(raiz)}")
        return 0

    base = p.config.get("base")
    empeoro = []
    print(f"Deuda técnica de {raiz.name}")
    print("=" * 60)
    for clave, valor in actual.items():
        if isinstance(valor, int):
            antes = base.get(clave) if base else None
            marca = ""
            if antes is not None and valor > antes:
                marca, _ = f"  ← EMPEORÓ (base {antes})", empeoro.append(clave)
            elif antes is not None and valor < antes:
                marca = f"  (mejoró: base {antes}; actualizá la base)"
            print(f"{clave:22} {valor:5}{marca}")
        else:
            nuevos = sorted(set(valor) - set(base.get(clave, []) if base else []))
            print(f"{clave:22} {len(valor):5}" + (f"  ← {len(nuevos)} NUEVOS" if nuevos and base else ""))
            for item in (nuevos if base else valor):
                print(f"    - {item}")
            if nuevos and base:
                empeoro.append(clave)

    if "--detalle" in sys.argv:
        for grupo, lista in pares.items():
            if lista:
                print(f"\nPares más duplicados ({grupo}):")
                for n, a, b in lista:
                    print(f"  {n:4}  {a}  <->  {b}")

    print("=" * 60)
    if base is None:
        print("No hay línea base. Corré con --actualizar-base para crearla.")
        return 0
    if empeoro:
        print("La deuda técnica empeoró: " + ", ".join(empeoro))
        return 1
    print("Sin deuda técnica nueva respecto de la base.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
