import csv
import json
import os

import folium

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output", "capas")


def map_demographics():
    census = []
    with open(os.path.join(RAW_DIR, "census.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["census_year"] = int(row["census_year"])
            row["population"] = int(row["population"])
            census.append(row)

    geojson_path = os.path.join(RAW_DIR, "..", "raw", "regiones.geojson")
    if not os.path.exists(geojson_path):
        print("ERROR: regiones.geojson not found. Run collect_geojson.py first.")
        return None

    with open(geojson_path, encoding="utf-8") as f:
        regions = json.load(f)

    years = sorted({r["census_year"] for r in census})

    m = folium.Map(location=[-35.0, -71.0], zoom_start=5, tiles="CartoDB positron")

    for year in years:
        year_data = {
            r["region"]: r["population"] for r in census if r["census_year"] == year
        }
        fg = folium.FeatureGroup(name=f"Censo {year}")

        for feature in regions["features"]:
            props = feature["properties"]
            region_name = props.get("Region", props.get("region", ""))
            pop = year_data.get(region_name, 0)

            color = "#ffffcc"
            if pop > 0:
                intensity = min(pop / 3000, 1.0)
                r_val = int(255 * (1 - intensity) + 178 * intensity)
                g_val = int(255 * (1 - intensity) + 24 * intensity)
                b_val = int(255 * (1 - intensity) + 43 * intensity)
                color = f"#{r_val:02x}{g_val:02x}{b_val:02x}"

            folium.GeoJson(
                feature,
                style_function=lambda x, c=color: {
                    "fillColor": c,
                    "color": "grey",
                    "weight": 1,
                    "fillOpacity": 0.7,
                },
                popup=folium.Popup(
                    f"<b>{region_name}</b><br>Población: {pop:,}",
                    max_width=200,
                ),
            ).add_to(fg)

        fg.add_to(m)

    folium.LayerControl().add_to(m)

    legend_html = """
    <div style="position:fixed;bottom:30px;left:30px;z-index:1000;
         background-color:white;padding:10px;border:2px solid grey;border-radius:5px;">
    <b>Población por región</b><br>
    <div style="background:#ffffcc;width:20px;height:10px;display:inline-block;"></div> Baja<br>
    <div style="background:#ff6f2b;width:20px;height:10px;display:inline-block;"></div> Media<br>
    <div style="background:#b2182b;width:20px;height:10px;display:inline-block;"></div> Alta
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = os.path.join(OUTPUT_DIR, "demographics.html")
    m.save(out)
    print(f"OK: census data ({len(years)} decades) -> {out}")
    return m


if __name__ == "__main__":
    map_demographics()
