"""
Extractor de contexto macroeconómico — Finance Analytics España (Fase 1, Paso 2).

Trae las 4 fuentes externas reales aprobadas en FICHA.md §2.1: Euríbor 12M
(BCE), IPC (INE), EUR/USD (Frankfurter) y feriados (Nager.Date). A diferencia
del generador —que solo pescaba los números para inyectar correlaciones—,
este es el extractor oficial: reintentos, logging y validación. Su salida es
la que carga load_to_postgres.py en dim_contexto_macro.

Uso:  python 01_etl/extract_contexto_macro.py
"""

import datetime as dt
import sys
import time
from datetime import date
from pathlib import Path

import pandas as pd
import requests
import truststore

truststore.inject_into_ssl()  # esta máquina intercepta TLS: ver SETUP.md

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data" / "raw"
LOGS = RAIZ / "logs"

DESDE = "2023-01"              # margen de 1 año antes del negocio (FICHA.md: 2024-01)
FECHA_FIN = date(2026, 6, 30)  # debe coincidir con generate_facturas_data.py

# Rangos plausibles para la validación final (regla de calidad transversal #4)
RANGOS_VALIDOS = {
    "euribor_12m": (-1.0, 10.0),
    "ipc_var_anual": (-5.0, 15.0),
    "eur_usd": (0.5, 2.0),
}

incidencias = []  # se acumulan durante la corrida y van al log


def get_con_reintentos(url, intentos=3, espera_base=2):
    ultimo_error = None
    for intento in range(1, intentos + 1):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            return r
        except requests.RequestException as error:
            ultimo_error = error
            incidencias.append(f"Intento {intento}/{intentos} falló para {url}: {error}")
            if intento < intentos:
                time.sleep(espera_base * intento)
    raise ultimo_error


def fetch_euribor(desde=DESDE):
    url = ("https://data-api.ecb.europa.eu/service/data/FM/M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA"
           f"?format=jsondata&startPeriod={desde}")
    datos = get_con_reintentos(url).json()
    serie = next(iter(datos["dataSets"][0]["series"].values()))["observations"]
    periodos = datos["structure"]["dimensions"]["observation"][0]["values"]
    filas = [(pd.Period(periodos[int(i)]["id"], "M").to_timestamp(), v[0])
             for i, v in serie.items()]
    if not filas:
        raise ValueError("BCE respondió sin observaciones de Euríbor")
    return pd.DataFrame(filas, columns=["mes", "euribor_12m"]).sort_values("mes")


def fetch_ipc(n_ultimos=60):
    url = f"https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/IPC251856?nult={n_ultimos}"
    datos = get_con_reintentos(url).json()["Data"]
    if not datos:
        raise ValueError("INE respondió sin observaciones de IPC")
    # "Fecha" viene en epoch ms, ambiguo por huso horario; Anyo + FK_Periodo
    # (mes 1-12) identifican el período sin ambigüedad — la misma trampa
    # documentada en FICHA.md §2.1.
    filas = [(pd.Timestamp(d["Anyo"], d["FK_Periodo"], 1), d["Valor"]) for d in datos]
    return pd.DataFrame(filas, columns=["mes", "ipc_var_anual"]).sort_values("mes")


def fetch_eurusd(desde=f"{DESDE}-01", hasta=str(FECHA_FIN)):
    url = f"https://api.frankfurter.app/{desde}..{hasta}?from=EUR&to=USD"
    datos = get_con_reintentos(url).json()
    tasas = datos.get("rates", {})
    if not tasas:
        raise ValueError("Frankfurter respondió sin tasas EUR/USD")
    filas = [(pd.Timestamp(f), v["USD"]) for f, v in tasas.items()]
    df = pd.DataFrame(filas, columns=["fecha", "eur_usd"]).sort_values("fecha")
    dias_totales = (pd.Timestamp(hasta) - pd.Timestamp(desde)).days + 1
    incidencias.append(
        f"Frankfurter: {len(df)} días con dato de {dias_totales} del rango total "
        f"({dias_totales - len(df)} son fines de semana/feriados de mercado; se rellenan con ffill)"
    )
    return df


