# Ficha del Proyecto — Finance Analytics España

> Fuente de verdad del proyecto. Todas las fases leen de acá.
> Estado: **APROBADA** — 2026-07-17, revisada por Rosmary González Isasa.

## 0. País y contexto

| Campo | Valor |
|---|---|
| **País** | España |
| **Código ISO-2** | ES |
| **Moneda** | € EUR (formato español: 1.234,56 €) |
| **Mercado al que apunta** | España (ofertas locales de analista de datos) |
| **Geografía del modelo** | Comunidades autónomas (Madrid, Cataluña, Andalucía, C. Valenciana, País Vasco, Galicia…) |
| **Idioma del proyecto** | Español (código, comentarios y documentación) |

## 1. Identidad

| Campo | Valor |
|---|---|
| **Estudiante** | *(Rosmary González Isasa)* |
| **Rubro** | Servicios B2B multi-cliente — finanzas operativas (facturación, cobros, morosidad) |
| **Por qué este rubro** | Experiencia real como analista de datos en el sector financiero (dashboards para ticketing, peajes, aseguradoras) y como responsable de cuentas a pagar. Las métricas del proyecto (DSO, aging, morosidad) son las que puedo defender desde adentro en una entrevista. |
| **Organización ficticia** | **Tamarindo Servicios Empresariales, S.L.** — fundada en 2015, ~85 empleados, sede en Madrid. Presta servicios de BI, soporte de aplicaciones y outsourcing financiero a empresas de varios sectores. |
| **Nombre del repositorio** | `finance-analytics-espana` |
| **Pregunta central del proyecto** | ¿Cómo afecta el entorno macroeconómico español (Euríbor, IPC) a la facturación y al cobro de una empresa B2B, y qué debe hacer Finanzas al respecto? |
| **La historia en una línea** | "Soy analista de datos. Me pidieron entender por qué se alargaban los cobros. Crucé la facturación con el Euríbor y el IPC y descubrí qué clientes estiran los plazos cuando sube el precio del dinero." |

## 2. Fuentes de datos

### 2.1 Fuentes externas REALES (obligatorias)

**Principal — Euríbor 12M (BCE):**

