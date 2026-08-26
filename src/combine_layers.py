import csv
import json
import os

import folium

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")

TYPE_COLORS = {
    "político": "blue",
    "militar": "red",
    "desastre": "orange",
    "social": "green",
    "deportivo": "purple",
}

PRESIDENT_COLORS = {
    (1820, 1850): "blue",
    (1850, 1890): "green",
    (1890, 1930): "orange",
    (1930, 1970): "red",
    (1970, 2000): "purple",
    (2000, 2030): "darkblue",
}


def get_president_color(start):
    for (y0, y1), c in PRESIDENT_COLORS.items():
        if y0 <= start < y1:
            return c
    return "gray"


def combine_layers():
    presidents = []
    with open(os.path.join(RAW_DIR, "presidents.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["start"] = int(row["start"])
            row["end"] = int(row["end"])
            row["lat"] = float(row["lat"])
            row["lon"] = float(row["lon"])
            presidents.append(row)

    events = []
    with open(os.path.join(RAW_DIR, "events.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["year"] = int(row["year"])
            row["lat"] = float(row["lat"])
            row["lon"] = float(row["lon"])
            events.append(row)

    census = []
    with open(os.path.join(RAW_DIR, "census.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["census_year"] = int(row["census_year"])
            row["population"] = int(row["population"])
            census.append(row)

    geojson_path = os.path.join(RAW_DIR, "..", "raw", "regiones.geojson")
    regions = None
    if os.path.exists(geojson_path):
        with open(geojson_path, encoding="utf-8") as f:
            regions = json.load(f)

    m = folium.Map(location=[-35.0, -71.0], zoom_start=5, tiles="CartoDB positron")

    if regions:
        fg_boundaries = folium.FeatureGroup(name="Límites Regionales")
        folium.GeoJson(
            regions,
            style_function=lambda x: {
                "fillColor": "#3388ff",
                "color": "black",
                "weight": 2,
                "fillOpacity": 0.1,
            },
        ).add_to(fg_boundaries)
        fg_boundaries.add_to(m)

    years = sorted({r["census_year"] for r in census})
    for year in years:
        year_data = {
            r["region"]: r["population"] for r in census if r["census_year"] == year
        }
        if regions:
            fg = folium.FeatureGroup(name=f"Población {year}", show=(year == 2017))
            for feature in regions["features"]:
                props = feature["properties"]
                region_name = props.get("Region", props.get("region", ""))
                pop = year_data.get(region_name, 0)
                intensity = min(pop / 3000, 1.0) if pop > 0 else 0
                r_val = int(255 * (1 - intensity) + 178 * intensity)
                g_val = int(255 * (1 - intensity) + 24 * intensity)
                b_val = int(255 * (1 - intensity) + 43 * intensity)
                color = f"#{r_val:02x}{g_val:02x}{b_val:02x}"
                folium.GeoJson(
                    feature,
                    style_function=lambda x, c=color: {
                        "fillColor": c,
                        "color": "grey",
                        "weight": 0.5,
                        "fillOpacity": 0.6,
                    },
                    popup=folium.Popup(
                        f"<b>{region_name}</b><br>Población: {pop:,}", max_width=200
                    ),
                ).add_to(fg)
            fg.add_to(m)

    fg_presidents = folium.FeatureGroup(name="Presidentes")
    for p in presidents:
        folium.CircleMarker(
            location=[p["lat"], p["lon"]],
            radius=8,
            color=get_president_color(p["start"]),
            fill=True,
            fill_color=get_president_color(p["start"]),
            fill_opacity=0.7,
            popup=folium.Popup(
                f"<b>{p['name']}</b><br>{p['start']}-{p['end']}<br>{p['birthplace']}",
                max_width=250,
            ),
            tooltip=f"{p['name']} ({p['start']})",
        ).add_to(fg_presidents)
    fg_presidents.add_to(m)

    fg_events = folium.FeatureGroup(name="Eventos Históricos", show=False)
    for e in events:
        color = TYPE_COLORS.get(e["type"], "gray")
        folium.CircleMarker(
            location=[e["lat"], e["lon"]],
            radius=10,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(
                f"<b>{e['year']} - {e['event']}</b><br>{e['city']}<br>{e['type']}",
                max_width=280,
            ),
            tooltip=f"{e['year']}: {e['event']}",
        ).add_to(fg_events)
    fg_events.add_to(m)

    folium.LayerControl().add_to(m)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = os.path.join(OUTPUT_DIR, "chile_historico.html")
    m.save(out)
    print(
        f"OK: Combined map ({len(presidents)} presidents, {len(events)} events) -> {out}"
    )


if __name__ == "__main__":
    combine_layers()
