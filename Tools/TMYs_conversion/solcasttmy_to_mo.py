#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 00:19:59 2022

@author: srspoke
"""
import pandas as pd
import numpy as np
import datetime as dt
import csv
import glob
import os

general_path = r'/home/srspoke/Scripts_PHD/TMYs_postproc/TMYs_input/solcast/'
tmy_list_files = glob.glob(os.path.join(general_path, "*.csv"))
path_output = r'/home/srspoke/Scripts_PHD/TMYs_postproc/TMYs_motab/solcast/'

def solcast_to_mo(path_in, path_out):
    """
    path_in: enter the path where pre-processed tmys are stored
    path_out: enter the path where post-processed tmys must be saved
    
    """
    
    cols=[10,8,7,3,6,12,14,16,15,18] # ghi,dni,dhi,dry,dew,rhum,p,wspd,wdir,albedo
    file = pd.read_csv(path_in, delimiter=",", usecols=cols, header=None,skiprows=[0])
    file[19] = np.arange(0,31534200,3600)
    Startdate='2005-01-01 00:00'
    Enddate='2005-12-31 23:00'
    l = pd.DataFrame(pd.date_range(start=Startdate, 
                          end=Enddate, 
                          #tz=Timezone, 
                          freq="1h" ))
    l['jday'] = l[0].dt.strftime('%j').astype('float')
    # l['month'] = l[0].dt.strftime('%m').astype('float')
    # l['day'] = l[0].dt.strftime('%d').astype('float')
    file[20] = l['jday']
    cols_2 = [19,10,8,7,3,6,12,14,16,15,18,20]
    file = file.reindex(columns=cols_2)
    file.columns = range(file.shape[1])
    lines= list()
    for row in file.itertuples(index=False):
        try:
            lines.append("%.0f, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s\n" % (row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]))
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
    filOut.write("#METADATA,Crucero-Chile,-26.96,-69.85,1915,-4.0,0.0\n")
    filOut.writelines(lines)
    filOut.close()
    
    
for path in tmy_list_files:
    solcast_to_mo(path, path_output)
    
#%%%

"""
Weather .motab file format to solstice function

"""

general_path = r'/home/srspoke/Scripts_PHD/TMYs_postproc/TMYs_input/solcast/'
tmy_list_files = glob.glob(os.path.join(general_path, "*.csv"))
path_output = r'/home/srspoke/Scripts_PHD/TMYs_postproc/TMYs_motab/solcast/solstice_files/'

def solcast_to_mo(path_in, path_out):
    """
    path_in: enter the path where pre-processed tmys are stored
    path_out: enter the path where post-processed tmys must be saved
    
    """
    
    cols=[10,8,7,3,6,12,14,16,15,18] # ghi,dni,dhi,dry,dew,rhum,p,wspd,wdir,albedo
    file = pd.read_csv(path_in, delimiter=",", usecols=cols, header=None,skiprows=[0])
    file[19] = np.arange(0,31534200,3600)
    cols_2 = [19,10,8,7,3,6,12,14,16,15,18]
    file = file.reindex(columns=cols_2)
    file.columns = range(file.shape[1])
    lines= list()
    for row in file.itertuples(index=False):
        try:
            lines.append("%.0f, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10]))
            previousRow = row
        except ValueError:
            pass
    
    name= os.path.splitext(os.path.split(path)[1])[0]
    extension='.motab'
    saving_path= path_out     
    filOut = open(saving_path+name+extension, 'w')
    filOut.write("#1\n")
    filOut.write("double data(%s,11)\n"% len(lines))
    filOut.write("#METALABELS,name,lat,lon,elev,tzone,tstart\n")
    filOut.write("#METAUNITS,str,deg,deg,m,h,s\n")
    filOut.write("#TABLELABELS,time, ghi, dni, dhi, dry, dew, rhum, p, wspd, wdir, albedo\n")
    filOut.write("#TABLEUNITS,s,W/m2,W/m2,W/m2,degC,degC,%,mbar, m/s, deg, N/A\n")
    filOut.write("#METADATA,Crucero-Chile,-26.96,-69.85,1915,-4.0,0.0\n")
    filOut.writelines(lines)
    filOut.close()

for path in tmy_list_files:
    solcast_to_mo(path, path_output)
