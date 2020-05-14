#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 15:53:59 2020

@author: cfillmor
"""
import numpy as np
import json

def elip0():
    a=10
    b=10
    
    lift = 0.2
    rand_const = 0.01
    
    x0 = 0
    y0 = -5
    
    deg = 361*np.random.rand()
    theta = deg*np.pi/180
    x = a*np.cos(theta) - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + x0
    y = b*np.sin(theta) - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + y0
    z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0]
    return [x,y,z]

def elip1():
    a=10
    b=10
    
    lift = 0.2
    rand_const = 0.01
    
    x0 = 0
    y0 = 5
    
    deg = 361*np.random.rand()
    theta = deg*np.pi/180
    x = a*np.cos(theta) - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + x0
    y = b*np.sin(theta) - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + y0
    z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0]
    return [z,y,x]

N = 100
for N in [100,300,500,1000,3000,5000,10000]:
    pt = np.array([elip0() for i in range(N)] + [elip1() for i in range(N)] )
    col = ['red']*N + ['green']*N
    a = [i for i in zip(pt,col)]
    np.random.shuffle(a)
    pts,colours = (np.array([i for i,j in a]), [j for i,j in a])
    '''
    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(pts.T[0], pts.T[1], pts.T[2], color=colours)
    for i in ["x", "y", "z"]:
        eval("ax.set_{:s}label('{:s}')".format(i, i))
    plt.show()
    ax.set_xlim3d(-20, 20)
    ax.set_ylim3d(-20, 20)
    ax.set_zlim3d(-20, 20)
    '''
    
    with open('/home/cfillmor/topology/medial/pt_sets/hopf_link_3d_'+str(N) + '.json', 'w') as out:
        json.dump([pts.tolist(), colours], out)
    






