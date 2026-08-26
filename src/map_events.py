import csv
import os

import folium

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output", "capas")

TYPE_COLORS = {
    "político": "blue",
    "militar": "red",
    "desastre": "orange",
    "social": "green",
    "deportivo": "purple",
}


def map_events():
    events = []
    with open(os.path.join(RAW_DIR, "events.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["year"] = int(row["year"])
            row["lat"] = float(row["lat"])
            row["lon"] = float(row["lon"])
            events.append(row)

    m = folium.Map(location=[-35.0, -71.0], zoom_start=5, tiles="CartoDB dark_matter")

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
                f"<b>{e['year']} - {e['event']}</b><br>"
                f"Ubicación: {e['city']}<br>"
                f"Tipo: {e['type']}",
                max_width=280,
            ),
            tooltip=f"{e['year']}: {e['event']}",
        ).add_to(m)

    legend_html = """
    <div style="position:fixed;bottom:30px;left:30px;z-index:1000;
         background-color:white;padding:10px;border:2px solid grey;border-radius:5px;">
    <b>Eventos históricos</b><br>
    <i style="color:blue">●</i> Político<br>
    <i style="color:red">●</i> Militar<br>
    <i style="color:orange">●</i> Desastre<br>
    <i style="color:green">●</i> Social<br>
    <i style="color:purple">●</i> Deportivo
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = os.path.join(OUTPUT_DIR, "events.html")
    m.save(out)
    print(f"OK: {len(events)} events -> {out}")
    return m


if __name__ == "__main__":
    map_events()
