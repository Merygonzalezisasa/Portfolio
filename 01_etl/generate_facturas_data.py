"""
Generador sintético de facturas — Finance Analytics España (Fase 1, Paso 1).

Construye las cuatro tablas del modelo estrella (dim_tiempo, dim_cliente,
dim_servicio, fact_facturas) con las 5 correlaciones intencionales de
FICHA.md §2.3. Los datos son sintéticos y reproducibles (SEED fija).

impacto_contexto() usa el Euríbor y el IPC REALES (BCE / INE) para inyectar
la correlación contra el mismo dato que el extractor de la Fase 1 Paso 2 va
a cargar como dim_contexto_macro — así el cruce de la Fase 4 encuentra una
señal real, no una coincidencia con un número inventado.

Uso:  python 01_etl/generate_facturas_data.py
"""

import datetime as dt
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import truststore
from faker import Faker

truststore.inject_into_ssl()  # esta máquina intercepta TLS: ver SETUP.md

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data" / "raw"

SEED = 42
FECHA_INICIO = date(2024, 1, 1)
FECHA_FIN = date(2026, 6, 30)
N_CLIENTES = 120
N_SERVICIOS = 25
N_FACTURAS = 15_000

rng = np.random.default_rng(SEED)
fake = Faker("es_ES")
Faker.seed(SEED)

COMUNIDADES = [
    "Madrid", "Cataluña", "Andalucía", "Comunidad Valenciana", "País Vasco",
    "Galicia", "Castilla y León", "Castilla-La Mancha", "Aragón", "Canarias",
]
SECTORES = ["retail", "seguros", "banca", "peajes", "ticketing",
            "inmobiliario", "sector público", "construcción"]
PESOS_SECTOR = [0.20, 0.15, 0.10, 0.05, 0.10, 0.15, 0.10, 0.15]
CANALES = ["licitación pública", "comercial directo", "referido", "inbound web", "partner"]

# línea -> (tarifa mínima, tarifa máxima, tipo de facturación, indexado a IPC)
LINEAS_SERVICIO = {
    "BI & Reporting": (1500, 6000, "recurrente", True),
    "Soporte de aplicaciones": (800, 3000, "recurrente", True),
    "Outsourcing financiero": (2000, 8000, "recurrente", True),
    "Consultoría": (3000, 15000, "proyecto", False),
    "Formación": (500, 2500, "proyecto", False),
}


def fetch_euribor_mensual(desde="2023-01"):
    url = ("https://data-api.ecb.europa.eu/service/data/FM/M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA"
           f"?format=jsondata&startPeriod={desde}")
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    datos = r.json()
    serie = next(iter(datos["dataSets"][0]["series"].values()))["observations"]
    periodos = datos["structure"]["dimensions"]["observation"][0]["values"]
    filas = [(pd.Period(periodos[int(i)]["id"], "M").to_timestamp(), v[0])
             for i, v in serie.items()]
    return pd.DataFrame(filas, columns=["mes", "euribor_12m"]).sort_values("mes")


def fetch_ipc_mensual(n_ultimos=48):
    url = f"https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/IPC251856?nult={n_ultimos}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    datos = r.json()["Data"]
    # El INE manda "Fecha" en epoch ms, ambiguo por huso horario (ver FICHA.md
    # §2.1). Anyo + FK_Periodo (mes 1-12) identifican el período sin ambigüedad.
    filas = [(pd.Timestamp(d["Anyo"], d["FK_Periodo"], 1), d["Valor"]) for d in datos]
    return pd.DataFrame(filas, columns=["mes", "ipc_var_anual"]).sort_values("mes")


def fetch_feriados(anios):
    feriados = {}
    for anio in anios:
        r = requests.get(f"https://date.nager.at/api/v3/PublicHolidays/{anio}/ES", timeout=30)
        r.raise_for_status()
        feriados.update({f["date"]: f["localName"] for f in r.json()})
    return feriados


def build_serie_contexto():
    """Euríbor + IPC reales, a diario (forward fill: las series son mensuales
    pero el negocio emite y vence facturas cualquier día)."""
    contexto = pd.merge(fetch_euribor_mensual(), fetch_ipc_mensual(), on="mes", how="inner")
    if contexto.empty:
        sys.exit("No hay solape entre Euríbor e IPC — revisar las APIs (FICHA.md §2.1).")

    rango = pd.date_range(FECHA_INICIO, FECHA_FIN + timedelta(days=100))
    diario = contexto.set_index("mes").reindex(rango, method="ffill").bfill()
    diario.index.name = "fecha"
    return diario


