#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
Created on 2025/01/30 11:32:44

@author: Javiera Jilberto Vallejos 
'''

from matplotlib import pyplot as plt
import nibabel as nib
import numpy as np
import cheartio as chio

img = nib.load('data/5_trimmed_label_maps.nii.gz')
data = img.get_fdata()

# Plot data
plt.figure(1, clear=True)
plt.imshow(data[:,:,59])
plt.show()


voxel_dim = img.header.get_zooms()
voxel_vol = voxel_dim[0]*voxel_dim[1]*voxel_dim[2] # mm^3

lv = data == 1
voxel_lv = np.sum(lv)
vol_lv = voxel_lv*voxel_vol

# Loop over all images and calculate the volume of the left ventricle and right ventricle, left atrium, right atrium

# Plot of volume vs time for each ventricle
# chio.write_dfile('lv_volume.INIT')