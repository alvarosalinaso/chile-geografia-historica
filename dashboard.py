"""Dash Dashboard: Chile Geographic & Historical Analysis — Ernst Haeckel Art Nouveau Style."""

import json
import os
from pathlib import Path

import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dash_table, dcc, html, no_update

app = dash.Dash(
    __name__,
    title="Chile — Geografía Histórica",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server

FONT_UI = "'Inter',Georgia,serif"
FONT_DATA = "'JetBrains Mono',Consolas,monospace"

COLORS = {
    "bg": "#0a0e14",
    "card": "#11161f",
    "card_alt": "#141b2a",
    "border": "rgba(255,255,255,0.08)",
    "teal": "#2dd4bf",
    "sienna": "#fb923c",
    "olive": "#a3b86b",
    "gold": "#fbbf24",
    "navy": "#818cf8",
    "text": "#e8edf2",
    "muted": "#8b94a3",
    "cream": "#11161f",
}

DATA_DIR = Path(__file__).parent / "data" / "processed"
RAW_DIR = Path(__file__).parent / "data" / "raw"


def load_data():
    data = {}
    census_path = DATA_DIR / "census.csv"
    if census_path.exists():
        data["census"] = pd.read_csv(census_path)
    events_path = DATA_DIR / "events.csv"
    if events_path.exists():
        data["events"] = pd.read_csv(events_path)
    presidents_path = DATA_DIR / "presidents.csv"
    if presidents_path.exists():
        data["presidents"] = pd.read_csv(presidents_path)
    geojson_path = RAW_DIR / "regiones.geojson"
    if geojson_path.exists():
        with open(geojson_path) as f:
            data["geojson"] = json.load(f)
    forecast_path = DATA_DIR.parent / "export" / "forecast_results.json"
    if forecast_path.exists():
        with open(forecast_path) as f:
            data["forecast"] = json.load(f)
    return data


DATA = load_data()


EARTHTONE_PLOTLY = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter,Georgia,serif", color="#e8edf2", size=13),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.12)",
        title=dict(font=dict(size=13)),
        tickfont=dict(family="JetBrains Mono,monospace", size=12),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.12)",
        title=dict(font=dict(size=13)),
        tickfont=dict(family="JetBrains Mono,monospace", size=12),
    ),
    legend=dict(font=dict(size=12), bgcolor="rgba(0,0,0,0)"),
    colorway=[
        "#56B4E9",
        "#E69F00",
        "#009E73",
        "#F0E442",
        "#CC79A7",
        "#D55E00",
        "#0072B2",
        "#999999",
    ],
)

DATA_CANVAS_SVG = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' width='1200' height='90' viewBox='0 0 1200 90'%3E"
    "%3Crect width='1200' height='90' fill='%230a0e14'/%3E"
    "%3Cg fill='%2322d3ee' opacity='0.16'%3E"
    + "".join(
        f"%3Ccircle cx='{x}' cy='{y}' r='2'/%3E"
        for x in range(30, 1200, 60)
        for y in range(20, 90, 30)
    )
    + "%3C/g%3E%3Cg fill='none' stroke='%232dd4bf' stroke-width='2' opacity='0.7'%3E"
    "%3Cpath d='M0,70 Q200,30 400,55 T800,30 T1200,50'/%3E%3C/g%3E"
    "%3C/svg%3E"
)


