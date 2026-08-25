import folium
import json
import os

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output", "capas")


def map_boundaries():
    geojson_path = os.path.join(RAW_DIR, "regiones.geojson")
    if not os.path.exists(geojson_path):
        print("ERROR: regiones.geojson not found. Run collect_geojson.py first.")
        return None

    with open(geojson_path, encoding="utf-8") as f:
        regions = json.load(f)

    m = folium.Map(location=[-35.0, -71.0], zoom_start=5, tiles="CartoDB positron")

    folium.GeoJson(
        regions,
        style_function=lambda x: {
            "fillColor": "#3388ff",
            "color": "black",
            "weight": 2,
            "fillOpacity": 0.15,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=list(regions["features"][0]["properties"].keys()),
            aliases=list(regions["features"][0]["properties"].keys()),
            localize=True,
        ),
        popup=folium.GeoJsonPopup(
            fields=list(regions["features"][0]["properties"].keys()),
            aliases=list(regions["features"][0]["properties"].keys()),
            localize=True,
        ),
    ).add_to(m)

    info_html = """
    <div style="position:fixed;top:10px;left:10px;z-index:1000;
         background-color:white;padding:10px;border:2px solid grey;border-radius:5px;max-width:300px;">
    <h4>Límites Regionales de Chile</h4>
    <p>16 regiones actuales. Los límites han cambiado a lo largo de la historia:</p>
    <ul>
        <li>1900: 23 provincias</li>
        <li>1940: 25 provincias</li>
        <li>1970: 37 provincias</li>
        <li>2000: 43 provincias</li>
        <li>2017: 54 provincias</li>
    </ul>
    </div>
    """
    m.get_root().html.add_child(folium.Element(info_html))

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = os.path.join(OUTPUT_DIR, "boundaries.html")
    m.save(out)
    print(f"OK: {len(regions['features'])} regions -> {out}")
    return m


if __name__ == "__main__":
    map_boundaries()
