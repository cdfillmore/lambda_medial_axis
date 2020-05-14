#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 15:53:59 2020

@author: cfillmor
"""
import numpy as np
import json


for N in [100,300,500,1000,3000,5000,10000]:
    j = N/4
    rand_const = 0.01
    side = 20*np.random.rand(int(j)) - 10 
    side1 = [ [ i , -10 , 0 ] for i in side]
    side2 = [ [ i , 10 , 0 ] for i in side]
    side3 = [ [ -10 , i , 0 ] for i in side]
    side4 = [ [ 10 , i , 0 ] for i in side]
    
    pts = pts = side1 + side2 + side3 + side4
    
    pts = np.array([ [ j+rand_const*np.random.rand() for j in i] for i in pts])
    colours = ['red' for i in range(len(pts))]
    
    with open('/home/cfillmor/topology/medial/pt_sets/square_plane_'+str(N) + '.json', 'w') as out:
        json.dump([pts.tolist(), colours], out)
    
    