def sparkline(values, color="#2dd4bf"):
    if not values or len(values) < 2:
        return html.Div(style={"height": "34px"})
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            y=list(values),
            mode="lines",
            line={"color": color, "width": 3, "shape": "spline"},
            fill="tozeroy",
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.update_layout(
        margin={"t": 0, "b": 0, "l": 0, "r": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis={"visible": False},
        yaxis={"visible": False},
        height=34,
    )
    return dcc.Graph(
        figure=fig, config={"displayModeBar": False}, style={"height": "34px"}
    )


def insight_card(question, answer, accent="#2dd4bf"):
    return html.Div(
        style={
            "backgroundColor": "#11161f",
            "border": "1px solid rgba(255,255,255,0.08)",
            "borderLeft": f"3px solid {accent}",
            "borderRadius": "10px",
            "padding": "14px 16px",
            "marginBottom": "12px",
        },
        children=[
            html.Div(
                question,
                style={
                    "fontWeight": "700",
                    "textTransform": "uppercase",
                    "fontSize": "0.75rem",
                    "letterSpacing": "0.06em",
                    "fontFamily": "Inter,Georgia,serif",
                    "color": accent,
                },
            ),
            html.Div(
                answer,
                style={
                    "marginTop": "4px",
                    "fontFamily": "Georgia,serif",
                    "lineHeight": "1.55",
                    "color": "#e8edf2",
                },
            ),
        ],
    )


def _leaf_ornament():
    return html.Div(
        style={
            "display": "flex",
            "justifyContent": "center",
            "gap": "4px",
            "marginBottom": "20px",
            "paddingTop": "5px",
        },
        children=[
            html.Div(
                style={
                    "width": "6px",
                    "height": "18px",
                    "backgroundColor": COLORS["teal"],
                    "borderRadius": "50% 50% 50% 50% / 60% 60% 40% 40%",
                    "transform": f"rotate({deg}deg)",
                    "opacity": "0.6",
                }
            )
            for deg in [-30, 0, 30]
        ]
        + [
            html.Div(
                style={
                    "width": "40px",
                    "height": "2px",
                    "backgroundColor": COLORS["gold"],
                    "marginTop": "8px",
                    "borderRadius": "1px",
                }
            )
        ]
        + [
            html.Div(
                style={
                    "width": "6px",
                    "height": "18px",
                    "backgroundColor": COLORS["teal"],
                    "borderRadius": "50% 50% 50% 50% / 60% 60% 40% 40%",
                    "transform": f"rotate({deg}deg)",
                    "opacity": "0.6",
                }
            )
            for deg in [30, 0, -30]
        ],
    )


def card(title, children, color=COLORS["card"]):
    child_list = children if isinstance(children, list) else [children]
    return html.Div(
        style={
            "backgroundColor": color,
            "borderRadius": "14px",
            "padding": "22px 24px",
            "marginBottom": "22px",
            "border": "1px solid rgba(255,255,255,0.08)",
            "boxShadow": "0 8px 32px rgba(0,0,0,0.35)",
            "position": "relative",
            "overflow": "hidden",
        },
        children=[
            html.Div(
                style={
                    "position": "absolute",
                    "top": "0",
                    "left": "0",
                    "right": "0",
                    "height": "3px",
                    "background": f"linear-gradient(90deg, {COLORS['teal']}, {COLORS['gold']}, {COLORS['sienna']})",
                    "borderRadius": "20px 20px 0 0",
                },
            ),
            html.H3(
                title,
                style={
                    "color": COLORS["teal"],
                    "fontSize": "1.25rem",
                    "fontWeight": "700",
                    "marginBottom": "18px",
                    "paddingBottom": "12px",
                    "borderBottom": f"1px solid {COLORS['border']}",
                    "fontFamily": "Georgia, 'Times New Roman', serif",
                    "letterSpacing": "0.02em",
                },
            ),
        ]
        + child_list,
    )


def stat_row(stats):
    def _norm(item):
        if len(item) == 5:
            return item
        if len(item) == 2:
            val, label = item
            return (val, label, COLORS["teal"], None, None)
        raise ValueError(
            f"stat_row item debe ser (val,label) o (val,label,color,trend,delta), got {item}"
        )

    return html.Div(
        style={
            "display": "flex",
            "gap": "14px",
            "flexWrap": "wrap",
            "marginBottom": "24px",
        },
        children=[
            html.Div(
                style={
                    "flex": "1",
                    "minWidth": "150px",
                    "backgroundColor": COLORS["card"],
                    "borderRadius": "12px",
                    "padding": "18px 14px",
                    "textAlign": "center",
                    "border": "1px solid rgba(255,255,255,0.08)",
                },
                children=[
                    html.Div(
                        str(val),
                        style={
                            "fontSize": "2.1rem",
                            "fontWeight": "800",
                            "color": "#e8edf2",
                            "fontFamily": "JetBrains Mono,monospace",
                            "lineHeight": "1.1",
                        },
                    ),
                    html.Div(
                        label,
                        style={
                            "fontSize": "0.75rem",
                            "fontWeight": "800",
                            "color": COLORS["sienna"],
                            "marginTop": "6px",
                            "letterSpacing": "0.06em",
                            "textTransform": "uppercase",
                        },
                    ),
                    sparkline(trend or [], color),
                    html.Div(
                        delta or "",
                        title="Variación vs periodo anterior",
                        style={
                            "fontSize": "0.78rem",
                            "fontWeight": "800",
                            "color": color,
                            "marginTop": "4px",
                        },
                    ),
                ],
            )
            for val, label, color, trend, delta in [_norm(item) for item in stats]
        ],
    )


def _tab_style():
    return {
        "style": {
            "backgroundColor": COLORS["card"],
            "color": COLORS["muted"],
            "border": "none",
            "borderBottom": "2px solid transparent",
            "fontFamily": "Georgia, 'Times New Roman', serif",
            "fontSize": "0.95rem",
            "fontWeight": "600",
            "letterSpacing": "0.02em",
            "padding": "14px 24px",
            "borderRadius": "0",
        },
        "selected_style": {
            "backgroundColor": COLORS["cream"],
            "color": COLORS["teal"],
            "border": "none",
            "borderBottom": f"3px solid {COLORS['teal']}",
            "fontFamily": "Georgia, 'Times New Roman', serif",
            "fontSize": "0.95rem",
            "fontWeight": "700",
            "letterSpacing": "0.02em",
            "padding": "14px 24px",
            "borderRadius": "0",
        },
    }


app.layout = html.Div(
    style={
        "backgroundColor": COLORS["bg"],
        "minHeight": "100vh",
        "fontFamily": "'Segoe UI', system-ui, -apple-system, sans-serif",
        "color": COLORS["text"],
        "backgroundImage": (
            "url(\"data:image/svg+xml,%3Csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3E"
            "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E"
            "%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E\")"
        ),
    },
    children=[
        html.Div(
            style={
                "background": f"linear-gradient(180deg, {COLORS['card']} 0%, {COLORS['cream']} 100%)",
                "padding": "48px 20px 0",
                "textAlign": "center",
                "borderBottom": f"2px solid {COLORS['border']}",
                "position": "relative",
            },
            children=[
                html.Div(
                    style={
                        "position": "absolute",
                        "bottom": "0",
                        "left": "5%",
                        "right": "5%",
                        "height": "40px",
                        "borderBottom": f"2px solid {COLORS['teal']}",
                        "borderLeft": f"2px solid {COLORS['teal']}",
                        "borderRight": f"2px solid {COLORS['teal']}",
                        "borderRadius": "0 0 40px 40px",
                        "opacity": "0.3",
                    },
                ),
                html.Div(
                    style={
                        "width": "60px",
                        "height": "3px",
                        "background": f"linear-gradient(90deg, {COLORS['teal']}, {COLORS['gold']})",
                        "margin": "0 auto 16px",
                        "borderRadius": "2px",
                    },
                ),
                html.H1(
                    "CHILE: GEOGRAFÍA HISTÓRICA",
                    style={
                        "fontSize": "2.4rem",
                        "fontWeight": "800",
                        "color": COLORS["teal"],
                        "margin": "0",
                        "fontFamily": "Georgia, 'Times New Roman', serif",
                        "letterSpacing": "0.08em",
                    },
                ),
                html.P(
                    "Evolución demográfica, eventos históricos y presidentes",
                    style={
                        "color": COLORS["sienna"],
                        "marginTop": "10px",
                        "fontSize": "1.05rem",
                        "fontStyle": "italic",
                        "fontFamily": "Georgia, 'Times New Roman', serif",
                    },
                ),
                _leaf_ornament(),
                html.Div(
                    style={
                        "backgroundImage": f'url("{DATA_CANVAS_SVG}")',
                        "backgroundSize": "cover",
                        "backgroundPosition": "center",
                        "height": "90px",
                        "border": "1px solid rgba(255,255,255,0.08)",
                        "marginTop": "16px",
                    }
                ),
            ],
        ),
        dcc.Tabs(
            id="tabs",
            value="census",
            style={
                "backgroundColor": COLORS["card"],
                "borderBottom": f"1px solid {COLORS['border']}",
                "boxShadow": "0 1px 4px rgba(0,0,0,0.04)",
            },
            children=[
                dcc.Tab(label="Censo", value="census", **_tab_style()),
                dcc.Tab(label="Eventos", value="events", **_tab_style()),
                dcc.Tab(label="Presidentes", value="presidents", **_tab_style()),
                dcc.Tab(label="Mapa", value="map", **_tab_style()),
                dcc.Tab(label="Forecast", value="forecast", **_tab_style()),
                dcc.Tab(label="Eventos-Población", value="events_pop", **_tab_style()),
            ],
        ),
        html.Div(
            id="tab-content",
            style={
                "maxWidth": "1200px",
                "margin": "0 auto",
                "padding": "36px 24px",
            },
        ),
    ],
)


@callback(Output("tab-content", "children"), Input("tabs", "value"))
def render_tab(tab):
    if tab == "census":
        return census_tab()
    elif tab == "events":
        return events_tab()
    elif tab == "presidents":
        return presidents_tab()
    elif tab == "map":
        return map_tab()
    elif tab == "forecast":
        return forecast_tab()
    elif tab == "events_pop":
        return events_pop_tab()
    return census_tab()


def census_tab():
    if "census" not in DATA:
        return card("Censo", html.P("No hay datos disponibles"))
    df = DATA["census"]
    national = df.groupby("census_year")["population"].sum().sort_index()
    top_region = (
        df[df["census_year"] == df["census_year"].max()]
        .sort_values("population", ascending=False)
        .iloc[0]
    )
    stats = stat_row(
        [
            (
                str(df["region"].nunique()),
                "Regiones",
                COLORS["teal"],
                national.values.tolist(),
                f"{national.iloc[-1]:,.0f} miles hoy",
            ),
            (
                str(int(df["census_year"].min()))
                + "–"
                + str(int(df["census_year"].max())),
                "Censos",
                COLORS["sienna"],
                national.values.tolist(),
                f"{len(national)} censos",
            ),
            (
                str(int(national.iloc[-1])),
                "Población (miles)",
                COLORS["gold"],
                national.values.tolist(),
                f"Top: {top_region['region']}",
            ),
        ]
    )
    fig_line = px.line(
        df,
        x="census_year",
        y="population",
        color="region",
        title="Población por Región (miles) — clic una serie para aislar",
        markers=True,
    )
    fig_line.update_layout(**EARTHTONE_PLOTLY, height=600)
    fig_line.update_traces(
        line=dict(shape="spline", width=2.5),
        marker=dict(size=7, symbol="circle"),
        hovertemplate="<b>%{fullData.name}</b><br>Año: %{x}<br>Población: %{y:,.0f} miles<extra></extra>",
    )
    pivot = df.pivot_table(
        index="region", columns="census_year", values="population", fill_value=0
    )
    fig_heat = px.imshow(
        pivot,
        title="Mapa de Calor: Población por Región y Año",
        labels={"color": "Población (miles)"},
        aspect="auto",
    )
    fig_heat.update_layout(**EARTHTONE_PLOTLY, height=500)
    fig_violin = px.violin(
        df,
        x="census_year",
        y="population",
        box=True,
        points=False,
        title="Distribución regional por censo (ridgeline)",
        color_discrete_sequence=[COLORS["teal"]],
    )
    fig_violin.update_layout(**EARTHTONE_PLOTLY, height=420)
    fig_violin.update_traces(
        meanline_visible=True,
        hovertemplate="Censo %{x}<br>Población: %{y:,.0f} miles<extra></extra>",
    )
    return html.Div(
        [
            stats,
            card(
                "Key Insights — Censo",
                html.Div(
                    [
                        insight_card(
                            "¿Problema?",
                            "Regiones históricas (1907–1970) no calzan con GeoJSON moderno; la serie se rompe sin mapeo.",
                            COLORS["teal"],
                        ),
                        insight_card(
                            "¿Metodología?",
                            "Columna modern_region + forecast lineal con IC 95% y warnings de extrapolación.",
                            COLORS["sienna"],
                        ),
                        insight_card(
                            "¿Decisión?",
                            "Usa la serie nacional para planificar; clic una región para aislarla en el mapa.",
                            COLORS["gold"],
                        ),
                    ]
                ),
            ),
            card(
                "Evolución Demográfica",
                html.Div(
                    [
                        dcc.Graph(id="census-line", figure=fig_line),
                        html.Div(
                            id="census-crossfilter-output",
                            style={
                                "marginTop": "8px",
                                "fontWeight": "700",
                                "fontFamily": "Georgia, serif",
                            },
                        ),
                    ]
                ),
            ),
            card(
                "Distribución por Censo — violines",
                html.Div(
                    [
                        dcc.Graph(figure=fig_violin),
                        html.Div(
                            "Insight: la cola superior se alarga con el tiempo — la concentración metropolitana crece.",
                            style={
                                "fontStyle": "italic",
                                "color": COLORS["muted"],
                                "marginTop": "8px",
                                "fontFamily": "Georgia, serif",
                            },
                        ),
                    ]
                ),
            ),
            card("Mapa de Calor", dcc.Graph(figure=fig_heat)),
        ]
    )


@callback(
    Output("census-crossfilter-output", "children"),
    Input("census-line", "clickData"),
    prevent_initial_call=True,
)
def census_crossfilter(click):
    if not click:
        return no_update
    pt = click["points"][0]
    region = pt.get("legendgroup", pt.get("curveNumber", "?"))
    return (
        f"Serie seleccionada: {region} — abre el tab Mapa para verla georreferenciada."
    )


def events_tab():
    if "events" not in DATA:
        return card("Eventos", html.P("No hay datos disponibles"))
    df = DATA["events"].sort_values("year")
    stats = stat_row([(str(len(df)), "Eventos")])
    fig_events = px.scatter(
        df,
        x="year",
        y="type",
        color="type",
        hover_data=["event", "city"],
        title="Línea de Tiempo de Eventos Históricos — clic para filtrar",
        size=[10] * len(df),
    )
    fig_events.update_layout(**EARTHTONE_PLOTLY, height=400)
    fig_events.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>Año: %{x}<br>Tipo: %{y}<extra>Clic para filtrar</extra>",
    )
    type_counts = df["type"].value_counts()
    fig_types = px.pie(
        values=type_counts.values,
        names=type_counts.index,
        title="Distribución por Tipo de Evento",
        color_discrete_sequence=[
            "#1a6b5a",
            "#a0522d",
            "#556b2f",
            "#b8860b",
            "#191970",
            "#8b4513",
        ],
    )
    fig_types.update_layout(**EARTHTONE_PLOTLY, height=400)
    fig_types.update_traces(
        marker=dict(line=dict(color="#f7f3e9", width=2)),
        textfont_size=12,
    )
    return html.Div(
        [
            stats,
            card(
                "Línea de Tiempo",
                html.Div(
                    [
                        dcc.Graph(id="events-scatter", figure=fig_events),
                        html.Div(
                            id="events-crossfilter-output",
                            style={
                                "marginTop": "8px",
                                "fontWeight": "700",
                                "fontFamily": "Georgia, serif",
                            },
                        ),
                    ]
                ),
            ),
            card("Distribución por Tipo", dcc.Graph(figure=fig_types)),
        ]
    )


