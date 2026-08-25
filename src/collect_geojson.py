import os
import requests

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

REGIONES_GEOJSON_URL = "https://raw.githubusercontent.com/caracena/chile-geojson/master/regiones.json"
COMUNAS_GEOJSON_URL = "https://raw.githubusercontent.com/fcortes/Chile-GeoJSON/master/Regional.geojson"


def download_file(url, dest):
    if os.path.exists(dest):
        print(f"  SKIP (exists): {os.path.basename(dest)}")
        return
    print(f"  Downloading: {os.path.basename(dest)}...")
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    with open(dest, "w", encoding="utf-8") as f:
        f.write(r.text)
    print(f"  OK: {os.path.basename(dest)} ({len(r.text)} bytes)")


def collect_geojson():
    os.makedirs(RAW_DIR, exist_ok=True)
    print("[1/2] Downloading regiones GeoJSON...")
    download_file(REGIONES_GEOJSON_URL, os.path.join(RAW_DIR, "regiones.geojson"))
    print("[2/2] Downloading comunas/regional GeoJSON...")
    download_file(COMUNAS_GEOJSON_URL, os.path.join(RAW_DIR, "comunas.geojson"))
    print("Done!")


if __name__ == "__main__":
    collect_geojson()
