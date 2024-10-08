import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

# Create a sample figure for the graph
df = (
    px.data.gapminder()
    .query("year == 2007")
    .sort_values("pop", ascending=False)
    .head(10)
)
fig = px.bar(df, x="country", y="pop", hover_data=["pop"], labels={"pop": "Population"})

x_axis_name = fig.layout.xaxis.title.text
y_axis_name = fig.layout.yaxis.title.text

# Initialize the Dash app
app = dash.Dash(__name__)

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
                                    options=[
                                        {"label": "Option A", "value": 1},
                                        {"label": "Option B", "value": 2},
                                        {"label": "Option C", "value": 3},
                                    ],
                                    value=1,
                                    clearable=False,
                                    optionHeight=40,
                                    className="customDropdown",
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.H2("Unclearable Dropdown:"),
                                dcc.Dropdown(
                                    options=[
                                        {"label": "Option A", "value": 1},
                                        {"label": "Option B", "value": 2},
                                        {"label": "Option C", "value": 3},
                                    ],
                                    value=2,
                                    clearable=False,
                                    optionHeight=40,
                                    className="customDropdown",
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.H2("Clearable Dropdown:"),
                                dcc.Dropdown(
                                    options=[
                                        {"label": "Option A", "value": 1},
                                        {"label": "Option B", "value": 2},
                                        {"label": "Option C", "value": 3},
                                    ],
                                    clearable=True,
                                    optionHeight=40,
                                    className="customDropdown",
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
                    dcc.Graph(id="graph", figure=fig),  # ID for the graph component
                    style={"width": 790},
                ),
                html.Div(
                    [
                        html.H2(f"{x_axis_name}:"),
                        html.Div(
                            html.H3("Selected Value", id="hover-output1"),
                            className="Output",
                        ),  # Div for the x value (country)
                        html.H2(f"{y_axis_name}:"),
                        html.Div(
                            html.H3("Selected Value", id="hover-output2"),
                            className="Output",
                        ),  # H3 for the y value (population)
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


# Define the callback function to update both output elements
@app.callback(
    [
        Output(
            "hover-output1", "children"
        ),  # Update the div under Output 1 for the x value (country)
        Output("hover-output2", "children"),
    ],  # Update the h3 for the y value (population)
    Input("graph", "hoverData"),  # Get the hover data from the graph
)
def update_hover_data(hoverData):
    if hoverData is None:
        return "Hover over a bar", "Selected Value"  # Default text if no hover data

    # Extract x (country) and y (population) values from the hoverData
    country = hoverData["points"][0]["x"]
    population = hoverData["points"][0]["y"]

    # Return the country to output-1 div and population to hover-output h3
    return f"{country}", f"{population}"


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
