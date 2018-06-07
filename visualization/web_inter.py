import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import numpy as np

from pandas_datareader import data as web
from datetime import datetime as dt
from latice_db import db_query as db

import datetime, os

app = dash.Dash('Hello World')

app.layout = html.Div([
dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Water depth', 'name': 'depth'},
            {'label': 'Water temperature', 'name': 'temp'}
        ],
        value='COKE'
),
    dcc.Graph(id='gr_discharge')
], style={'width': '1000'})

@app.callback(Output('gr_discharge', 'figure'), [Input('my-dropdown', 'name')])
def update_graph(selected_dropdown_value):
    start = datetime.datetime.now() - datetime.timedelta(days=25)
    end = datetime.datetime.now()

    serial = 6951419298100303058
    df_middal = db.query_df(serial=serial, time__gte=start, time__lte=end, limit=10000)
    df = df_middal.loc[~np.isnan(df_middal.ctd_depth)]
    df = df.reset_index()
    return {
        'data': [{
            'x': df.time,
            'y': df.ctd_depth/10, 'name': 'depth'},
            {'x': df.time,
             'y': df.ctd_temp, 'name':'temp'}]#,
        #'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
    }


#app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server()