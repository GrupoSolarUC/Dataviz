#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 10:40:18 2022

@author: srspoke
"""

import pandas as pd
import numpy as np
import datetime as dt
import csv
import glob
import os

general_path = r'/home/srspoke/TMYs_postproc/TMYs_input/nrel/'
tmy_list_files = glob.glob(os.path.join(general_path, "*.csv"))
path_output = r'/home/srspoke/TMYs_postproc/TMYs_motab/nrel/'

def nrel_to_mo(path_in, path_out):
    """
    path_in: enter the path where pre-processed tmys are stored
    path_out: enter the path where post-processed tmys must be saved
    
    """
    
    cols=[7,5,6,9,8,10,12,11,13] # ghi, dni, dhi, dry, dew, p, wspd, wdir, albedo,
    file = pd.read_csv(path_in, delimiter=",", usecols=cols, header=None,skiprows=[0,1,2])
    file[14] = np.arange(0,31534200,3600)
    Startdate='2005-01-01 00:00'
    Enddate='2005-12-31 23:00'
    l = pd.DataFrame(pd.date_range(start=Startdate, 
                          end=Enddate, 
                          #tz=Timezone, 
                          freq="1h" ))
    l['jday'] = l[0].dt.strftime('%j').astype('float')
    # l['month'] = l[0].dt.strftime('%m').astype('float')
    # l['day'] = l[0].dt.strftime('%d').astype('float')
    file[15] = l['jday']
    file[16] = 0
    cols_2 = [14,7,5,6,9,8,16,10,12,11,13,15] #time, ghi, dni, dhi, dry, dew, rhum, p, wspd, wdir, albedo, jday
    file = file.reindex(columns=cols_2)
    file.columns = range(file.shape[1])
    lines= list()
    for row in file.itertuples(index=False):
        try:
            lines.append("%.0f, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]))
            previousRow = row
        except ValueError:
            pass
    
    name= os.path.splitext(os.path.split(path)[1])[0]
    extension='.motab'
    saving_path= path_out     
    filOut = open(saving_path+name+extension, 'w')
    filOut.write("#1\n")
    filOut.write("double data(%s,12)\n"% len(lines))
    filOut.write("#METALABELS,name,lat,lon,elev,tzone,tstart\n")
    filOut.write("#METAUNITS,str,deg,deg,m,h,s\n")
    filOut.write("#TABLELABELS,time, ghi, dni, dhi, dry, dew, rhum, p, wspd, wdir, albedo, jday\n")
    filOut.write("#TABLEUNITS,s,W/m2,W/m2,W/m2,degC,degC,%,mbar, m/s, deg, N/A, day\n")
    filOut.write("#METADATA,Dagget-California,34.865371,-116.783023,586,-8.0,0\n")
    filOut.writelines(lines)
    filOut.close()
    
for path in tmy_list_files:
    nrel_to_mo(path, path_output)