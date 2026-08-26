import csv
import os

import folium

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output", "capas")


def map_presidents():
    presidents = []
    with open(os.path.join(RAW_DIR, "presidents.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["start"] = int(row["start"])
            row["end"] = int(row["end"])
            row["lat"] = float(row["lat"])
            row["lon"] = float(row["lon"])
            presidents.append(row)

    m = folium.Map(location=[-35.0, -71.0], zoom_start=5, tiles="CartoDB positron")

    colors = {
        (1820, 1850): "blue",
        (1850, 1890): "green",
        (1890, 1930): "orange",
        (1930, 1970): "red",
        (1970, 2000): "purple",
        (2000, 2030): "darkblue",
    }

    def get_color(start):
        for (y0, y1), c in colors.items():
            if y0 <= start < y1:
                return c
        return "gray"

    for p in presidents:
        folium.CircleMarker(
            location=[p["lat"], p["lon"]],
            radius=8,
            color=get_color(p["start"]),
            fill=True,
            fill_color=get_color(p["start"]),
            fill_opacity=0.7,
            popup=folium.Popup(
                f"<b>{p['name']}</b><br>"
                f"Gobierno: {p['start']}-{p['end']}<br>"
                f"Nacimiento: {p['birthplace']}",
                max_width=250,
            ),
            tooltip=f"{p['name']} ({p['start']}-{p['end']})",
        ).add_to(m)

    legend_html = """
    <div style="position:fixed;bottom:30px;left:30px;z-index:1000;
         background-color:white;padding:10px;border:2px solid grey;border-radius:5px;">
    <b>Presidentes por década</b><br>
    <i style="color:blue">●</i> 1820-1850<br>
    <i style="color:green">●</i> 1850-1890<br>
    <i style="color:orange">●</i> 1890-1930<br>
    <i style="color:red">●</i> 1930-1970<br>
    <i style="color:purple">●</i> 1970-2000<br>
    <i style="color:darkblue">●</i> 2000-2026
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = os.path.join(OUTPUT_DIR, "presidents.html")
    m.save(out)
    print(f"OK: {len(presidents)} presidents -> {out}")
    return m


if __name__ == "__main__":
    map_presidents()
