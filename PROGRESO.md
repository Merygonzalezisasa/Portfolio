# Progreso — Finance Analytics España

## Estado actual
**Fase:** 0.5 (Entorno) · **Paso:** 1 de 4 (instalación de herramientas) · **Última sesión:** 2026-07-17

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
- [ ] Paso 1b — Instalar Python 3.12, Git y la base de datos  ← ACÁ VAMOS
- [ ] Paso 2 — Crear estructura del proyecto + venv + requirements
- [ ] Paso 3 — Levantar PostgreSQL y probar conexión
- [ ] Paso 4 — `verificar_entorno.py` en verde + repo Git con primer commit + SETUP.md

## Decisiones técnicas anotadas
- En Windows PowerShell 5.1, las APIs HTTPS exigen forzar TLS 1.2
  (`[Net.ServicePointManager]::SecurityProtocol = Tls12`). En Python con `requests` no aplica.
- El "python OK" de la terminal era el alias stub de Microsoft Store, no un Python real.

## Dudas abiertas
- ¿El forward fill del fin de semana (EUR/USD) puede sesgar la correlación? → revisar en la Fase 4
  y declararlo en el notebook.