@callback(
    Output("events-crossfilter-output", "children"),
    Input("events-scatter", "clickData"),
    prevent_initial_call=True,
)
def events_crossfilter(click):
    if not click:
        return no_update
    pt = click["points"][0]
    return f"Evento: año {pt.get('x', '?')} ({pt.get('y', '?')}) — ver su diferencia entre censos en Eventos-Población."


def presidents_tab():
    if "presidents" not in DATA:
        return card("Presidentes", html.P("No hay datos disponibles"))
    df = DATA["presidents"].sort_values("start")
    stats = stat_row([(str(len(df)), "Presidentes")])
    fig_pres = px.timeline(
        df,
        x_start="start",
        x_end="end",
        y="name",
        color="name",
        hover_data=["birthplace"],
        title="Línea de Tiempo de Presidentes",
    )
    fig_pres.update_layout(**EARTHTONE_PLOTLY, height=800, showlegend=False)
    if "birthplace" in df.columns:
        birth_counts = df["birthplace"].value_counts().head(10)
        fig_birth = px.bar(
            x=birth_counts.index,
            y=birth_counts.values,
            title="Top 10 Ciudades de Origen",
            labels={"x": "Ciudad", "y": "Cantidad"},
            color_discrete_sequence=[
                "#1a6b5a",
                "#a0522d",
                "#556b2f",
                "#b8860b",
                "#191970",
                "#8b4513",
                "#6b8e23",
                "#cd853f",
                "#1a6b5a",
                "#a0522d",
            ],
        )
        fig_birth.update_layout(**EARTHTONE_PLOTLY, height=400)
        fig_birth.update_traces(marker=dict(line=dict(width=0), cornerradius=4))
        return html.Div(
            [
                stats,
                card("Línea de Tiempo", dcc.Graph(figure=fig_pres)),
                card("Ciudades de Origen", dcc.Graph(figure=fig_birth)),
            ]
        )
    return html.Div([stats, card("Línea de Tiempo", dcc.Graph(figure=fig_pres))])


