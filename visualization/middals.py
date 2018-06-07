import dash
import dash_core_components as dcc
import dash_html_components as html


import numpy as np
import db_query as db

import datetime

start = datetime.datetime.now() - datetime.timedelta(days=25)
end = datetime.datetime.now()

serial = 6951419298100303058
df_middal = db.query_df(serial=serial, time__gte=start, time__lte=end, limit=10000)
df = df_middal.loc[~np.isnan(df_middal.ctd_depth)]
df = df.reset_index()
df.ctd_cond.loc[df.ctd_cond<0.01] = np.nan

app = dash.Dash()
app.layout = html.Div(children=[html.Div([
    html.Link(href='static/whitey.css', rel='stylesheet')]),
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

'''

    ),
    html.H2(children='Water Discharge'),
    dcc.Graph(
        id='gr1',
        figure={
            'data': [{
            'x': df.time,
            'y': df.ctd_depth/10, 'name': 'depth'}],
            'layout':{'yaxis':{'title':'Water Depth [cm]'}}
        }),
    html.H2(children='Water Temperature'),
    dcc.Graph(
        id='gr2',
        figure={
            'data': [{
            'x': df.time,
            'y': df.ctd_temp, 'name': 'temp'}],
            'layout':{'yaxis':{'title':'Temperature [degC]'}}
        }),
    html.H2(children='Water Electrical Conductivity'),
    dcc.Graph(
        id='gr3',
        figure={
            'data': [{
            'x': df.time,
            'y': df.ctd_cond, 'name': 'cond'}],
            'layout':{'yaxis':{'title':'Electrical conductivity [dS/m]'}}
        }),
    dcc.Markdown('''
## Page future development:
- Add running average for conductivity and depth
- get shared x-axis for the three plots
- have an input box setting the start and final date to display, default being 15 days until now
''')
])

#app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
#app.css.append_css({'external_url':'https://raw.githubusercontent.com/oxalorg/sakura/master/css/sakura.css'})
app.scripts.config.serve_locally=True
app.css.config.serve_locally=True


if __name__ == '__main__':
    app.run_server()