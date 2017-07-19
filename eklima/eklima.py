from __future__ import division
import os, sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st

# Include class and function here

eklima_terminology = {'St.no':'statoinID','Year':'year','Mnth':'month','Date':'date','Time(UTC)':'hour','PO':'air_pressure',
                      'NN':'cloud_cover','UU':'rel_humidity','RR_1':'precip_1','RR_12':'precip_12','RR_24':'precip_24',
                      'SA':'snow_depth','SD':'snow_cover','TA':'air_temp','WW':'weather','DD':'wind_dir','FF':'wind_speed'}

def import_eklima(myfile):
    '''
    Function to import data from an Eklima text file into a dataframe format.
    S. Filhol, July 2017

    :param myfile: path to an Eklima csv file with tab delimiter
    :return: a dataframe
    '''
    data = pd.read_csv(myfile, skiprows=33, sep="\t", skipfooter=25, engine='python')
    colname = []
    for col in data.columns:
        colname.append(eklima_terminology.get(col))
    data.columns = colname

    data['time'] = data['year'].astype(str) + '/' + data['month'].astype(str) + '/' + data['date'].astype(str) + ' ' + data['hour'].astype(str) + ':' + np.zeros(data['hour'].shape).astype(str)
    data.time = pd.to_datetime(data.time)

    data = data.set_index('time')
    data['julian_day'] = data.index.dayofyear
    data = data.replace('-9999', np.nan)
    data = data.replace('x', np.nan)
    #data.wind_speed = data.wind_speed.replace('x',np.nan).astype(float)
    data.precip_1 = data.precip_1.replace(np.nan, 0)
    data.precip_1 = data.precip_1.replace('.', 0)
    data.precip_24 = data.precip_24.replace(np.nan, 0)
    data.precip_12 = data.precip_12.replace(np.nan, 0)
    data.precip_24 = data.precip_24.replace('.', 0)
    data.precip_12 = data.precip_12.replace('.', 0)
    data.snow_depth = data.snow_depth.replace('.', 0)
    data.snow_cover = data.snow_cover.replace('.', 0)
    data.air_temp = data.air_temp.astype(float)
    data.precip_24 = data.precip_24.astype(float)
    data.precip_12 = data.precip_12.astype(float)
    data.air_pressure = data.air_pressure.astype(float)
    data.snow_depth = data.snow_depth.astype(float)
    data.snow_cover = data.snow_cover.astype(float)
    data.wind_dir = data.wind_dir.astype(float)
    data.wind_speed = data.wind_speed.astype(float)
    data.rel_humidity.astype(float)

    #data['winter'] = np.repeat
    print 'Done'
    return data

def wind_hist2D(u=None, v=None, Ws=None, Wd=None, plot=False, xmin=-30, xmax=30, ymin=-30, ymax=30, nbins=60):
    '''
    Function to plot wind distribution in 2d as used in this paper:
    http://www.sciencedirect.com/science/article/pii/S0167610514001056

    :param u: East component of wind vector
    :param v: North component of wind vector
    :param Ws: Wind speed [m/s]
    :param Wd: Wind direction [degree]
    :return: 2d array histo
    '''

    range_arr = [[xmin, xmax], [ymin, ymax]]

    if Ws is not None and Wd is not None:
        v = np.cos((Wd) * np.pi/180) * Ws
        u = np.sin((Wd) * np.pi/180) * Ws

    H, xedges, yedges = np.histogram2d(v,u, range=range_arr, bins=nbins)

    if plot:
        '''
        1. find color scale with log scale pattern to allow for seeing all events
        2. add contour rings of absolute wind speed
        '''

        plt.figure()
        plt.imshow(H, cmap=plt.cm.terrain, vmin=0, vmax=100, extent=(xmin, xmax, ymin, ymax), aspect=1, origin='lower')
        plt.colorbar()

    return H, xedges, yedges

def wind_kde2D(u=None, v=None, Ws=None, Wd=None, plot=False, Umin=-30, Umax=30, Vmin=-30, Vmax=30, nbins=60):
    '''
    Function to derive (and optionally plot) a 2D kernel distribution estimation of the wind vector (U, V).
    S. Filhol, july 2017

    :param u: u-component of wind velocity
    :param v: v-component of wind velocity
    :param Ws: wind speed (optional if u and v component are not known)
    :param Wd: wind direction (optional if u and v component are not known)
    :param plot: boolean to plot the estimated probability distribution
    :param Umin:
    :param Umax:
    :param Vmin:
    :param Vmax:
    :param nbins: number of bins
    :return: 2d array of the KDE values
    '''

    if Ws is not None and Wd is not None:
        v = np.cos((Wd) * np.pi/180) * Ws
        u = np.sin((Wd) * np.pi/180) * Ws

    vv, uu = np.meshgrid(np.linspace(Umin, Umax, nbins), np.linspace(Vmin, Vmax, nbins))
    positions = np.vstack([vv.ravel(), uu.ravel()])
    values = np.vstack([v, u])
    values = values.T[~np.isnan(values.T).any(axis=1)]
    kernel = st.gaussian_kde(values.T)
    f = np.reshape(kernel(positions).T, vv.shape)

    if plot:
        fig = plt.figure()
        ax = fig.gca()
        ax.set_xlim(Umin, Umax)
        ax.set_ylim(Vmin, Vmax)
        # Contourf plot
        #cfset = ax.contourf(vv, uu, f, cmap='Blues')
        ## Or kernel density estimate plot instead of the contourf plot
        ax.imshow(np.rot90(f), cmap='terrain', extent=[Umin, Umax, Vmin, Vmax])
        # Contour plot
        cset = ax.contour(uu, vv, f, colors='k')
        # Label plot
        ax.clabel(cset, inline=1, fontsize=10)
        ax.set_xlabel('V')
        ax.set_ylabel('U')

        ## Code to add circles of windspeed
        # x = np.linspace(Umin, Umax, 180)
        # y = np.linspace(Vmin, Vmax, 180)
        # X, Y = np.meshgrid(x, y)
        # S = np.sqrt(X ** 2 + Y ** 2)
        # Cspeed = ax.contour(uu, vv, S, vmin=0, vmax=30, linewidth=0.2, colors='k')
        # ax.clabel(Cspeed, inline=1, fontsize=10, fmt='%d')

        plt.show()

    return f



# Include script in this if statement
if __name__ == '__main__':
    print 'ciao!'