def fetch_feriados(anios):
    filas = []
    for anio in anios:
        r = get_con_reintentos(f"https://date.nager.at/api/v3/PublicHolidays/{anio}/ES")
        for f in r.json():
            filas.append({
                "fecha": f["date"], "nombre": f["localName"],
                "comunidades": ",".join(f.get("counties") or []) or "nacional",
            })
    if not filas:
        raise ValueError("Nager.Date respondió sin feriados")
    return pd.DataFrame(filas)


def construir_dim_contexto_macro(euribor, ipc, eurusd):
    rango = pd.date_range(f"{DESDE}-01", FECHA_FIN, freq="D")
    macro = pd.DataFrame({"fecha": rango})
    macro = macro.merge(euribor.rename(columns={"mes": "fecha"}), on="fecha", how="left")
    macro = macro.merge(ipc.rename(columns={"mes": "fecha"}), on="fecha", how="left")
    macro = macro.merge(eurusd, on="fecha", how="left")
    # Forward fill: las series mensuales solo publican un valor por mes, y
    # Frankfurter omite findes/feriados de mercado (declarado en FICHA.md §2.1).
    columnas = ["euribor_12m", "ipc_var_anual", "eur_usd"]
    macro[columnas] = macro[columnas].ffill().bfill()
    return macro


def validar(macro):
    errores = []
    if macro["fecha"].isna().any():
        errores.append("hay fechas nulas en dim_contexto_macro")
    for columna, (minimo, maximo) in RANGOS_VALIDOS.items():
        fuera_de_rango = macro[(macro[columna] < minimo) | (macro[columna] > maximo)]
        if not fuera_de_rango.empty:
            errores.append(f"{len(fuera_de_rango)} valores de {columna} fuera del rango plausible")
        if macro[columna].isna().any():
            errores.append(f"quedaron nulos en {columna} tras el forward fill")
    if macro["fecha"].max() < pd.Timestamp(FECHA_FIN):
        errores.append(f"la serie no llega hasta {FECHA_FIN} (FICHA.md exige cubrir el período)")
    return errores


def escribir_log(resumen):
    LOGS.mkdir(exist_ok=True)
    marca = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    contenido = resumen + "\n\nIncidencias:\n" + ("\n".join(incidencias) or "ninguna")
    (LOGS / f"extract_contexto_macro_{marca}.log").write_text(contenido, encoding="utf-8")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("Extrayendo contexto macroeconómico real — Finance Analytics España\n")
    SALIDA.mkdir(parents=True, exist_ok=True)

    print("· BCE — Euríbor 12M mensual...")
    euribor = fetch_euribor()
    print("· INE — IPC variación anual mensual...")
    ipc = fetch_ipc()
    print("· Frankfurter — EUR/USD diario...")
    eurusd = fetch_eurusd()
    print("· Nager.Date — feriados de España 2023-2026...")
    feriados = fetch_feriados(range(2023, FECHA_FIN.year + 1))

    macro = construir_dim_contexto_macro(euribor, ipc, eurusd)
    errores = validar(macro)

    macro.to_csv(SALIDA / "dim_contexto_macro.csv", index=False)
    feriados.to_csv(SALIDA / "feriados_es.csv", index=False)

    resumen = (
        f"Extracción: {dt.datetime.now().isoformat(timespec='seconds')}\n"
        f"dim_contexto_macro   {len(macro):>7,} filas  "
        f"({macro['fecha'].min().date()} -> {macro['fecha'].max().date()})\n"
        f"feriados_es           {len(feriados):>7,} filas\n"
        f"Validación: {'OK — sin errores' if not errores else 'FALLÓ'}\n"
        + "\n".join(f"  - {e}" for e in errores)
    )
    print(f"\nResumen:\n{resumen}\n→ CSVs en {SALIDA}")
    escribir_log(resumen)

    if errores:
        sys.exit(1)


if __name__ == "__main__":
    main()
