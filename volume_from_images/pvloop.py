#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
Created on 2025/02/05 15:56:31

@author: Javiera Jilberto Vallejos 
'''

import numpy as np
import cheartio as chio
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

def repeat_traces(trace):
    return np.concatenate((trace, trace, trace))

def rescale_pressure_magnitude(pressure, ed_pressure, es_pressure):
    pressure = pressure.copy()

    # Calculate mean pressure
    mbp = 2/3*ed_pressure + 1/3*es_pressure
    sp = es_pressure
    dp = ed_pressure

    aux = pressure.copy()
    a = (sp - dp)/(1.0 - aux[0])
    pressure[aux > aux[0]] = aux[aux > aux[0]]*a + sp - a
    pressure[aux <= aux[0]] = aux[aux <= aux[0]]/aux[0]*dp
    return pressure


lv_vol = chio.read_dfile('data/lv_volume.INIT')[:,1]
rv_vol = chio.read_dfile('data/rv_volume.INIT')[:,1]
time_vol = chio.read_dfile('data/lv_volume.INIT')[:,0]

lv_edp = 1.33322
lv_sysp = 16.0
rv_edp = 0.53329
rv_sysp = 3.33306

# Deal with volume
lv_vol_ext = repeat_traces(lv_vol)
time_vol_ext = np.linspace(-1, 2, len(lv_vol_ext))
lv_vol_func = PchipInterpolator(time_vol_ext, lv_vol_ext)

rv_vol_ext = repeat_traces(rv_vol)
rv_vol_func = PchipInterpolator(time_vol_ext, rv_vol_ext)

# Deal with pressure
norm_pres_time, norm_pres = np.load('refdata/normalized_human_pressure.npy').T
lv_pres = rescale_pressure_magnitude(norm_pres, lv_edp, lv_sysp)
lv_pres_ext = repeat_traces(lv_pres)

rv_pres = rescale_pressure_magnitude(norm_pres, rv_edp, rv_sysp)
rv_pres_ext = repeat_traces(rv_pres)

time_pres_ext = np.linspace(-1, 2, len(lv_pres_ext))
func_lv_pres = PchipInterpolator(time_pres_ext, lv_pres_ext)
func_rv_pres = PchipInterpolator(time_pres_ext, rv_pres_ext)

vol_shift = -0.1
time_pv = np.linspace(0, 1, 100)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 12))

# Volume subplot
ax1.plot(time_pv, lv_vol_func(time_pv+vol_shift), label='LV Volume')
ax1.plot(time_pv, rv_vol_func(time_pv+vol_shift), label='RV Volume')
ax1.axvline(x=0, color='gray', linestyle='--')
ax1.axvline(x=1, color='gray', linestyle='--')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Volume (ml)')
ax1.legend()
ax1.set_title('Volume over Time')

# Pressure subplot
ax2.plot(time_pv, func_lv_pres(time_pv), label='LV Pressure')
ax2.plot(time_pv, func_rv_pres(time_pv), label='RV Pressure')
ax2.axvline(x=0, color='gray', linestyle='--')
ax2.axvline(x=1, color='gray', linestyle='--')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Pressure (mmHg)')
ax2.legend()
ax2.set_title('Pressure over Time')

# Pressure vs Volume subplot
ax3.plot(lv_vol_func(time_pv+vol_shift), func_lv_pres(time_pv), label='LV Pressure-Volume Loop')
ax3.plot(rv_vol_func(time_pv+vol_shift), func_rv_pres(time_pv), label='RV Pressure-Volume Loop')
ax3.set_xlabel('Volume (ml)')
ax3.set_ylabel('Pressure (mmHg)')
ax3.legend()
ax3.set_title('Pressure vs Volume')

plt.tight_layout()
plt.show()