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


def test_events_corrected_per_audit():
    """P5: correcciones de la auditoría 2026-10."""
    from collect_events import EVENTS

    by_name = {e["event"]: e for e in EVENTS}
    # Combate Naval de Iquique: 1879, no 1866
    assert "Combate Naval de Iquique" in by_name
    assert by_name["Combate Naval de Iquique"]["year"] == 1879
    assert "Batalla de Iquique" not in by_name
    # Atentado contra Pinochet: 1986, no 1985
    assert by_name["Atentado contra Pinochet"]["year"] == 1986
    # Tratado de Ancón: firmado en Ancón, Perú (lat ~-11.8), no en Chile
    ancon = by_name["Tratado de Ancón"]
    assert -12.0 < ancon["lat"] < -11.5
    assert -77.5 < ancon["lon"] < -77.0


def test_presidents_birthplaces_corrected_per_audit():
    """P5: correcciones de la auditoría 2026-10."""
    from collect_presidents import PRESIDENTS

    by_name = {p["name"]: p for p in PRESIDENTS}
    # Blanco Encalada nació en Buenos Aires (BCN Historia Política), no Santiago
    assert by_name["Manuel Blanco Encalada"]["birthplace"] == "Buenos Aires"
    # Aníbal Pinto nació en Santiago (BCN), no Concepción
    assert by_name["Aníbal Pinto"]["birthplace"] == "Santiago"
