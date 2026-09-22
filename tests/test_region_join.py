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
    """A6: el censo histórico colapsa a regiones modernas (unidades sumadas)."""
    census = _load_census()
    totals_1907 = aggregate_population(census, 1907)
    geo_names = _load_canonical_geojson_names()
    # 1907 no tiene Arica y Parinacota ni regiones posteriores separadas
    matched = [n for n in geo_names if totals_1907.get(n, 0) > 0]
    assert len(matched) >= 14
    # Aconcagua (histórica) debe sumarse a Valparaíso
    assert totals_1907["Valparaíso"] >= 388 + 312
    # Santiago (histórica) -> Metropolitana
    assert totals_1907["Metropolitana"] == 519


def test_population_in_thousands_plausible():
    census = _load_census()
    totals_2017 = aggregate_population(census, 2017)
    # RM 2017 ≈ 7.113 millones -> 7113 en miles
    assert totals_2017["Metropolitana"] == 7113
    assert 17000 <= sum(totals_2017.values()) <= 19000
