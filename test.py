import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc


# Mock function for get_data (you can replace it with your actual function)
def get_data(sport, duree):
    data = {
        "semaine": ["2023-10-02", "2023-10-09", "2023-10-16", "2023-10-23"],
        "distance": [5, 10, 15, 7] if sport == 1 else [3, 8, 13, 6],
    }
    return pd.DataFrame(data)


# Options pour le type d'activité (exemple)
type_activite = [{"label": "Running", "value": 1}, {"label": "Cycling", "value": 2}]

# Initialisation de l'application
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Layout de l'application
app.layout = dbc.Container(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H1(["Welcome", html.Br(), "to my beautiful dashboard!"]),
                        html.P(
                            "This dashboard prototype shows how to create an effective layout."
                        ),
                    ],
                    style={"vertical-alignment": "top", "height": 260},
                ),
                html.Div(
                    [
                        html.Div(
                            dbc.RadioItems(
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-outline-light",
                                labelCheckedClassName="btn btn-light",
                                options=[
                                    {"label": "Graph", "value": 1},
                                    {"label": "Table", "value": 2},
                                ],
                                value=1,
                                style={"width": "100%"},
                            ),
                            style={"width": 206},
                        ),
                        html.Div(
                            dbc.Button("About", className="btn btn-info", n_clicks=0),
                            style={"width": 104},
                        ),
                    ],
                    style={"margin-left": 15, "margin-right": 15, "display": "flex"},
                ),
                html.Div(
                    [
                        # Interrupteur pour sélectionner le type de sport
                        html.Div(
                            [
                                html.H2("Type d'activité:"),
                                html.Div(
                                    [
                                        html.Label(
                                            "Running", style={"margin-right": "10px"}
                                        ),  # Label gauche
                                        dbc.Switch(
                                            id="sport_type_switch",
                                            label="",
                                            value=True,  # Valeur par défaut
                                            className="customSwitch",
                                            style={
                                                "margin-left": "10px",
                                                "margin-right": "10px",
                                            },
                                        ),
                                        html.Label(
                                            "Cycling", style={"margin-left": "10px"}
                                        ),  # Label droit
                                    ],
                                    style={
                                        "display": "flex",
                                        "align-items": "center",
                                        "justify-content": "space-between",
                                        "width": "200px",
                                    },  # Centering and width control
                                ),
                            ],
                            style={"margin-bottom": "20px", "text-align": "center"},
                        ),
                        # Interrupteur pour sélectionner la durée
                        html.Div(
                            [
                                html.H2("Durée:"),
                                html.Div(
                                    [
                                        html.Label(
                                            "Semaine", style={"margin-right": "10px"}
                                        ),  # Label gauche
                                        html.Div(
                                            [
                                                dbc.Switch(
                                                    id="duree_type_switch",
                                                    label="",
                                                    value=True,  # Valeur par défaut (semaine)
                                                    className="customSwitch",
                                                    style={
                                                        "margin-left": "10px",
                                                        "margin-right": "10px",
                                                    },
                                                )
                                            ]
                                        ),
                                        html.Label(
                                            "Mois", style={"margin-left": "10px"}
                                        ),  # Label droit
                                    ],
                                    style={
                                        "display": "flex",
                                        "align-items": "center",
                                        "justify-content": "space-between",
                                        "width": "200px",
                                    },  # Centering and width control
                                ),
                            ],
                            style={"margin-bottom": "20px", "text-align": "center"},
                        ),
                    ],
                    style={"margin-left": 15, "margin-right": 15, "margin-top": 30},
                ),
                html.Div(
                    html.Img(
                        src="assets/image.svg",
                        style={
                            "margin-left": 15,
                            "margin-right": 15,
                            "margin-top": 30,
                            "width": 310,
                        },
                    )
                ),
            ],
            style={
                "width": 340,
                "margin-left": 35,
                "margin-top": 35,
                "margin-bottom": 35,
            },
        ),
        html.Div(
            [
                html.Div(
                    dcc.Graph(id="graph"),  # ID du composant graphique
                    style={"width": 790},
                ),
                html.Div(
                    [
                        html.H2(id="x_axis_label"),  # Label dynamique pour l'axe X
                        html.Div(
                            html.H3("Selected Value", id="click-output1"),
                            className="Output",
                        ),  # Affichage pour la valeur X
                        html.H2(id="y_axis_label"),  # Label dynamique pour l'axe Y
                        html.Div(
                            html.H3("Selected Value", id="click-output2"),
                            className="Output",
                        ),  # Affichage pour la valeur Y
                    ],
                    style={"width": 198},
                ),
            ],
            style={
                "width": 990,
                "margin-top": 35,
                "margin-right": 35,
                "margin-bottom": 35,
                "display": "flex",
            },
        ),
    ],
    fluid=True,
    style={"display": "flex"},
    className="dashboard-container",
)


# Callback pour mettre à jour le graphique en fonction des interrupteurs
@app.callback(
    [
        Output("graph", "figure"),
        Output("x_axis_label", "children"),
        Output("y_axis_label", "children"),
    ],
    [Input("sport_type_switch", "value"), Input("duree_type_switch", "value")],
)
def update_graph(sport_switch, duree_switch):
    # Convertir la valeur des interrupteurs en options correspondantes
    sport = 1 if sport_switch else 2  # 1 = Running, 2 = Cycling
    duree = "semaine_date" if duree_switch else "mois"

    # Obtenir les données basées sur le sport et la durée
    weekly_dist = get_data(sport, duree)
    weekly_df = weekly_dist.reset_index()

    # Créer le graphique
    fig = go.Figure(
        go.Bar(
            x=weekly_df["semaine"],
            y=weekly_df["distance"],
            hovertemplate="<b>Semaine:</b> %{x}<br>"
            + "<b>Dist:</b> %{y}<br>"
            + "<extra></extra>",
        )
    )
    fig.update_yaxes(ticklabelposition="inside top", title=None, title_font_color="red")
    fig.update_layout(
        plot_bgcolor="#ffffff",
        width=790,
        height=730,
        xaxis_visible=False,
        yaxis=dict(gridcolor="#525252"),
        yaxis_visible=True,
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
    )

    # Retourner le graphique et les labels d'axes
    return fig, "Semaine:", "Distance:"


# Callback pour afficher les données cliquées sur le graphique
@app.callback(
    [Output("click-output1", "children"), Output("click-output2", "children")],
    [Input("graph", "clickData")],
)
def display_click_data(clickData):
    if clickData is None:
        return "No bar clicked", "No bar clicked"

    # Récupérer les valeurs X et Y cliquées
    x_value = clickData["points"][0]["x"]
    y_value = clickData["points"][0]["y"]

    # Mettre à jour l'affichage avec les données cliquées
    return x_value, y_value


if __name__ == "__main__":
    app.run_server(debug=True)
