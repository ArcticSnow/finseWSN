    #!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import wsn_query as wq
import matplotlib.dates as mdates

'''
Set of functions to plot data collected by the Weather Station Network in Finse as saved in the hycamp.org database at UiO.
S. Filhol, December 2017

'''

def print_mote_sensor(data):
    '''
    Function to list the waspmotes contained within a dataset. Print ot console waspmote ID and its corresponding sensors
    :param data: pandas dataframe from query_*() functions. Must have columns 'mote', 'sensors', 'value', 'epoch'

    '''
    motes = np.unique(data.mote).tolist()
    sensors = np.unique(data.sensor)
    print('==========================')
    print('Waspmote available:')
    print(motes)
    print('==========================')
    print('All sensors available:')
    print(sensors)

    for mote in motes:
        s = np.unique(data.sensor[data.mote == mote])
        print('==========================')
        print('Senors available for waspmote ' + str(mote) + ':')
        for sens in s:
            print sens


def plot_sensor(df, sensor='bat', motes=None):
    '''
    Function to plot sensors value from wasmpotes
    :param df: pandas dataframe from query_*() functions. Must have columns 'mote', 'sensors', 'value', 'epoch'
    :param sensor: Sensor name to be plotted
    :param motes: Motes ID for which to plot values
    '''
    print('-----')
    print('List of sensor available:')
    print(np.unique(df.sensor))
    print('-----')
    gr = df.groupby(by='sensor')
    sens_df = gr.get_group(sensor)
    if motes is None:
        motes = np.unique(sens_df.mote).tolist()

    # add line to convert epoch to datetime
    plt.figure()
    for m in motes:
        plt.plot(sens_df.timestamp[sens_df.mote == m], sens_df.value[sens_df.mote==m], label=('Mote: ' + str(m)))

    plt.ylabel(sensor)
    plt.xlabel('Time')
    plt.legend()


def plot_mote(df, mote=None, sensors=None):
    '''
    Function to plot data from one particular waspmote. It is possible to plot ony for selected sensors
    :param df: pandas dataframe from query_*() functions. Must have columns 'mote', 'sensors', 'value', 'epoch'
    :param sensor: Sensor name to be plotted. A list can be given
    :param motes: Motes ID for which to plot values. a list can be given
json_normalize(resp['results'])
    TODO:   - convert epoch timestamp to human time
    '''

    motes = np.unique(df.mote)
    if mote is None:
        mote = motes[0]

        print('-----')
        print('List of waspmote available:')
        print(np.unique(df.mote))
        print('-----')
    if sensors is None:
        sensors = np.unique(df.sensor[df.mote==mote])

    print('-----')
    print('Sensor to plot for ' + str(mote) + ' mote: ' + str(sensors))
    print('-----')

    gr = df.groupby(by='mote')
    mote_df = gr.get_group(mote)
    mote_df.timestamp = pd.to_datetime(mote_df.timestamp)
    mote_df = mote_df.set_index(mote_df.timestamp)
    print(mote_df.head())


    myFmt = mdates.DateFormatter('%m-%d')

    fig, axes = plt.subplots(sensors.__len__(), 1, sharex=True)
    #fig.autofmt_xdate()
    for i, ax in enumerate(axes):
        ax.plot(mote_df.timestamp[mote_df.sensor == sensors[i]], mote_df.value[mote_df.sensor==sensors[i]])
        ax.set_ylabel(sensors[i])
        #ax.xaxis.set_major_formatter(myFmt)


if __name__ == '__main__':

    # query the hycamp.org database
    data = wq.query_df(limit=5000)

    # print to console all waspmote IDs and
    print_mote_sensor(data)

    # plot data
    plot_mote(data)
    plt.show()
    # plot_mote(data, sensors=['ds2_speed', 'ds2_dir'])

    # # plot data for one particualr sensor
    # plot_sensor(data)
    # plot_sensor(data, sensor='bat')
    #
    # # example from csv file:
    # try:
    #     df = pd.read_csv('waspmote/waspmote_test.csv')
    #     plot_sensor(df)

