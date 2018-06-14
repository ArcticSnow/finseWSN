import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
import datetime


'''
1. Check when which waspmote has data since September 2017, how many source_addr
2. what type of data


Check 

'''

#================================================================
# Script to Analyze waspmote power consumption



from latice_db import db_query as db

serials = [8596359061997376531, 7873531321804412124,
           7383483387351159950, 6951419298100303058,
           6153719214102303789, 4634607560887915575,
           4574644594755523609, 3390197892757083161,
           2258114332519847047, 1833078321593734303,
           1391162608158004432, 161398434909148276]

start = datetime.datetime.now() - datetime.timedelta(days=200)
end = datetime.datetime.now() - datetime.timedelta(days=0)


df = db.query_df(serial=serials[1], time__gte=start, time__lte=end, limit=10000000000, tags=['serial', 'source_addr_long'])



df.set_index(pd.to_datetime(df.time), inplace=True)

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