"""Tests for forecast_analysis module (chile-geografia-historica)."""

import json

import pandas as pd

from src.forecast_analysis import analyze


def test_analyze_returns_dict_with_ci(tmp_path, monkeypatch):
    """Test that analyze returns forecasts with confidence intervals."""
    import src.forecast_analysis as fa_module

    monkeypatch.setattr(fa_module, "BASE", tmp_path)

    data_processed = tmp_path / "data" / "processed"
    data_processed.mkdir(parents=True)

    # Create census.csv with enough data points for CI
    census_data = pd.DataFrame(
        {
            "region": [
                "Region A",
                "Region A",
                "Region A",
                "Region B",
                "Region B",
                "Region B",
            ],
            "census_year": [1992, 2002, 2017, 1992, 2002, 2017],
            "population": [100, 150, 200, 200, 250, 300],
        }
    )
    census_data.to_csv(data_processed / "census.csv", index=False)

    # Create events.csv
    events_data = pd.DataFrame(
        {
            "year": [1995, 2005],
            "event": ["Event 1", "Event 2"],
            "type": ["Political", "Economic"],
            "city": ["Santiago", "Valparaiso"],
        }
    )
    events_data.to_csv(data_processed / "events.csv", index=False)

    result = analyze()
    assert isinstance(result, dict)
    assert "forecasts" in result
    assert "event_temporal_diff" in result
    assert len(result["forecasts"]) == 2

    # Check CI fields exist
    for f in result["forecasts"]:
        assert "pop_2025_ci_lower" in f
        assert "pop_2025_ci_upper" in f
        assert "pop_2030_ci_lower" in f
        assert "pop_2030_ci_upper" in f
        assert "growth_rate_ci_lower" in f
        assert "growth_rate_ci_upper" in f
        assert "warning" in f
        assert f["n_observations"] >= 3
        # CI should be ordered correctly
        assert f["pop_2025_ci_lower"] <= f["pop_2025"] <= f["pop_2025_ci_upper"]
        assert f["pop_2030_ci_lower"] <= f["pop_2030"] <= f["pop_2030_ci_upper"]


def test_analyze_no_census(tmp_path, monkeypatch):
    """Test analyze with no census data returns None."""
    import src.forecast_analysis as fa_module

    monkeypatch.setattr(fa_module, "BASE", tmp_path)

    result = analyze()
    assert result is None


def test_analyze_insufficient_data_skipped(tmp_path, monkeypatch):
    """Test that regions with < 3 data points are skipped."""
    import src.forecast_analysis as fa_module

    monkeypatch.setattr(fa_module, "BASE", tmp_path)

    data_processed = tmp_path / "data" / "processed"
    data_processed.mkdir(parents=True)

    # Only 2 data points for Region A
    census_data = pd.DataFrame(
        {
            "region": ["Region A", "Region A", "Region B", "Region B", "Region B"],
            "census_year": [1992, 2017, 1992, 2002, 2017],
            "population": [100, 200, 200, 250, 300],
        }
    )
    census_data.to_csv(data_processed / "census.csv", index=False)

    result = analyze()
    assert isinstance(result, dict)
    # Region A should be skipped (only 2 points)
    regions = [f["region"] for f in result["forecasts"]]
    assert "Region A" not in regions
    assert "Region B" in regions


def test_analyze_creates_output_file(tmp_path, monkeypatch):
    """Test that analyze creates forecast_results.json."""
    import src.forecast_analysis as fa_module

    monkeypatch.setattr(fa_module, "BASE", tmp_path)

    data_processed = tmp_path / "data" / "processed"
    data_processed.mkdir(parents=True)

    census_data = pd.DataFrame(
        {
            "region": ["Region A", "Region A", "Region A"],
            "census_year": [1992, 2002, 2017],
            "population": [100, 150, 200],
        }
    )
    census_data.to_csv(data_processed / "census.csv", index=False)

    analyze()
    output_file = tmp_path / "data" / "export" / "forecast_results.json"
    assert output_file.exists()

    with open(output_file) as f:
        content = json.load(f)
    assert "forecasts" in content
    assert len(content["forecasts"]) == 1


def test_analyze_event_temporal_diff(tmp_path, monkeypatch):
    """Test de diferencia temporal entre censos (asociación, no impacto causal)."""
    import src.forecast_analysis as fa_module

    monkeypatch.setattr(fa_module, "BASE", tmp_path)

    data_processed = tmp_path / "data" / "processed"
    data_processed.mkdir(parents=True)

    census_data = pd.DataFrame(
        {
            "region": ["Region A", "Region A", "Region A"],
            "census_year": [1992, 2002, 2017],
            "population": [100, 150, 200],
        }
    )
    census_data.to_csv(data_processed / "census.csv", index=False)

    events_data = pd.DataFrame(
        {
            "year": [1995],
            "event": ["Test Event"],
            "type": ["Political"],
            "city": ["Santiago"],
        }
    )
    events_data.to_csv(data_processed / "events.csv", index=False)

    result = analyze()
    assert "event_temporal_diff" in result
    assert len(result["event_temporal_diff"]) == 1
    assert result["event_temporal_diff"][0]["event"] == "Test Event"