def map_tab():
    if "census" not in DATA or "geojson" not in DATA:
        return card("Mapa", html.P("No hay datos disponibles"))
    df = DATA["census"]
    max_year = int(df["census_year"].max())
    latest = df[df["census_year"] == max_year]
    fig_map = px.choropleth(
        latest,
        geojson=DATA["geojson"],
        locations="region",
        featureidkey="properties.NOM_REG",
        color="population",
        title=f"Población por Región — Censo {max_year} (clic una región)",
        hover_name="region",
        color_continuous_scale=[
            [0, "#f5eed8"],
            [0.2, "#c8e6c9"],
            [0.4, "#81c784"],
            [0.6, "#1a6b5a"],
            [0.8, "#0d4f3f"],
            [1.0, "#191970"],
        ],
    )
    fig_map.update_geos(fitbounds="locations", visible=False, bgcolor="#0a0e14")
    fig_map.update_layout(
        **EARTHTONE_PLOTLY,
        height=700,
        margin=dict(l=0, r=0, t=50, b=0),
        coloraxis_colorbar=dict(
            title=dict(
                text="Población (miles)", font=dict(family="Georgia, serif", size=13)
            ),
            tickfont=dict(family="JetBrains Mono,monospace"),
            thickness=18,
            len=0.6,
        ),
    )
    fig_map.update_traces(
        hovertemplate="<b>%{location}</b><br>Población: %{z:,.0f} miles<extra>Clic para filtrar</extra>",
    )
    return card(
        "Mapa de Chile — clic una región",
        html.Div(
            [
                dcc.Graph(id="geo-choropleth", figure=fig_map),
                html.Div(
                    id="map-crossfilter-output",
                    style={
                        "marginTop": "8px",
                        "fontWeight": "700",
                        "fontFamily": "Georgia, serif",
                    },
                ),
            ]
        ),
    )


