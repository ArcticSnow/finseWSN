# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 18:17:11 2017

@author: astridva

"""
import pandas as pd
import os.path
import glob


def load_metdata(mypath,filename_pattern='Data_',biomet=False,sub_dir=True):
    """Returns pandas dataframe with met data from files with certain filename
    pattern. Searches for subfolders in path and for file with certain 
    pattern in each subfolder. For each folder, function samla() is called 
    which concatenates data from  files in  folder. File formats is TOA5 or 
    licor's biomet.data. 
    
    Parameters
    ----------
    mypath: str
    path of folder with subfolders containing data files 
    (e.g project/data/CR6) 
    
    filename_pattern: str
    pattern of filename to be recognized in folder (e.g. 'Data_' or 
    'biomet.data')
    
    biomet: boolean
    True if data is in licor's biomet.data file format. Default is False.
    
    sub_dir: boolean
    True if path is for folder containing subfolders with data. Default is True.
    
    Returns
    -------
    data: pandas.DataFrame
    dataframe or concatenated data with datetime index
    
    unitlist: list
    list of pandas.DataFrames. One df for each folder. In df's one row for each
    time units changes. Lot of potential for improvement here.
    """
    
    
    if sub_dir:
        undermapper=os.listdir(mypath)
        frames=[]
        unitlist=[]
        
        for mappe in undermapper:
            if os.path.isdir(os.path.join(mypath,mappe)):
                print("Reading data from folder: "+mappe)
                filer=glob.glob(os.path.join(mypath,mappe,'*'+filename_pattern+'*'))
                if filer:
                    data,units=samla(filer,biomet)
                    frames.append(data)
                    unitlist.append(units)      
        data=pd.concat(frames)
        data.sort_index(inplace=True)
    elif os.path.isdir(mypath):
        print("Reading data from folder: "+mypath)
        filer=glob.glob(os.path.join(mypath,'*'+filename_pattern+'*'))
        if filer:
            data,units=samla(filer,biomet)
        else:
            data=[]
        unitlist=[]
        print('No files in '+mypath+' matched given filename_pattern')
            
    return data,unitlist
    
def samla(filer,biomet=False):
    """Returns dataframe from a list of paths of data files. File format is 
    TOA5 (default) or licor's biomet.data.
    
    Parameters
    ----------
    filer: list
    list of paths of files with data
    
    biomet: boolean
    True if data is in file format biomet.data. Default False.
 
    Returns
    -------
    data: pandas.DataFrame
    df of data with datetime index.
    
    units: pandas.DataFrame
    df of unitlist 
    """
    frames=[]
    unitlist=[]
    
    if not biomet:
        for fil in filer:
            if os.path.isfile(fil) and os.path.getsize(fil)>100:
                #print('Reading file: '+fil)
                data,units=les_TOA5(fil)
                frames.append(data)
                if not unitlist:
                    unitlist.append(units)
                elif not units.equals(unitlist[-1]):
                    units['unit_change']=data.index[0].strftime('%Y-%m-%d')
                    unitlist.append(units)
            elif os.path.getsize(fil)<100:
                print('OBS: '+fil+' does not contain any data.')
                       
    elif biomet:
        for fil in filer:
            if os.path.isfile(fil) and os.path.getsize(fil)>360:
                #print('Reading file: '+fil)
                data,units=les_biomet(fil)
                frames.append(data)
                if not unitlist:
                    unitlist.append(units)
                elif not units.equals(unitlist[-1]):
                    units['unit_change']=data.index[0].strftime('%Y-%m-%d')
                    unitlist.append(units)
            elif os.path.getsize(fil)<360:
                print('OBS: '+fil+' does not contain any data.')    
    unitlist=pd.concat(unitlist)            
    samla_data=pd.concat(frames) 
    samla_data.sort_index(inplace=True)  
    return samla_data,unitlist 

def les_TOA5(fil):
    
    """
    Reads one TOA5 file
    
    Parameters
    ----------
    fil: str
    path of file with data
 
    Returns
    -------
    data: pandas.DataFrame
    df of data with datetime index.
    
    units: pandas.DataFrame
    df of units 
    """
    #print('Reading file: '+fil)
    columns=pd.read_csv(fil, sep=',',header=None,skiprows=1,nrows=1)
    data=pd.read_table(fil,sep=',',index_col=0,parse_dates=True,header=None,
                      dtype='a',skiprows=4, names=columns.iloc[0],
                      na_values=[-99999,-99.9,'NAN','-INF','INF'],engine='c')   
    units=pd.read_csv(fil,sep=',',header=None,skiprows=2,nrows=1)
    units.columns=columns.iloc[0].tolist()
    return data,units

def les_biomet(fil):
    """Reads one biomet file
    
    Parameters
    ----------
    fil: str
    path of file with data
 
    Returns
    -------
    data: pandas.DataFrame
    df of data with datetime index.
    
    units: pandas.DataFrame
    df of units 
    """
    kols=['DATE','TIME','LWIN_1_1_1(W/m^2)', 'LWOUT_1_1_1(W/m^2)','PA_1_1_1(kPa)', 'RH_1_1_1(%)',
          'RN_1_1_1(W/m^2)', 'SHF_1_1_1(W/m^2)','SHF_2_1_1(W/m^2)',
          'SWIN_1_1_1(W/m^2)', 'SWOUT_1_1_1(W/m^2)','TA_1_1_0(C)', 'TA_1_2_1(C)',
          'TSS_1_1_1(C)', 'TS_1_1_1(C)', 'TS_2_1_1(C)', 'TS_3_1_1(C)',
          'WD_1_1_1(degrees)', 'WS_1_1_1(m/s)']  
    data = pd.read_table(fil, sep='\t', header=3, skiprows=2,usecols=kols,
                         na_values=[-9999],dtype='str')
    data['TIMESTAMP']=pd.to_datetime(data['DATE'] + ' ' + data['TIME'].str[:8],
        format='%Y-%m-%d %H:%M:%S')    
    data.set_index('TIMESTAMP',inplace=True)
    data.drop(['DATE','TIME'],axis=1,inplace=True)  
    data=data.apply(pd.to_numeric)
    units=[]
    for name in data.columns:
        u=(name[name.find("(")+1:name.find(")")])
        units.append(u)
    units=pd.DataFrame([units],columns=data.columns)
    new_cols={'LWIN_1_1_1(W/m^2)': 'Rl_downwell', 'LWOUT_1_1_1(W/m^2)': 'Rl_upwell',
                    'SWIN_1_1_1(W/m^2)': 'Rs_downwell', 'SWOUT_1_1_1(W/m^2)': 'Rs_upwell',
                    'RN_1_1_1(W/m^2)': 'Rn', 'TSS_1_1_1(C)': 'TSS_1477', 'SHF_1_1_1(W/m^2)': 'Heatflux_1',
                    'SHF_2_1_1(W/m^2)': 'Heatflux_2', 'TA_1_1_0(C)': 'T_a_1477', 'TA_1_2_1(C)': 'T_b_1477',
                    'TS_3_1_1(C)': 'CS650_Temp', 'TS_2_1_1(C)': 'Tsoil', 'TS_1_1_1(C)': 'T_TJ_1477',
                    'WD_1_1_1(degrees)': 'D_g_1477', 'WS_1_1_1(m/s)': 'F_1_s_g_1477', 'RH_1_1_1(%)': 'U_1477',
                    'PA_1_1_1(kPa)': 'AT_mbar'
                    }
    data.rename(columns=new_cols, inplace=True)
    units.rename(columns=new_cols, inplace=True)
    return data,units

