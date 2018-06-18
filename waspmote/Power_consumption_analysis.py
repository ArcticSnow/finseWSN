import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
import datetime

import plotly.offline as py
import plotly.graph_objs as go

'''
1. Check when which waspmote has data since September 2017, how many source_addr
2. what type of data


Check 

'''

# ================================================================
# Script to Analyze waspmote power consumption


from latice_db import db_query as db
import pandas as pd
import matplotlib.pyplot as plt

serials = [8596359061997376531, 7873531321804412124,
           7383483387351159950, 6951419298100303058,
           6153719214102303789, 4634607560887915575,
           4574644594755523609, 3390197892757083161,
           2258114332519847047, 1833078321593734303,
           1391162608158004432, 161398434909148276]

get = False
if get:
    start = datetime.datetime.now() - datetime.timedelta(days=200)
    end = datetime.datetime.now()

    df = db.query_df(fields=['bat', 'rssi'], time__gte=start, time__lte=end, limit=10000000000,
                     tags=['serial', 'source_addr_long'])

    df.set_index(pd.to_datetime(df.time), inplace=True)

    save = False
    if save:
        df.to_pickle('power_wasp.pkl')
else:
    df = pd.read_pickle('power_wasp.pkl')


df_bat = df.dropna(subset=['bat'])
df_rssi = df.dropna(subset=['rssi'])


traces = list()
for ser in df.serial.unique():
    trace = go.Scatter(
        x=df_bat.time.loc[df_bat.serial == ser],
        y=df_bat.bat.loc[df_bat.serial == ser],
        name=ser,
        mode='lines'
    )
    traces.append(trace)
py.plot(traces, filename='scatter-mode')

traces = list()
for ser in df.serial.unique():
    trace = go.Scatter(
        x=df_rssi.time.loc[df_rssi.serial == ser],
        y=df_rssi.rssi.loc[df_rssi.serial == ser],
        name=ser,
        mode='markers'
    )
    traces.append(trace)
py.plot(traces, filename='scatter-mode')


def lithium_bat_level_to_voltage(level):
    return (level+442)/(90/108)*2/1023*3.3



df_bat['volt'] = lithium_bat_level_to_voltage(df_bat.bat)
df_bat['volt_6H'] = df_bat.volt.resample('6H').mean()
df_bat['volt_12H'] = df_bat.volt.resample('12H').mean()

traces = list()
for ser in df.serial.unique():
    trace = go.Scatter(
        x=df_bat.time.loc[df_bat.serial == ser],
        y=df_bat.volt.loc[df_bat.serial == ser],
        name=ser,
        mode='lines'
    )
    traces.append(trace)
py.plot(traces, filename='scatter-mode')









plt.subplot(211)
df.bat.plot()
plt.ylabel('lithium Battery level [%]')
plt.grid()
df['bat_1H'] = df.bat.resample('1H').mean()
df['bat_6H'] = df.bat.resample('6H').mean()
df['bat_12H'] = df.bat.resample('12H').mean()
df.bat_1H.dropna().plot()
df.bat_6H.dropna().plot()
df.bat_12H.dropna().plot()

plt.subplot(212)
df.bat_12H.dropna().diff().divide(12).plot()

# calculate rate of charge/discharge


plt.figure()
plt.scatter(df.time.loc[~np.isnan(df.rssi)], df.rssi.loc[~np.isnan(df.rssi)])
plt.show()




#========






