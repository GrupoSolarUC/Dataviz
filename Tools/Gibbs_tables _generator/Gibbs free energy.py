# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 17:58:13 2022

@author: ignac
"""

import pandas as pd
import numpy as np
import math as mt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib as mpl
import CoolProp.CoolProp as CP
import matplotlib.lines as mlines

Dmolar_H2O = CP.PropsSI("Dmolar", "T", 298.15, "P", 101325, "H2O")
Dmolar_H2 = CP.PropsSI("Dmolar", "T", 298.15, "P", 101325, "H2")
Dmolar_O2 = CP.PropsSI("Dmolar", "T", 298.15, "P", 101325, "O2")
CP.set_reference_state('H2O', 298.15, Dmolar_H2O, -285830, 69.91) # fluid, T, D (mol/m^3), h (J/mol), s (J/mol/K)
CP.set_reference_state('H2', 298.15, Dmolar_H2, 0, 130.68)
CP.set_reference_state('O2', 298.15, Dmolar_O2, 0, 205.14)


# CP.PropsSI('Hmolar', 'T', 298.15, 'P', 101325, 'Water')
# CP.PropsSI('Smolar', 'T', 298.15, 'P', 101325, 'Water')
# CP.PropsSI('Gmolar', 'T', 298.15, 'P', 101325, 'Water')
# CP.set_reference_state('H2O','DEF')
# CP.set_reference_state('H2','DEF')
# CP.set_reference_state('O2','DEF')


counter = 0
df_H = pd.DataFrame()
df_S = pd.DataFrame()
df_G = pd.DataFrame()
Delta_H = {}
Delta_S = {}
Delta_G = {}
for n in np.arange(1,101,1):
    Delta_H[f"{n}"] = {}
    Delta_S[f"{n}"] = {}
    Delta_G[f"{n}"] = {}
    for i in np.arange(298.15, 2263.15, 1):
        Delta_H[f"{n}"][counter] = (CP.PropsSI('Hmolar', 'T', i, 'P', 101325*n, 'H2') + 0.5*CP.PropsSI('Hmolar', 'T', i, 'P', 101325*n, 'O2') - CP.PropsSI('Hmolar', 'T', i, 'P', 101325*n, 'H2O')) 
        Delta_S[f"{n}"][counter] = (CP.PropsSI('Smolar', 'T', i, 'P', 101325*n, 'H2') + 0.5*CP.PropsSI('Smolar', 'T', i, 'P', 101325*n, 'O2') - CP.PropsSI('Smolar', 'T', i, 'P', 101325*n, 'H2O'))
        Delta_G[f"{n}"][counter] = Delta_H[f"{n}"][counter] - Delta_S[f"{n}"][counter]*i
        counter +=1
    df_H[f"H{n}"] = Delta_H[f"{n}"].values()
    df_S[f"S{n}"] = Delta_S[f"{n}"].values()
    df_G[f"G{n}"] = Delta_G[f"{n}"].values()


df_H2 = df_H
df_S2 = df_S

df_H2.insert(0, "Temp (K)", np.arange(298.15, 2263.15, 1))
df_S2.insert(0, "Temp (K)", np.arange(298.15, 2263.15, 1))

df_H2.loc[-1] = np.arange(0,101*101325,101325)
df_H2.index = df_H2.index + 1  # shifting index
df_H2.sort_index(inplace=True)

df_S2.loc[-1] = np.arange(0,101*101325,101325)
df_S2.index = df_S2.index + 1  # shifting index
df_S2.sort_index(inplace=True) 




#%%%%

"""  Creating motab table  """


    
file = df_H2
file.columns = range(file.shape[1])
lines= list()
for row in file.itertuples(index=False):
    try:
        lines.append("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s \n" % (row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11], row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21], row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30], row[31], row[32],row[33],row[34],row[35],row[36],row[37],row[38],row[39],row[40], row[41], row[42],row[43],row[44],row[45],row[46],row[47],row[48],row[49],row[50],
                                                                             row[51], row[52],row[53],row[54],row[55],row[56],row[57],row[58],row[59],row[60], row[61], row[62],row[63],row[64],row[65],row[66],row[67],row[68],row[69],row[70], row[71], row[72],row[73],row[74],row[75],row[76],row[77],row[78],row[79],row[80], row[81], row[82],row[83],row[84],row[85],row[86],row[87],row[88],row[89],row[90], row[91], row[92],row[93],row[94],row[95],row[96],row[97],row[98],row[99],row[100]))
        previousRow = row
    except ValueError:
        pass

name= 'DeltaH'
extension='.motab'
saving_path='/home/srspoke/'      
filOut = open(saving_path+name+extension, 'w')
filOut.write("#1\n")
filOut.write("double data(%s,101)\n"% len(lines))
filOut.writelines(lines)
filOut.close()

file = df_S2
file.columns = range(file.shape[1])
lines= list()
for row in file.itertuples(index=False):
    try:
        lines.append("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s \n" % (row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11], row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21], row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30], row[31], row[32],row[33],row[34],row[35],row[36],row[37],row[38],row[39],row[40], row[41], row[42],row[43],row[44],row[45],row[46],row[47],row[48],row[49],row[50],
                                                                             row[51], row[52],row[53],row[54],row[55],row[56],row[57],row[58],row[59],row[60], row[61], row[62],row[63],row[64],row[65],row[66],row[67],row[68],row[69],row[70], row[71], row[72],row[73],row[74],row[75],row[76],row[77],row[78],row[79],row[80], row[81], row[82],row[83],row[84],row[85],row[86],row[87],row[88],row[89],row[90], row[91], row[92],row[93],row[94],row[95],row[96],row[97],row[98],row[99],row[100]))
        previousRow = row
    except ValueError:
        pass

name= 'DeltaS'
extension='.motab'
saving_path='/home/srspoke/'      
filOut = open(saving_path+name+extension, 'w')
filOut.write("#1\n")
filOut.write("double data(%s,101)\n"% len(lines))
filOut.writelines(lines)
filOut.close()





#%%%%

Y = range(df_H.shape[0])
X = range(df_H.shape[1])
X, Y = np.meshgrid(X, Y)
Z = df_H.values
fig = plt.figure(figsize=(20,10), dpi=400)
ax = fig.gca(projection='3d')
surface = ax.plot_surface(Y, X, Z, cmap='viridis', rstride=1, cstride=1)
ax.set_xlabel("K", fontsize=14, labelpad=10)
ax.set_ylabel("Bar", fontsize=14, labelpad=10)
ax.set_zlabel("J/mol", fontsize=14, labelpad=10)
fig.colorbar(surface, ax = ax, shrink = 0.5, pad=0.05)
plt.show()

Y = range(df_S.shape[0])
X = range(df_S.shape[1])
X, Y = np.meshgrid(X, Y)
Z = df_S.values
fig = plt.figure(figsize=(20,10), dpi=800)
ax = fig.gca(projection='3d')
surface = ax.plot_surface(Y, X, Z, cmap='viridis', rstride=1, cstride=1)
ax.set_xlabel("K", fontsize=14, labelpad=10)
ax.set_ylabel("Bar", fontsize=14, labelpad=10)
ax.set_zlabel("J/mol*K", fontsize=14, labelpad=10)
fig.colorbar(surface, ax = ax, shrink = 0.5, pad=0.05)
plt.show()

Y = range(df_G.shape[0])
X = range(df_G.shape[1])
X, Y = np.meshgrid(X, Y)
Z = df_G.values
fig = plt.figure(figsize=(20,10), dpi=800)
ax = fig.gca(projection='3d')
surface = ax.plot_surface(Y, X, Z, cmap='viridis', rstride=1, cstride=1)
ax.set_xlabel("K", fontsize=14, labelpad=10)
ax.set_ylabel("Bar", fontsize=14, labelpad=10)
ax.set_zlabel("J/mol", fontsize=14, labelpad=10)
fig.colorbar(surface, ax = ax, shrink = 0.5, pad=0.05)
plt.show()

for n in np.arange(1,101,11):
    fig, axs = plt.subplots(figsize=(15,8), dpi=300)
    Y_label = r"kJ/mol"
    X_label = r"K"   
    axs.plot(np.arange(298.15, 2263.15, 1),df_G[f"G{n}"]*pow(10,-3), "-", marker='+', markersize=5)
    axs.plot(np.arange(298.15, 2263.15, 1),df_H[f"H{n}"]*pow(10,-3), "-", marker='+', markersize=5)
    axs.plot(np.arange(298.15, 2263.15, 1),df_S[f"S{n}"]*np.arange(298.15, 2263.15, 1)*pow(10,-3), "-", marker='+', markersize=5)
    axs.set_ylabel(Y_label, fontsize=20)
    axs.set_xlabel(X_label, fontsize=20)
    axs.tick_params(axis="x", labelsize=20)
    axs.tick_params(axis="y", labelsize=20)
    var_1 = mlines.Line2D([], [], marker='+', linestyle='None', markerfacecolor='None', markeredgecolor='blue',
                          markersize=7, label='Gibbs free energy')
    var_2 = mlines.Line2D([], [], marker='o', linestyle='None', markerfacecolor='None', markeredgecolor='orange',
                          markersize=7, label='Entalphy')
    var_3 = mlines.Line2D([], [], marker='o', linestyle='None', markerfacecolor='None', markeredgecolor='green',
                          markersize=7, label='T*delta_S')
    axs.set_title(f"{n} Bar", fontsize=20)
    plt.legend(handles=[var_1, var_2, var_3],  fontsize=14, loc = 'upper right')
    plt.show()
