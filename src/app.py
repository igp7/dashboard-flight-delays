import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as datatable
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import numpy as np


COLS_TO_SHOW = ['FLIGHT_NUMBER', 'DATE_FLIGHT', 'AIRLINE_CODE',
                'ORIGIN_CITY', 'DESTINATION_CITY', 'DEPARTURE_DELAY']
MESES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
         'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']


external_stylesheets = [dbc.themes.SIMPLEX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = pd.read_csv('./data/vuelos.csv')
df.assign(DATE_FLIGHT=pd.to_datetime(df.YEAR * 10000 + df.MONTH * 100 + df.DAY, format='%Y%m%d'))


body = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div(
                html.H2("Dashboard sobre retrasos en vuelos de EEUU en 2015")
            ), align='center'
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Dropdown(
                    id='origin_state',
                    options=[{'label': state, 'value': state} for state in df.ORIGIN_STATE.unique()],
                    value=[],
                    placeholder="Selecciona un estado",
                    multi=True
                )
            ), width=4, align='center'
        ),
        dbc.Col(
            html.Div(
                dcc.Dropdown(
                    id='origin_city',
                    options=[],
                    value=[],
                    placeholder="Selecciona una ciudad",
                    multi=True
                )
            ), width=4, align='center'
        )
    ], justify='center', align='end'),
    dbc.Row([
        dbc.Col(
            html.Div(
                datatable.DataTable(
                    id='table',
                    columns=[{'id': col, 'name': col} for col in COLS_TO_SHOW],
                    data=df.to_dict('records'),
                    page_size=10,
                    sort_action='native',
                    filter_action='native',
                    style_table={'overflowX': 'scroll', 'overflowY': 'scroll', 'maxHeight': '40vh'},
                    style_data_conditional=[
                        {
                            'if': {
                                'row_index': 'odd'
                            },
                            'backgroundColor': '#EBEBEB'
                        },
                        {
                            'if': {'filter_query': '{DEPARTURE_DELAY} > 60'},
                            'backgroundColor': '#FD6666',
                            'color': '#000000'
                        },
                        {
                            'if': {'filter_query': '{DEPARTURE_DELAY} < 0'},
                            'backgroundColor': '#B7FA9B',
                            'color': '#000000'
                        }
                    ],
                    style_header={
                        'backgroundColor': '#cbddf2',
                        'fontWeight': 'bold'
                    },
                    style_cell={
                        'padding-left': '2px',
                        'textAlign': 'left',
                        'border': 'thin black solid'
                    }
                )
            ), width=6, align='center'
        ),
        dbc.Col(
            html.Div(
                dcc.Graph(
                    id='grafico',
                    figure={
                        'data': [
                            go.Scattergl(
                                x=df['AIRLINE_CODE'],
                                y=df['DEPARTURE_DELAY'],
                                text=df['ORIGIN_CITY'],
                                mode='markers',
                                opacity=0.9,
                                marker={
                                    'size': 8,
                                    'line': {'width': 0.5, 'color': 'white'},
                                    'color': '#FD6666'
                                },
                                name='Departure delay'
                            ),
                            go.Box(
                                x=df['AIRLINE_CODE'],
                                y=df['DEPARTURE_DELAY'],
                                boxmean=True,
                                opacity=0.5,
                                marker=dict(
                                    color='rgb(8,81,156)',
                                    outliercolor='rgb(219,64,82, 0.6)',
                                    line=dict(
                                        outliercolor='rgb(219,64,82, 0.6)',
                                        outlierwidth=2
                                    )
                                ),
                                name='Boxplot'
                            )
                        ],
                        'layout': go.Layout(
                            xaxis={'title': 'Airline'},
                            yaxis={'title': 'Delay',
                                   'range': [df.DEPARTURE_DELAY.min() - 10, df.DEPARTURE_DELAY.max()]},
                            margin={'l': 80, 'b': 40, 't': 80, 'r': 10},
                            legend={'x': 0, 'y': 1},
                            hovermode='closest',
                            autosize=True
                        )
                    }
                )
            ), width=6, align='end'
        )
    ], align='end', style={'padding-top': '2%'}),
    dbc.Row(),
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.RangeSlider(
                    id='range_months',
                    min=1,
                    max=12,
                    step=1,
                    value=[1, 12],
                    marks={int(mes): MESES[mes - 1] for mes in np.arange(1, 13)}
                )
            ), width=10, align='center'
        ),
        dbc.Col(
            html.Div(
                dcc.Input(
                    id='input_delay',
                    type='number',
                    placeholder='Delay minimo',
                    value=None
                )
            ), width=1, align='center'
        )
    ], justify='center'),
    dcc.Store(
        id='intermediate_filter_data',
        storage_type='memory'
    )
], fluid=True)
app.layout = html.Div([body])


# Callbacks
@app.callback(
    Output('origin_city', 'options'),
    Input('origin_state', 'value')
)
def update_city_options(states):
    options = df.loc[df.ORIGIN_STATE.isin(states)].ORIGIN_CITY.unique()
    return [{'label': city, 'value': city} for city in options]


@app.callback(
    Output('intermediate_filter_data', 'data'),
    [Input('origin_state', 'value'),
     Input('origin_city', 'value'),
     Input('range_months', 'value'),
     State('input_delay', 'value')]
)
def save_filter_data(states, cities, months, delay_min):
    df_filter = df.copy()
    rango_meses = np.arange(months[0], months[1] + 1)
    df_filter = df_filter.loc[df.MONTH.isin(list(rango_meses))]
    if delay_min is not None:
        df_filter = df_filter.loc[df.DEPARTURE_DELAY >= delay_min]
    if len(states) > 0:
        df_filter = df_filter.loc[df.ORIGIN_STATE.isin(states)]
    if len(cities) > 0:
        df_filter = df_filter.loc[df.ORIGIN_CITY.isin(cities)]
    return df_filter.to_json()


@app.callback(
    [Output('table', 'data'),
     Output('grafico', 'figure')],
    Input('intermediate_filter_data', 'data')
)
def update_table(data_json):
    df_filter_table_graph = pd.read_json(data_json, convert_dates=['DATE_FLIGHT'])
    return [df_filter_table_graph.to_dict('records'),
            {
                'data': [
                    go.Scattergl(
                        x=df_filter_table_graph['AIRLINE_CODE'],
                        y=df_filter_table_graph['DEPARTURE_DELAY'],
                        text=df_filter_table_graph['ORIGIN_CITY'],
                        mode='markers',
                        opacity=0.9,
                        marker={
                            'size': 8,
                            'line': {'width': 0.5, 'color': 'white'},
                            'color': '#FD6666'
                        },
                        name='Departure delay'
                    ),
                    go.Box(
                        x=df_filter_table_graph['AIRLINE_CODE'],
                        y=df_filter_table_graph['DEPARTURE_DELAY'],
                        boxmean=True,
                        opacity=0.5,
                        marker=dict(
                            color='rgb(8,81,156)',
                            outliercolor='rgb(219,64,82, 0.6)',
                            line=dict(
                                outliercolor='rgb(219,64,82, 0.6)',
                                outlierwidth=2
                            )
                        ),
                        name='Boxplot'
                    )
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Airline'},
                    yaxis={'title': 'Delay', 'range': [df_filter_table_graph.DEPARTURE_DELAY.min() - 10,
                                                       df_filter_table_graph.DEPARTURE_DELAY.max()]},
                    margin={'l': 80, 'b': 40, 't': 80, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest',
                    autosize=True
                )
            }]
