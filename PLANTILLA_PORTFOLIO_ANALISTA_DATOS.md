# Plantilla: Portfolio de Analista de Datos (end-to-end)

**Qué es esto:** el molde reutilizable para construir un portfolio completo de analista de datos,
**para cualquier rubro y cualquier país**. Define la estructura, el orden de las fases, los
entregables de cada una y el sistema de contenido para LinkedIn que viene después.

**Cómo se usa:** el estudiante llena primero la **Ficha del Proyecto** (Fase 0). Esa ficha es la
**única fuente de verdad**: todas las fases siguientes leen de ella. El país, el rubro, los datos y
el flujo los decide el estudiante; el esqueleto no cambia.

**Tres cosas que esta plantilla hace por sí sola:**

1. **Pregunta el país antes que nada.** De esa respuesta salen la fuente externa real, la moneda,
   el calendario de feriados y la geografía del modelo (Fase 0, Paso 0).
2. **Instala y verifica el entorno completo** — Python, PostgreSQL, la herramienta de BI, Git — en
   Windows, macOS o Linux, y no deja avanzar hasta que todo responde (Fase 0.5 + Anexo F).
3. **Acompaña paso a paso**, con checkpoints que hay que pasar antes de seguir, y deja rastro del
   avance en `PROGRESO.md` para poder retomar en otra sesión (el protocolo de la Parte 0).

**Versión:** 2.0 — internacional. Derivada del proyecto de referencia *Retail Analytics Chile*
(Mariabelén Dumont), que es **una instancia** de esta plantilla, no la plantilla misma.

---

## Índice