@callback(
    Output("map-crossfilter-output", "children"),
    Input("geo-choropleth", "clickData"),
    prevent_initial_call=True,
)
def map_crossfilter(click):
    if not click:
        return no_update
    r = click["points"][0].get("location", "?")
    return f"Región seleccionada: {r} — ver su serie en Censo y su forecast."


@callback(
    Output("forecast-crossfilter-output", "children"),
    Input("forecast-growth-bar", "clickData"),
    prevent_initial_call=True,
)
def forecast_crossfilter(click):
    if not click:
        return no_update
    r = click["points"][0].get("x", "?")
    return f"Región seleccionada: {r} — ver su serie histórica en Censo y su posición en el Mapa."


def forecast_tab():
    if "forecast" not in DATA:
        return card(
            "Forecast",
            html.P(
                "Ejecuta `python src/forecast_analysis.py` para generar pronósticos"
            ),
        )
    fc = DATA["forecast"]
    fdf = pd.DataFrame(fc["forecasts"])
    stats = stat_row(
        [
            (str(len(fdf)), "Regiones"),
            (str(fdf[fdf["growth_rate"] > 0].shape[0]), "En crecimiento"),
            (str(fdf[fdf["growth_rate"] < 0].shape[0]), "En declive"),
        ]
    )
    fig_forecast = go.Figure()
    for _, row in fdf.iterrows():
        fig_forecast.add_trace(
            go.Bar(
                x=[row["region"]],
                y=[row["pop_2025"]],
                name=row["region"],
                marker_color=COLORS["teal"]
                if row["growth_rate"] > 0
                else COLORS["sienna"],
                marker_line=dict(width=0),
            )
        )
        fig_forecast.add_trace(
            go.Bar(
                x=[row["region"]],
                y=[row["pop_2030"] - row["pop_2025"]],
                name=row["region"],
                marker_color=COLORS["gold"]
                if row["growth_rate"] > 0
                else COLORS["olive"],
                marker_line=dict(width=0),
                base=[row["pop_2025"]],
                showlegend=False,
            )
        )
    fig_forecast.update_layout(
        barmode="stack",
        **EARTHTONE_PLOTLY,
        height=500,
        title="Población Proyectada 2025 vs 2030",
    )
    fig_forecast.update_layout(xaxis_tickangle=-45, yaxis_title="Población (miles)")
    fig_growth = px.bar(
        fdf,
        x="region",
        y="growth_rate",
        color="growth_rate",
        color_continuous_scale=[
            [0, COLORS["sienna"]],
            [0.5, COLORS["gold"]],
            [1, COLORS["teal"]],
        ],
        title="Tasa de Crecimiento por Región — clic para filtrar",
    )
    fig_growth.update_layout(**EARTHTONE_PLOTLY, height=400)
    fig_growth.update_layout(xaxis_tickangle=-45)
    fig_growth.update_traces(
        marker=dict(cornerradius=4),
        hovertemplate="<b>%{x}</b><br>Crecimiento: %{y:.2%}<extra>Clic para filtrar</extra>",
    )
    return html.Div(
        [
            stats,
            card("Población Proyectada", dcc.Graph(figure=fig_forecast)),
            card(
                "Tasas de Crecimiento — clic para filtrar",
                html.Div(
                    [
                        dcc.Graph(id="forecast-growth-bar", figure=fig_growth),
                        html.Div(
                            id="forecast-crossfilter-output",
                            style={
                                "marginTop": "8px",
                                "fontWeight": "700",
                                "fontFamily": "Georgia, serif",
                            },
                        ),
                    ]
                ),
            ),
            card(
                "Tabla de Pronósticos",
                dash_table.DataTable(
                    data=fdf.to_dict("records"),
                    columns=[{"name": c, "id": c} for c in fdf.columns],
                    sort_action="native",
                    style_table={"overflowX": "auto"},
                    style_header={
                        "backgroundColor": COLORS["cream"],
                        "color": COLORS["teal"],
                        "fontWeight": "bold",
                        "fontFamily": "Georgia, serif",
                        "borderBottom": f"2px solid {COLORS['gold']}",
                    },
                    style_cell={
                        "backgroundColor": COLORS["card"],
                        "color": COLORS["text"],
                        "border": f"1px solid {COLORS['border']}",
                        "padding": "10px 14px",
                        "fontFamily": "'Segoe UI', system-ui, sans-serif",
                    },
                    style_data_conditional=[
                        {
                            "if": {"row_index": "odd"},
                            "backgroundColor": COLORS["card_alt"],
                        },
                    ],
                ),
            ),
        ]
    )


