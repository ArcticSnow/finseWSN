import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from app import app
import var_dict as vd

import numpy as np
import db_query as db
import datetime
import pandas as pd

serial = 3668


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


layout = html.Div(children=[
    html.Div([html.Link(href='/static/whitey.css', rel='stylesheet')]),
    dcc.Markdown('''
# Stationnary Eddy-Covariance Station

This station records information about:
- air temperature, air pressure
- wind speed and direction
- snow depth,
- incoming and out going radiation (shortwave and longwave)
- soil heat flux, soil temperature
- surface temperature
- snow drfiting
- precipitation

Station Description:
- Location: []()
- Sensors:

- Database ID: 3668


'''),
    dcc.Slider(id='ndays', min=1, max=10, step=1, value=5, marks={i: '{} days'.format(i) for i in range(2, 10, 1)}),
    html.Div(id='output_graphs_thomas'),
    dcc.Markdown('''
---
## Return to [Home](index)
''')
])


@app.callback(
    Output(component_id='output_graphs_thomas', component_property='children'),
    [Input(component_id='ndays', component_property='value')]
)
def update_graph_table_thomas(input_ndays):
    start = datetime.datetime.now() - datetime.timedelta(days=input_ndays)
    end = datetime.datetime.now()

    var_oi = ['RECORD', 'TA_2_1_1_1_1',
              'RH_19_3_1_1_1',
              'WD_20_35_1_1_1', 'WS_16_33_1_1_1',
              'METNOR_99_99_1_1_1',
              'FC1DRIFTmean_99_99_1_1_1', 'FC2DRIFTmean_99_99_1_1_1','time'
              ]
    df = db.query_df(serial=serial, table_name='Biomet', time__gte=start, time__lte=end, limit=2500000, fields=var_oi)

    #df = db.query_df(serial=serial, table_name='Biomet', time__gte=start, time__lte=end, limit=100000)

    df.set_index(pd.to_datetime(df.time), inplace=True)
    df.rename(columns=vd.CR6_biomet_perm, inplace=True)
    df.ws = df.ws.astype(float, inplace=True)
    df.fc2drift_mean = df.fc2drift_mean.astype(float)
    df.fc1drift_mean = df.fc1drift_mean.astype(float)


    graph_content = html.Div([
        html.H2(children='Air Temperature'),
        dcc.Graph(
            id='gr1',
            figure={
                'data': [{
                    'x': df.time,
                    'y': df.ta, 'name': 'temp'}],
                'layout': {'yaxis': {'title': 'Temperature [degC]'}}
            }),
        html.H2(children='Wind Speed'),
        dcc.Graph(
            id='gr2',
            figure={
                'data': [{
                    'x': df.time,
                    'y': df.ws, 'name': 'speed'}],
                'layout': {'yaxis': {'title': 'Wind speed [m/s]'}}
            }),
        html.H2(children='Wind Direction'),
        dcc.Graph(
            id='gr3',
            figure={
                'data': [{
                    'x': df.time,
                    'y': df.wd, 'name': 'direction'}],
                'layout': {'yaxis': {'title': 'Wind direction [deg]'}}
            }),
        html.H2(children='Snow Drift Flux'),
        dcc.Graph(
            id='gr4',
            figure={
                'data': [{
                    'x': df.time,
                    'y': df.fc1drift_mean + df.fc2drift_mean, 'name': 'drift'}],
                'layout': {'yaxis': {'title': 'Flux [kg/(m.s)]'}}
            }),
        html.H2(children='Precipitation'),
        dcc.Graph(
            id='gr5',
            figure={
                'data': [{
                    'x': df.time,
                    'y': df.metno_rr, 'name': 'precip'}],
                'layout': {'yaxis': {'title': 'Precipitation [mm]'}}
            }),
        html.H2(children='Table head of the Stationnary Flux data'),
        generate_table(df.tail(100), 10)
    ])
    return graph_content



