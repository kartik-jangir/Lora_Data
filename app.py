# importing dash Modules
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import functions as f


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],  )
server = app.server  # the Flask app
app.title = 'pH Dashboard'
app.config.suppress_callback_exceptions=True


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.RadioItems(
                        id='time_period',
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "1D", "value": 1},
                            {"label": "7D Funds", "value": 2},
                            {"label": "All", "value": 3},
                        ],
                        value=1,
                    ),
            ],
            className="radio-group",style={'display':'inline'}
                ),
        ]),
        dbc.Col([
            html.H6(id = 'last_update_time')
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id = 'pH_div')
        ])
    ], class_name = 'mb-3'),
    dbc.Row([
        dbc.Col([
            html.Div(id = 'flow_div')
        ])
    ], class_name = 'mb-3'),
    dbc.Row([
        dbc.Col([
            html.Div(id = 'pressure_div')
        ])
    ], class_name = 'mb-3'),
    dcc.Interval(id = 'refresh_graphs', interval = 300000),
    dcc.Interval(id = 'refresh_data', interval = 60000)

])

@app.callback(Output('pH_div', 'children'),
              Output('flow_div', 'children'),
              Output('pressure_div', 'children'),
              Input('refresh_graphs', 'n_intervals'),
              Input('time_period', 'value')
              )
def graph_funct(n, time_period):
    ph, flow, pressure = f.graph_maker(time_period)
    return ph, flow, pressure

@app.callback(Output('last_update_time', 'children'),
              Input('refresh_data', 'n_intervals')
              )
def data_funct(n):
    update_time = f.update_data()
    return update_time

# Running the Dash Server
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=5050,debug=True)
