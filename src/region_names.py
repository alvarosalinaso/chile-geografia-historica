"""Normalización de nombres de región para unir censo ↔ GeoJSON.

El GeoJSON usa nombres largos (p. ej. "Región de Tarapacá") y el censo
nombres cortos/canónicos (p. ej. "Tarapacá"). Sin esta capa el join nunca
matchea y los mapas coropléticos quedan en población 0.
"""

from __future__ import annotations

# Nombres exactos del GeoJSON (data/raw/regiones.geojson) -> canónico corto
GEOJSON_TO_CANONICAL = {
    "Región Metropolitana de Santiago": "Metropolitana",
    "Región de Antofagasta": "Antofagasta",
    "Región de Arica y Parinacota": "Arica y Parinacota",
    "Región de Atacama": "Atacama",
    "Región de Aysén del Gral.Ibañez del Campo": "Aysén",
    "Región de Coquimbo": "Coquimbo",
    "Región de La Araucanía": "La Araucanía",
    "Región de Los Lagos": "Los Lagos",
    "Región de Los Ríos": "Los Ríos",
    "Región de Magallanes y Antártica Chilena": "Magallanes",
    "Región de Tarapacá": "Tarapacá",
    "Región de Valparaíso": "Valparaíso",
    "Región de Ñuble": "Ñuble",
    "Región del Bío-Bío": "Biobío",
    "Región del Libertador Bernardo O'Higgins": "O'Higgins",
    "Región del Maule": "Maule",
}

# Alias de nombres cortos del censo/histórico -> canónico
ALIASES = {
    "Santiago": "Metropolitana",
    "Bío-Bío": "Biobío",
    "Bio Bio": "Biobío",
    "Aysén del Gral. Ibañez del Campo": "Aysén",
    "Magallanes y Antártica Chilena": "Magallanes",
}

_GEOJSON_PREFIXES = ("Región de ", "Región del ", "Región ")


def canonical_region(name: str) -> str:
    """Devuelve el nombre canónico corto de una región."""
    if not name:
        return ""
    if name in GEOJSON_TO_CANONICAL:
        return GEOJSON_TO_CANONICAL[name]
    if name in ALIASES:
        return ALIASES[name]
    for prefix in _GEOJSON_PREFIXES:
        if name.startswith(prefix):
            stripped = name[len(prefix) :]
            if stripped in GEOJSON_TO_CANONICAL.values():
                return stripped
            if stripped in ALIASES:
                return ALIASES[stripped]
            return stripped
    return name


def aggregate_population(census_rows: list[dict], census_year: int) -> dict[str, int]:
    """Suma población por región canónica moderna para un año de censo.

    Usa la columna ``modern_region`` si existe; si no, aplica el mapeo
    histórico→moderno de ``collect_census``. Las unidades históricas que
    colapsan en la misma región moderna se suman explícitamente.
    """
    from collect_census import map_to_modern_region

    totals: dict[str, int] = {}
    for row in census_rows:
        if int(row["census_year"]) != census_year:
            continue
        modern = row.get("modern_region") or map_to_modern_region(
            row["region"], census_year
        )
        key = canonical_region(modern)
        totals[key] = totals.get(key, 0) + int(row["population"])
    return totals