- [Parte 0 — Cómo usar este documento](#parte-0--cómo-usar-este-documento)
- [Parte 1 — El esqueleto invariante (lo que NO cambia)](#parte-1--el-esqueleto-invariante-lo-que-no-cambia)
- [Parte 2 — Fase 0: Decidir el proyecto (país, rubro, cruce)](#parte-2--fase-0-decidir-el-proyecto-país-rubro-cruce)
- [Parte 3 — Fase 0.5: Entorno (instalar y verificar)](#parte-3--fase-05-entorno-instalar-y-verificar)
- [Parte 4 — Fase 1: ETL (Python)](#parte-4--fase-1-etl-python)
- [Parte 5 — Fase 2: SQL (modelo + vistas + automatización)](#parte-5--fase-2-sql-modelo--vistas--automatización)
- [Parte 6 — Fase 3: BI (dashboard)](#parte-6--fase-3-bi-dashboard)
- [Parte 7 — Fase 4: Análisis en Python](#parte-7--fase-4-análisis-en-python)
- [Parte 8 — Fase 5: Documentación y vitrina](#parte-8--fase-5-documentación-y-vitrina)
- [Parte 9 — Fase 6: Sistema de contenido en LinkedIn](#parte-9--fase-6-sistema-de-contenido-en-linkedin)
- [Parte 10 — Cronograma, checklist maestro y errores comunes](#parte-10--cronograma-checklist-maestro-y-errores-comunes)
- [Anexo A — Ficha del Proyecto (en blanco, para copiar)](#anexo-a--ficha-del-proyecto-en-blanco-para-copiar)
- [Anexo B — Árbol de archivos completo (bootstrap)](#anexo-b--árbol-de-archivos-completo-bootstrap)
- [Anexo C — Prompts por fase (copiar y pegar)](#anexo-c--prompts-por-fase-copiar-y-pegar)
- [Anexo D — Tres proyectos de ejemplo, en tres países](#anexo-d--tres-proyectos-de-ejemplo-en-tres-países)
- [Anexo E — Glosario de variables](#anexo-e--glosario-de-variables)
- [Anexo F — Instalación del entorno, comando por comando](#anexo-f--instalación-del-entorno-comando-por-comando)

---

# Parte 0 — Cómo usar este documento

## Los tres momentos

| Momento | Qué pasa | Resultado |
|---|---|---|
| **Decidir** (Fase 0) | El estudiante elige **país**, rubro, fuentes de datos, preguntas de negocio y dibuja su flujo | `FICHA.md` aprobada |
| **Preparar** (Fase 0.5) | Se instala y se verifica el entorno completo: Python, base de datos, BI, Git | `SETUP.md` + `verificar_entorno.py` en verde |
| **Construir** (Fases 1–5) | Se levanta el pipeline, la base, el dashboard, el análisis y la documentación | Repositorio en GitHub, listo para mostrar |
| **Publicar** (Fase 6) | Se convierte el proyecto en contenido: posts, carruseles, medición | Presencia en LinkedIn sostenida |

**Dos reglas duras:**

- **No se avanza a la Fase 0.5 sin la Ficha aprobada.** El 80% de los portfolios flojos fallan acá:
  se ponen a programar sin saber qué pregunta responden.
- **No se avanza a la Fase 1 sin el entorno en verde.** Instalar a mitad del ETL, con un error de
  conexión encima, es la forma más rápida de abandonar el proyecto.

## Cómo usarlo con IA (Claude Code)

1. Crear la carpeta del nuevo proyecto y copiar **este documento** en la raíz.
2. Abrir Claude Code en esa carpeta.
3. Trabajar fase por fase, con los prompts del [Anexo C](#anexo-c--prompts-por-fase-copiar-y-pegar).
   Cada prompt asume que la IA leyó `FICHA.md` + este documento.
4. **No pedir "hazme todo el proyecto".** Se pierde control, la calidad baja y el estudiante no
   aprende a defenderlo en una entrevista. Una fase por sesión.

### El protocolo de acompañamiento (cómo debe guiar la IA)

Esto no es una sugerencia de estilo: es lo que separa "tengo un repo" de "sé lo que hay en mi repo".
La IA que acompañe al estudiante con esta plantilla debe seguir estas seis reglas.

1. **Un paso a la vez.** Dentro de una fase se avanza por pasos chicos. Se termina uno, se verifica,
   y recién ahí empieza el siguiente.
2. **Explicar antes de escribir.** Antes de cada bloque de código nuevo: qué va a hacer, por qué así
   y qué decisión hay detrás. En tres frases, no en tres párrafos.
3. **Checkpoint obligatorio.** Cada paso termina con un **comando exacto** que el estudiante corre en
   su máquina y cuya salida pega de vuelta. **Si no hay salida, no se avanza.** La IA no puede dar
   por bueno lo que no vio correr.
4. **Pregunta de control.** Al cerrar cada paso, la IA le pregunta al estudiante algo que solo puede
   responder si entendió (*"¿por qué el upsert va por la clave y no por el índice?"*). Si no lo sabe,
   se explica de nuevo antes de seguir.
5. **Registrar el avance.** Al cerrar cada paso se actualiza `PROGRESO.md`: qué se hizo, qué comando
   lo verificó, qué quedó pendiente. Ese archivo es lo que permite retomar en otra sesión, con otra
   IA o dentro de tres semanas, sin volver a explicar el proyecto entero.
6. **Frenar el atajo.** Si el estudiante pide "hacelo todo de una vez", la IA se lo recuerda: el
   objetivo no es el repo, es poder defenderlo.

> **Criterio de honestidad:** el estudiante debe poder explicar cada línea de su repo. Si hay algo
> que la IA escribió y no entiende, se revisa o se borra. En la entrevista pregunta un humano.

## Cómo usarlo sin IA

Cada fase trae su especificación, plantilla y *Definition of Done*. Se puede construir a mano
siguiendo el mismo orden; el Anexo F trae la instalación comando por comando. La estimación de
tiempo (Parte 10) considera trabajo manual.

---

# Parte 1 — El esqueleto invariante (lo que NO cambia)

Cambia el rubro, cambian los datos, cambian los KPIs. **Esto se mantiene siempre:**

## 1.1 El patrón de cinco capas

```
┌──────────────────────┐     ┌──────────────────────┐
│  FUENTE EXTERNA REAL │     │  FUENTE INTERNA      │
│  (API pública)       │     │  (sintética o        │
│  → el "contexto"     │     │   dataset público)   │
│                      │     │  → el "negocio"      │
└──────────┬───────────┘     └──────────┬───────────┘
           │                            │
           └─────────────┬──────────────┘
                         ▼
            ┌────────────────────────┐
            │  CAPA 1 — ETL (Python) │
            │  extraer · limpiar     │
            │  validar · cargar      │
            └────────────┬───────────┘
                         ▼
            ┌────────────────────────┐
            │  CAPA 2 — SQL          │
            │  esquema estrella      │
            │  vistas · SPs · índices│
            └────────┬───────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌─────────────────┐     ┌──────────────────────┐
│ CAPA 3 — POWER  │     │ CAPA 4 — ANÁLISIS    │
│ BI (el "qué")   │     │ PYTHON (el "por qué")│
│ dashboard, DAX  │     │ notebook, estadística│
└─────────────────┘     └──────────────────────┘
        └────────────┬────────────┘
                     ▼
            ┌────────────────────────┐
            │  CAPA 5 — NARRATIVA    │
            │  README · docs ·       │
            │  insights · LinkedIn   │
            └────────────────────────┘
```

**Por qué estas cinco y no otras:** cubren exactamente lo que pide una oferta de analista junior
(ETL, SQL, BI, Python, comunicación). Cada capa es una casilla que el reclutador marca.

## 1.2 El modelo de datos genérico

Todo dominio, sin excepción, se puede modelar así:

| Rol | Qué representa | Nombre genérico |
|---|---|---|
| **HECHO** | El evento que se cuenta y se mide | `fact_{{HECHO}}` |
| **QUIÉN** | La persona/organización que protagoniza el evento | `dim_{{ENTIDAD}}` |
| **QUÉ** | El objeto o servicio involucrado | `dim_{{ITEM}}` |
| **CUÁNDO** | El calendario, con eventos y estacionalidad | `dim_tiempo` |
| **DÓNDE** *(opcional)* | Geografía, sucursal, zona | `dim_{{LUGAR}}` |
| **CONTEXTO EXTERNO** | La variable del mundo real que explica variaciones | `dim_{{CONTEXTO}}` |

**El diferenciador está en la última fila.** Un portfolio con solo datos internos es un dashboard.
Un portfolio que cruza datos internos con **una fuente externa real vía API** es un análisis.

### Traducción por rubro

La columna de contexto está escrita en **variables**, no en fuentes: la fuente concreta depende del
país y se elige en la Fase 0 (Paso 3).

| Rubro | `fact_` | `dim_` QUIÉN | `dim_` QUÉ | `dim_` CONTEXTO (variable externa real) |
|---|---|---|---|---|
| Retail / e-commerce | ventas | cliente | producto | tipo de cambio, inflación, actividad económica |
| Marketing digital | gasto de pauta, conversiones | cliente / lead | campaña | tipo de cambio (las plataformas cobran en USD), inflación |
| Salud / clínica | atenciones | paciente | prestación | temperatura, calidad del aire |
| Educación / EdTech | inscripciones, actividad | estudiante | curso | desempleo, indicadores del mercado laboral |
| Logística / delivery | envíos | cliente | ruta / zona | lluvia, viento, feriados, precio del combustible |
| Banca / fintech | transacciones | cliente | comercio / categoría | inflación, tasa de interés, tipo de cambio |
| Turismo / hotelería | reservas | huésped | habitación / tarifa | tipo de cambio, feriados, clima |
| Energía / utilities | consumo | cliente | medidor / tarifa | temperatura, generación eléctrica |
| Agro / exportación | despachos | predio | cultivo | clima, precios internacionales de commodities |
| Suscripción / gimnasio | visitas, membresías | socio | clase / plan | clima, estacionalidad, feriados |
| Municipal / gobierno | reclamos, incidentes | ciudadano / zona | tipo de reclamo | clima, población, presupuesto |

> **Se pueden combinar rubros.** Ejemplo: *retail + logística* (ventas y tiempos de entrega),
> *salud + clima* (urgencias y temperatura), *educación + empleo* (matrícula y desempleo por sector).
> La combinación es exactamente lo que hace que el proyecto no parezca un tutorial de Kaggle.

### La regla del plan B global

Cualquiera sea el país, **siempre existen tres variables externas reales disponibles**: el **clima**
(Open-Meteo), los **feriados** (Nager.Date) y el **tipo de cambio** (Frankfurter u open.er-api).
Las tres cubren el mundo entero, son gratis y no piden API key.

Por lo tanto: **ningún estudiante se puede quedar sin fuente externa por vivir en el país "equivocado".**
Si la fuente nacional que quería no existe, no responde o no cubre su período, el proyecto sigue con
el plan B global. Se pierde algo de color local; no se pierde el proyecto.

## 1.3 Los ocho módulos de análisis (catálogo)

Se eligen **5 o 6**, no los ocho. Cada uno responde una pregunta genérica que existe en todo rubro:

| # | Módulo | Pregunta genérica | Técnica | Ejemplo retail | Ejemplo salud | Ejemplo educación |
|---|---|---|---|---|---|---|
| 1 | **Pareto / ABC** | ¿Dónde se concentra el valor? | Ranking + % acumulado | Productos que dan el 80% de ingresos | Prestaciones que consumen el 80% del costo | Cursos que traen el 80% de la matrícula |
| 2 | **RFM + Clustering** | ¿Cómo agrupo a las personas por comportamiento? | Recency/Frequency/Monetary + K-Means | Segmentos de clientes | Adherencia de pacientes a controles | Estudiantes por nivel de actividad |
| 3 | **Cohortes** | ¿Cuánto retengo mes a mes? | Matriz de retención | Recompra | Continuidad de tratamiento | Deserción por cohorte de ingreso |
| 4 | **Market Basket** | ¿Qué ocurre junto? | Apriori (lift, confidence) | Productos comprados juntos | Exámenes que se piden juntos | Cursos que se toman juntos |
| 5 | **Forecast** | ¿Cuánto habrá el próximo trimestre? | Prophet / ARIMA | Ventas | Demanda de atenciones | Matrículas |
| 6 | **Correlación con contexto** | ¿Qué explica las variaciones? | Pearson/Spearman + significancia | Dólar vs ventas | Temperatura vs urgencias | Desempleo vs matrícula |
| 7 | **Churn / riesgo** | ¿Quién se va a ir? | Regresión logística | Cliente inactivo | Paciente que abandona control | Estudiante en riesgo de deserción |
| 8 | **Calidad y outliers** | ¿Qué datos no cuadran? | IQR, nulos, duplicados | Tickets anómalos | Duraciones imposibles | Notas fuera de rango |

**Recomendación de mezcla:** 1 módulo de calidad (#8, obligatorio) + 2 descriptivos (#1, #3) +
1 de segmentación (#2) + 1 predictivo (#5 o #7) + **#6 siempre**, porque es el que justifica haber
traído la fuente externa.

## 1.4 Estructura de carpetas (idéntica para todos)

```
{{PROYECTO}}/
├── FICHA.md                        ← la decisión (Fase 0). Fuente de verdad.
├── SETUP.md                        ← cómo se instaló el entorno (Fase 0.5)
├── PROGRESO.md                     ← bitácora: qué se hizo, qué falta. Permite retomar.
├── README.md                       ← la vitrina
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
├── index.html                      ← landing opcional (GitHub Pages)
│
├── 00_setup/
│   ├── verificar_entorno.py        ← chequea versiones, conexión a la base y a la API
│   └── docker-compose.yml          ← PostgreSQL en un comando (opcional pero recomendado)
│
├── 01_etl/
│   ├── extract_{{FUENTE_EXTERNA}}.py
│   ├── generate_{{HECHO}}_data.py
│   ├── load_to_postgres.py
│   └── verificar_carga.py
│
├── 02_sql/
│   ├── 01_create_schema.sql
│   ├── 02_create_views.sql
│   ├── 03_stored_procedures.sql
│   └── 04_sample_queries.sql
│
├── 03_bi/                          ← se llama 03_powerbi/ si la herramienta es Power BI
│   ├── {{PROYECTO}}.pbip / .pbix
│   ├── measures_documentation.md
│   └── screenshots/
│
├── 04_analysis/
│   ├── eda_completo.ipynb
│   └── outputs/                    ← PNG que se reutilizan en docs y LinkedIn
│
├── 05_docs/
│   ├── business_case.md
│   ├── data_dictionary.md
│   └── insights_findings.md
│
├── data/
│   ├── raw/
│   └── processed/
│
└── logs/
```

Y, en paralelo (fuera del repo público o en otro repo):

```
post/
├── _quarto.yml
├── 0. Sistema/
│   ├── README.md              ← el flujo de producción
│   ├── guia-voz.md            ← el tono (fuente de verdad de la voz)
│   ├── prompt-maestro.md      ← prompt para generar cada post
│   ├── calendario.md          ← publicados + backlog
│   └── plantilla/
│       ├── _estilo.qmd        ← marca visual (Typst)
│       └── marca.py           ← estilo de gráficos (matplotlib)
├── N. post/
│   ├── carrusel.qmd           ← único archivo editable
│   ├── texto.md               ← caption de LinkedIn
│   ├── img/                   ← PNG generados por código
│   └── carrusel.pdf           ← entregable
└── rendimiento/
    ├── seguimiento.csv
    └── analisis.qmd           ← reporte de métricas
```

## 1.5 Reglas de calidad transversales

Aplican a todas las fases. Son las que separan un proyecto de portfolio de un ejercicio de curso:

1. **Reproducible.** Cualquiera clona, sigue el README y obtiene el mismo resultado. Sin pasos
   manuales ocultos.
2. **Idempotente.** Correr el ETL dos veces no duplica datos (upsert por clave, no `INSERT` ciego).
3. **Con logs.** Cada script deja registro en `logs/` (qué corrió, cuántas filas, qué falló).
4. **Validado.** Cada carga verifica: conteo de filas, nulos en claves, rangos imposibles.
5. **Sin secretos en git.** Credenciales en `.env`, nunca en el código. `.env` en `.gitignore`.
6. **Comentado en el idioma del proyecto.** Español, consistente, explicando el *por qué* y no el *qué*.
7. **Datos sintéticos declarados.** Se dice explícitamente qué es real y qué es generado. Mentir
   sobre el origen de los datos es la única falta que descalifica un portfolio.

---

# Parte 2 — Fase 0: Decidir el proyecto (país, rubro, cruce)

**Entregable:** `FICHA.md` completa y aprobada.
**Tiempo:** medio día a un día. Es la fase más barata y la más determinante.

## Paso 0 — Elegir el país (la primera pregunta, siempre)

**Antes de hablar de rubro, de datos o de código, se define el país.** No es un detalle de
ambientación: de esa respuesta salen cuatro cosas que atraviesan todo el proyecto.

| Lo que define el país | Dónde impacta |
|---|---|
| **La fuente externa real** | Qué API existe, qué variables publica y desde qué año (Fase 0, Paso 3) |
| **La moneda** | El formato de los montos en el generador, en SQL y en el dashboard |
| **El calendario** | Feriados y eventos comerciales — no son los mismos en México que en España |
| **La geografía** | Si el modelo lleva `dim_{{LUGAR}}`: regiones, estados, provincias, departamentos |

**La IA tiene que preguntarlo explícitamente**, con estas tres preguntas, y no seguir hasta tenerlas
respondidas:

```
1. ¿En qué país vas a ambientar el proyecto?
   (Normalmente el tuyo, o aquel donde vas a postular: el reclutador que lo lea es de ahí.)
2. ¿En qué moneda operan los montos?
3. ¿Vas a apuntar a ofertas de ese país o de otro?
```

> **Ambientar el proyecto en el país donde se busca trabajo es una ventaja concreta.** Un reclutador
> mexicano entiende de inmediato un proyecto que habla de estados, de pesos y del INEGI. Si el
> estudiante busca trabajo remoto para otro mercado, se ambienta en ese mercado.

**Con eso ya se puede completar el bloque "País" de la Ficha y elegir la fuente externa del Paso 3.**

## Paso 1 — Elegir el rubro

Tres criterios, en orden de importancia:

1. **¿Puedo defenderlo en una entrevista?** Si el estudiante viene de salud, un portfolio de salud
   le da una ventaja narrativa enorme: *"conozco el problema desde adentro"*. La afinidad con la
   experiencia previa vale más que la moda del rubro.
2. **¿Existe una fuente externa real que cruzar?** Si no hay API pública que aporte contexto, el
   rubro se debilita. Ver el catálogo del Paso 3.
3. **¿A qué ofertas de trabajo apunto?** Si postula a retail, un portfolio de retail entra directo.
   Si postula a "analista de datos" genérico, cualquier rubro con buen cruce funciona.

> **Combinar rubros es válido y recomendable.** No hace falta una historia de inicio a fin: puede
> ser un *portafolio de piezas* alrededor de un dominio (KPIs de un área + una automatización + un
> modelo predictivo). Lo que debe existir es un **hilo conductor**: la misma base de datos alimenta
> todo.

## Paso 2 — Elegir el cruce (la decisión de diseño clave)

Todo proyecto necesita **dos** fuentes:

| Fuente | Rol | Puede ser sintética |
|---|---|---|
| **Interna** — el negocio | Los hechos que se miden (ventas, atenciones, envíos…) | ✅ Sí, generada con Faker + NumPy con correlaciones intencionales |
| **Externa** — el contexto | La variable del mundo real que explica las variaciones | ❌ **No.** Debe venir de una API pública real |

**Por qué la interna puede ser sintética:** nadie va a entregar datos reales de su empresa a un
estudiante. Generarlos con distribuciones realistas *y correlaciones intencionales* demuestra que
se entiende el negocio. Se declara abiertamente en el README.

**Por qué la externa debe ser real:** es la prueba de que se sabe consumir una API, manejar errores,
paginación, formatos de fecha y datos que no se controlan. Y es lo que hace el proyecto único.

### Correlaciones intencionales (el truco del dato sintético)

Al generar los datos internos, se inyectan **relaciones que el análisis después va a descubrir**.
Ejemplo del proyecto de referencia (retail, Chile):

- Las ventas bajan cuando sube el dólar (productos importados más caros).
- Las ventas suben en los eventos comerciales del país.
- Los clientes premium son menos sensibles a las variaciones económicas.
- Los productos de entrada son más sensibles a la tasa de desempleo.

> **Los eventos comerciales son locales, y hay que buscar los del país elegido:** CyberDay y
> Black Friday en Chile, **El Buen Fin** en México, **Hot Sale** en Argentina, las **Rebajas** de
> enero y julio en España, el **Día del Shopping** en Colombia. Poner Thanksgiving en un e-commerce
> peruano es exactamente el tipo de detalle que delata un proyecto copiado.

Sin esto, el análisis no encuentra nada y el notebook queda vacío. **Se diseñan las correlaciones
antes de generar los datos**, y se documentan en la Ficha.

> **Honestidad estadística, otra vez:** estas correlaciones las inyecta el propio generador. El
> análisis no descubre una verdad del mundo — **demuestra que el pipeline detecta y cuantifica bien
> una señal cuya magnitud se conocía de antemano.** El estudiante tiene que poder decir esa frase en
> voz alta, y explicar por qué cada relación es plausible en la realidad de su país. Es la diferencia
> entre un portfolio que aguanta una repregunta y uno que se cae en la primera.

## Paso 3 — Elegir la fuente externa real

El catálogo tiene **dos niveles**. Se busca primero en el Nivel 2 (la fuente del país, que da color
local); si no hay, se usa el Nivel 1, que funciona en cualquier parte del mundo.

### Nivel 1 — Fuentes globales (funcionan en los 195 países, sin API key)

Son la **columna vertebral** de la plantilla. Un proyecto construido solo con estas tres ya cumple
el requisito de fuente externa real.

| Fuente | Qué entrega | Granularidad | URL base |
|---|---|---|---|
| **Open-Meteo** | Clima histórico y pronóstico: temperatura, lluvia, viento, humedad | **Diaria u horaria**, desde 1940 | `https://archive-api.open-meteo.com/v1/archive` |
| **Nager.Date** | Feriados oficiales por país y año | Por fecha | `https://date.nager.at/api/v3/PublicHolidays/{{año}}/{{ISO2}}` |
| **Frankfurter** | Tipos de cambio históricos (referencia del BCE) | **Diaria**, días hábiles | `https://api.frankfurter.app` |
| **Banco Mundial** | Macro por país: PIB, inflación, población, desempleo | **Anual** ⚠️ | `https://api.worldbank.org/v2` |
| **OpenAQ** | Calidad del aire por estación | Horaria | `https://api.openaq.org/v3` |
| **CoinGecko** | Precios de criptomonedas | Diaria | `https://api.coingecko.com/api/v3` |

> ⚠️ **Dos trampas de granularidad que hunden el análisis de correlación:**
> - El **Banco Mundial es anual**. Con 2 años de proyecto son **2 puntos**: no se puede correlacionar
>   nada. Sirve como contexto en el README, no como `dim_{{CONTEXTO}}`.
> - **Frankfurter cubre las ~30 monedas del BCE** (USD, EUR, MXN, BRL, GBP, JPY…), pero **no** el peso
>   chileno, el colombiano, el argentino ni el sol peruano. Para esas monedas hay que ir al banco
>   central del país (Nivel 2).
>
> **La regla:** para el módulo de correlación se necesita una serie **diaria o mensual**, nunca anual.

### Nivel 2 — Fuentes nacionales (el color local)

Estas son **candidatas, no promesas**: las APIs públicas cambian de URL, se caen y se rehacen. Hay
que probarlas (ver el protocolo más abajo) antes de comprometer el proyecto con una.

| País | Fuente candidata | Qué entrega | Requiere key |
|---|---|---|---|
| 🇨🇱 Chile | **mindicador.cl** | Dólar, euro, UF, UTM, IPC, IMACEC, desempleo | No |
| 🇲🇽 México | **Banxico SIE** · INEGI | Tipo de cambio, inflación, tasas · indicadores | Sí (gratis) |
| 🇨🇴 Colombia | **datos.gov.co** (Socrata) | TRM (tipo de cambio), datasets del Estado | No |
| 🇵🇪 Perú | **BCRP** (estadísticas) | Tipo de cambio, inflación, actividad | No |
| 🇦🇷 Argentina | **BCRA** · **datos.gob.ar** (API de series) | Tipo de cambio, inflación, series de tiempo | No |
| 🇧🇷 Brasil | **Banco Central (SGS)** | Câmbio, IPCA, Selic | No |
| 🇪🇸 España | **INE** · **Eurostat** · **BCE** | IPC, paro, indicadores europeos | No |
| 🇺🇸 EE.UU. | **FRED** (St. Louis Fed) · BLS | Miles de series macro, diarias y mensuales | Sí (gratis) |
| 🌎 Resto | **Datos abiertos del país** + Nivel 1 | Varía | Varía |

### Nivel 3 — Si el país no está en la tabla

Se busca en este orden, y casi siempre aparece algo en los dos primeros:

1. **El banco central del país.** Casi todos publican series de tipo de cambio e inflación, muchos
   con API abierta. Buscar: `"banco central" {{PAIS}} API series estadísticas`.
2. **El portal de datos abiertos del gobierno.** Suelen correr sobre CKAN o Socrata, que tienen API
   REST estándar. Buscar: `datos abiertos {{PAIS}} API`.
3. **Si no hay nada:** se usa el plan B global (clima + feriados + tipo de cambio). No se abandona el
   proyecto por esto.

### Protocolo de prueba (obligatorio antes de cerrar la Ficha)

Una fuente **no se elige, se aprueba**. Cuatro chequeos, y los cuatro tienen que pasar:

```
1. ¿Responde?          Abrir la URL en el navegador o correr:
                       curl -s "{{ENDPOINT}}" | head -c 500
2. ¿Cubre el período?  La serie tiene que llegar hasta el rango de la Ficha (2 años mínimo).
3. ¿Tiene la granularidad correcta?   Diaria o mensual. Anual NO sirve para correlacionar.
4. ¿Requiere key?      Si pide key: ¿es gratis y se consigue en 5 minutos? Si no, se descarta.
```

**Se pega en la Ficha la respuesta cruda de la API** (los primeros 300 caracteres del JSON). Eso
prueba que se probó, y de paso deja a la vista el formato de fechas que después hay que normalizar.

> Regla de la plantilla: **ninguna fase avanza con una fuente externa "que debería funcionar".**
> El error más caro de todos es descubrir en la Fase 1 que la API no cubre el país o el período.

## Paso 4 — Definir las preguntas de negocio

**Entre 5 y 6.** Cada una debe:
- Nacer de un dolor real de un área (comercial, operaciones, finanzas, CRM…).
- Poder responderse con los datos que se van a tener.
- Mapear a un módulo de análisis del catálogo (§1.3).
- Terminar en una **acción**, no en un gráfico.

Formato obligatorio (tabla, va en `FICHA.md` y en `05_docs/business_case.md`):

| # | Pregunta | Área que la sufre | Módulo | Acción esperada |
|---|---|---|---|---|
| 1 | ¿Qué {{ITEM}} genera el 80% del {{METRICA}}? | Operaciones | Pareto ABC | Priorizar stock/recursos |
| … | | | | |

> **Prueba ácida:** si a la pregunta se le puede responder *"y con eso qué hago"* y no hay respuesta,
> la pregunta no sirve. Se reemplaza.

## Paso 5 — Dibujar el flujo

El estudiante dibuja su propia versión del diagrama de §1.1, con **sus** fuentes, **sus** tablas y
**sus** salidas. En ASCII, dentro de la Ficha. Este dibujo es después el slide 2 del primer post de
LinkedIn y la sección "Arquitectura" del README.

## Paso 6 — Llenar la Ficha

Ver [Anexo A](#anexo-a--ficha-del-proyecto-en-blanco-para-copiar). Se copia, se llena, se revisa.

### Definition of Done — Fase 0

- [ ] **País, moneda y mercado objetivo definidos.**
- [ ] Rubro elegido y justificado en dos frases.
- [ ] Organización ficticia con nombre, tamaño, canales y catálogo definidos.
- [ ] Fuente externa **real** identificada y **aprobada con los 4 chequeos del Paso 3**, con la
      respuesta cruda de la API pegada en la Ficha.
- [ ] Fuente interna definida: entidades, volúmenes, período (mínimo **2 años** para permitir YoY).
- [ ] 3–5 correlaciones intencionales escritas.
- [ ] 5–6 preguntas de negocio, cada una mapeada a un módulo y a una acción.
- [ ] Modelo dimensional esbozado (nombre de las 4–6 tablas).
- [ ] Diagrama de arquitectura dibujado.
- [ ] Nombre del repositorio decidido (`{{rubro}}-analytics-{{pais}}` o similar).

---

# Parte 3 — Fase 0.5: Entorno (instalar y verificar)

**Objetivo:** que todo lo que el proyecto necesita esté instalado, conectado y **probado**, antes de
escribir la primera línea de ETL.
**Entregables:** `SETUP.md`, `00_setup/verificar_entorno.py` en verde, `PROGRESO.md` iniciado.
**Tiempo:** medio día. Menos si ya hay Python; más si es la primera vez que se instala una base de datos.

> **Por qué existe esta fase.** Instalar PostgreSQL en medio del ETL, con un error de conexión
> encima y sin entender si el problema es el código o el puerto, es el momento exacto en que la
> mayoría de los estudiantes abandona. Se instala primero, se verifica, y recién ahí se programa.

## 3.1 Qué se instala y para qué

| Herramienta | Para qué | Obligatorio |
|---|---|---|
| **Python 3.11+** | ETL, generación de datos, análisis | ✅ |
| **Entorno virtual** (`venv`) | Aislar las dependencias del proyecto | ✅ |
| **PostgreSQL 15+** | La base de datos del proyecto | ✅ |
| **Un cliente SQL** (DBeaver, pgAdmin o la extensión de VS Code) | Ver las tablas sin escribir código | ✅ |
| **Git + cuenta de GitHub** | Versionar y publicar el repo | ✅ |
| **VS Code** (o el editor que sea) | Escribir código y notebooks | ✅ |
| **Herramienta de BI** | El dashboard — ver el árbol de decisión de §3.2 | ✅ |
| **Docker Desktop** | Levantar PostgreSQL en un comando, sin instalarlo | Recomendado |
| **Quarto** | Los carruseles de LinkedIn (Fase 6) | Opcional |

**Los comandos exactos, por sistema operativo, están en el [Anexo F](#anexo-f--instalación-del-entorno-comando-por-comando).**

## 3.2 La decisión de la herramienta de BI (árbol)

Esto **depende del sistema operativo**, y hay que resolverlo acá, no en la Fase 3:

```
¿El estudiante tiene Windows?
│
├── SÍ  → Power BI Desktop (gratis). Es la opción por defecto:
│         es la herramienta que más aparece en las ofertas de analista.
│
└── NO (macOS / Linux) → Power BI Desktop NO existe para su sistema. Tres caminos:
    │
    ├── A. Windows en una VM (Parallels, UTM, VirtualBox) o una máquina prestada.
    │      → Sigue teniendo "Power BI" en el CV. Es el camino más pesado.
    │
    ├── B. Otra herramienta de BI, declarada como tal:
    │      · Metabase (Docker, se conecta a Postgres, gratis)
    │      · Looker Studio (web, gratis; conecta a Postgres con conector)
    │      · Tableau Public (gratis; no conecta a Postgres en vivo → se exporta a CSV)
    │      · Streamlit (Python puro; es la opción más natural si ya sabe Python)
    │      → En el CV se pone la herramienta que se usó. No se miente.
    │
    └── C. Power BI Service (versión web) → limitado, no recomendado para este proyecto.
```

> **Regla:** cambiar de herramienta **no cambia el proyecto.** Las cinco capas, el modelo, las
> vistas y las medidas son las mismas; cambia dónde se dibujan. La Parte 6 está escrita en DAX
> (Power BI) porque es el caso más común, y trae la traducción a SQL para las demás.

## 3.3 PostgreSQL: el atajo de Docker

Instalar PostgreSQL a mano en tres sistemas operativos distintos genera tres clases de problemas
distintos. Con Docker es **un archivo y un comando**, igual en todas partes:

```yaml
# 00_setup/docker-compose.yml
services:
  db:
    image: postgres:16
    container_name: {{PROYECTO}}_db
    environment:
      POSTGRES_USER: analista
      POSTGRES_PASSWORD: ${DB_PASSWORD}      # se lee del .env, nunca se escribe acá
      POSTGRES_DB: {{PROYECTO}}
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data      # los datos sobreviven al reinicio
volumes:
  pgdata:
```

```bash
docker compose -f 00_setup/docker-compose.yml up -d    # levantar
docker compose -f 00_setup/docker-compose.yml down     # apagar (los datos quedan)
```

> **Vale la pena aprender esto.** "Levanté la base con Docker" es una frase que suma en una
> entrevista, y son diez minutos. Si aun así el estudiante prefiere el instalador nativo, el Anexo F
> lo cubre.

## 3.4 `verificar_entorno.py` — el checkpoint de la fase

Un solo script que se corre y responde, sin ambigüedad, si se puede avanzar. **Imprime una tabla con
una fila por chequeo, y termina con código de salida 1 si algo falló.**

```
Chequeos que hace:
1. Versión de Python ≥ 3.11
2. Que esté corriendo dentro del entorno virtual (y avisar si no)
3. Que las librerías de requirements.txt estén instaladas e importables
4. Que exista .env y tenga todas las claves de .env.example (sin mostrar los valores)
5. Que PostgreSQL responda: conectar, SELECT version(), cerrar
6. Que se pueda crear y borrar una tabla temporal (permisos de escritura)
7. Que la API externa de la FICHA responda: status 200 y ≥ 1 registro en el rango pedido
8. Que git esté configurado (user.name y user.email)

Salida esperada:
  ✅ Python 3.12.1
  ✅ Entorno virtual activo (.venv)
  ✅ 14/14 librerías instaladas
  ✅ .env completo (8 claves)
  ✅ PostgreSQL 16.2 — conexión OK
  ✅ Permisos de escritura OK
  ✅ API {{FUENTE_EXTERNA}} — 251 registros en 2025
  ✅ Git configurado
  → ENTORNO LISTO. Podés avanzar a la Fase 1.
```

**El chequeo 7 es el más importante:** vuelve a probar la API que se aprobó en la Fase 0, ahora desde
Python y no desde el navegador. Es distinto, y es donde aparecen los problemas de certificados, de
proxy corporativo y de user-agent bloqueado.

## 3.5 `PROGRESO.md` — la bitácora

Se crea acá y se actualiza al cerrar **cada paso** de cada fase. Es lo que permite retomar el
proyecto en otra sesión sin volver a explicar nada:

```markdown
# Progreso — {{PROYECTO}}

## Estado actual
**Fase:** 1 (ETL) · **Paso:** 2 de 4 · **Última sesión:** 2026-03-14

## Bitácora
### Fase 0 — Decidir ✅
- FICHA.md aprobada. Fuente externa: {{FUENTE}} (probada, 251 registros/año).

### Fase 0.5 — Entorno ✅
- Python 3.12, PostgreSQL 16 en Docker, Power BI Desktop.
- `verificar_entorno.py` → 8/8 en verde.

### Fase 1 — ETL 🚧
- [x] Paso 1 — Generador sintético. Verificado: `python 01_etl/generate_ventas_data.py` → 25.431 filas.
- [ ] Paso 2 — Extractor de la API  ← ACÁ VOY
- [ ] Paso 3 — Carga a Postgres
- [ ] Paso 4 — Verificación de carga

## Dudas abiertas
- ¿El forward fill del fin de semana puede sesgar la correlación? Preguntar en la Fase 4.
```

### Definition of Done — Fase 0.5

- [ ] `python 00_setup/verificar_entorno.py` devuelve **todo en verde**.
- [ ] La base responde y se puede crear una tabla desde Python.
- [ ] La API de la Ficha responde **desde Python**, no solo desde el navegador.
- [ ] `.env` existe, está completo y **está en `.gitignore`**; `.env.example` está versionado.
- [ ] Herramienta de BI instalada y abierta al menos una vez.
- [ ] Repo creado en GitHub, con el primer commit hecho.
- [ ] `SETUP.md` documenta lo que se instaló y **con qué comando** (el "yo" del futuro lo agradece).
- [ ] `PROGRESO.md` creado.

---

# Parte 4 — Fase 1: ETL (Python)

**Objetivo:** tener los datos en CSV y cargados en PostgreSQL, de forma reproducible e idempotente.
**Tiempo:** 2 a 3 días.

## Entregables

| Archivo | Qué hace | Puntos de control |
|---|---|---|
| `01_etl/generate_{{HECHO}}_data.py` | Genera el dataset sintético interno con las correlaciones de la Ficha | Semilla fija (`SEED`) para reproducibilidad |
| `01_etl/extract_{{FUENTE_EXTERNA}}.py` | Consume la API real, normaliza y guarda CSV | Reintentos, timeout, logging, validación de rangos |
| `01_etl/load_to_postgres.py` | Carga los CSV a la base con **upsert** | `--tabla X` para cargar una sola; valida conteos |
| `01_etl/verificar_carga.py` | Chequea que lo cargado cuadre con el origen | Filas, nulos en claves, FKs huérfanas |
| `requirements.txt` | Dependencias fijadas | |
| `.env.example` | Variables de entorno, sin valores reales | |
| `logs/` | Un log por corrida | |

## Especificación del generador sintético

```
1. Constantes arriba y visibles: SEED, N_ENTIDADES, N_ITEMS, N_HECHOS, FECHA_INICIO, FECHA_FIN.
2. build_dim_tiempo()       → calendario completo: año, trimestre, mes, día de semana,
                              es_fin_semana, es_feriado, evento_comercial.
3. build_dim_{{ITEM}}()     → catálogo con jerarquía (categoría > subcategoría), precio/costo,
                              atributo que interactúe con el contexto externo (ej. es_importado).
4. build_dim_{{ENTIDAD}}()  → personas con geografía, segmento, fecha de alta, canal de captación.
5. build_serie_contexto()   → serie de la variable externa (o se lee del CSV de la API real).
6. impacto_contexto(...)    → LA FUNCIÓN CLAVE: modula la probabilidad/monto del hecho según
                              el valor del contexto y la sensibilidad del ítem/entidad.
7. build_fact_{{HECHO}}()   → genera los eventos aplicando estacionalidad + eventos + impacto.
8. Exporta a data/raw/*.csv y deja resumen en consola (filas por tabla, rangos de fecha).
```

**Detalle que marca diferencia:** el `impacto_contexto()` no debe ser un ruido aleatorio. Debe ser
una función explícita del valor externo (ej.: si el dólar está a más de 1 desviación estándar sobre
la media, la probabilidad de compra de importados cae un X%). Eso es lo que después el notebook
"descubre" y lo que se cuenta en LinkedIn.

## Especificación del extractor de API

- Función `fetch_serie(indicador, año)` → DataFrame normalizado.
- Manejo de: timeout, `raise_for_status()`, reintentos con espera, respuesta vacía.
- Normalización de fechas a `YYYY-MM-DD` (las APIs entregan formatos raros: ISO con zona,
  `dd-mm-yyyy`, epoch).
- Rellenar días sin dato (fines de semana, feriados) con *forward fill* si la variable es continua
  (ej. el dólar no se publica el domingo, pero el negocio sí vende).
- Validación final: rango de fechas cubierto, sin nulos en la clave, valores dentro de un rango
  plausible.
- Log a `logs/extract_*.log`.

## Especificación de la carga

- Conexión con SQLAlchemy leyendo `.env`.
- **Upsert** (`INSERT … ON CONFLICT (pk) DO UPDATE`), nunca `INSERT` a secas: correr dos veces no
  duplica.
- Orden de carga respetando FKs: dimensiones primero, hechos al final.
- Filtro de integridad: descartar hechos cuya FK no exista en la dimensión, y **reportarlo**.
- Argumento `--tabla` para recargar una sola tabla (esto habilita la actualización diaria).
- Al terminar: tabla de conteos origen vs destino.

### Definition of Done — Fase 1

- [ ] `python 01_etl/generate_*.py` corre limpio y produce los CSV en `data/raw/`.
- [ ] `python 01_etl/extract_*.py` trae datos reales de la API y los valida.
- [ ] `python 01_etl/load_to_postgres.py` carga todo; **correrlo dos veces no cambia los conteos**.
- [ ] `verificar_carga.py` pasa sin errores.
- [ ] Hay logs en `logs/`.
- [ ] `.env` está en `.gitignore` y `.env.example` está versionado.

---

# Parte 5 — Fase 2: SQL (modelo + vistas + automatización)

**Objetivo:** que la lógica de negocio viva junto a los datos, y que Power BI consuma vistas
limpias en vez de tablas crudas.
**Tiempo:** 1 a 1,5 días.

## Entregables

| Archivo | Contenido |
|---|---|
| `01_create_schema.sql` | Esquema, tablas (esquema estrella), PKs, FKs, índices, comentarios |
| `02_create_views.sql` | 4 vistas: la enriquecida, la de KPIs diarios, la de segmentación, la de concentración |
| `03_stored_procedures.sql` | 2–3 SPs: recálculo de segmentación, reporte periódico, refresco de contexto |
| `04_sample_queries.sql` | 6–10 consultas comentadas que responden las preguntas de la Ficha |

## Las cuatro vistas canónicas

Cambian de nombre según el rubro, pero cumplen siempre el mismo rol:

| Vista | Rol | Consume |
|---|---|---|
| `v_{{HECHO}}_enriquecida` | El hecho unido a **todas** sus dimensiones + el contexto del día. La vista principal. | Power BI, notebook |
| `v_kpis_diarios` | Agregación por día: volumen, monto, ticket, entidades únicas + contexto | Power BI (líneas de tiempo) |
| `v_rfm_segmentacion` | Recency / Frequency / Monetary por entidad, con etiqueta de segmento | Power BI (matriz), notebook |
| `v_pareto_{{ITEM}}` | Ranking con % acumulado, para el gráfico de concentración | Power BI, notebook |

## Los procedimientos almacenados

Son la **prueba de "sé automatizar"**, no un adorno:

- `sp_calcular_segmentacion_{{X}}(fecha_corte)` — recalcula los segmentos a una fecha dada.
- `sp_reporte_{{PERIODO}}(mes, año)` — genera el reporte ejecutivo del período.
- *(opcional)* `sp_refrescar_contexto()` — actualiza la dimensión externa.

Y se cierra el círculo con el **flujo de actualización periódica** documentado en el README:

```bash
python 01_etl/extract_{{FUENTE}}.py                            # 1. traer contexto nuevo
python 01_etl/load_to_postgres.py --tabla dim_{{CONTEXTO}}     # 2. upsert (no toca el resto)
psql -c "CALL {{esquema}}.sp_calcular_segmentacion(CURRENT_DATE);"  # 3. recalcular
```
> Automatizable con `cron` (Linux), Programador de Tareas (Windows) o un DAG de Airflow.

### Definition of Done — Fase 2

- [ ] El esquema crea sin errores desde cero, en una base vacía.
- [ ] Hay índices en las columnas que se filtran (fechas, FKs, categoría).
- [ ] Las 4 vistas devuelven filas y no tardan más de 2 segundos.
- [ ] Los SPs corren y se puede demostrar el antes/después.
- [ ] `04_sample_queries.sql` responde, una por una, las preguntas de la Ficha.

---

# Parte 6 — Fase 3: BI (dashboard)

**Objetivo:** el "qué está pasando", en dos páginas. No más.
**Tiempo:** 2 días.

> **Herramienta:** esta parte está escrita para **Power BI**, que es el caso más común y el que más
> piden las ofertas. Si el estudiante eligió otra en la Fase 0.5 (§3.2), **la estructura de las dos
> páginas, los visuales y los KPIs no cambian**: lo único que cambia es el lenguaje de las medidas.
> Cada bloque DAX de acá se puede escribir como una columna calculada en la vista SQL y consumirla
> desde Metabase, Looker Studio o Streamlit sin perder nada.

## Estructura fija: dos páginas

### Página 1 — Dashboard ejecutivo ("¿cómo vamos?")

| Zona | Visual | Contenido |
|---|---|---|
| Fila superior | 5 tarjetas KPI | Total {{METRICA}}, ticket/valor promedio, N° de {{ENTIDAD}}, N° de {{HECHO}}, crecimiento YoY % |
| Centro izq. | Gráfico de líneas | Evolución temporal con comparativa año anterior |
| Centro der. | Pareto | Barras de {{ITEM}} + línea de % acumulado |
| Inferior izq. | Treemap o barras | Distribución por categoría |
| Inferior der. | Mapa | Distribución geográfica |
| Lateral | Slicers | Fecha, categoría, geografía, canal |

### Página 2 — Análisis estratégico ("¿por qué?")

Es la página que cuenta la historia del **cruce con el contexto externo**:

| Visual | Contenido |
|---|---|
| Doble eje | {{METRICA}} vs variable externa, en el tiempo |
| Dispersión | Correlación entre ambas, con línea de tendencia |
| Combo | {{METRICA}} por categoría vs variación del contexto |
| Matriz | Segmentación (RFM o equivalente) |
| Tarjeta | Coeficiente de correlación calculado |

> **La página 2 debe rematar en una frase accionable**, visible en el propio dashboard:
> *"Cuando {{CONTEXTO}} sube X, {{METRICA}} cae Y%. Recomendación: …"*

## Medidas DAX — el set base (se adapta, no se inventa de cero)

```dax
{{METRICA}} Total = SUM(fact_{{HECHO}}[{{columna_monto}}])

{{METRICA}} Año Anterior =
    CALCULATE([{{METRICA}} Total], SAMEPERIODLASTYEAR(dim_tiempo[fecha]))

Crecimiento YoY % =
    DIVIDE([{{METRICA}} Total] - [{{METRICA}} Año Anterior], [{{METRICA}} Año Anterior])

Valor Promedio =
    DIVIDE([{{METRICA}} Total], DISTINCTCOUNT(fact_{{HECHO}}[{{HECHO}}_id]))

{{ENTIDAD}}s Únicos = DISTINCTCOUNT(fact_{{HECHO}}[{{ENTIDAD}}_id])

% Acumulado Pareto =
    VAR ValorItem = [{{METRICA}} Total]
    VAR ValorSuperior =
        CALCULATE([{{METRICA}} Total],
            FILTER(ALL(dim_{{ITEM}}), [{{METRICA}} Total] >= ValorItem))
    RETURN DIVIDE(ValorSuperior, CALCULATE([{{METRICA}} Total], ALL(dim_{{ITEM}})))
```

Se documentan **todas** las medidas en `03_powerbi/measures_documentation.md`, agrupadas por
familia (base, YoY, Pareto, contexto, segmentación, formato de tarjetas), con la explicación de
qué hace cada una en una frase. Ese archivo es, además, materia prima directa para 3 o 4 posts.

## Reglas de diseño

- Conexión a PostgreSQL en **Import** (no DirectQuery) y **contra las vistas**, no las tablas.
- Máximo 6–7 visuales por página. Si hay más, sobra información.
- Una paleta de 4 colores + gris. Nada de arcoíris.
- Títulos que digan la conclusión, no el campo: *"Smartphones concentra el 44% de los ingresos"*,
  no *"Ventas por categoría"*.
- Formato de números localizado (separador de miles, moneda, sin decimales en las tarjetas).

### Definition of Done — Fase 3

- [ ] Dos páginas, con la relación entre tablas bien definida (estrella, filtro unidireccional).
- [ ] Todas las medidas documentadas en `measures_documentation.md`.
- [ ] Capturas exportadas a PNG (van al README y a LinkedIn).
- [ ] El dashboard responde, visualmente, al menos 3 de las preguntas de la Ficha.

---

# Parte 7 — Fase 4: Análisis en Python

**Objetivo:** el "por qué". Lo que el dashboard no puede mostrar.
**Tiempo:** 2 a 3 días.

## Estructura del notebook (`04_analysis/eda_completo.ipynb`)

Bloques numerados, cada uno con **markdown que interpreta el resultado**, no solo código:

| Bloque | Contenido | Salida a `outputs/` |
|---|---|---|
| **0. Setup** | Conexión a PostgreSQL, carga de las vistas, contexto del negocio | — |
| **0.1 Calidad de datos** | Nulos, duplicados, tipos, rangos imposibles | `00_calidad_datos.png` |
| **1. Descriptivo** | Distribuciones, outliers (IQR + boxplot) | `01_distribucion.png` |
| **2. Estacionalidad** | Por mes/día de semana, uplift de eventos vs día normal | `02_estacionalidad.png` |
| **3. Pareto ABC** | Ranking + % acumulado, clasificación A/B/C | `03_pareto.png` |
| **4. Segmentación** | RFM + K-Means, elección de k (codo/silueta) | `04_clusters.png` |
| **5. Contexto externo** | Correlación con la variable real, test de significancia | `05_correlacion.png` |
| **6. Cohortes** | Matriz de retención por cohorte de alta | `06_cohortes.png` |
| **7. Market Basket** | Apriori, reglas con lift y confidence | `07_basket.png` |
| **8. Forecast** | Descomposición + Prophet, proyección con IC 95% | `08_forecast.png` |
| **9. Hallazgos** | 5–7 insights accionables | — |

*(Se toman los bloques correspondientes a los módulos elegidos en la Ficha, no todos.)*

## La regla del hallazgo

Cada hallazgo, en el notebook y en `05_docs/insights_findings.md`, se escribe con **tres partes**:

```markdown
## Hallazgo N — [Titular con la conclusión, no el método]

**Dato:** [el número, con su medida. Tablas si aplica.]

**Interpretación:** [qué significa para el negocio, en 2–3 frases. Incluye los matices:
si la correlación es débil, se dice que es débil.]

**Acción recomendada:**
- [Acción concreta, con área responsable y plazo si aplica]
- [Otra]
```

> **Honestidad estadística:** si el resultado es "no hay correlación", **ese es el hallazgo** y hay
> que escribirlo. El proyecto de referencia encontró r = −0,06 entre dólar y ventas, lo reportó como
> impacto débil y construyó la recomendación sobre eso ("no reaccionar con descuentos ante
> variaciones puntuales"). Eso es más creíble que un r = 0,9 inventado.

## Detalle no obvio: los PNG son un activo

Los gráficos de `04_analysis/outputs/` se reutilizan en el README, en `insights_findings.md` y en
los carruseles de LinkedIn. Vale la pena que salgan con la **misma paleta** que el dashboard y con
títulos autoexplicativos. Se guardan a 150 dpi mínimo.

### Definition of Done — Fase 4

- [ ] El notebook corre de arriba a abajo sin errores, en un kernel limpio.
- [ ] Cada bloque tiene una celda markdown que **interpreta** el resultado.
- [ ] Los PNG están en `outputs/` con la paleta del proyecto.
- [ ] `insights_findings.md` tiene 5–7 hallazgos con el formato dato/interpretación/acción.
- [ ] Hay al menos un hallazgo contraintuitivo o negativo (le da credibilidad al conjunto).

---

# Parte 8 — Fase 5: Documentación y vitrina

**Objetivo:** que un reclutador entienda el proyecto en 90 segundos sin abrir un solo archivo de código.
**Tiempo:** 1 día.

## `README.md` — la estructura que funciona

```markdown
# {{ORG}} — {{PROYECTO}}
[badges: Python, PostgreSQL, Power BI, Jupyter, Status]

Una frase de qué es. Una frase del ciclo cubierto.
> **Stack:** …

## Preguntas de Negocio
[tabla: pregunta | técnica | resultado ← con el número concreto]

## Estructura del Proyecto
[árbol de carpetas comentado]

## Setup Rápido
[6 pasos numerados, con los comandos exactos]

## Flujo de Actualización Periódica
[los 3 comandos de la automatización + mención a cron/Airflow]

## Modelo de Datos
[diagrama estrella en ASCII + conteo de tablas/vistas/índices]

## Principales Hallazgos
[6 bullets con el número al frente]

## Herramientas y Técnicas
[tabla: área | herramienta]

## Autor
[nombre, rol, ciudad, LinkedIn, GitHub]

---
*Declaración explícita de qué datos son sintéticos y cuáles reales, con la fuente.*
```

**La tabla de "Preguntas de Negocio" con el resultado al lado es lo primero que se lee.** Ahí es
donde el reclutador decide si sigue leyendo. Se llena con números reales del análisis.

## Los tres documentos de `05_docs/`

| Documento | Rol | Audiencia |
|---|---|---|
| `business_case.md` | Contexto de la organización, el desafío, las preguntas, el stack y **las limitaciones** | Reclutador / líder |
| `data_dictionary.md` | Cada tabla, cada columna, tipo, descripción y ejemplo | Técnico que audita |
| `insights_findings.md` | Los hallazgos con dato/interpretación/acción + resumen ejecutivo | Todos |

> La sección **"Alcance y limitaciones"** del business case (qué queda fuera, qué datos son
> sintéticos, qué no se puede concluir) es contraintuitiva pero suma: demuestra criterio.

## Vitrina opcional pero de alto retorno

- **`index.html`** — landing de una página con GitHub Pages: título, arquitectura, capturas del
  dashboard, hallazgos, enlaces. Es el link que se pega en el CV.
- **Capturas del dashboard** en el README (un reclutador no va a instalar Power BI).
- **Repo público con nombre serio:** `{{rubro}}-analytics-{{pais}}`, no `proyecto-final-v3`.

### Definition of Done — Fase 5

- [ ] README completo, con capturas y números reales.
- [ ] Los tres documentos de `05_docs/` escritos.
- [ ] Repo público, con LICENSE y sin secretos en el historial de git.
- [ ] Un tercero clona y llega al dashboard siguiendo solo el README.
- [ ] El proyecto está en el CV y en el "Destacado" del perfil de LinkedIn.

---

# Parte 9 — Fase 6: Sistema de contenido en LinkedIn

**Objetivo:** que el proyecto trabaje durante meses, no una semana. Cada pieza del repo es un post.
**Tiempo:** 1 día de montaje del sistema + ~2 horas por post.

## 8.1 La idea del sistema

Cada post se arma en **un solo archivo** `carrusel.qmd`: texto de los slides + gráficos Python
inline. Se edita, se corre `quarto render` y sale el PDF cuadrado (1080×1080) listo para LinkedIn.
El caption vive aparte en `texto.md`.

**Todo es texto plano y código.** Nada de diseñar a mano en Canva cada vez: se itera y se recompila.
La marca visual (colores, tipografías, funciones de slide) vive en un solo lugar compartido.

> **Alternativa sin Quarto:** si el estudiante no quiere instalar Quarto/Typst, el mismo sistema
> funciona con una plantilla de Canva/Figma + los PNG de `04_analysis/outputs/`. Se pierde la
> reproducibilidad, se gana simplicidad. El resto del sistema (voz, calendario, medición) es igual.

## 8.2 Las cuatro piezas del sistema

### a) `guia-voz.md` — el tono
Es la **fuente de verdad de la voz**, y solo de la voz: el tema y los ejemplos salen siempre del
proyecto. Debe contener:

- **Cómo escribo** — 3–4 frases en primera persona.
- **Objetivo de cada post** — a quién le habla (¿reclutadores? ¿pares? ¿líderes no técnicos?).
- **Reglas firmes** — p. ej. *"no inventar métricas que no estén en el proyecto"*, *"explicar cada
  término técnico en una frase"*.
- **Patrones a evitar (suenan a IA)** — frases-eslogan, simetrías forzadas ("no es X, es Y"), tríos
  perfectos, cadenas de frases cortísimas, exceso de guiones largos y emojis, tono motivacional.
- **Estructura del texto** — contexto real → desarrollo → cierre con reflexión genuina + pregunta
  suave → separación visual para móvil → 4–6 hashtags.
- **Chequeo final** — *"¿suena a algo que yo escribiría o a IA genérica?"*

> Esta guía se escribe **una vez, a mano, con las palabras del estudiante**. Si se la escribe la IA,
> los posts van a sonar a IA. Un buen atajo: que el estudiante escriba un WhatsApp largo explicando
> su proyecto a un amigo, y de ahí se extraen las reglas de su voz real.

### b) `calendario.md` — qué se publica y cuándo

- **Cadencia:** 2 posts por semana (lunes y miércoles funciona bien). Sostenible durante 3 meses.
- **Pilares:** rotarlos para no aburrir. Con este proyecto salen cuatro naturales:
  **Power BI · SQL · Python · Negocio/storytelling** (+ **Marca** para el post ancla).
- **Tabla de publicados** (N, fecha, día, tema, pilar, formato) + **backlog** de temas.

### c) `prompt-maestro.md` — cómo se genera cada post
Un prompt fijo donde solo cambia `[TEMA]` y el bloque de **contenido técnico** (que se pega desde el
proyecto). Le pide a la IA: idea central → post completo → carrusel → archivos de salida. Y le
recuerda: **la voz sale de `guia-voz.md`; el contenido sale del proyecto, nunca de la imaginación.**

### d) `rendimiento/` — la medición
`seguimiento.csv` con una fila por post:

```
num, fecha, pilar, tema, formato, variante, impresiones, interacciones,
comentarios, guardados, clics, seguidores_nuevos
```

Y un reporte (`analisis.qmd`) que calcula **tasa de engagement** (interacciones ÷ impresiones) y
compara por pilar y por variante. Se mira:
- **Guardados y clics:** señal de contenido útil y de alta intención (más valiosa que los "me gusta").
- **Engagement por pilar:** qué tema resuena, para hacer más de eso.
- **Evolución en el tiempo.**

Se puede correr un **A/B direccional** (no controlado, porque los temas difieren): p. ej. variante A
= visual fuerte en el slide 2; variante B = portada reforzada. Da una señal, no una prueba.

## 8.3 El generador de temas (de repo a calendario)

**Cada artefacto del proyecto es, al menos, un post.** Esta tabla convierte el repo en ~20 temas,
que a 2 por semana son 10 semanas de contenido:

| Pilar | Tema | Sale de |
|---|---|---|
| Marca | Presentación del proyecto (el ancla) | README + diagrama |
| Marca | La arquitectura del flujo, explicada simple | §1.1 de la Ficha |
| Python | Conectarse a una API pública paso a paso | `extract_*.py` |
| Python | Generar datos sintéticos que se parezcan a la realidad | `generate_*.py` |
| Python | Limpieza y preparación (el 90% del trabajo) | ETL |
| Python | Unir muchos archivos con pandas + glob | ETL |
| Python | Logs y reintentos: qué pasa cuando la API falla | `extract_*.py` |
| SQL | Cómo leer un query paso a paso | `04_sample_queries.sql` |
| SQL | Qué es una vista y por qué te salva el informe | `02_create_views.sql` |
| SQL | Modelo estrella: por qué le da estabilidad al reporte | `01_create_schema.sql` |
| SQL | Procedimientos almacenados y automatización | `03_stored_procedures.sql` |
| SQL | Segmentación RFM explicada sin tecnicismos | vista RFM |
| Power BI | Formas de mostrar un KPI (y cuál elegir) | Página 1 |
| Power BI | Visualizaciones comunes y cuándo usar cada una | Página 1 |
| Power BI | DAX time intelligence: comparar contra el año anterior | medidas YoY |
| Power BI | El 90% del informe ocurre antes de abrir Power BI | modelo + vistas |
| Análisis | Pareto: dónde se concentra el valor | Bloque 3 |
| Análisis | Cohortes: cuánta gente vuelve | Bloque 6 |
| Análisis | Forecast: tendencia y estacionalidad | Bloque 8 |
| Negocio | **El insight central** del proyecto (el cruce con el contexto) | Bloque 5 |
| Negocio | Cuando el dato dice "no hay efecto": cómo se reporta eso | Hallazgo negativo |
| Negocio | IA en el análisis de datos: qué cambia y qué no | Experiencia propia |

## 8.4 Flujo para producir el post N

1. Elegir el tema del `calendario.md`.
2. Abrir `prompt-maestro.md`, pegar el extracto técnico del proyecto correspondiente.
3. Redactar `texto.md` (el caption) siguiendo `guia-voz.md`.
4. Escribir `carrusel.qmd` — lo más rápido es copiar el del post anterior y cambiar el contenido.
5. `quarto render carrusel.qmd` → sale `carrusel.pdf`.
6. Publicar, y al día siguiente registrar métricas en `rendimiento/seguimiento.csv`.
7. Actualizar la fila en `calendario.md`.

### Definition of Done — Fase 6

- [ ] `guia-voz.md` escrita **con las palabras del estudiante**, no de la IA.
- [ ] Calendario con los primeros 8 temas y fechas.
- [ ] Plantilla visual (estilo compartido) definida y funcionando.
- [ ] Post ancla publicado (el de presentación del proyecto).
- [ ] `seguimiento.csv` creado, con la rutina semanal de registro agendada.

---

# Parte 10 — Cronograma, checklist maestro y errores comunes

## Cronograma

| Fase | Entregable | Tiempo |
|---|---|---|
| **0. Decidir** | `FICHA.md` aprobada (país, rubro, fuente probada) | 0,5 – 1 día |
| **0.5. Entorno** | Stack instalado + `verificar_entorno.py` en verde | 0,5 día |
| **1. ETL** | Datos generados, extraídos y cargados | 2 – 3 días |
| **2. SQL** | Esquema, vistas, SPs, queries | 1 – 1,5 días |
| **3. BI** | Dashboard de 2 páginas + medidas documentadas | 2 días |
| **4. Análisis** | Notebook + hallazgos | 2 – 3 días |
| **5. Documentación** | README, docs, repo público, landing | 1 día |
| **6. Contenido** | Sistema de posts montado + post ancla | 1 día |
| | **Total** | **10,5 – 13,5 días** de trabajo enfocado |

Repartido en tiempo real (con trabajo o estudios en paralelo): **4 a 6 semanas**.

## Checklist maestro

**El proyecto está listo para mostrar cuando:**

- [ ] Un extraño clona el repo, sigue el README y llega al dashboard sin preguntar nada.
- [ ] El ETL corre dos veces sin duplicar datos.
- [ ] Hay al menos una fuente de datos **real** vía API.
- [ ] El dashboard responde 3+ preguntas de la Ficha.
- [ ] El notebook tiene 5–7 hallazgos con acción recomendada.
- [ ] Al menos un hallazgo es negativo o contraintuitivo.
- [ ] Está declarado qué datos son sintéticos.
- [ ] El estudiante puede explicar **cada archivo** del repo sin mirar.
- [ ] El proyecto está en el CV, en el perfil de LinkedIn y en un post ancla.

## Los diez errores que hunden un portfolio

1. **Empezar a programar sin la Ficha.** Se termina con un dashboard bonito que no responde nada.
2. **Empezar el ETL sin el entorno verificado.** El primer error de conexión se confunde con un error
   de código, y ahí se abandona.
3. **Copiar la fuente externa del ejemplo sin probarla en el propio país.** La API del ejemplo puede
   no cubrir el país del estudiante, no llegar al período o haber cambiado de URL. Se prueba **antes**
   (Fase 0, Paso 3), no en medio de la Fase 1.
4. **Solo datos sintéticos.** Sin una fuente real, no se demostró consumir una API.
5. **Datos sintéticos sin correlaciones intencionales.** El análisis no encuentra nada y el notebook
   queda vacío.
6. **Un dataset de Kaggle sin transformar.** Lo tienen 10.000 postulantes más.
7. **Dashboard de 6 páginas.** Nadie las mira. Dos, bien hechas.
8. **Gráficos sin conclusión.** Un título que dice "Ventas por mes" no aporta nada. El título es la
   conclusión.
9. **Inventar métricas para que suenen mejor.** Se cae en la primera pregunta de la entrevista.
10. **Publicarlo una vez y olvidarlo.** El proyecto es materia prima para 20 posts durante 3 meses.

---

# Anexo A — Ficha del Proyecto (en blanco, para copiar)

> Copiar este bloque a `FICHA.md` en la raíz del nuevo proyecto y completarlo.
> **Ninguna fase avanza hasta que esta ficha esté completa.**

````markdown
# Ficha del Proyecto — {{PROYECTO}}

## 0. País y contexto  ← se llena PRIMERO

| Campo | Valor |
|---|---|
| **País** | (dónde se ambienta el proyecto) |
| **Código ISO-2** | (CL, MX, CO, PE, AR, ES, US… lo pide la API de feriados) |
| **Moneda** | (símbolo y código: $ CLP, $ MXN, € EUR…) |
| **Mercado al que apunta** | (¿busca trabajo en ese país, en otro, o remoto?) |
| **Geografía del modelo** | (regiones / estados / provincias / departamentos) |
| **Idioma del proyecto** | (el del código, los comentarios y la documentación) |

## 1. Identidad

| Campo | Valor |
|---|---|
| **Estudiante** | |
| **Rubro** | |
| **Por qué este rubro** | (2 frases: afinidad, ofertas a las que apunta) |
| **Organización ficticia** | Nombre, año de fundación, tamaño |
| **Nombre del repositorio** | `{{rubro}}-analytics-{{pais}}` |
| **Pregunta central del proyecto** | Una sola frase, la que da sentido a todo |
| **La historia en una línea** | "Soy analista de datos. Me pidieron entender X. Crucé Y con Z y descubrí…" |

## 2. Fuentes de datos

### 2.1 Fuente externa REAL (obligatoria)
| Campo | Valor |
|---|---|
| API | |
| Endpoint base | |
| Nivel | Nacional (Nivel 2) / Global (Nivel 1) |
| Variables que trae | |
| Frecuencia | **Diaria / mensual.** Anual NO sirve para correlacionar. |
| Período que cubre | (¿llega hasta el rango de la §2.2?) |
| Para qué sirve en el análisis | |
| ¿Requiere key? | |
| **Prueba** | Pegar acá los primeros ~300 caracteres de la respuesta cruda: |

```json
{ ... respuesta real de la API, copiada del navegador o de curl ... }
```

### 2.2 Fuente interna (sintética o dataset público)
| Campo | Valor |
|---|---|
| Origen | Sintética (Faker + NumPy) / Dataset público / Mixta |
| Período | Mínimo **2 años completos** (para permitir comparación año a año) |
| Volumen de hechos | ~N transacciones/eventos |
| Volumen de entidades | ~N personas |
| Volumen de ítems | ~N productos/servicios |
| Geografía | |

### 2.3 Correlaciones intencionales (3–5)
Lo que el generador va a inyectar y el análisis va a "descubrir":
1.
2.
3.

## 3. Modelo dimensional

| Rol | Tabla | Columnas clave |
|---|---|---|
| HECHO | `fact_` | |
| QUIÉN | `dim_` | |
| QUÉ | `dim_` | |
| CUÁNDO | `dim_tiempo` | |
| DÓNDE | `dim_` | |
| CONTEXTO | `dim_` | |

## 4. Preguntas de negocio (5–6)

| # | Pregunta | Área | Módulo de análisis | Acción esperada |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

## 5. Módulos de análisis elegidos
- [ ] Calidad y outliers *(obligatorio)*
- [ ] Pareto / ABC
- [ ] RFM + Clustering
- [ ] Cohortes
- [ ] Market Basket
- [ ] Forecast
- [ ] Correlación con contexto externo *(muy recomendado)*
- [ ] Churn / riesgo

## 6. Arquitectura (dibujo del flujo)

```
[dibujar aquí en ASCII: fuentes → ETL → base → BI + análisis → narrativa]
```

## 7. Stack y entorno

| Capa | Herramienta | Por qué |
|---|---|---|
| Generación | | |
| Extracción | | |
| Base | | |
| Transformación | | |
| Visualización | | ← depende del SO: ver el árbol de la Fase 0.5 (§3.2) |
| Análisis | | |

| Campo | Valor |
|---|---|
| **Sistema operativo del estudiante** | Windows / macOS / Linux |
| **Herramienta de BI elegida** | Power BI / Metabase / Looker Studio / Streamlit / otra |
| **PostgreSQL** | Docker / instalación nativa / servicio en la nube |

## 8. Alcance y limitaciones

**Dentro:**
**Fuera:**
**Limitaciones de los datos:**

## 9. Aprobación
- [ ] **País, moneda y mercado objetivo definidos.**
- [ ] La fuente externa pasó los **4 chequeos** del Paso 3, y la respuesta cruda está pegada arriba.
- [ ] La serie externa es **diaria o mensual** (no anual).
- [ ] Cada pregunta termina en una acción concreta.
- [ ] El período cubre al menos 2 años.
- [ ] Las correlaciones intencionales están escritas.
- [ ] La herramienta de BI es compatible con el sistema operativo del estudiante.
````

---

# Anexo B — Árbol de archivos completo (bootstrap)

Para que una IA (o el estudiante) levante el esqueleto vacío del proyecto en un paso. Todos los
archivos se crean con su encabezado y un `TODO:` que apunta a la sección correspondiente de este
documento.

```
{{PROYECTO}}/
├── FICHA.md                            ← Anexo A, completado
├── SETUP.md                            ← Fase 0.5: qué se instaló y con qué comando
├── PROGRESO.md                         ← bitácora (§3.5). Se actualiza en cada paso.
├── README.md                           ← Parte 8
├── requirements.txt                    ← Fase 0.5
├── .env.example                        ← Fase 0.5
├── .gitignore                          ← incluye: .env, data/raw/fact_*.csv, logs/, __pycache__/
├── LICENSE                             ← MIT
├── index.html                          ← Parte 8 (opcional)
│
├── 00_setup/
│   ├── verificar_entorno.py            ← el checkpoint de la Fase 0.5
│   └── docker-compose.yml              ← PostgreSQL en un comando
│
├── 01_etl/
│   ├── generate_{{HECHO}}_data.py
│   ├── extract_{{FUENTE_EXTERNA}}.py
│   ├── load_to_postgres.py
│   ├── verificar_carga.py
│   └── documentacion_api.txt           ← cómo funciona la API elegida, en el país elegido
│
├── 02_sql/
│   ├── 01_create_schema.sql
│   ├── 02_create_views.sql
│   ├── 03_stored_procedures.sql
│   └── 04_sample_queries.sql
│
├── 03_bi/                              ← 03_powerbi/ si la herramienta es Power BI
│   ├── {{PROYECTO}}.pbix
│   ├── measures_documentation.md
│   └── screenshots/
│
├── 04_analysis/
│   ├── eda_completo.ipynb
│   └── outputs/
│
├── 05_docs/
│   ├── business_case.md
│   ├── data_dictionary.md
│   └── insights_findings.md
│
├── data/
│   ├── raw/
│   └── processed/
│
└── logs/
```

**`.gitignore` mínimo:**
```
.env
__pycache__/
*.pyc
logs/*.log
data/raw/fact_*.csv          # el archivo de hechos puede ser pesado
.ipynb_checkpoints/
```

---

# Anexo C — Prompts por fase (copiar y pegar)

Todos asumen que la IA tiene acceso a `FICHA.md` y a este documento.

> **Los prompts terminan todos con la misma línea**, y no es un adorno: es lo que activa el
> protocolo de acompañamiento de la Parte 0. Si se borra esa línea, la IA escribe los cuatro
> archivos de una vez y el estudiante se queda con un repo que no sabe explicar.

### Fase 0 — Ayuda a decidir
```
Voy a construir un portfolio de analista de datos siguiendo PLANTILLA_PORTFOLIO_ANALISTA_DATOS.md.

Antes de proponerme nada, hazme las 3 preguntas del Paso 0 (país, moneda, mercado al que apunto).

Mi contexto: [experiencia previa, rubro que me interesa, tipo de ofertas a las que postulo].

Después ayúdame con la Fase 0:
1. Propón 3 opciones de rubro (pueden ser combinaciones), cada una con una fuente externa real que
   EXISTA PARA MI PAÍS (usa el catálogo de dos niveles del Paso 3) y su cruce.
2. Antes de seguir, prueba conmigo la fuente elegida con los 4 chequeos del Paso 3.
3. Para el rubro que más se ajuste: 5-6 preguntas de negocio con su módulo de análisis y su acción.
4. Propón el modelo dimensional y 3-5 correlaciones intencionales.
5. Dibuja el diagrama de arquitectura.

No escribas código todavía. Entrégame la FICHA.md lista para revisar.
```

### Fase 0.5 — Entorno
```
Lee FICHA.md y la Parte 3.

Guíame para dejar el entorno listo. Trabajamos así:
1. Pregúntame qué sistema operativo tengo y qué tengo ya instalado. No supongas nada.
2. Con eso, dime cuál es el árbol de decisión de mi herramienta de BI (§3.2) y ayúdame a elegir.
3. Dame los comandos del Anexo F que me tocan, DE A UNO. Después de cada uno espera mi salida.
4. Cuando estén todos, escribe 00_setup/verificar_entorno.py y córrelo conmigo hasta que dé verde.
5. Escribe SETUP.md con lo que realmente instalamos, y crea PROGRESO.md.

Si algo falla, diagnostícalo conmigo: no me des un comando alternativo sin explicarme qué pasó.
```

### Fase 1 — ETL
```
Lee FICHA.md y la Parte 4.

Construye la capa ETL, UN PASO A LA VEZ:
1. generate_{{HECHO}}_data.py — con SEED fija y las correlaciones intencionales de la ficha.
2. extract_{{FUENTE}}.py — con reintentos, timeout, normalización de fechas, validación y logging.
3. load_to_postgres.py — con upsert idempotente, orden por FK, argumento --tabla y validación de conteos.
4. verificar_carga.py

Explícame el impacto_contexto() ANTES de escribirlo, para que yo lo pueda defender.
Al terminar cada script: dame el comando para correrlo, espera mi salida, y actualiza PROGRESO.md.
```

### Fase 2 — SQL
```
Lee FICHA.md y la Parte 5.

Escribe los 4 scripts de 02_sql/: esquema estrella con índices y comentarios, las 4 vistas
canónicas, 2-3 stored procedures y 6-10 queries de ejemplo que respondan las preguntas de la ficha.

Cada query debe llevar un comentario arriba con la pregunta de negocio que responde.
Vamos archivo por archivo: yo lo corro contra mi base y te pego el resultado antes de seguir.
```

### Fase 3 — BI
```
Lee FICHA.md y la Parte 6.

Mi herramienta de BI es: [la de la ficha].

Genera 03_bi/measures_documentation.md con:
- La conexión a PostgreSQL contra las vistas.
- Todas las medidas agrupadas por familia, cada una con su explicación en una frase.
  (Si uso Power BI: en DAX. Si uso otra herramienta: como columnas/agregaciones sobre las vistas.)
- La especificación visual de las 2 páginas (qué visual, dónde, con qué campos).
- Los slicers y el formato recomendado, con la moneda y el separador de miles de mi país.

El dashboard lo armo yo siguiendo esa especificación. Guíame página por página.
```

### Fase 4 — Análisis
```
Lee FICHA.md y la Parte 7.

Construye 04_analysis/eda_completo.ipynb con los módulos elegidos en la ficha.
Cada bloque: código + celda markdown que interpreta el resultado + PNG a outputs/.
Al final, 5-7 hallazgos con formato dato / interpretación / acción recomendada.

Vamos bloque por bloque: yo lo ejecuto y te pego la salida antes de que escribas el siguiente.
Si un resultado es débil o negativo, repórtalo como tal. No inflar conclusiones.
```

### Fase 5 — Documentación
```
Lee todo el proyecto y la Parte 8.

Escribe README.md, 05_docs/business_case.md, data_dictionary.md e insights_findings.md,
usando los números reales que salieron del notebook (no inventes ninguno).
Incluye la declaración explícita de qué datos son sintéticos y cuáles reales.
```

### Fase 6 — Sistema de contenido
```
Lee la Parte 9.

Monta el sistema de posts en post/:
- La estructura de carpetas y el _quarto.yml.
- calendario.md con los primeros 8 temas derivados de mi proyecto (usa el generador de temas).
- prompt-maestro.md.
- La plantilla visual compartida.

La guia-voz.md la escribo yo. Hazme 6 preguntas para ayudarme a definirla.
```

### Retomar el proyecto después de una pausa
```
Lee PROGRESO.md, FICHA.md y PLANTILLA_PORTFOLIO_ANALISTA_DATOS.md.

Dime en qué fase y en qué paso quedé, qué fue lo último que verifiqué y qué sigue.
Antes de escribir nada, hazme correr el checkpoint del último paso cerrado, para confirmar que el
proyecto sigue en pie (entorno, base, datos).
```

### Post N (uso recurrente)
```
[usar prompt-maestro.md, con el tema del calendario y el extracto técnico pegado del proyecto]
```

---

# Anexo D — Tres proyectos de ejemplo, en tres países

Tres rubros, tres países, tres fuentes externas distintas. **El esqueleto es idéntico en los tres.**
Fijarse en un detalle: el país no cambia solo la ambientación — cambia qué API existe.

## D1 — Salud, 🇲🇽 México: "Demanda de urgencias, calor y contaminación"

| Campo | Valor |
|---|---|
| **Organización** | Red de centros de urgencia, 4 sedes en la Ciudad de México |
| **Pregunta central** | ¿Cómo el calor y la contaminación anticipan la demanda de urgencias, y cómo dimensionamos turnos? |
| **Fuente externa real** | Open-Meteo (temperatura, humedad) + OpenAQ (PM2.5) — **ambas globales, sirven en cualquier ciudad del mundo** |
| **Fuente interna** | Sintética: 2 años, ~40.000 atenciones, 12.000 pacientes, 60 prestaciones. Montos en MXN |
| **Modelo** | `fact_atenciones` · `dim_paciente` · `dim_prestacion` · `dim_tiempo` · `dim_sede` · `dim_clima` |
| **Correlaciones intencionales** | Las consultas respiratorias suben con PM2.5 alto y con frío; los pacientes crónicos son menos sensibles al clima; los lunes concentran la demanda acumulada del fin de semana |
| **Módulos** | Calidad · Pareto (prestaciones por costo) · Cohortes (adherencia a control) · Correlación con clima · Forecast de demanda |
| **Insight central** | "Cuando el PM2.5 supera X por 3 días seguidos, las consultas respiratorias suben Y% con 48h de rezago. Recomendación: reforzar turnos con esa antelación." |

## D2 — Educación, 🇪🇸 España: "Deserción y mercado laboral"

| Campo | Valor |
|---|---|
| **Organización** | Centro de formación profesional online, 8 titulaciones |
| **Pregunta central** | ¿Qué predice el abandono de un estudiante y cuánto influye el mercado laboral de su sector? |
| **Fuente externa real** | INE / Eurostat (tasa de paro por sector y trimestre) — **mensual/trimestral, suficiente para correlacionar** |
| **Fuente interna** | Sintética: 3 años, ~8.000 estudiantes, ~200.000 registros de actividad. Montos en EUR |
| **Modelo** | `fact_actividad` · `dim_estudiante` · `dim_curso` · `dim_tiempo` · `dim_indicadores_laborales` |
| **Correlaciones intencionales** | El abandono sube cuando el paro del sector cae (se van a trabajar); los estudiantes con actividad nocturna retienen más; la cohorte de septiembre retiene mejor que la de enero |
| **Módulos** | Calidad · Cohortes (retención por cohorte de ingreso) · RFM adaptado (actividad) · Churn (abandono) · Correlación con empleo |
| **Insight central** | "El abandono no es por notas: el mejor predictor es la caída de actividad en la semana 3. Recomendación: alerta automática y contacto del tutor." |

## D3 — Logística, 🇨🇴 Colombia: "Tiempos de entrega, lluvia y festivos"

| Campo | Valor |
|---|---|
| **Organización** | Última milla, 3 ciudades, 200 repartidores |
| **Pregunta central** | ¿Qué explica los atrasos y cómo priorizamos zonas y horarios? |
| **Fuente externa real** | Open-Meteo (lluvia, viento) + Nager.Date (festivos de Colombia — **son 18 al año, y eso mueve el volumen**) |
| **Fuente interna** | Sintética: 2 años, ~120.000 envíos, 15.000 clientes, 40 zonas. Montos en COP |
| **Modelo** | `fact_envios` · `dim_cliente` · `dim_zona` · `dim_repartidor` · `dim_tiempo` · `dim_clima` |
| **Correlaciones intencionales** | La lluvia sobre 5 mm agrega 22 min promedio; las zonas periféricas se degradan más rápido; los días previos a un puente festivo el volumen sube 60% |
| **Módulos** | Calidad · Pareto (zonas que concentran los atrasos) · Correlación con clima · Forecast de volumen · Outliers (entregas imposibles) |
| **Insight central** | "El 70% de los atrasos se concentran en 9 de 40 zonas, y la lluvia los duplica. Recomendación: refuerzo dinámico por pronóstico." |

> **Lo que hay que ver en estos tres:** D1 y D3 usan **solo fuentes globales** (clima, aire, feriados).
> Ninguno depende de que exista una API nacional. Ese es el piso garantizado de la plantilla: se puede
> construir un proyecto completo desde cualquier país del mundo con Open-Meteo y Nager.Date.

---

# Anexo E — Glosario de variables

Estas son las variables que se reemplazan en todo el documento al instanciar un proyecto nuevo:

| Variable | Qué es | Ejemplo retail 🇨🇱 | Ejemplo salud 🇲🇽 |
|---|---|---|---|
| `{{PAIS}}` | País donde se ambienta | Chile | México |
| `{{ISO2}}` | Código de 2 letras (lo pide la API de feriados) | `CL` | `MX` |
| `{{MONEDA}}` | Moneda de los montos | CLP | MXN |
| `{{PROYECTO}}` | Nombre del proyecto/repo | `retail-analytics-chile` | `urgencias-clima-cdmx` |
| `{{ORG}}` | Organización ficticia | TechStore.cl | RedUrgencias |
| `{{RUBRO}}` | Sector | Retail / e-commerce | Salud |
| `{{HECHO}}` | El evento que se mide | ventas | atenciones |
| `{{ENTIDAD}}` | El "quién" | cliente | paciente |
| `{{ITEM}}` | El "qué" | producto | prestación |
| `{{LUGAR}}` | El "dónde" | región | sede |
| `{{CONTEXTO}}` | La variable externa | dólar / IPC | temperatura / PM2.5 |
| `{{METRICA}}` | La medida principal | monto vendido | N° de atenciones |
| `{{FUENTE_EXTERNA}}` | La API real | mindicador | open_meteo |
| `{{PERIODO}}` | Granularidad del reporte | mensual | semanal |

---

# Anexo F — Instalación del entorno, comando por comando

Es el material de apoyo de la **Fase 0.5** (Parte 3). La IA que acompañe al estudiante debe darle
**solo los comandos de su sistema operativo, de a uno**, y esperar la salida de cada uno antes de
seguir.

## F.1 Windows

Con **winget**, que viene incluido en Windows 10 y 11 (se corre en PowerShell):

```powershell
winget install Python.Python.3.12
winget install Git.Git
winget install Microsoft.VisualStudioCode
winget install Microsoft.PowerBI                # solo Windows
winget install Docker.DockerDesktop             # opción recomendada para la base
winget install dbeaver.dbeaver                  # cliente SQL

# Alternativa sin Docker: PostgreSQL nativo
winget install PostgreSQL.PostgreSQL.16
```

> **Cerrar y volver a abrir la terminal** después de instalar, o los comandos no se encuentran.

## F.2 macOS

Con **Homebrew** (si no está: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`):

```bash
brew install python@3.12
brew install git
brew install --cask visual-studio-code
brew install --cask docker          # recomendado para la base
brew install --cask dbeaver-community

# Alternativa sin Docker: PostgreSQL nativo
brew install postgresql@16 && brew services start postgresql@16
```

> ⚠️ **Power BI Desktop no existe para macOS.** Acá se aplica el árbol de decisión de §3.2: o se corre
> Windows en una VM, o se elige otra herramienta de BI y se declara. No hay una tercera vía.

## F.3 Linux (Debian / Ubuntu)

```bash
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3-pip git
sudo snap install --classic code
sudo apt install -y docker.io docker-compose-v2 && sudo usermod -aG docker $USER  # relogin después

# Alternativa sin Docker: PostgreSQL nativo
sudo apt install -y postgresql-16
```

> ⚠️ Igual que en macOS: **no hay Power BI Desktop para Linux.** Ver §3.2.

## F.4 El resto, igual en los tres sistemas

```bash
# 1. Entorno virtual (SIEMPRE, nunca instalar librerías al Python del sistema)
python -m venv .venv

# 2. Activarlo
source .venv/bin/activate          # macOS / Linux
.venv\Scripts\Activate.ps1         # Windows (PowerShell)

# 3. Dependencias
pip install -r requirements.txt

# 4. Base de datos con Docker
docker compose -f 00_setup/docker-compose.yml up -d

# 5. Configurar Git (si es la primera vez)
git config --global user.name  "Nombre Apellido"
git config --global user.email "correo@ejemplo.com"

# 6. El checkpoint de la fase
python 00_setup/verificar_entorno.py
```

**`requirements.txt` base** (se ajusta según los módulos elegidos en la Ficha):

```
pandas
numpy
faker
requests
python-dotenv
sqlalchemy
psycopg2-binary
jupyter
matplotlib
seaborn
scikit-learn
statsmodels
prophet                # solo si se eligió el módulo de Forecast
mlxtend                # solo si se eligió Market Basket
```

## F.5 Los cinco errores de instalación que más tiempo cuestan

| Síntoma | Causa casi segura | Solución |
|---|---|---|
| `ModuleNotFoundError` de algo que "ya instalé" | Se instaló fuera del entorno virtual, o la terminal se abrió sin activarlo | Activar el `.venv` y reinstalar. Si el prompt no muestra `(.venv)`, no está activo. |
| `connection refused` en el puerto 5432 | La base no está corriendo | `docker compose ps` (o el servicio de PostgreSQL). Levantarla. |
| `password authentication failed` | El `.env` no coincide con lo que se levantó | Revisar `.env` contra el `docker-compose.yml`. Ojo con espacios al final de la línea. |
| `psycopg2` no compila al instalarse | Falta el compilador de C | Usar `psycopg2-binary`, no `psycopg2`. |
| La API funciona en el navegador pero falla en Python | Proxy corporativo, certificado o user-agent bloqueado | Probar con `curl`; si `curl` anda y Python no, es el `requests` sin headers. |

> **Regla de oro de esta fase:** cada error que se resuelve se anota en `SETUP.md`. Al estudiante le
> va a volver a pasar en tres semanas, en otra máquina, y va a agradecer haberlo escrito.

---

## Cierre

El proyecto de referencia (*Retail Analytics Chile*) es **una instancia** de esta plantilla, no la
plantilla misma. Lo que se reutiliza no es el país, ni el rubro, ni los datos: es el **orden**
(decidir → preparar → construir → publicar), el **esqueleto de cinco capas**, el **modelo genérico
hecho/quién/qué/cuándo/contexto**, los **ocho módulos de análisis**, y el **sistema de contenido**
que convierte el repo en tres meses de presencia profesional.

Un estudiante en Bogotá, en Madrid o en Monterrey construye exactamente el mismo esqueleto: cambia la
API que le da el contexto, cambia la moneda, cambia el calendario. Y termina con algo que puede
defender línea por línea. Ese es el punto.