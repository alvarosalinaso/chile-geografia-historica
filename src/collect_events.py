import csv
import os

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

# Key historical events geolocalized
# Source: Wikipedia, BCN Historia Política
EVENTS = [
    {"year": 1810, "event": "Primera Junta de Gobierno", "city": "Santiago", "lat": -33.4489, "lon": -70.6693, "type": "político"},
    {"year": 1817, "event": "Batalla de Chacabuco", "city": "Cuesta de Chacabuco", "lat": -33.1500, "lon": -70.6667, "type": "militar"},
    {"year": 1818, "event": "Batalla de Maipú", "city": "Santiago", "lat": -33.5167, "lon": -70.7500, "type": "militar"},
    {"year": 1818, "event": "Independencia de Chile", "city": "Talca", "lat": -35.4264, "lon": -71.6554, "type": "político"},
    {"year": 1833, "event": "Constitución Política", "city": "Santiago", "lat": -33.4489, "lon": -70.6693, "type": "político"},
    {"year": 1866, "event": "Batalla de Iquique", "city": "Iquique", "lat": -20.2141, "lon": -70.1524, "type": "militar"},
    {"year": 1879, "event": "Guerra del Pacífico (inicio)", "city": "Antofagasta", "lat": -23.6509, "lon": -70.3975, "type": "militar"},
    {"year": 1883, "event": "Tratado de Ancón", "city": "Ancón", "lat": -27.1710, "lon": -70.9920, "type": "político"},
    {"year": 1906, "event": "Terremoto de Valparaíso", "city": "Valparaíso", "lat": -33.0472, "lon": -71.6127, "type": "desastre"},
    {"year": 1925, "event": "Nueva Constitución", "city": "Santiago", "lat": -33.4489, "lon": -70.6693, "type": "político"},
    {"year": 1938, "event": "Matanza del Seguro Obrero", "city": "Santiago", "lat": -33.4489, "lon": -70.6693, "type": "político"},
    {"year": 1945, "event": "Fin de la Segunda Guerra Mundial", "city": "Santiago", "lat": -33.4489, "lon": -70.6693, "type": "político"},
    {"year": 1960, "event": "Gran Terremoto de Valdivia", "city": "Valdivia", "lat": -39.8196, "lon": -73.2452, "type": "desastre"},
    {"year": 1962, "event": "Copa Mundial de Fútbol", "city": "Santiago", "lat": -33.4652, "lon": -70.6105, "type": "deportivo"},
    {"year": 1964, "event": "Reforma Agraria", "city": "Santiago", "lat": -33.4489, "lon": -70.6693, "type": "político"},
    {"year": 1970, "event": "Elección de Salvador Allende", "city": "Santiago", "lat": -33.4489, "lon": -70.6693, "type": "político"},
    {"year": 1973, "event": "Golpe de Estado", "city": "Santiago", "lat": -33.4489, "lon": -70.6693, "type": "político"},
    {"year": 1985, "event": "Atentado contra Pinochet", "city": "Santiago", "lat": -33.4489, "lon": -70.6693, "type": "político"},
    {"year": 1988, "event": "Plebiscito (NO gana)", "city": "Santiago", "lat": -33.4489, "lon": -70.6693, "type": "político"},
    {"year": 1990, "event": "Retorno a la democracia", "city": "Santiago", "lat": -33.4489, "lon": -70.6693, "type": "político"},
    {"year": 2010, "event": "Terremoto del 27F", "city": "Concepción", "lat": -36.8201, "lon": -73.0444, "type": "desastre"},
    {"year": 2010, "event": "Rescate mineros Copiapó", "city": "Copiapó", "lat": -27.3668, "lon": -70.3323, "type": "social"},
    {"year": 2019, "event": "Estallido Social", "city": "Santiago", "lat": -33.4489, "lon": -70.6693, "type": "político"},
    {"year": 2022, "event": "Proceso Constituyente", "city": "Santiago", "lat": -33.4489, "lon": -70.6693, "type": "político"},
]


def collect_events():
    os.makedirs(RAW_DIR, exist_ok=True)
    out = os.path.join(RAW_DIR, "events.csv")
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["year", "event", "city", "lat", "lon", "type"])
        w.writeheader()
        w.writerows(EVENTS)
    print(f"OK: {len(EVENTS)} events -> {out}")


if __name__ == "__main__":
    collect_events()
