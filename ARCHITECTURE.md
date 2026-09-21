# Arquitectura — chile-geografia-historica

## Visión general
Análisis histórico-geográfico de Chile: evolución demográfica (censos 1907-2017), eventos históricos, presidentes, mapas coropléticos y forecasting demográfico.

## Componentes principales

### Datos
- `data/raw/regiones.geojson` — GeoJSON de regiones actuales
- `data/processed/census.csv` — Censos por región (población en miles)
- `data/processed/events.csv` — Eventos históricos (año, tipo, ciudad)
- `data/processed/presidents.csv` — Presidentes (nombre, inicio, fin, lugar_nacimiento)
- `data/export/forecast_results.json` — Proyecciones 2025/2030 + impacto eventos

### Recolección (src/)
- `collect_census.py` — CENSUS hardcodeado (1907, 1940, 1970, 1992, 2002, 2017)
- `collect_events.py` — EVENTS hardcodeado
- `collect_presidents.py` — PRESIDENTS hardcodeado + coordenadas
- `collect_geojson.py` — Descarga GeoJSON de regiones

### Procesamiento
- `combine_layers.py` — Combina capas para mapas
- `map_boundaries.py` — Mapa de fronteras históricas
- `map_demographics.py` — Coropléticos demográficos
- `map_events.py` — Eventos en mapa
- `map_presidents.py` — Presidentes en mapa

### Análisis
- `forecast_analysis.py` — analyze: regresión lineal por región (2025, 2030) + correlación eventos-población
- `analyze_all.py` — Orquestador

### Dashboard
- `dashboard.py` — Dash app con tabs: Censo, Eventos, Presidentes, Mapa, Forecast, Eventos-Población

## Flujo de datos
```
collect_*.py → data/processed/*.csv
forecast_analysis.analyze → data/export/forecast_results.json
dashboard.py carga DATA = load_data() al importar (módulo level)
```

## Despliegue
- Render: `gunicorn dashboard:server` (ver `render.yaml`)

## Problemas conocidos
- `dashboard.py:54` path hardcodeado `data/data/export/` (corregido a `export/`)
- `dashboard.py` carga datos a nivel módulo (difícil de testear)
- Censos pre-1992 usan nombres de regiones antiguas que no matchean GeoJSON moderno
- Forecast con solo 5-6 puntos y regresión lineal a 2030

## Tests
- `tests/test_analysis.py` — Datos hardcodeados (presidents, events, census)
- `tests/test_forecast_analysis.py` — analyze() con mocks
- CI: pytest + coverage + ruff (Python 3.10, 3.11, 3.12)