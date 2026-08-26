import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def test_imports():
    assert True


def test_presidents_data():
    from collect_presidents import PRESIDENTS

    assert len(PRESIDENTS) > 0
    assert all("name" in p for p in PRESIDENTS)
    assert all("lat" in p and "lon" in p for p in PRESIDENTS)


def test_events_data():
    from collect_events import EVENTS

    assert len(EVENTS) > 0
    assert all("year" in e and "event" in e for e in EVENTS)


def test_census_data():
    from collect_census import CENSUS

    assert len(CENSUS) > 0
    assert all("region" in c and "population" in c for c in CENSUS)
