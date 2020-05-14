#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 14:49:01 2020

@author: cfillmor
"""
import itertools as it
import numpy as np
import json
import os

#file = 'boro_plane_1000'



for file in os.listdir('/home/cfillmor/topology/medial/pt_sets/'):
    file = file[:-5]
    runfile('/home/cfillmor/topology/medial/medial_axis_approx.py')
    try:
        pts, pt_cols, dpts, tris2, poles = approx_medial_axis('/home/cfillmor/topology/medial/pt_sets/' + file + '.json', 30, 0, False)
    except:
        print(file + ' failed!')
        continue
    print(file + ' passed!')
    
    tris3 = np.array([list(i) for i in tris2 if len(i)==3]).flatten()
    
    pt_dex = [i for (i,j) in enumerate(dpts)]
    
    
    good_points = [dpts[i] for i in pt_dex if i in tris3]
    
    
    with open('/home/cfillmor/topology/kathi_pts/' + file + '.txt', 'w') as file:
        for i in good_points:
            file.write(' '.join([str(j) for j in i]) + '\n')
            #print(' '.join([str(j) for j in i]) + '\n')
    
    
    
    








