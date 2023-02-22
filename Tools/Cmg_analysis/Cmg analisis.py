# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 17:27:26 2022

@author: ignac
"""

#%%%
"""
Chargin libraries
"""
import pandas as pd
import numpy as np
import math as mt
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import glob 
#import skill_metrics as skm
import seaborn as sns
from datetime import timedelta
# from sklearn.metrics import mean_squared_error
# import pvlib as pvl
# from datetime import timedelta
# from scipy import stats

#%%%
# from sklearn.metrics import mean_absolute_error
"""
Set path where the files are contained
"""
#C:\Users\ignac\OneDrive - Universidad Católica de Chile\PUC\Tesis PHD\Costos marginales\Barra Crucero\
    #/home/srspoke/CMg_Chile/
#%%%%

general_path =  input("Insert the general directory of the files : ")
path_output = r'/home/srspoke/CMg_Chile/'
tsv_list_files = glob.glob(os.path.join(general_path, "*.xlsx"))
tsv_list = [f"file {i}" for i in range(len(tsv_list_files))]

#%%%

"""
Read the data
"""
Cmg_dataframe_collection = {}
counter = 0
for file in tsv_list:
    Cmg_dataframe_collection[file] = pd.read_excel(tsv_list_files[counter])
    counter += 1

def Cmg_to_mo(path_in, path_out):
    """
    path_in: enter the path where pre-processed tmys are stored
    path_out: enter the path where post-processed tmys must be saved
    
    """
    
    cols=[1] # ghi, dni, dhi, dry, dew, p, wspd, wdir, albedo,
    file = pd.read_excel(path_in, usecols=cols, header=None,skiprows=[0,2])
    file[2] = np.arange(0,31534200,3600)
    cols_2 = [2,1] #time, ghi, dni, dhi, dry, dew, rhum, p, wspd, wdir, albedo, jday
    file = file.reindex(columns=cols_2)
    file.columns = range(file.shape[1])
    lines= list()
    for row in file.itertuples(index=False):
        try:
            lines.append("%.0f, %s\n" % (row[0], row[1]))
            previousRow = row
        except ValueError:
            pass
    
    name = os.path.splitext(os.path.split(path_in)[1])[0]
    extension='.motab'
    saving_path= path_out     
    filOut = open(saving_path+name+extension, 'w')
    filOut.write("#1\n")
    filOut.write("double prices(%s,2)\n"% len(lines))
    filOut.write("#TABLELABELS,time,price\n")
    filOut.write("#TABLEUNITS,s,USD\n")
    filOut.writelines(lines)
    filOut.close()



# for file in tsv_list:
#     Cmg_dataframe_collection[file]['hora'] = Cmg_dataframe_collection[file]['item'].dt.strftime('%H').astype("float")
#     Cmg_dataframe_collection[file]['dia'] = Cmg_dataframe_collection[file]['item'].dt.strftime('%j').astype("float")
#     Cmg_dataframe_collection[file]['mes'] = Cmg_dataframe_collection[file]['item'].dt.strftime('%m').astype("float")
#     Cmg_dataframe_collection[file]['año'] = Cmg_dataframe_collection[file]['item'].dt.strftime('%Y').astype("float")
#     counter += 1

# Headers = list(Cmg_dataframe_collection[tsv_list[0]].columns.values)

# #%%%


# start='2017-01-01 00:00'
# end='2021-12-31 23:00'

# for file in tsv_list:
#     plt.figure(figsize = (20,10), dpi=500)
#     x=np.arange(0,len(Cmg_dataframe_collection[file].loc[(Cmg_dataframe_collection[file]['item']>=start)&(Cmg_dataframe_collection[file]['item']<=end)]['Crucero']),1)           
#     plt.plot(x, Cmg_dataframe_collection[file].loc[(Cmg_dataframe_collection[file]['item']>=start)&(Cmg_dataframe_collection[file]['item']<=end)]['Crucero'])
#     plt.legend("Cmg", loc='upper left', fontsize=12)
#     plt.xlabel('hours', fontsize=18)
#     plt.ylabel('$/MWh', fontsize=18)
#     plt.xticks(fontsize=18)
#     plt.yticks(fontsize=18)
#     plt.show()  
    
# for file in tsv_list:
#     fig, ax = plt.subplots(figsize=(20,10), dpi=500)
#     sns.boxplot(x=Cmg_dataframe_collection[file].loc[(Cmg_dataframe_collection[file]['item']>=start)&(Cmg_dataframe_collection[file]['item']<=end)]['hora'], y=Cmg_dataframe_collection[file].loc[(Cmg_dataframe_collection[file]['item']>=start)&(Cmg_dataframe_collection[file]['item']<=end)]['Crucero'], ax=ax)
#     plt.xlabel('hours', fontsize=18)
#     plt.ylabel('$/MWh', fontsize=18)
#     plt.xticks(fontsize=18)
#     plt.yticks(fontsize=18)
#     plt.show() 


# for file in tsv_list:
#     fig, (axs1, axs2) = plt.subplots(2, 1, constrained_layout=True, figsize = (20,6), dpi= 600)
      
#     #fig.1
#     data_pivot = Cmg_dataframe_collection[file].loc[(Cmg_dataframe_collection[file]['item']>='2017-01-01 01:00')&(Cmg_dataframe_collection[file]['item']<='2017-12-31 23:00')]['Crucero'].values.reshape(24, 365, order="F")
#     axs1 = sns.heatmap(data_pivot, cbar_kws={'label': 'Cmg [$/MWh]'}, vmin=0, vmax=Cmg_dataframe_collection[file].loc[(Cmg_dataframe_collection[file]['item']>='2017-01-01 01:00')&(Cmg_dataframe_collection[file]['item']<='2017-12-31 23:00')]['Crucero'].max(), cmap='jet', linewidths = 0.15, ax=axs1)   
#     axs1.set_xlabel('Dias', fontsize=15)
#     axs1.set_ylabel('horas', fontsize=15)
    
#     #fig.2
#     axs2.hist(Cmg_dataframe_collection[file].loc[(Cmg_dataframe_collection[file]['item']>='2017-01-01 01:00')&(Cmg_dataframe_collection[file]['item']<='2017-12-31 00:00')]['Crucero'].values, alpha=0.6, bins=50)
#     axs2.set_xlabel('Cmg [$/MWh]', fontsize=15)
#     axs2.set_ylabel('frec', fontsize=15)
    
#     #fig.3
#     # twin object for two different y-axis on the sample plot
#     axs3=axs2.twinx()
 
#     count, bins_count = np.histogram(Cmg_dataframe_collection[file].loc[(Cmg_dataframe_collection[file]['item']>='2017-01-01 01:00')&(Cmg_dataframe_collection[file]['item']<='2017-12-31 23:00')]['Crucero'].values, bins=50)
#     pdf = count / sum(count)
#     cdf = np.cumsum(pdf)
#     axs3.plot(bins_count[1:], cdf, label="CDF",  c="green")
#     axs3.set_ylabel('CDF', fontsize=15) 
#     plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
#     #plt.tight_layout(layout='constrained')
#     fig.suptitle(Headers[1], fontsize=20)
#     plt.show()

 
# for file in tsv_list:
#     fig, (axs1, axs2) = plt.subplots(2, 1, constrained_layout=True, figsize = (13,10), dpi= 600)
      
#     #fig.1
#     data_pivot = Cmg_dataframe_collection[file].loc[(Cmg_dataframe_collection[file]['item']>='2017-01-01 01:00')&(Cmg_dataframe_collection[file]['item']<='2021-12-31 19:00')]['Crucero'].values.reshape(24, 1826, order="F")
#     axs1 = sns.heatmap(data_pivot, cbar_kws={'label': 'Cmg [$USD/MWh]'}, vmin=0, vmax=Cmg_dataframe_collection[file].loc[(Cmg_dataframe_collection[file]['item']>='2017-01-01 00:01')&(Cmg_dataframe_collection[file]['item']<='2021-12-31 19:00')]['Crucero'].max(), cmap='jet',  ax=axs1)   
#     axs1.set_xlabel('Dias', fontsize=15)
#     axs1.set_ylabel('horas', fontsize=15)
    
#     #fig.2
#     axs2.hist(Cmg_dataframe_collection[file].loc[(Cmg_dataframe_collection[file]['item']>='2017-01-01 01:00')&(Cmg_dataframe_collection[file]['item']<='2021-12-31 19:00')]['Crucero'].values, alpha=0.6, bins=50)
#     axs2.set_xlabel('Cmg [$USD/MWh]', fontsize=15)
#     axs2.set_ylabel('frec', fontsize=15)
    
#     #fig.3
#     # twin object for two different y-axis on the sample plot
#     axs3=axs2.twinx()
 
#     count, bins_count = np.histogram(Cmg_dataframe_collection[file].loc[(Cmg_dataframe_collection[file]['item']>='2017-01-01 01:00')&(Cmg_dataframe_collection[file]['item']<='2021-12-31 19:00')]['Crucero'].values, bins=50)
#     pdf = count / sum(count)
#     cdf = np.cumsum(pdf)
#     axs3.plot(bins_count[1:], cdf, label="CDF",  c="green")
#     axs3.set_ylabel('CDF', fontsize=15) 
#     plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
#     #plt.tight_layout(layout='constrained')
#     fig.suptitle('Crucero periodo 2017 - 2021', fontsize=20)
#     plt.show()