#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
Created on 2024/11/20 14:59:42

@author: Javiera Jilberto Vallejos 
'''

import numpy as np
import cheartio as chio

def get_normal_plane_svd(points):   # Find the plane that minimizes the distance given N points
    centroid = np.mean(points, axis=0)
    svd = np.linalg.svd(points - centroid)
    normal = svd[2][-1]
    normal = normal/np.linalg.norm(normal)
    return normal, centroid

# User inputs. TODO: you need to change it depending on the mesh
mesh_fldr = 'BiV/mesh/'
model_name = 'bv_model'
mv_patch = 1
av_patch = 2
tv_patch = 3
pv_patch = 4

# Load meshes and boundary data
mesh = chio.read_mesh(mesh_fldr + model_name, meshio=True)
bdata = chio.read_bfile(mesh_fldr + model_name)

# Grab the nodes corresponding to each valve
labels = bdata[:,-1]
mv_nodes = np.unique(bdata[labels == mv_patch, 1:-1])
av_nodes = np.unique(bdata[labels == av_patch, 1:-1])
tv_nodes = np.unique(bdata[labels == tv_patch, 1:-1])
pv_nodes = np.unique(bdata[labels == pv_patch, 1:-1])

# Find normal vectors for each valve
mv_points = mesh.points[mv_nodes]
av_points = mesh.points[av_nodes]
tv_points = mesh.points[tv_nodes]
pv_points = mesh.points[pv_nodes]

mv_normal, mv_centroid = get_normal_plane_svd(mv_points)
av_normal, av_centroid = get_normal_plane_svd(av_points)
tv_normal, tv_centroid = get_normal_plane_svd(tv_points)
pv_normal, pv_centroid = get_normal_plane_svd(pv_points)

# N3 vector
n3 = np.cross(mv_normal, av_normal)
lv_n3 = n3/np.linalg.norm(n3)
n3 = np.cross(tv_normal, pv_normal)
rv_n3 = n3/np.linalg.norm(n3)

# Save to mesh folder
chio.write_dfile(mesh_fldr + 'N3_lv.FE', lv_n3)
chio.write_dfile(mesh_fldr + 'N3_rv.FE', rv_n3)