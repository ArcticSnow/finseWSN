from __future__ import division
import os, sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Include class and function here

def CR6_load(filelist, mypath=None):

    # leser campbell data-filer og returnerer DataFrame
    def read_campbell(fil, path=None):
        dat = pd.read_csv(path+fil, sep=',', header=None, skiprows=4)
        columns = pd.read_csv(path+fil, sep=',', header=None, skiprows=1, nrows=1, na_values=np.nan)
        dat.columns = columns.iloc[0].tolist()
        units = pd.read_csv(path+fil, sep=',', header=None, skiprows=2, nrows=1)
        return dat, units

    all_data = pd.DataFrame()

    if mypath == None:
        mypath = ''
    for i, file in enumerate(filelist):
        print('Reading file: ' + str(file))

        if os.path.isfile(mypath+str(file)):
            data, units = read_campbell(file, mypath)
            all_data = all_data.append(data)
        else:
            print(str(file) + ' does not exist.')

    return all_data, units


# Include script in this if statement
if __name__ == '__main__':

    # Example on how to use the function here above:
    fname = ['/flux_station/data_example/CR6 Finse_Data.dat']
    weather = CR6_load(fname)[0]