| Campo | Valor |
|---|---|
| API | ECB Data Portal |
| Endpoint base | `https://data-api.ecb.europa.eu/service/data/FM/M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA?format=jsondata` |
| Nivel | Nivel 1–2 (BCE, cubre España) |
| Variables que trae | Euríbor 12 meses, tasa de referencia hipotecaria y de crédito |
| Frecuencia | **Mensual** ✓ |
| Período que cubre | Desde los años 90 hasta hoy ✓ (probado: 6 obs. en 2026) |
| Para qué sirve en el análisis | Correlacionar con DSO y morosidad (correlaciones #1 y #2) |
| ¿Requiere key? | No |
| **Prueba** (2026-07-17) | `Euribor 12M mensual - observaciones 2026: 6 · Periodos: 2026-01, 2026-02, 2026-03, 2026-04, 2026-05, 2026-06` |

**Secundarias (probadas el 2026-07-17):**

| API | Endpoint | Variable | Frecuencia | Key |
|---|---|---|---|---|
| INE Tempus | `https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/IPC251856?nult=N` | IPC variación anual (Nacional, índice general) | Mensual | No |
| Frankfurter | `https://api.frankfurter.app/{inicio}..{fin}?from=EUR&to=USD` | Tipo de cambio EUR/USD | Diaria (días hábiles) | No |
| Nager.Date | `https://date.nager.at/api/v3/PublicHolidays/{año}/ES` | Feriados oficiales de España (incl. autonómicos) | Por fecha | No |

Respuestas crudas de la prueba:

```json
// INE — IPC251856 (fechas en epoch ms: hay que normalizar en el extractor)
{"COD":"IPC251856","Nombre":"Nacional. Índice general. Variación anual. ","FK_Unidad":135,"FK_Escala":1,
 "Data":[{"Fecha":1759269600000,"FK_TipoDato":1,"FK_Periodo":10,"Anyo":2025,"Valor":3.1,"Secreto":false}, ...]}

// Frankfurter — EUR/USD (omite fines de semana: forward fill en nuestro ETL)
{"amount":1.0,"base":"EUR","start_date":"2026-06-01","end_date":"2026-06-10",
 "rates":{"2026-06-01":{"USD":1.1646},"2026-06-02":{"USD":1.1649},"2026-06-03":{"USD":1.1614},
          "2026-06-04":{"USD":1.164},"2026-06-05":{"USD":1.164},"2026-06-08":{"USD":1.154}, ...}}

// Nager.Date — 32 feriados ES 2026, con comunidad autónoma en "counties"
[{"date":"2026-01-01","localName":"Año Nuevo","countryCode":"ES","global":true,"types":["Public"]},
 {"date":"2026-02-28","localName":"Día de Andalucía","global":false,"counties":["ES-AN"],"types":["Public"]}, ...]
```

**Notas técnicas de la prueba:**
- El INE entrega fechas en **epoch milisegundos** → normalizar a `YYYY-MM-DD` en el extractor.
- Frankfurter **omite fines de semana** (mercado cerrado) → *forward fill* en nuestro ETL, declarado en el notebook.
- En Windows PowerShell 5.1 hubo que forzar TLS 1.2; en Python con `requests` no aplica.

### 2.2 Fuente interna (sintética)

| Campo | Valor |
|---|---|
| Origen | Sintética (Faker + NumPy, con correlaciones intencionales). **Declarada como tal en el README.** |
| Período | 2024-01-01 a 2026-06-30 (2,5 años → permite comparación YoY) |
| Volumen de hechos | ~15.000 facturas |
| Volumen de entidades | ~120 clientes empresa |
| Volumen de ítems | ~25 servicios en 5 líneas de servicio |
| Geografía | Clientes distribuidos por comunidades autónomas |

### 2.3 Correlaciones intencionales (5)

Lo que el generador va a inyectar y el análisis va a "descubrir" (todas plausibles en la España real):

1. **Euríbor ↑ → DSO ↑**: cuando sube el Euríbor, los clientes estiran sus plazos de pago (financiarse cuesta más).
2. **Pymes más sensibles que corporate**: el retraso de pago ante subidas de tipos es mayor en el segmento pyme.
3. **IPC → facturación**: los servicios recurrentes con cláusula de revisión anual suben con la inflación acumulada.
4. **Estacionalidad española**: agosto con actividad mínima, picos de facturación en cierres de trimestre, cobros concentrados a fin de mes.
5. **Morosidad por sector**: sector público paga tarde pero siempre; construcción concentra la morosidad real.

> **Honestidad estadística:** estas señales las inyecta el propio generador. El análisis no descubre una
> verdad del mundo — demuestra que el pipeline detecta y cuantifica bien una señal conocida de antemano.
> Se declara así en el README y en el notebook.

## 3. Modelo dimensional

| Rol | Tabla | Columnas clave |
|---|---|---|
| HECHO | `fact_facturas` | factura_id, cliente_id, servicio_id, fecha_emision, fecha_vencimiento, fecha_cobro (NULL = pendiente), importe_neto, iva, importe_total, dias_pago, estado |
| QUIÉN | `dim_cliente` | cliente_id, nombre, sector (peajes, seguros, ticketing, banca, inmobiliario, s. público, construcción, retail), segmento (corporate/pyme), comunidad_autonoma, fecha_alta, canal_captacion |
| QUÉ | `dim_servicio` | servicio_id, linea_servicio (BI & Reporting, Soporte de aplicaciones, Outsourcing financiero, Consultoría, Formación), servicio, tarifa_base, tipo_facturacion (recurrente/proyecto), indexado_ipc |
| CUÁNDO | `dim_tiempo` | fecha, año, trimestre, mes, dia_semana, es_fin_de_semana, es_feriado, nombre_feriado, es_cierre_trimestre |
| DÓNDE | *(incluido en `dim_cliente`: comunidad_autonoma)* | |
| CONTEXTO | `dim_contexto_macro` | fecha/mes, euribor_12m, ipc_var_anual, eur_usd |

## 4. Preguntas de negocio (6)

| # | Pregunta | Área | Módulo de análisis | Acción esperada |
|---|---|---|---|---|
| 1 | ¿Qué clientes concentran el 80% de la facturación, y qué riesgo implica esa concentración? | Dirección Comercial | Pareto ABC | Plan de cuentas clave + diversificación de cartera |
| 2 | ¿Cómo se segmenta la cartera según comportamiento de compra **y de pago**? | Finanzas / CRM | RFM + K-Means | Política de crédito diferenciada por segmento (límites, plazos) |
| 3 | ¿Qué clientes dejan de facturar mes a mes, y cuándo se pierden? | Comercial | Cohortes | Alerta temprana de inactividad + plan de reactivación |
| 4 | ¿Cómo evolucionan el DSO y el aging de deuda, y cuánta caja entrará el próximo trimestre? | Tesorería | Forecast | Anticipar necesidades de financiación (o excedentes) |
| 5 | ¿La subida del Euríbor alarga los plazos de pago? ¿El IPC empuja la facturación? | Dirección Financiera | Correlación con contexto | Endurecer/relajar política de cobros según ciclo de tipos |
| 6 | ¿Qué facturas presentan anomalías (duplicados, importes fuera de rango, fechas imposibles)? | Control interno | Calidad y outliers | Protocolo de revisión previo al cierre mensual |

## 5. Módulos de análisis elegidos (7 de 8)

- [x] Calidad y outliers *(obligatorio)*
- [x] Pareto / ABC
- [x] RFM + Clustering *(con la dimensión de pago añadida: días promedio de pago, % vencidas)*
- [x] Cohortes
- [ ] Market Basket
- [x] Forecast *(cashflow de cobros, Prophet)*
- [x] Correlación con contexto externo
- [x] Churn / riesgo *(la señal de inactividad queda cubierta por Cohortes)*

## 6. Arquitectura (dibujo del flujo)

```
┌───────────────────────────┐      ┌────────────────────────────┐
│  FUENTES EXTERNAS REALES  │      │  FUENTE INTERNA SINTÉTICA  │
│  BCE  → Euríbor 12M (mes) │      │  Ábaco Servicios (ficticia)│
│  INE  → IPC (mes)         │      │  ~15.000 facturas          │
│  Frankfurter → EUR/USD    │      │  ~120 clientes · 25 servs. │
│  Nager.Date  → feriados ES│      │  2024-01 → 2026-06         │
└─────────────┬─────────────┘      └─────────────┬──────────────┘
              │                                  │
              └────────────────┬─────────────────┘
                               ▼
              ┌─────────────────────────────────┐
              │  CAPA 1 — ETL (Python)          │
              │  extract_macro.py · generate_   │
              │  facturas_data.py · load (upsert)│
              └────────────────┬────────────────┘
                               ▼
              ┌─────────────────────────────────┐
              │  CAPA 2 — SQL (PostgreSQL)      │
              │  esquema estrella · vistas:     │
              │  enriquecida, KPIs diarios,     │
              │  RFM-pago, Pareto, aging/DSO    │
              └───────┬─────────────────┬───────┘
                      ▼                 ▼
        ┌──────────────────────┐  ┌──────────────────────────┐
        │ CAPA 3 — POWER BI    │  │ CAPA 4 — ANÁLISIS PYTHON │
        │ pág.1: ejecutivo     │  │ calidad · Pareto · RFM   │
        │ (KPIs, YoY, Pareto)  │  │ cohortes · correlación   │
        │ pág.2: cruce macro   │  │ macro · forecast cashflow│
        │ (DSO vs Euríbor)     │  │                          │
        └──────────┬───────────┘  └───────────┬──────────────┘
                   └──────────────┬───────────┘
                                  ▼
              ┌─────────────────────────────────┐
              │  CAPA 5 — NARRATIVA             │
              │  README · insights_findings ·   │
              │  posts LinkedIn                 │
              └─────────────────────────────────┘
```

## 7. Stack y entorno

| Capa | Herramienta | Por qué |
|---|---|---|
| Generación | Python 3.11+ (Faker, NumPy, pandas) | Datos sintéticos con correlaciones controladas y semilla fija |
| Extracción | Python (requests) | Consumo de las 4 APIs con reintentos, timeout y logs |
| Base | PostgreSQL 16 (Docker) | Estándar del mercado; Docker = un comando, reproducible |
| Transformación | SQL (vistas + stored procedures) | La lógica de negocio vive junto a los datos |
| Visualización | Power BI Desktop | Windows ✓, la estudiante ya lo domina, es lo más pedido en ofertas ES |
| Análisis | Jupyter (pandas, scipy, scikit-learn, Prophet) | Los 6 módulos elegidos |

| Campo | Valor |
|---|---|
| **Sistema operativo del estudiante** | Windows 11 |
| **Herramienta de BI elegida** | Power BI Desktop |
| **PostgreSQL** | (a confirmar en Fase 0.5; alternativa: instalación nativa) |

## 8. Alcance y limitaciones

**Dentro:** pipeline completo end-to-end (ETL → SQL → BI → análisis → documentación), los 6 módulos
elegidos, flujo de actualización periódica documentado, sistema de contenido LinkedIn (Fase 6).

**Fuera:** pagos parciales (una factura = un cobro único), multi-moneda en la facturación (todo en EUR;
el EUR/USD es variable de contexto), presupuestos/contabilidad analítica, Airflow real (se documenta cómo
se automatizaría).

**Limitaciones de los datos:** la fuente interna es sintética y sus correlaciones son inyectadas
(declarado en README y notebook). El forward fill de fines de semana en EUR/USD se declara en el
análisis. El cruce con Euríbor e IPC se hace a granularidad mensual (la de esas series).

## 9. Aprobación

- [x] **País, moneda y mercado objetivo definidos.**
- [x] Las fuentes externas pasaron los **4 chequeos** del Paso 3, y la respuesta cruda está pegada arriba.
- [x] Las series externas son **diarias o mensuales** (no anuales).
- [x] Cada pregunta termina en una acción concreta.
- [x] El período cubre al menos 2 años (2,5).
- [x] Las correlaciones intencionales están escritas (5).
- [x] La herramienta de BI es compatible con el sistema operativo (Power BI Desktop en Windows 11).
- [x] **Aprobación final del estudiante** (2026-07-17, Rosmary González Isasa)
