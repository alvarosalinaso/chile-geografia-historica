# Chile Geografía Histórica

[![CI](https://github.com/alvarosalinaso/chile-geografia-historica/actions/workflows/ci.yml/badge.svg)](https://github.com/alvarosalinaso/chile-geografia-historica/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://python.org)

---

## Hallazgo principal

**Chile pasó de 3.231.022 habitantes (censo 1907) a 17.574.003 (censo 2017) — 5,4× en 110 años — y la Región Metropolitana concentró el 40,5% de la población en 2017 (7.112.808 personas, INE).** El dashboard muestra esa serie oficial, el coroplético regional (censos 1992-2017) y un forecast lineal con intervalos de confianza y advertencias de extrapolación.

**Captura de pantalla:** ![Dashboard de Chile Geografía Histórica](docs/screenshot.png)

## Qué mide y qué no

| Mide | No mide |
|------|---------|
| Población total y regional en censos oficiales (nacional 1907-2017; regional 1992-2017, personas exactas del INE) | Cifras regionales 1907-1970 (INE no las publica en forma utilizable; se estimaron y se eliminaron en la auditoría 2026-10) |
| Presidentes por ciudad de nacimiento (41, según BCN Historia Política) | Orígenes étnicos, carreras previas o afiliaciones |
| 24 eventos históricos geolocalizados (año, tipo, ciudad, coordenadas) | Causalidad: la serie eventos↔población es asociación entre censos contiguos, no efecto causal |
| Tendencia lineal 2025/2030 con IC 95% (3 puntos por región: 1992-2017) | Predicción real: extrapolación beyond 2017 con n=3 es de alta incertidumbre |
| Fronteras regionales actuales (16, GeoJSON descargado en build) | Cambios de límites provinciales históricos (capa de límites en desuso) |

---

## What is this?

EN: An interactive dashboard of Chile's historical geography: presidents by birthplace, official census population by region, key historical events, and a demographic forecast with explicit uncertainty.

ES: Un dashboard interactivo de la geografía histórica de Chile: presidentes por lugar de nacimiento, población oficial del censo por región, eventos históricos clave y un pronóstico demográfico con incertidumbre explícita.

## The layers

| Layer | What it shows | Data |
|-------|--------------|------|
| **Censo** | Serie nacional 1907-2017 + regional 1992-2017 (personas) | INE |
| **Presidentes** | 41 presidentes geolocalizados por nacimiento | BCN Historia Política |
| **Eventos** | 24 eventos (batallas, desastres, hitos políticos) | BCN/Wikipedia |
| **Mapa** | Coroplético regional, censo más reciente | INE + GeoJSON |
| **Forecast** | Proyección lineal 2025/2030 con IC 95% y warnings | INE (regresión propia) |

---

## How to run

```bash
git clone https://github.com/alvarosalinaso/chile-geografia-historica
cd chile-geografia-historica
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/analyze_all.py       # regenera CSVs y mapas HTML
python src/forecast_analysis.py # regenera data/export/forecast_results.json
python dashboard.py             # dashboard en http://localhost:8052
```

Open `output/chile_historico.html` in your browser for the static map.

---

## Data sources and licenses

- **Region boundaries (GeoJSON):** downloaded at build/run time by `src/collect_geojson.py` from [caracena/chile-geojson](https://github.com/caracena/chile-geojson) (regiones) and [fcortes/Chile-GeoJSON](https://github.com/fcortes/Chile-GeoJSON) (comunas). Neither repository declares a LICENSE, so the file is not committed to this repo (see `.gitignore`); Render's `buildCommand` downloads it automatically.
- **Census:** all population figures are official INE numbers in exact persons.
  - `data/processed/census_national.csv` — national totals: 1907 = 3.231.022; 1940 = 5.023.539; 1970 = 8.884.768 (INE series compiled by [Memoria Chilena](https://www.memoriachilena.gob.cl/602/w3-article-74943.html)); 1992 = 13.348.401 ([INE, Censo 1992, Resultados Generales](https://archivopatrimonial.uahurtado.cl/uploads/r/archivo-institucional-universidad-alberto-hurtado/5/b/3/5b391f1b221427792b4a02e33601c4b2d9abb69047d576c6ec18e3f6d27365d8/92-31067.pdf)); 2002 = 15.116.435 ([INE, síntesis censal 2002](https://www.ine.gob.cl/docs/default-source/censo-de-poblacion-y-vivienda/publicaciones-y-anuarios/2002/sintesiscensal-2002.pdf)); 2017 = 17.574.003 ([INE, síntesis Censo 2017](https://www.ine.gob.cl/docs/default-source/censo-de-poblacion-y-vivienda/publicaciones-y-anuarios/2017/publicaci%C3%B3n-de-resultados/sintesis-de-resultados-censo2017.pdf)).
  - `data/processed/census.csv` — regional rows for 1992, 2002, 2017 only (official INE tables; each year's regional sum equals the national total exactly). The former 1907/1940/1970 regional rows were estimates that summed to the wrong totals (e.g. 1907: 4.250.000 fabricated vs 3.231.022 official) and were removed, not corrected: INE does not publish official historical regional tables in machine-readable form.
- **Events and presidents:** see CSVs in `data/processed/` (sources noted in the scripts that generate them: `src/collect_events.py`, `src/collect_presidents.py`).

### Data corrections (audit 2026-10)

| Record | Was | Now | Source |
|--------|-----|-----|--------|
| Iquique naval event | "Batalla de Iquique", 1866 | "Combate Naval de Iquique", 1879 | [BCN Historia Política](https://www.bcn.cl/historiapolitica/militares/index.html) |
| Atentado contra Pinochet | 1985 | 1986 (7 Sep 1986, Santiago) | [BCN Historia Política](https://www.bcn.cl/historiapolitica/index.html) |
| Tratado de Ancón (1883) | coords in Chile (−27.2, −71.0) | Ancón, Perú (−11.77, −77.18) | Treaty signed in Ancón, Peru |
| Manuel Blanco Encalada (nacimiento) | Santiago, Chile | Buenos Aires, Argentina (1790) | [BCN Historia Política](https://www.bcn.cl/historiapolitica/resenas_biograficas/wiki/Manuel_Blanco_Encalada) |
| Aníbal Pinto (nacimiento) | Concepción | Santiago | [BCN Historia Política](https://www.bcn.cl/historiapolitica/resenas_biograficas/wiki/An%C3%ADbal_Pinto_Garmendia) |

All other event coordinates and presidential birthplaces were reviewed against BCN/INE sources and kept.

---

## Project structure

```
chile-geografia-historica/
├── src/
│   ├── collect_geojson.py       # Download GeoJSON from GitHub
│   ├── collect_presidents.py    # Presidents + birthplace coordinates
│   ├── collect_events.py        # Historical events geolocalized
│   ├── collect_census.py        # INE census data by decade
│   ├── map_presidents.py        # Layer 1: President markers
│   ├── map_demographics.py      # Layer 2: Population choropleth
│   ├── map_events.py            # Layer 3: Event markers
│   ├── map_boundaries.py        # Layer 4: Regional boundaries
│   ├── combine_layers.py        # Combine all 4 layers
│   └── analyze_all.py           # Orchestrator
├── data/
│   ├── raw/                     # GeoJSON files
│   └── processed/               # Presidents, events, census CSVs
├── output/                      # Generated HTML maps
├── tests/
└── requirements.txt
```

---

## Dependencies

```
geopandas>=0.14.0
folium>=0.16.0
pandas>=2.0.0
requests>=2.31.0
branca>=0.7.0
shapely>=2.0.0
scipy>=1.11.0
scikit-learn>=1.3.0
dash>=2.14.0
plotly>=5.18.0
```

Note: the dashboard (`dashboard.py`) needs `dash` and `plotly` (listed in `requirements.txt` and `requirements-render.txt`). `polars` was listed here before but the codebase never uses it.

---

## Related projects

- [Chilean Video Games](https://github.com/alvarosalinaso/chilean-videogames-analysis) — Market analysis of Chilean indie games
- [Chilean Political Discourse + NLP](https://github.com/alvarosalinaso/geopolitica-textual-nlp) — NLP on presidential speeches
- [Portfolio Web](https://github.com/alvarosalinaso/portfolio-web) — Dashboard with all projects

---

> **Álvaro Salinas Ortiz**
> [LinkedIn](https://www.linkedin.com/in/alvaro-salinas-ortiz) | [Portfolio](https://alvarosalinaso.github.io/portfolio-web/)