def build_dim_tiempo():
    feriados = fetch_feriados(range(FECHA_INICIO.year, FECHA_FIN.year + 1))
    df = pd.DataFrame({"fecha": pd.date_range(FECHA_INICIO, FECHA_FIN, freq="D")})
    df["anio"] = df["fecha"].dt.year
    df["trimestre"] = df["fecha"].dt.quarter
    df["mes"] = df["fecha"].dt.month
    dias_es = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    df["dia_semana"] = df["fecha"].dt.dayofweek.map(lambda i: dias_es[i])
    df["es_fin_de_semana"] = df["fecha"].dt.dayofweek >= 5
    df["nombre_feriado"] = df["fecha"].dt.strftime("%Y-%m-%d").map(feriados)
    df["es_feriado"] = df["nombre_feriado"].notna()
    # Últimos 5 días de cada mes de cierre de trimestre: la ventana real
    # donde se concentra la facturación (correlación #4 de FICHA.md §2.3).
    dias_restantes = df["fecha"].dt.days_in_month - df["fecha"].dt.day
    df["es_cierre_trimestre"] = df["mes"].isin([3, 6, 9, 12]) & (dias_restantes < 5)
    return df


def build_dim_cliente(n=N_CLIENTES):
    segmento = rng.choice(["corporate", "pyme"], size=n, p=[0.3, 0.7])
    # El plazo pactado lo impone quien tiene más poder de negociación: el
    # corporate exige 60-90 días; la pyme acepta las condiciones estándar.
    dso_pactado = np.where(
        segmento == "corporate",
        rng.choice([60, 90], size=n, p=[0.6, 0.4]),
        rng.choice([30, 60], size=n, p=[0.8, 0.2]),
    )
    # Sensibilidad al Euríbor: la pyme se financia más caro y reacciona más
    # a las subidas de tipos (correlación #2 de FICHA.md §2.3).
    sensibilidad_euribor = np.where(
        segmento == "corporate",
        rng.uniform(0.1, 0.4, size=n),
        rng.uniform(0.6, 1.5, size=n),
    ).round(2)
    fecha_alta = [FECHA_INICIO - timedelta(days=int(d))
                  for d in rng.integers(0, 365 * 3, size=n)]
    return pd.DataFrame({
        "cliente_id": np.arange(1, n + 1),
        "nombre": [fake.company() for _ in range(n)],
        "sector": rng.choice(SECTORES, size=n, p=PESOS_SECTOR),
        "segmento": segmento,
        "comunidad_autonoma": rng.choice(COMUNIDADES, size=n),
        "fecha_alta": fecha_alta,
        "canal_captacion": rng.choice(CANALES, size=n),
        "dso_pactado": dso_pactado,
        "sensibilidad_euribor": sensibilidad_euribor,
    })


def build_dim_servicio(n=N_SERVICIOS):
    lineas = list(LINEAS_SERVICIO.keys())
    por_linea = n // len(lineas)
    filas, servicio_id = [], 1
    for linea in lineas:
        precio_min, precio_max, tipo, indexado = LINEAS_SERVICIO[linea]
        for i in range(por_linea):
            filas.append({
                "servicio_id": servicio_id,
                "linea_servicio": linea,
                "servicio": f"{linea} — paquete {i + 1}",
                "tarifa_base": round(rng.uniform(precio_min, precio_max), 2),
                "tipo_facturacion": tipo,
                "indexado_ipc": indexado,
            })
            servicio_id += 1
    return pd.DataFrame(filas)


def aplica_ipc(importe_base, fecha_emision, contexto_diario):
    ipc = contexto_diario.loc[pd.Timestamp(fecha_emision), "ipc_var_anual"]
    # Correlación #3: los contratos con cláusula de revisión trasladan
    # típicamente la mitad del IPC acumulado, no el 100%.
    return importe_base * (1 + max(0.0, ipc) / 100 * 0.5)


def impacto_contexto(fecha_venc, sensibilidad, sector, contexto_diario, euribor_baseline):
    euribor_venc = contexto_diario.loc[pd.Timestamp(fecha_venc), "euribor_12m"]
    desviacion = max(0.0, euribor_venc - euribor_baseline)
    # Correlaciones #1 y #2: el Euríbor por encima de su media histórica
    # alarga el pago; cuánto, depende de la sensibilidad de cada cliente.
    dias_extra = desviacion * sensibilidad * 25

    # Correlación #5: el sector público paga tarde pero siempre paga; la
    # construcción es la que de verdad deja facturas sin cobrar.
    if sector == "sector público":
        dias_extra += rng.normal(20, 5)
        prob_impago = 0.01
    elif sector == "construcción":
        prob_impago = 0.12
    else:
        prob_impago = 0.03

    dias_extra += rng.normal(0, 4)  # ruido individual de cada factura
    return max(0, round(dias_extra)), prob_impago


