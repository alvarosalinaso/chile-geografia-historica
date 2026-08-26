import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from collect_census import collect_census
from collect_events import collect_events
from collect_geojson import collect_geojson
from collect_presidents import collect_presidents
from combine_layers import combine_layers
from map_boundaries import map_boundaries
from map_demographics import map_demographics
from map_events import map_events
from map_presidents import map_presidents


def analyze_all():
    print("=" * 60)
    print("CHILE GEOGRAFÍA HISTÓRICA")
    print("=" * 60)

    print("\n[1/5] Collecting data...")
    collect_geojson()
    collect_presidents()
    collect_events()
    collect_census()

    print("\n[2/5] Generating president map...")
    map_presidents()

    print("\n[3/5] Generating demographics map...")
    map_demographics()

    print("\n[4/5] Generating events map...")
    map_events()

    print("\n[5/5] Generating boundaries map...")
    map_boundaries()

    print("\n[6/6] Combining all layers...")
    combine_layers()

    print("\n" + "=" * 60)
    print("DONE! Output: output/chile_historico.html")
    print("=" * 60)


if __name__ == "__main__":
    analyze_all()
