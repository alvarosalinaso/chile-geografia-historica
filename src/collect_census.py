import csv
import os

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

# Chilean census data by region (selected censuses)
# Source: INE - Instituto Nacional de Estadísticas
# Population in thousands
CENSUS = [
    # 1907 census (7 regions)
    {"region": "Tarapacá", "census_year": 1907, "population": 118},
    {"region": "Antofagasta", "census_year": 1907, "population": 136},
    {"region": "Atacama", "census_year": 1907, "population": 83},
    {"region": "Coquimbo", "census_year": 1907, "population": 266},
    {"region": "Aconcagua", "census_year": 1907, "population": 312},
    {"region": "Valparaíso", "census_year": 1907, "population": 388},
    {"region": "Santiago", "census_year": 1907, "population": 519},
    {"region": "O'Higgins", "census_year": 1907, "population": 182},
    {"region": "Colchagua", "census_year": 1907, "population": 264},
    {"region": "Cauquenes", "census_year": 1907, "population": 122},
    {"region": "Talca", "census_year": 1907, "population": 227},
    {"region": "Linares", "census_year": 1907, "population": 148},
    {"region": "Ñuble", "census_year": 1907, "population": 262},
    {"region": "Concepción", "census_year": 1907, "population": 323},
    {"region": "Arauco", "census_year": 1907, "population": 85},
    {"region": "Biobío", "census_year": 1907, "population": 115},
    {"region": "Malleco", "census_year": 1907, "population": 122},
    {"region": "Cautín", "census_year": 1907, "population": 163},
    {"region": "Valdivia", "census_year": 1907, "population": 183},
    {"region": "Llanquihue", "census_year": 1907, "population": 99},
    {"region": "Chiloé", "census_year": 1907, "population": 107},
    {"region": "Aysén", "census_year": 1907, "population": 8},
    {"region": "Magallanes", "census_year": 1907, "population": 18},
    # 1940 census
    {"region": "Tarapacá", "census_year": 1940, "population": 195},
    {"region": "Antofagasta", "census_year": 1940, "population": 225},
    {"region": "Atacama", "census_year": 1940, "population": 114},
    {"region": "Coquimbo", "census_year": 1940, "population": 353},
    {"region": "Aconcagua", "census_year": 1940, "population": 362},
    {"region": "Valparaíso", "census_year": 1940, "population": 550},
    {"region": "Santiago", "census_year": 1940, "population": 1009},
    {"region": "O'Higgins", "census_year": 1940, "population": 243},
    {"region": "Colchagua", "census_year": 1940, "population": 316},
    {"region": "Cauquenes", "census_year": 1940, "population": 145},
    {"region": "Talca", "census_year": 1940, "population": 281},
    {"region": "Linares", "census_year": 1940, "population": 187},
    {"region": "Ñuble", "census_year": 1940, "population": 314},
    {"region": "Concepción", "census_year": 1940, "population": 454},
    {"region": "Arauco", "census_year": 1940, "population": 107},
    {"region": "Biobío", "census_year": 1940, "population": 167},
    {"region": "Malleco", "census_year": 1940, "population": 148},
    {"region": "Cautín", "census_year": 1940, "population": 249},
    {"region": "Valdivia", "census_year": 1940, "population": 245},
    {"region": "Llanquihue", "census_year": 1940, "population": 157},
    {"region": "Chiloé", "census_year": 1940, "population": 143},
    {"region": "Aysén", "census_year": 1940, "population": 25},
    {"region": "Magallanes", "census_year": 1940, "population": 48},
    # 1970 census (13 regions by then)
    {"region": "Tarapacá", "census_year": 1970, "population": 237},
    {"region": "Antofagasta", "census_year": 1970, "population": 319},
    {"region": "Atacama", "census_year": 1970, "population": 167},
    {"region": "Coquimbo", "census_year": 1970, "population": 444},
    {"region": "Valparaíso", "census_year": 1970, "population": 822},
    {"region": "Santiago", "census_year": 1970, "population": 3227},
    {"region": "O'Higgins", "census_year": 1970, "population": 527},
    {"region": "Colchagua", "census_year": 1970, "population": 350},
    {"region": "Curicó", "census_year": 1970, "population": 239},
    {"region": "Talca", "census_year": 1970, "population": 513},
    {"region": "Linares", "census_year": 1970, "population": 295},
    {"region": "Ñuble", "census_year": 1970, "population": 430},
    {"region": "Concepción", "census_year": 1970, "population": 750},
    {"region": "Arauco", "census_year": 1970, "population": 139},
    {"region": "Biobío", "census_year": 1970, "population": 243},
    {"region": "Malleco", "census_year": 1970, "population": 181},
    {"region": "Cautín", "census_year": 1970, "population": 390},
    {"region": "Valdivia", "census_year": 1970, "population": 304},
    {"region": "Osorno", "census_year": 1970, "population": 300},
    {"region": "Llanquihue", "census_year": 1970, "population": 242},
    {"region": "Chiloé", "census_year": 1970, "population": 149},
    {"region": "Aysén", "census_year": 1970, "population": 66},
    {"region": "Magallanes", "census_year": 1970, "population": 101},
    # 1992 census (13 regions)
    {"region": "Tarapacá", "census_year": 1992, "population": 315},
    {"region": "Antofagasta", "census_year": 1992, "population": 430},
    {"region": "Atacama", "census_year": 1992, "population": 214},
    {"region": "Coquimbo", "census_year": 1992, "population": 527},
    {"region": "Valparaíso", "census_year": 1992, "population": 1370},
    {"region": "Metropolitana", "census_year": 1992, "population": 5223},
    {"region": "O'Higgins", "census_year": 1992, "population": 746},
    {"region": "Maule", "census_year": 1992, "population": 836},
    {"region": "Biobío", "census_year": 1992, "population": 1823},
    {"region": "La Araucanía", "census_year": 1992, "population": 868},
    {"region": "Los Ríos", "census_year": 1992, "population": 344},
    {"region": "Los Lagos", "census_year": 1992, "population": 667},
    {"region": "Aysén", "census_year": 1992, "population": 84},
    {"region": "Magallanes", "census_year": 1992, "population": 143},
    # 2002 census (13 regions)
    {"region": "Tarapacá", "census_year": 2002, "population": 428},
    {"region": "Antofagasta", "census_year": 2002, "population": 514},
    {"region": "Atacama", "census_year": 2002, "population": 254},
    {"region": "Coquimbo", "census_year": 2002, "population": 604},
    {"region": "Valparaíso", "census_year": 2002, "population": 1547},
    {"region": "Metropolitana", "census_year": 2002, "population": 6061},
    {"region": "O'Higgins", "census_year": 2002, "population": 812},
    {"region": "Maule", "census_year": 2002, "population": 915},
    {"region": "Biobío", "census_year": 2002, "population": 1951},
    {"region": "La Araucanía", "census_year": 2002, "population": 942},
    {"region": "Los Ríos", "census_year": 2002, "population": 372},
    {"region": "Los Lagos", "census_year": 2002, "population": 731},
    {"region": "Aysén", "census_year": 2002, "population": 97},
    {"region": "Magallanes", "census_year": 2002, "population": 157},
    # 2017 census (16 regions)
    {"region": "Arica y Parinacota", "census_year": 2017, "population": 226},
    {"region": "Tarapacá", "census_year": 2017, "population": 382},
    {"region": "Antofagasta", "census_year": 2017, "population": 607},
    {"region": "Atacama", "census_year": 2017, "population": 301},
    {"region": "Coquimbo", "census_year": 2017, "population": 757},
    {"region": "Valparaíso", "census_year": 2017, "population": 1855},
    {"region": "Metropolitana", "census_year": 2017, "population": 7113},
    {"region": "O'Higgins", "census_year": 2017, "population": 915},
    {"region": "Maule", "census_year": 2017, "population": 1045},
    {"region": "Ñuble", "census_year": 2017, "population": 511},
    {"region": "Biobío", "census_year": 2017, "population": 1555},
    {"region": "La Araucanía", "census_year": 2017, "population": 957},
    {"region": "Los Ríos", "census_year": 2017, "population": 406},
    {"region": "Los Lagos", "census_year": 2017, "population": 823},
    {"region": "Aysén", "census_year": 2017, "population": 107},
    {"region": "Magallanes", "census_year": 2017, "population": 178},
]


def collect_census():
    os.makedirs(RAW_DIR, exist_ok=True)
    out = os.path.join(RAW_DIR, "census.csv")
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["region", "census_year", "population"])
        w.writeheader()
        w.writerows(CENSUS)
    print(f"OK: {len(CENSUS)} records -> {out}")


if __name__ == "__main__":
    collect_census()
