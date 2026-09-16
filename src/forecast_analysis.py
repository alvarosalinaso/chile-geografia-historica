"""Demographic forecasting and event-population correlation for Chile."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

BASE = Path(__file__).parent.parent


def analyze():
    census_path = BASE / "data" / "processed" / "census.csv"
    events_path = BASE / "data" / "processed" / "events.csv"
    if not census_path.exists():
        return None

    census = pd.read_csv(census_path)
    forecasts = []

    for region in census["region"].unique():
        rdf = census[census["region"] == region].sort_values("census_year")
        if len(rdf) < 2:
            continue
        X = rdf["census_year"].values.reshape(-1, 1)
        y = rdf["population"].values

        model = LinearRegression()
        model.fit(X, y)

        pop_2025 = float(model.predict([[2025]])[0])
        pop_2030 = float(model.predict([[2030]])[0])
        slope = float(model.coef_[0])
        mean_pop = y.mean()
        growth_rate = slope / mean_pop if mean_pop > 0 else 0

        forecasts.append({
            "region": region,
            "pop_2025": round(pop_2025, 1),
            "pop_2030": round(pop_2030, 1),
            "growth_rate": round(growth_rate, 4),
            "r2": round(float(model.score(X, y)), 3),
        })

    forecasts.sort(key=lambda x: -x["growth_rate"])

    event_impact = []
    if events_path.exists():
        events = pd.read_csv(events_path)
        national = census.groupby("census_year")["population"].sum().reset_index()
        national = national.sort_values("census_year")

        for _, ev in events.iterrows():
            ev_year = int(ev["year"])
            before = national[national["census_year"] <= ev_year]
            after = national[national["census_year"] > ev_year]
            if not before.empty and not after.empty:
                pop_before = float(before.iloc[-1]["population"])
                pop_after = float(after.iloc[0]["population"])
                year_before = int(before.iloc[-1]["census_year"])
                year_after = int(after.iloc[0]["census_year"])
                change_pct = ((pop_after - pop_before) / pop_before * 100) if pop_before > 0 else 0
                event_impact.append({
                    "event": ev["event"],
                    "year": ev_year,
                    "pop_before": round(pop_before, 1),
                    "pop_after": round(pop_after, 1),
                    "year_before": year_before,
                    "year_after": year_after,
                    "change_pct": round(change_pct, 1),
                })

    result = {"forecasts": forecasts, "event_impact": event_impact}

    output = BASE / "data" / "export" / "forecast_results.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return result


if __name__ == "__main__":
    result = analyze()
    if result:
        print(f"Regions forecasted: {len(result['forecasts'])}")
        print(f"Events analyzed: {len(result['event_impact'])}")
        for f in result["forecasts"][:5]:
            print(f"  {f['region']}: 2025={f['pop_2025']}, rate={f['growth_rate']}")
    else:
        print("No data")
