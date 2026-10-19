import csv
import os

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

# Mapeo de regiones históricas (pre-1992) a regiones modernas (post-1992 / 2017)
# Basado en la reorganización administrativa chilena
HISTORIC_TO_MODERN_REGION = {
    # 1907-1970 regions -> modern equivalents
    "Aconcagua": "Valparaíso",  # Se fusionó en Valparaíso
    "Colchagua": "O'Higgins",  # Se convirtió en O'Higgins
    "Cauquenes": "Maule",  # Parte del Maule
    "Talca": "Maule",  # Parte del Maule
    "Linares": "Maule",  # Parte del Maule
    "Ñuble": "Ñuble",  # Ahora es región propia (2018)
    "Concepción": "Biobío",  # Parte de Biobío
    "Arauco": "Biobío",  # Parte de Biobío
    "Biobío": "Biobío",  # Se mantiene
    "Malleco": "La Araucanía",  # Parte de La Araucanía
    "Cautín": "La Araucanía",  # Parte de La Araucanía
    "Valdivia": "Los Ríos",  # Ahora es Los Ríos
    "Osorno": "Los Lagos",  # Parte de Los Lagos
    "Llanquihue": "Los Lagos",  # Parte de Los Lagos
    "Chiloé": "Los Lagos",  # Parte de Los Lagos
    "Aysén": "Aysén",  # Se mantiene
    "Magallanes": "Magallanes",  # Se mantiene
    "Curicó": "Maule",  # Parte del Maule (1970)
    # Regions that map to themselves
    "Tarapacá": "Tarapacá",
    "Antofagasta": "Antofagasta",
    "Atacama": "Atacama",
    "Coquimbo": "Coquimbo",
    "Valparaíso": "Valparaíso",
    "Santiago": "Metropolitana",
    "O'Higgins": "O'Higgins",
}


def map_to_modern_region(region: str, census_year: int) -> str:
    """Mapea nombre de región histórica a región moderna según el año del censo."""
    if census_year >= 1992:
        return region
    return HISTORIC_TO_MODERN_REGION.get(region, region)


# Totales nacionales oficiales por censo (personas, no miles).
# 1907/1940/1970: recopilación del INE publicada por Memoria Chilena (Biblioteca
# Nacional). 1992: INE, "Censo 1992, Resultados Generales" (cuadro 1). 2002: INE,
# síntesis censal 2002. 2017: INE, síntesis de resultados Censo 2017.
NATIONAL_TOTALS = [
    {
        "census_year": 1907,
        "population": 3231022,
        "source": "https://www.memoriachilena.gob.cl/602/w3-article-74943.html",
    },
    {
        "census_year": 1940,
        "population": 5023539,
        "source": "https://www.memoriachilena.gob.cl/602/w3-article-74943.html",
    },
    {
        "census_year": 1970,
        "population": 8884768,
        "source": "https://www.memoriachilena.gob.cl/602/w3-article-74943.html",
    },
    {
        "census_year": 1992,
        "population": 13348401,
        "source": "https://archivopatrimonial.uahurtado.cl/uploads/r/archivo-institucional-universidad-alberto-hurtado/5/b/3/5b391f1b221427792b4a02e33601c4b2d9abb69047d576c6ec18e3f6d27365d8/92-31067.pdf",
    },
    {
        "census_year": 2002,
        "population": 15116435,
        "source": "https://www.ine.gob.cl/docs/default-source/censo-de-poblacion-y-vivienda/publicaciones-y-anuarios/2002/sintesiscensal-2002.pdf",
    },
    {
        "census_year": 2017,
        "population": 17574003,
        "source": "https://www.ine.gob.cl/docs/default-source/censo-de-poblacion-y-vivienda/publicaciones-y-anuarios/2017/publicaci%C3%B3n-de-resultados/sintesis-de-resultados-censo2017.pdf",
    },
]

