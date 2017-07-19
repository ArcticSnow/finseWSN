from __future__ import division
import os, sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Include class and function here

class frameObj(object):
    def __init__(self):
        self.waspID = np.nan
        self.frameID = np.nan
        self.epoch = np.nan
        self.bat = np.nan
        self.tcb = np.nan
        self.in_temp = np.nan
        self.humb = np.nan

def read_wasp_data(file):
    '''
    function to parse frames saved in a text file
    S. Filhol

    :param file: file path to read
    :return: a dataframe containing all parsed frames

    '''
    f = open(file)
    data = pd.DataFrame()
    for line in f:
        if line[:3] == '<=>':
            #print line
            frame = frameObj()
            spline = line.split('#')
            # for sp in spline:
            #     print sp
            frame.waspID = int(spline[1])
            frame.frameID = int(spline[3])

            for sp in spline:
                s = sp.split(':')
                #print s
                if s.__len__()>1:
                    if s[0] == 'BAT':
                        frame.bat = s[1]
                    if s[0] == 'IN_TEMP':
                        frame.in_temp = s[1]
                    if s[0] == 'TCB':
                        frame.tcb = s[1]
                    if s[0] == 'HUMB':
                        frame.humb = s[1]
                    if s[0] == 'TST':
                        frame.epoch = s[1]

            data = data.append(frame.__dict__, ignore_index=True)

    return data

# Include script in this if statement
if __name__ == '__main__':
    print 'nothing there'