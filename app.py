import utils.params as p
import utils.functions as f

import pandas as pd
from datetime import datetime

import plotly.graph_objects as go
from dash import html, dcc, Dash

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import strava_api as sa

# nb_ajout = sa.update_db()

year = "2024-01-01"
# workout_data = f.retrieve_workout({"start_date>= ": year, "sport_type=": "Run"})
workout_data = f.retrieve_workout()
columns_name = [el[0] for el in f.retrieve_col_name("activities_infos")]


df = pd.DataFrame(data=workout_data, columns=columns_name)
df["mois"] = pd.to_datetime(df["start_date"], format="%Y-%m-%d").dt.strftime("%B %Y")
df["semaine_date"] = (
    pd.to_datetime(df["start_date"], format="%Y-%m-%d")
    .dt.to_period("W")
    .apply(lambda r: r.start_time)
)


type_activite_df = (
    df[["id", "sport_type"]]
    .groupby("sport_type")
    .count()
    .reset_index()
    .to_dict("records")
)

type_activite = [
    {
        "label": "" + el["sport_type"] + " (" + str(el["id"]) + ")",
        "value": el["sport_type"],
    }
    for el in type_activite_df
]

# weekly_dist = get_data(agregat, unite, sport_type)
# weekly_df = weekly_dist.reset_index()

# weekly_dist = get_data(sport, duree)
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

"""fig = go.Figure(
    go.Bar(
        x=weekly_df["semaine"],
        y=weekly_df["distance"],
        hovertemplate="<b>Semaine:</b> %{x}<br>"  # The x-axis value
        + "<b>Dist:</b> %{y}<br>"  # The y-axis value
        + "<extra></extra>",  # Removes the default trace label, marker_line_width=0
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


x_axis_name = fig.layout.xaxis.title.text
y_axis_name = fig.layout.yaxis.title.text"""

# Layout definition
app.layout = dbc.Container(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H1(
                            [
                                html.Span("Welcome"),
                                html.Br(),
                                html.Span("to my beautiful dashboard!"),
                            ]
                        ),
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
                        html.Div(
                            [
                                html.H2("Unclearable Dropdown:"),
                                dcc.Dropdown(
                                    options=type_activite,
                                    clearable=False,
                                    optionHeight=40,
                                    className="customDropdown",
                                    id="sport_type",
                                    value=type_activite[0]["value"],
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.H2("Unclearable Dropdown:"),
                                dcc.Dropdown(
                                    options=[
                                        {"label": "Semaine", "value": "semaine_date"},
                                        {"label": "Mois", "value": "mois"},
                                    ],
                                    clearable=False,
                                    optionHeight=40,
                                    className="customDropdown",
                                    id="agreg_type",
                                    value="semaine_date",
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.H2("Clearable Dropdown:"),
                                dcc.Dropdown(
                                    options=[
                                        {"label": "Distance", "value": "distance"},
                                        {"label": "Duree", "value": "duree"},
                                    ],
                                    clearable=True,
                                    optionHeight=40,
                                    className="customDropdown",
                                    id="duree_type",
                                    value="distance",
                                ),
                            ]
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
                    dcc.Graph(id="graph"),  # ID for the graph component
                    style={"width": 790},
                ),
                html.Div(
                    [
                        html.H2(id="x_axis_label"),  # Dynamic X axis label
                        html.Div(
                            html.H3("Selected Value", id="click-output1"),
                            className="Output",
                        ),  # Div for the x value
                        html.H2(id="y_axis_label"),  # Dynamic Y axis label
                        html.Div(
                            html.H3("Selected Value", id="click-output2"),
                            className="Output",
                        ),  # H3 for the y value
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


@app.callback(
    [
        Output("click-output1", "children"),  # Output to the X-value display
        Output("click-output2", "children"),  # Output to the Y-value display
    ],  # Y Value label
    [Input("graph", "clickData")],  # Input is clickData from the bar chart
)
def display_click_data(clickData):
    if clickData is None:
        return "No bar clicked", "No bar clicked"

    # Get the clicked x and y values
    x_value = clickData["points"][0]["x"]
    y_value = clickData["points"][0]["y"]

    # Update the output with the clicked data
    return (x_value, y_value)


# Callback to update the graph based on dropdown selections
@app.callback(
    [
        Output("graph", "figure"),
        Output("x_axis_label", "children"),
        Output("y_axis_label", "children"),
    ],
    [
        Input("sport_type", "value"),
        Input("duree_type", "value"),
        Input("agreg_type", "value"),
    ],
)
def update_graph(sport, duree, agreg):
    # Get the data based on selected sport and duration
    weekly_dist = df.loc[df["sport_type"] == sport].groupby(agreg).sum(duree)
    weekly_df = weekly_dist.reset_index()

    # Create the figure
    fig = go.Figure(
        go.Bar(
            x=weekly_df[agreg],
            y=weekly_df[duree],
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

    # Return updated figure and axis labels
    return fig, "Semaine:", "Distance:"


if __name__ == "__main__":
    app.run_server(debug=True)
