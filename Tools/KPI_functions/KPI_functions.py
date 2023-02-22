#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 11:40:39 2023

@author: srspoke
"""
import pandas as pd
# import numpy as np
# import math as mt
from scipy.optimize import curve_fit
"""
Cost of water 
reference: 
 Alvez, A., Aitken, D., Rivera, D., Vergara, M., McIntyre, N., & Concha, F. (2020). 
 At the crossroads: can desalination be a suitable public policy solution to address 
 water scarcity in Chile's mining zones?. Journal of environmental management, 258, 110039.

"""

def func(x, a, b):
    return a*x + b

df = pd.read_csv('/home/srspoke/Downloads/watercost.csv', header=None)
popt, pcov = curve_fit(func, df[0], df[1])

def s(x):
    return sum(x)

#%%%

"""
Economic analysis
"""
# capex 1326 #$/kW - 1182 #$/kW
# opex = USA: 40 $/kW ; EU: 50$/kW

def LCOH_2(Pinst, H, E_demad, H2_prod, h2o_req, CAPEX, OPEX, C_el, r, t_life, t_cons):
    """
    Pinst: gross power installed capacity electrolyzer plant in [W]+
    H: Altitude of the location from the sea level m.s.n.m
    E_demad:
    H2_prod:
    C_H20: cost of water in $/m3 is computed in function to the altitude from sea level
    CAPEX:1326 #$/kW - 1182 #$/kW
    OPEX: USA: 40 $/kW ; EU: 50$/kW
    C_el: cost of electricity in $/MWh
    r: discount rate usually 7%
    t_life: usually 30 years
    t_cons: usually 2 years 
    """
    
    nu = 0
    de = 0
    
    C_H20 = func(H,*popt)
	# Assume capital cost is evenly split between years in construction phase,
	# else if no construction phase it is all paid up front
    
    if t_cons == 0:
        nu += CAPEX*(Pinst/1e3)
    else:
        for i in range(t_cons):
            nu += (CAPEX*(Pinst/1e3)/t_cons)/((1 + r)**i)
    
    for i in range(t_cons+1, t_cons+t_life+1):
        nu += (OPEX*(Pinst/1e3) + C_H20*(h2o_req/1e3) + C_el*(E_demad/1e6))/((1 + r)**i)
        de += H2_prod/((1 + r)**i)
    
    return nu/de


def lcoe_pv(PV_cap, BESS_cap, INV_ac_cap, r, t_life, t_cons, epy):
    nu = 0
    de = 0
    c_pv = 0.2 #$/Wdc
    c_bess = 299 #$/kWdc
    c_inv = 0.05 #$/Wac
    c_bop = 0.2 #$/Wdc
    c_ils = 0.16 #$/Wdc
    c_om_y = 0.012682 # $/W
    c_cap = BESS_cap*c_bess + INV_ac_cap*c_inv + (c_pv + c_bop + c_ils)*PV_cap
    c_year = c_om_y*PV_cap
	# Assume capital cost is evenly split between years in construction phase,
	# else if no construction phase it is all paid up front
    if t_cons == 0:
        nu += c_cap
    else:
        for i in range(t_cons):
            nu += (c_cap/t_cons)/((1 + r)**i)

    for i in range(t_cons+1, t_cons+t_life+1):
        nu += c_year/((1 + r)**i)
        de += epy/((1 + r)**i)
    
    return nu/de
