#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
Created on 2025/04/04 11:59:06

@author: Javiera Jilberto Vallejos 
'''

import numpy as np
import cheartio as chio

lved = 191301.09572213658
lv_volume = chio.read_dfile('data/lv_volume.INIT')
lv_volume[:,1] = lv_volume[:,1] + (lved-lv_volume[0,1])

chio.write_dfile('data/lv_volume_mod.INIT', lv_volume)

rved = 265213.23340421356
rv_volume = chio.read_dfile('data/rv_volume.INIT')
rv_volume[:,1] = rv_volume[:,1] + (rved-rv_volume[0,1])
chio.write_dfile('data/rv_volume_mod.INIT', rv_volume)