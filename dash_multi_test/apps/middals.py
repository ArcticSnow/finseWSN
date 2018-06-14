import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from app import app

import numpy as np
import db_query as db
import datetime


serial = 6951419298100303058


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
# Middalselvi Discharge Station

Located along the stream running out of middalsbreen, this discharge station records information about water depth, water temperature, water conductivity. 

- Location: [N 60.5767425, E 7.5024458](http://www.norgeskart.no/#!/?zoom=14&lon=89712.76&lat=6739076.09&project=seeiendom&layers=1002,1015)
- Sensor: [Decagon ctd-10](https://www.metergroup.com/environment/products/hydros-21-water-level-monitoring/)
- Database ID: 6951419298100303058
- Available variables :
    - water depth
    - water temperature
    - water electrical conductivity
    - Station battery
    - Station signal reception power (RSSI)

''' ),
    dcc.Slider(id='ndays', min=2, max=32, step=2, value=14,marks={i: '{} days'.format(i) for i in range(2,30,2)}),
    html.Div(id='output_graphs'),
dcc.Link('Go to Home', href='index'),
    dcc.Markdown('''
## Page future development:
- Example to pull data from DB
- See to show water level in a abstracted cross section
- Add running average for conductivity and depth
- get shared x-axis for the three plots
- have an input box setting the start and final date to display, default being 15 days until now
- Go multi-page, one for each station

---
## Return to [Home](index)

''')
])



@app.callback(
    Output(component_id='output_graphs', component_property='children'),
    [Input(component_id='ndays', component_property='value')]
)
def update_graph_table(input_ndays):
    start = datetime.datetime.now() - datetime.timedelta(days=input_ndays)
    end = datetime.datetime.now()


    df_middal = db.query_df(serial=serial, time__gte=start, time__lte=end, limit=100000)
    df = df_middal.loc[~np.isnan(df_middal.ctd_depth)]
    df = df.reset_index()
    df.ctd_cond.loc[df.ctd_cond < 0.01] = np.nan

    graph_content = html.Div([
        html.H2(children='Water Discharge'),
        dcc.Graph(
            id='gr1',
            figure={
                'data': [{
                    'x': df.time,
                    'y': df.ctd_depth / 10, 'name': 'depth'}],
                'layout': {'yaxis': {'title': 'Water Depth [cm]'}}
            }),
        html.H2(children='Water Temperature'),
        dcc.Graph(
            id='gr2',
            figure={
                'data': [{
                    'x': df.time,
                    'y': df.ctd_temp, 'name': 'temp'}],
                'layout': {'yaxis': {'title': 'Temperature [degC]'}}
            }),
        html.H2(children='Water Electrical Conductivity'),
        dcc.Graph(
            id='gr3',
            figure={
                'data': [{
                    'x': df.time,
                    'y': df.ctd_cond, 'name': 'cond'}],
                'layout': {'yaxis': {'title': 'Electrical conductivity [dS/m]'}}
            }),
        html.H2(children='Table head of Middalselvi data stream'),
        generate_table(df.tail(100), 5)]
    )
    return graph_content



