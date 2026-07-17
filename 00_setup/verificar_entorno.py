"""
Verificador del entorno — Finance Analytics España (Fase 0.5).

Corre los 8 chequeos de la plantilla (§3.4) y responde sin ambigüedad si se
puede avanzar a la Fase 1. Cada chequeo imprime una fila; si alguno falla,
el script termina con código de salida 1.

Uso:  python 00_setup/verificar_entorno.py
"""

import importlib
import os
import subprocess
import sys
from pathlib import Path

# La raíz del proyecto es el padre de 00_setup/, sin importar desde dónde se corra
RAIZ = Path(__file__).resolve().parent.parent

# API aprobada en FICHA.md §2.1: Euríbor 12M mensual del BCE
API_URL = (
    "https://data-api.ecb.europa.eu/service/data/"
    "FM/M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA"
    "?format=jsondata&startPeriod=2024-01"
)

# Los imports se prueban por su nombre de módulo, que no siempre coincide
# con el nombre del paquete en requirements.txt
LIBRERIAS = {
    "pandas": "pandas",
    "numpy": "numpy",
    "faker": "faker",
    "requests": "requests",
    "python-dotenv": "dotenv",
    "sqlalchemy": "sqlalchemy",
    "psycopg2-binary": "psycopg2",
    "jupyter": "jupyter_core",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "scipy": "scipy",
    "scikit-learn": "sklearn",
    "statsmodels": "statsmodels",
    "prophet": "prophet",
}

resultados = []  # (ok: bool, etiqueta: str, detalle: str)


def chequeo(etiqueta):
    """Decorador: registra el resultado del chequeo en vez de cortar el script."""
    def envoltura(funcion):
        def ejecutar():
            try:
                detalle = funcion()
                resultados.append((True, etiqueta, detalle))
            except Exception as error:
                resultados.append((False, etiqueta, str(error)))
        return ejecutar
    return envoltura


@chequeo("Versión de Python")
def check_python():
    if sys.version_info < (3, 11):
        raise RuntimeError(f"se necesita 3.11+, hay {sys.version.split()[0]}")
    return f"Python {sys.version.split()[0]}"


@chequeo("Entorno virtual")
def check_venv():
    if sys.prefix == sys.base_prefix:
        raise RuntimeError("no está activo — correr .venv\\Scripts\\Activate.ps1")
    return f"activo ({Path(sys.prefix).name})"


@chequeo("Librerías de requirements.txt")
def check_librerias():
    faltantes = [paquete for paquete, modulo in LIBRERIAS.items()
                 if importlib.util.find_spec(modulo) is None]
    if faltantes:
        raise RuntimeError(f"faltan: {', '.join(faltantes)} — pip install -r requirements.txt")
    return f"{len(LIBRERIAS)}/{len(LIBRERIAS)} instaladas"


@chequeo(".env completo")
def check_env():
    ejemplo, real = RAIZ / ".env.example", RAIZ / ".env"
    if not real.exists():
        raise RuntimeError("no existe .env — copiar .env.example y completarlo")

    def claves(ruta):
        return {linea.split("=")[0].strip() for linea in ruta.read_text(encoding="utf-8").splitlines()
                if "=" in linea and not linea.lstrip().startswith("#")}

    faltantes = claves(ejemplo) - claves(real)
    if faltantes:
        raise RuntimeError(f"faltan claves: {', '.join(sorted(faltantes))}")
    return f"{len(claves(ejemplo))} claves presentes"


def conexion_postgres():
    """Conexión con los datos del .env. Falla con mensaje claro si no hay servidor."""
    import psycopg2
    from dotenv import load_dotenv
    load_dotenv(RAIZ / ".env")
    return psycopg2.connect(
        host=os.environ["DB_HOST"], port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"], user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"], connect_timeout=5,
    )


@chequeo("Conexión a PostgreSQL")
def check_postgres():
    with conexion_postgres() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
    return version.split(",")[0]  # "PostgreSQL 16.x ..." sin el detalle del compilador


@chequeo("Permisos de escritura en la base")
def check_escritura():
    with conexion_postgres() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute("CREATE TEMP TABLE _chequeo_entorno (id int);")
            cursor.execute("DROP TABLE _chequeo_entorno;")
    return "crear y borrar tabla OK"


@chequeo("API externa (BCE — Euríbor 12M)")
def check_api():
    import requests
    respuesta = requests.get(API_URL, timeout=30)
    respuesta.raise_for_status()
    series = respuesta.json()["dataSets"][0]["series"]
    observaciones = next(iter(series.values()))["observations"]
    if not observaciones:
        raise RuntimeError("la API respondió pero sin observaciones en el rango")
    return f"status 200, {len(observaciones)} observaciones desde 2024-01"


@chequeo("Git configurado")
def check_git():
    valores = []
    for clave in ("user.name", "user.email"):
        salida = subprocess.run(["git", "config", "--get", clave],
                                capture_output=True, text=True)
        if salida.returncode != 0 or not salida.stdout.strip():
            raise RuntimeError(f'falta {clave} — git config --global {clave} "..."')
        valores.append(salida.stdout.strip())
    return f"{valores[0]} <{valores[1]}>"


if __name__ == "__main__":
    # La consola de Windows a veces arranca en cp1252 y rompe los ✅
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    for correr in (check_python, check_venv, check_librerias, check_env,
                   check_postgres, check_escritura, check_api, check_git):
        correr()

    print()
    for ok, etiqueta, detalle in resultados:
        print(f"  {'✅' if ok else '❌'} {etiqueta:<35} {detalle}")
    print()

    if all(ok for ok, _, _ in resultados):
        print("→ ENTORNO LISTO. Podés avanzar a la Fase 1.")
    else:
        fallidos = sum(1 for ok, _, _ in resultados if not ok)
        print(f"→ {fallidos} chequeo(s) en rojo. Resolver antes de avanzar.")
        sys.exit(1)