def events_pop_tab():
    if "forecast" not in DATA:
        return card(
            "Eventos-Población", html.P("Ejecuta `python src/forecast_analysis.py`")
        )
    fc = DATA["forecast"]
    if not fc.get("event_temporal_diff"):
        return card(
            "Eventos-Población", html.P("No hay diferencias temporales disponibles")
        )
    edf = pd.DataFrame(fc["event_temporal_diff"])
    census = DATA.get("census")
    national = (
        census.groupby("census_year")["population"].sum().reset_index()
        if census is not None
        else pd.DataFrame()
    )
    timeline_figs = []
    if not national.empty:
        fig_national = px.line(
            national,
            x="census_year",
            y="population",
            markers=True,
            title="Población Nacional a lo Largo del Tiempo",
        )
        fig_national.update_layout(**EARTHTONE_PLOTLY, height=400)
        fig_national.update_traces(
            line=dict(shape="spline", width=3, color=COLORS["teal"]),
            marker=dict(size=8, symbol="circle", color=COLORS["gold"]),
        )
        for _, ev in edf.iterrows():
            fig_national.add_vline(
                x=ev["year"],
                line_dash="dash",
                line_color=COLORS["sienna"],
                annotation_text=ev["event"][:20],
                annotation_font=dict(
                    family="Georgia, serif", size=10, color=COLORS["sienna"]
                ),
            )
        timeline_figs.append(
            card("Población con Eventos", dcc.Graph(figure=fig_national))
        )
    fig_impact = px.bar(
        edf,
        x="event",
        y="change_pct",
        color="change_pct",
        color_continuous_scale=[
            [0, COLORS["sienna"]],
            [0.5, COLORS["gold"]],
            [1, COLORS["teal"]],
        ],
        title="Δ Población entre censos contiguos al evento (%)",
    )
    fig_impact.update_layout(**EARTHTONE_PLOTLY, height=400)
    fig_impact.update_layout(xaxis_tickangle=-45)
    fig_impact.update_traces(marker=dict(cornerradius=4))
    fig_scatter = px.scatter(
        edf,
        x="year",
        y="change_pct",
        size="pop_before",
        hover_name="event",
        title="Densidad de Eventos vs Cambio Poblacional",
        color="change_pct",
        color_continuous_scale=[
            [0, COLORS["sienna"]],
            [0.5, COLORS["gold"]],
            [1, COLORS["teal"]],
        ],
    )
    fig_scatter.update_layout(**EARTHTONE_PLOTLY, height=400)
    return html.Div(
        timeline_figs
        + [
            card(
                "Δ Población por Evento (asociación, no causal)",
                dcc.Graph(figure=fig_impact),
            ),
            card("Eventos vs Cambio Poblacional", dcc.Graph(figure=fig_scatter)),
        ]
    )


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8052)))