def build_fact_facturas(dim_cliente, dim_servicio, dim_tiempo, contexto_diario):
    euribor_baseline = contexto_diario.loc[
        str(FECHA_INICIO):str(FECHA_FIN), "euribor_12m"
    ].mean()

    # Pareto de clientes: unos pocos concentran el grueso de la facturación
    # (alimenta la pregunta de negocio #1 — Pareto/ABC).
    peso_cliente = rng.lognormal(mean=0, sigma=0.9, size=len(dim_cliente))
    peso_cliente *= np.where(dim_cliente["segmento"] == "corporate", 2.5, 1.0)
    peso_cliente /= peso_cliente.sum()

    # Estacionalidad española: agosto casi parado, refuerzo en los días de
    # cierre de trimestre (correlación #4).
    habiles = dim_tiempo[~dim_tiempo["es_fin_de_semana"] & ~dim_tiempo["es_feriado"]]
    peso_dia = np.where(habiles["mes"] == 8, 0.15, 1.0)
    peso_dia = peso_dia * np.where(habiles["es_cierre_trimestre"], 2.0, 1.0)
    peso_dia = peso_dia / peso_dia.sum()

    idx_cliente = rng.choice(dim_cliente.index, size=N_FACTURAS, p=peso_cliente)
    idx_dia = rng.choice(habiles.index, size=N_FACTURAS, p=peso_dia)
    idx_servicio = rng.choice(dim_servicio.index, size=N_FACTURAS)

    filas = []
    for i in range(N_FACTURAS):
        cliente = dim_cliente.loc[idx_cliente[i]]
        servicio = dim_servicio.loc[idx_servicio[i]]
        fecha_emision = habiles.loc[idx_dia[i], "fecha"].date()
        fecha_vencimiento = fecha_emision + timedelta(days=int(cliente["dso_pactado"]))

        cantidad = 1 if servicio["tipo_facturacion"] == "recurrente" else int(rng.integers(1, 5))
        importe_neto = servicio["tarifa_base"] * cantidad
        if servicio["indexado_ipc"]:
            importe_neto = aplica_ipc(importe_neto, fecha_emision, contexto_diario)

        dias_extra, prob_impago = impacto_contexto(
            fecha_vencimiento, cliente["sensibilidad_euribor"], cliente["sector"],
            contexto_diario, euribor_baseline,
        )

        if rng.random() < prob_impago and fecha_vencimiento < FECHA_FIN:
            fecha_cobro, estado = None, "vencida"
        else:
            candidata = fecha_vencimiento + timedelta(days=dias_extra)
            if candidata <= FECHA_FIN:
                fecha_cobro, estado = candidata, "cobrada"
            else:
                fecha_cobro, estado = None, "pendiente"

        filas.append({
            "factura_id": i + 1,
            "cliente_id": cliente["cliente_id"],
            "servicio_id": servicio["servicio_id"],
            "fecha_emision": fecha_emision,
            "fecha_vencimiento": fecha_vencimiento,
            "fecha_cobro": fecha_cobro,
            "importe_neto": round(importe_neto, 2),
            "iva": round(importe_neto * 0.21, 2),
            "importe_total": round(importe_neto * 1.21, 2),
            "estado": estado,
        })

    return pd.DataFrame(filas)


def escribir_log(resumen):
    logs_dir = RAIZ / "logs"
    logs_dir.mkdir(exist_ok=True)
    marca = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    (logs_dir / f"generate_facturas_{marca}.log").write_text(resumen, encoding="utf-8")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("Generando Finance Analytics España — datos sintéticos (Fase 1, Paso 1)\n")
    SALIDA.mkdir(parents=True, exist_ok=True)

    print("· Trayendo Euríbor (BCE) e IPC (INE) reales para inyectar las correlaciones...")
    contexto_diario = build_serie_contexto()

    print("· Trayendo feriados de España (Nager.Date) para el calendario...")
    dim_tiempo = build_dim_tiempo()

    print("· Generando clientes y catálogo de servicios...")
    dim_cliente = build_dim_cliente()
    dim_servicio = build_dim_servicio()

    print(f"· Generando {N_FACTURAS:,} facturas con las 5 correlaciones de FICHA.md §2.3...")
    fact_facturas = build_fact_facturas(dim_cliente, dim_servicio, dim_tiempo, contexto_diario)

    dim_tiempo.to_csv(SALIDA / "dim_tiempo.csv", index=False)
    dim_cliente.to_csv(SALIDA / "dim_cliente.csv", index=False)
    dim_servicio.to_csv(SALIDA / "dim_servicio.csv", index=False)
    fact_facturas.to_csv(SALIDA / "fact_facturas.csv", index=False)

    resumen = (
        f"Generación: {dt.datetime.now().isoformat(timespec='seconds')}  (SEED={SEED})\n"
        f"dim_tiempo      {len(dim_tiempo):>7,} filas  "
        f"({dim_tiempo['fecha'].min().date()} -> {dim_tiempo['fecha'].max().date()})\n"
        f"dim_cliente     {len(dim_cliente):>7,} filas\n"
        f"dim_servicio    {len(dim_servicio):>7,} filas\n"
        f"fact_facturas   {len(fact_facturas):>7,} filas\n"
        f"estado de facturas:\n{fact_facturas['estado'].value_counts().to_string()}\n"
    )
    print(f"\nResumen:\n{resumen}\n→ CSVs en {SALIDA}")
    escribir_log(resumen)


if __name__ == "__main__":
    main()
