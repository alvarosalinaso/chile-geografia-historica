"""Demographic forecasting and event-population correlation for Chile.

⚠️ LIMITACIONES METODOLÓGICAS:
- Regresión lineal simple con 5-6 puntos de datos (censos 1907-2017)
- Proyección a 2030 (13 años más allá del último censo) es EXTRAPOLACIÓN
- No captura dinámicas no lineales (migración, natalidad, políticas públicas)
- R² reportado es bondad de ajuste histórico, NO precisión predictiva
- Intervalos de confianza asumen normalidad y homocedasticidad (poco realista con n=5-6)
- Usar solo como indicador de tendencia histórica, no como predicción real
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
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
        if len(rdf) < 3:  # Need at least 3 points for meaningful CI
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

        # Calculate prediction intervals (95% CI) for 2025 and 2030
        n = len(rdf)
        X_mean = rdf["census_year"].mean()
        SXX = ((rdf["census_year"] - X_mean) ** 2).sum()
        y_pred = model.predict(X)
        residuals = y - y_pred
        MSE = (residuals**2).sum() / (n - 2)
        se_pred_2025 = np.sqrt(MSE * (1 + 1 / n + (2025 - X_mean) ** 2 / SXX))
        se_pred_2030 = np.sqrt(MSE * (1 + 1 / n + (2030 - X_mean) ** 2 / SXX))
        t_val = stats.t.ppf(0.975, n - 2)

        forecasts.append(
            {
                "region": region,
                "pop_2025": round(pop_2025, 1),
                "pop_2025_ci_lower": round(pop_2025 - t_val * se_pred_2025, 1),
                "pop_2025_ci_upper": round(pop_2025 + t_val * se_pred_2025, 1),
                "pop_2030": round(pop_2030, 1),
                "pop_2030_ci_lower": round(pop_2030 - t_val * se_pred_2030, 1),
                "pop_2030_ci_upper": round(pop_2030 + t_val * se_pred_2030, 1),
                "growth_rate": round(growth_rate, 4),
                "growth_rate_ci_lower": round(
                    (slope - t_val * np.sqrt(MSE / SXX)) / mean_pop
                    if mean_pop > 0
                    else 0,
                    4,
                ),
                "growth_rate_ci_upper": round(
                    (slope + t_val * np.sqrt(MSE / SXX)) / mean_pop
                    if mean_pop > 0
                    else 0,
                    4,
                ),
                "r2": round(float(model.score(X, y)), 3),
                "n_observations": n,
                "method": "linear_regression",
                "warning": "EXTrapolation beyond 2017 - high uncertainty",
            }
        )

    forecasts.sort(key=lambda x: -x["growth_rate"])

    # A7: asociación temporal entre censos contiguos al evento — NO causalidad
    event_temporal_diff = []
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
                change_pct = (
                    ((pop_after - pop_before) / pop_before * 100)
                    if pop_before > 0
                    else 0
                )
                event_temporal_diff.append(
                    {
                        "event": ev["event"],
                        "year": ev_year,
                        "pop_before": round(pop_before, 1),
                        "pop_after": round(pop_after, 1),
                        "year_before": year_before,
                        "year_after": year_after,
                        "change_pct": round(change_pct, 1),
                    }
                )

    result = {"forecasts": forecasts, "event_temporal_diff": event_temporal_diff}

    output = BASE / "data" / "export" / "forecast_results.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return result


if __name__ == "__main__":
    result = analyze()
    if result:
        print(f"Regions forecasted: {len(result['forecasts'])}")
        print(f"Events analyzed: {len(result['event_temporal_diff'])}")
        for f in result["forecasts"][:5]:
            print(
                f"  {f['region']}: 2025={f['pop_2025']} (CI: {f['pop_2025_ci_lower']}-{f['pop_2025_ci_upper']}), rate={f['growth_rate']}"
            )
    else:
        print("No data")
