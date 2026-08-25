# Chile Geografía Histórica

[![CI](https://github.com/alvarosalinaso/chile-geografia-historica/actions/workflows/ci.yml/badge.svg)](https://github.com/alvarosalinaso/chile-geografia-historica/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://python.org)

---

## What is this?

EN: An interactive map of Chile's historical geography. Four layers showing how the country has changed over time: presidents by birthplace, population by region across census decades, key historical events, and provincial boundary evolution.

ES: Un mapa interactivo de la geografía histórica de Chile. Cuatro capas que muestran cómo el país ha cambiado a través del tiempo: presidentes por lugar de nacimiento, población por región en diferentes censos, eventos históricos clave y evolución de límites provinciales.

---

## The four layers

| Layer | What it shows | Data |
|-------|--------------|------|
| **Presidents** | 40+ presidents geolocalized by birthplace, color-coded by era | BCN Historia Política |
| **Demographics** | Population by region, slider by census year (1907-2017) | INE censuses |
| **Events** | ~24 historical events (battles, disasters, political milestones) | Wikipedia/BCN |
| **Boundaries** | Current 16 regional boundaries with province count evolution | GeoJSON INE |

---

## Key findings

- Santiago has always been the political center (most presidents born there)
- The Región Metropolitana concentrates ~40% of Chile's population
- Chile went from 23 provinces (1900) to 54 provinces (2017)
- Earthquake pattern: concentrated in central-south Chile
- Most presidents came from just 3 cities: Santiago, Valparaíso, Concepción

---

## How to run

```bash
git clone https://github.com/alvarosalinaso/chile-geografia-historica
cd chile-geografia-historica
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/analyze_all.py
```

Open `output/chile_historico.html` in your browser.

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
├── Dockerfile
└── requirements.txt
```

---

## Dependencies

```
geopandas>=0.14.0
folium>=0.16.0
pandas>=2.0.0
polars>=1.0.0
requests>=2.31.0
branca>=0.7.0
shapely>=2.0.0
```

---

## Related projects

- [Chilean Video Games](https://github.com/alvarosalinaso/chilean-videogames-analysis) — Market analysis of Chilean indie games
- [Chilean Political Discourse + NLP](https://github.com/alvarosalinaso/geopolitica-textual-nlp) — NLP on presidential speeches
- [Portfolio Web](https://github.com/alvarosalinaso/portfolio-web) — Dashboard with all projects

---

> **Álvaro Salinas Ortiz**
> [LinkedIn](https://www.linkedin.com/in/alvaro-salinas-ortiz) | [Portfolio](https://alvarosalinaso.github.io/portfolio-web/)
