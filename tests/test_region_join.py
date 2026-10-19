"""Tests A6/B3: el join censo ↔ GeoJSON debe matchear regiones reales."""

import csv
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from region_names import aggregate_population, canonical_region

BASE = os.path.join(os.path.dirname(__file__), "..")
GEOJSON = os.path.join(BASE, "data", "raw", "regiones.geojson")
CENSUS_CSV = os.path.join(BASE, "data", "processed", "census.csv")


def _load_census():
    with open(CENSUS_CSV, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _load_canonical_geojson_names():
    with open(GEOJSON, encoding="utf-8") as f:
        regions = json.load(f)
    return [
        canonical_region(f["properties"].get("Region", "")) for f in regions["features"]
    ]


def test_canonical_region_strips_geojson_prefix():
    assert canonical_region("Región de Tarapacá") == "Tarapacá"
    assert canonical_region("Región del Maule") == "Maule"
    assert canonical_region("Región Metropolitana de Santiago") == "Metropolitana"
    assert canonical_region("Región del Bío-Bío") == "Biobío"
    assert canonical_region("Tarapacá") == "Tarapacá"


def test_join_census_geojson_2017_matches_all_regions():
    """B3: en 2017 las 16 regiones del GeoJSON deben tener población > 0."""
    census = _load_census()
    totals = aggregate_population(census, 2017)
    geo_names = _load_canonical_geojson_names()
    assert len(geo_names) == 16
    matched = [n for n in geo_names if totals.get(n, 0) > 0]
    assert len(matched) == 16


def test_join_historical_census_aggregates_to_modern_regions():
    """A6: unidades históricas que colapsan se suman a la región moderna."""
    rows_1907 = [
        {"region": "Aconcagua", "census_year": 1907, "population": 312},
        {"region": "Valparaíso", "census_year": 1907, "population": 388},
        {"region": "Santiago", "census_year": 1907, "population": 519},
        {"region": "Colchagua", "census_year": 1907, "population": 264},
        {"region": "O'Higgins", "census_year": 1907, "population": 182},
    ]
    totals_1907 = aggregate_population(rows_1907, 1907)
    # Aconcagua (histórica) debe sumarse a Valparaíso
    assert totals_1907["Valparaíso"] == 388 + 312
    # Colchagua (histórica) -> O'Higgins
    assert totals_1907["O'Higgins"] == 264 + 182
    # Santiago (histórica) -> Metropolitana
    assert totals_1907["Metropolitana"] == 519


def test_population_in_persons_exact_official():
    """P4: cifras del INE en personas exactas (no miles)."""
    census = _load_census()
    totals_2017 = aggregate_population(census, 2017)
    # RM 2017 = 7.112.808 personas (INE)
    assert totals_2017["Metropolitana"] == 7112808
    assert sum(totals_2017.values()) == 17574003


def test_regional_sums_match_official_national_totals():
    """P4: la suma regional de 1992/2002/2017 coincide con el total nacional oficial."""
    import csv as _csv

    national_path = os.path.join(BASE, "data", "processed", "census_national.csv")
    with open(national_path, encoding="utf-8") as f:
        national = {
            int(r["census_year"]): int(r["population"]) for r in _csv.DictReader(f)
        }
    assert national == {
        1907: 3231022,
        1940: 5023539,
        1970: 8884768,
        1992: 13348401,
        2002: 15116435,
        2017: 17574003,
    }
    census = _load_census()
    for year in (1992, 2002, 2017):
        regional_sum = sum(
            int(r["population"]) for r in census if int(r["census_year"]) == year
        )
        assert regional_sum == national[year], year


def test_dashboard_map_join_matches_at_least_15_regions():
    """P1: el join real del dashboard (canonical + properties.Region) cubre el mapa."""
    import dashboard

    with open(GEOJSON, encoding="utf-8") as f:
        gj = dashboard.normalize_geojson_regions(json.load(f))
    geo_names = [feat["properties"]["Region"] for feat in gj["features"]]
    assert len(geo_names) == 16

    census = _load_census()
    latest_2017 = [r for r in census if int(r["census_year"]) == 2017]
    totals = {
        canonical_region(r["modern_region"]): int(r["population"]) for r in latest_2017
    }
    matched = [n for n in geo_names if totals.get(n, 0) > 0]
    assert len(matched) >= 15
