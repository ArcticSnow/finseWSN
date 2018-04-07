
'''
Write script to plot latest week of data for the waspmote data.
Simon Filhol, April 2018
'''

import matplotlib.pyplot as plt
from latice_db import db_query as db
import datetime, os
import numpy as np



#=============================================
#   1. import latest 3 days of data into datarame format

TOKEN = os.getenv('WSN_TOKEN')
plot_path = ''

start = datetime.datetime.now() - datetime.timedelta(days=3)
end = datetime.datetime.now()
serial = 3390197892757083161


df_therm = db.query_df(serial=serial, time__gte=start, time__lte=end, limit=10000)
df_therm_string = df_therm.loc[np.isnan(df_therm.rssi)]
df_therm_string['tempString'] = df_therm_string.ds1820.apply(np.array)
df_therm_string = df_therm_string.reset_index()

df_therm_rssi = df_therm.loc[~np.isnan(df_therm.rssi)]
df_therm_rssi = df_therm_rssi.reset_index()
depth = np.array([21.5, 31.5, 41.5, 52, 62, 72, 82, 92, 102.5, 112.5, 122.5, 133, 143, 153, 163.5, 173.5, 183.5, 193.5, 203.5, 213.5])



serial = 8596359061997376531
df_thomas = db.query_df(serial=serial, time__gte=start, time__lte=end, limit=10000)
df_thomas_ws = df_thomas.loc[~np.isnan(df_thomas.ds2_speed)]
df_thomas_ws = df_thomas_ws.reset_index()

df_thomas_mb = df_thomas.loc[~np.isnan(df_thomas.mb_median)]
df_thomas_mb = df_thomas_mb.reset_index()

df_thomas_rssi = df_thomas.loc[~np.isnan(df_thomas.rssi)]
df_thomas_rssi = df_thomas_rssi.reset_index()




#=============================================
#   2. plot data
#=============================================


#==================================================
# plot temperature profile and temperautre gradient
fig = plt.figure(figsize=(14, 12))
ax = fig.add_subplot(121)
line1, = ax.plot(df_therm_string.tempString.loc[1], depth, linewidth=4, c='k')
ax.set_xlim([-35,5])
ax.set_ylabel('Depth [cm]')
ax.set_xlabel('Temperature [degC]')
plt.grid()

for i, tempProfile in enumerate(df_therm_string.tempString):
    if i.__mod__(10)==0:
        plt.plot(tempProfile, depth, 'g', alpha=0.05)
        line1.set_xdata(tempProfile)

def gradient(t):
    depth = np.array(
        [21.5, 31.5, 41.5, 52, 62, 72, 82, 92, 102.5, 112.5, 122.5, 133, 143, 153, 163.5, 173.5, 183.5, 193.5, 203.5,
         213.5])
    return np.diff(t)/np.diff(depth)

# plot Temperature gradient
df_therm_string['temp_grad'] = df_therm_string.tempString.apply(gradient)

ax = fig.add_subplot(122)
line1, = ax.plot(df_therm_string.temp_grad.loc[1], depth[:-1], linewidth=4, c='k')
ax.set_ylabel('Depth [cm]')
ax.set_xlabel('Temperature gradient [degC/cm]')
plt.grid()

for i, tempProfile in enumerate(df_therm_string.temp_grad):
    if i.__mod__(10)==0:
        plt.plot(tempProfile, depth[:-1], 'g', alpha=0.05)
        line1.set_xdata(tempProfile)
plt.savefig(plot_path + 'SnowTempProfile.png')

#========================================
# Plot RSSI
plt.figure()
plt.plot(df_therm_rssi.time, df_therm_rssi.rssi, label='Orjan\'s station')
plt.plot(df_thomas_rssi.time, df_thomas_rssi.rssi, label='Thomas\'s station')
plt.legend()
plt.grid()
plt.savefig(plot_path + 'RSSI.png')


#=======================================
# Temperature, WS, WD
fig, ax = plt.subplots(4,1, sharex=True, figsize=(20,12))

ax[0].plot(df_thomas_ws.time, df_thomas_ws.ds2_temp)
ax[0].set_ylabel('Air temp [degC]')
ax[0].grid(linestyle=':')

ax[1].plot(df_thomas_ws.time, df_thomas_ws.ds2_speed, label='ws')
ax[1].set_ylabel('Wind speed [m/s]')
ax[1].grid(linestyle=':')

ax[2].plot(df_thomas_ws.time, df_thomas_ws.ds2_dir)
ax[2].set_ylabel('wind dir [deg]')
ax[2].grid(linestyle=':')

ax[3].plot(df_thomas_mb.time, df_thomas_mb.mb_median/10)
ax[3].set_ylabel('mb_dist [cm]')
ax[3].grid(linestyle=':')

plt.tight_layout()
plt.savefig('weather_thomas.png')

#===================================
# battery level
plt.figure()
plt.plot(df_therm.time.loc[~np.isnan(df_therm.bat)], df_therm.bat.loc[~np.isnan(df_therm.bat)], label='Orjan\'s station')
plt.plot(df_thomas.time.loc[~np.isnan(df_thomas.bat)], df_thomas.bat.loc[~np.isnan(df_thomas.bat)], label='Thomas\'s station')
plt.legend()
plt.savefig('battery_level.png')


