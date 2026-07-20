# Progreso — Finance Analytics España

## Estado actual
**Fase:** 1 (ETL) · **Paso:** 0 de 4 (por arrancar) · **Última sesión:** 2026-07-17
**Repo:** https://github.com/Merygonzalezisasa/Portfolio

## Bitácora

### Fase 0 — Decidir ✅ (2026-07-17)
- País: España · Moneda: EUR · Mercado: ofertas locales ES.
- Rubro: servicios B2B multi-cliente, finanzas operativas (facturación, cobros, morosidad).
  Organización ficticia: **Tamarindo Servicios Empresariales, S.L.**
- Fuentes externas aprobadas con los 4 chequeos (respuestas crudas en FICHA.md):
  - BCE — Euríbor 12M mensual (`FM.M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA`) ✓
  - INE — IPC variación anual (`IPC251856`), mensual, fechas en epoch ms ✓
  - Frankfurter — EUR/USD diario (omite findes → forward fill nuestro) ✓
  - Nager.Date — feriados ES (32 en 2026, incluye autonómicos) ✓
- 5 correlaciones intencionales definidas, 6 preguntas de negocio, 6 módulos de análisis elegidos.
- **FICHA.md aprobada por Rosmary el 2026-07-17.**

### Fase 0.5 — Entorno 🚧
- [x] Paso 1a — Inventario de la máquina (2026-07-17):
  - ✅ Power BI Desktop v2.155 (Microsoft Store) · ✅ VS Code
  - ❌ Python (solo el alias falso de la Store) · ❌ Git · ❌ Docker/PostgreSQL · ❌ Quarto (opcional, Fase 6)
- [x] Paso 1b — Python 3.12.10 ✓ (instalador directo; winget se colgaba, ver SETUP.md) ·
  Git 2.55 ✓ (identidad configurada) · PostgreSQL 16.12 descargando (347 MB)  ← ACÁ VAMOS
- [x] Paso 2 — Estructura bootstrap creada (Anexo B) · `.venv` creado ·
  `pip install -r requirements.txt` en curso · repo Git iniciado, primer commit `8f55188`
- [x] Paso 3 — PostgreSQL 16.12 instalado (servicio `postgresql-x64-16` corriendo), base
  `finance_analytics` creada (UTF8, locale español), `.env` generado con contraseña aleatoria
- [x] Paso 4 — **`verificar_entorno.py` → 8/8 EN VERDE** (2026-07-17). Trampas resueltas y
  documentadas en SETUP.md: inspección TLS (→ truststore), winget colgado (→ instalador directo)
- [x] Power BI Desktop abre correctamente (confirmado por Rosmary, 2026-07-17)
- [x] Repo publicado: **github.com/Merygonzalezisasa/Portfolio** (rama `main`, 2 commits)

## Fase 0.5 — CERRADA ✅ (2026-07-17)

## Decisiones técnicas anotadas
- En Windows PowerShell 5.1, las APIs HTTPS exigen forzar TLS 1.2
  (`[Net.ServicePointManager]::SecurityProtocol = Tls12`). En Python con `requests` no aplica.
- El "python OK" de la terminal era el alias stub de Microsoft Store, no un Python real.

### Fase 1 — ETL 🚧
- [x] Paso 1 — Generador sintético (`generate_facturas_data.py`). Verificado dos veces
  (por mí y por Rosmary en su máquina, mismo resultado gracias a SEED=42): dim_tiempo 912,
  dim_cliente 120, dim_servicio 25, fact_facturas 15.000 (13.444 cobradas, 989 pendientes,
  567 vencidas). Las 5 correlaciones de FICHA.md §2.3 confirmadas por separado (ver nota abajo).
- [x] Paso 2 — Extractor oficial (`extract_contexto_macro.py`), con reintentos, log y
  validación de rangos. Verificado por mí y por Rosmary (mismo resultado): dim_contexto_macro
  1.277 filas (2023-01 a 2026-06), feriados_es 130 filas, validación OK sin errores.
  Valores plausibles: Euríbor 2,08-4,16%, IPC 1,5-6%, EUR/USD 1,02-1,20.
  `01_etl/documentacion_api.txt` completado con las 4 APIs.
- [ ] Paso 3 — Carga a Postgres con upsert  ← ACÁ VAMOS
- [ ] Paso 4 — Verificación de carga

## Notas técnicas importantes
- **Al medir el retraso de pago, usar siempre `fecha_cobro − fecha_vencimiento` (retraso sobre
  lo PACTADO), nunca `fecha_cobro − fecha_emision` en bruto.** El `dso_pactado` (30 pyme vs
  60-90 corporate) es un factor de confusión que invierte el signo de la correlación con el
  Euríbor si se mide mal. Aplica igual en la Fase 2 (vistas SQL de aging/DSO) y la Fase 4.

## Dudas abiertas
- ¿El forward fill del fin de semana (EUR/USD) puede sesgar la correlación? → revisar en la Fase 4
  y declararlo en el notebook.
