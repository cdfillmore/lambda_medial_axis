#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 16:17:17 2020

@author: cfillmor
"""

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as a3
import scipy.spatial as spa
import numpy as np
import itertools as it
import pylab
from random import sample

import os
import json

N = 3000

directory = "/home/cfillmor/topology/medial/unformatted_pt_sets/"
for file in os.listdir(directory):
    if file !='vase.ply':
        continue
    with open(directory + file,'r') as f:
        lines = f.readlines()
    lines = lines[(lines.index('end_header\n')+1):]
    pts = np.array([ [float(j) for j in i.strip('\n').split(' ')] for i in lines])
    break

inds = sample(range(len(pts)),N)
pts = np.array([pts[i] for i in range(len(pts)) if i in inds])
ave = sum(pts)/len(pts)
pts = pts - ave

with open('/home/cfillmor/topology/medial/pt_sets/vase_'+str(N) + '.json', 'w') as out:
    json.dump([pts.tolist(), ['red' for i in range(len(pts))]], out)


fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')
ax.scatter(pts.T[0], pts.T[1], pts.T[2], color='red')
for i in ["x", "y", "z"]:
    eval("ax.set_{:s}label('{:s}')".format(i, i))
plt.show()