# Población por región (personas exactas), solo censos con tabla regional
# oficial del INE. Las sumas regionales coinciden exactamente con los totales
# nacionales de NATIONAL_TOTALS. No hay cifras regionales oficiales en formato
# publicado para 1907/1940/1970, así que esas filas se eliminaron en lugar de
# estimarse.
CENSUS = [
    # Censo 1992 (13 regiones) — INE, Resultados Generales Censo 1992
    {"region": "Tarapacá", "census_year": 1992, "population": 339579},
    {"region": "Antofagasta", "census_year": 1992, "population": 410724},
    {"region": "Atacama", "census_year": 1992, "population": 230873},
    {"region": "Coquimbo", "census_year": 1992, "population": 504387},
    {"region": "Valparaíso", "census_year": 1992, "population": 1384336},
    {"region": "Metropolitana", "census_year": 1992, "population": 5257937},
    {"region": "O'Higgins", "census_year": 1992, "population": 696369},
    {"region": "Maule", "census_year": 1992, "population": 836141},
    {"region": "Biobío", "census_year": 1992, "population": 1734305},
    {"region": "La Araucanía", "census_year": 1992, "population": 781242},
    {"region": "Los Lagos", "census_year": 1992, "population": 948809},
    {"region": "Aysén", "census_year": 1992, "population": 80501},
    {"region": "Magallanes", "census_year": 1992, "population": 143198},
    # Censo 2002 (13 regiones) — INE, síntesis censal 2002 / Anuario Est.
    # Regional 2008 (cuadros 2-3)
    {"region": "Tarapacá", "census_year": 2002, "population": 428594},
    {"region": "Antofagasta", "census_year": 2002, "population": 493984},
    {"region": "Atacama", "census_year": 2002, "population": 254336},
    {"region": "Coquimbo", "census_year": 2002, "population": 603210},
    {"region": "Valparaíso", "census_year": 2002, "population": 1539852},
    {"region": "Metropolitana", "census_year": 2002, "population": 6061185},
    {"region": "O'Higgins", "census_year": 2002, "population": 780627},
    {"region": "Maule", "census_year": 2002, "population": 908097},
    {"region": "Biobío", "census_year": 2002, "population": 1861562},
    {"region": "La Araucanía", "census_year": 2002, "population": 869535},
    {"region": "Los Lagos", "census_year": 2002, "population": 1073135},
    {"region": "Aysén", "census_year": 2002, "population": 91492},
    {"region": "Magallanes", "census_year": 2002, "population": 150826},
    # Censo 2017 (16 regiones) — INE, síntesis de resultados Censo 2017
    {"region": "Arica y Parinacota", "census_year": 2017, "population": 226068},
    {"region": "Tarapacá", "census_year": 2017, "population": 330558},
    {"region": "Antofagasta", "census_year": 2017, "population": 607534},
    {"region": "Atacama", "census_year": 2017, "population": 286168},
    {"region": "Coquimbo", "census_year": 2017, "population": 757586},
    {"region": "Valparaíso", "census_year": 2017, "population": 1815902},
    {"region": "Metropolitana", "census_year": 2017, "population": 7112808},
    {"region": "O'Higgins", "census_year": 2017, "population": 914555},
    {"region": "Maule", "census_year": 2017, "population": 1044950},
    {"region": "Ñuble", "census_year": 2017, "population": 480609},
    {"region": "Biobío", "census_year": 2017, "population": 1556805},
    {"region": "La Araucanía", "census_year": 2017, "population": 957224},
    {"region": "Los Ríos", "census_year": 2017, "population": 384837},
    {"region": "Los Lagos", "census_year": 2017, "population": 828708},
    {"region": "Aysén", "census_year": 2017, "population": 103158},
    {"region": "Magallanes", "census_year": 2017, "population": 166533},
]


def collect_census():
    os.makedirs(RAW_DIR, exist_ok=True)
    out = os.path.join(RAW_DIR, "census.csv")
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["region", "census_year", "population", "modern_region"]
        )
        w.writeheader()
        for record in CENSUS:
            modern = map_to_modern_region(record["region"], record["census_year"])
            w.writerow(
                {
                    "region": record["region"],
                    "census_year": record["census_year"],
                    "population": record["population"],
                    "modern_region": modern,
                }
            )
    out_national = os.path.join(RAW_DIR, "census_national.csv")
    with open(out_national, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["census_year", "population", "source"])
        w.writeheader()
        w.writerows(NATIONAL_TOTALS)
    print(f"OK: {len(CENSUS)} regional records -> {out}")
    print(f"OK: {len(NATIONAL_TOTALS)} national records -> {out_national}")


if __name__ == "__main__":
    collect_census()
