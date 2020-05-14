#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 15:49:38 2020

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
import json

def vect(p,q):
    return [ (p[i] - q[i]) for i in range(len(p))]

def dist(p,q):
    return np.sqrt( np.dot(vect(p,q), vect(p,q)) )

def angle(v,w):
    return np.arccos( np.dot(v,w) / (np.sqrt(np.dot(v,v))*np.sqrt(np.dot(w,w) ) ) )

def single_pole(pindex, pts, voronoi):
    p = pts[pindex]
    rindex = voronoi.point_region[pindex]
    reg = voronoi.regions[rindex]
    if -1 in reg:
        reg.remove(-1)
    r, index = max([(dist(p,j),i) for i,j in enumerate(voronoi.vertices[reg])])
    return [[voronoi.vertices[reg][index],r]]

def double_pole(pindex, pts, voronoi):
    p = pts[pindex]
    rindex = voronoi.point_region[pindex]
    reg = voronoi.regions[rindex]
    if -1 in reg:
        reg.remove(-1)
    
    p1,r1 = single_pole(pindex, pts, voronoi)[0]
    
    v1 = vect(p1,p)
    good_points = [ i for i in voronoi.vertices[reg] if angle(vect(i,p),v1) > np.pi/2]
    
    r2, index2 = max([(dist(p,j),i) for i,j in enumerate(good_points)])
    p2 = good_points[index2]
    return [[p1,r1], [p2,r2]]

def pole(pindex, pts, voronoi):
    rindex = voronoi.point_region[pindex]
    reg = voronoi.regions[rindex]
    if -1 in reg:
        return single_pole(pindex, pts, voronoi)
    else:
        return double_pole(pindex, pts, voronoi)

def find_neighbours(pindex, delaunay):
    return delaunay.vertex_neighbor_vertices[1][delaunay.vertex_neighbor_vertices[0][pindex]:delaunay.vertex_neighbor_vertices[0][pindex+1]]

def pt_at_angle(theta, x0, y0, r):
    a=r
    b=r
    
    x = a*np.cos(theta) + x0
    y = b*np.sin(theta) + y0
    z = 0.2
    return [x,y,z]

def delaunay_tri_2_voronoi_edge(triangle,ridge_dict):
    '''
    returns a vornoi edge with vertices indexed by voronoi vertices
    '''
    edges = [i for i in it.combinations(triangle,2)]
    dual_voro_faces = [ridge_dict[tuple(sorted(i))] for i in edges]
    return np.intersect1d(dual_voro_faces[0], dual_voro_faces[1], dual_voro_faces[2])

def torus():
    a=13
    b=13
    
    lift = 0.2
    rand_const = 0.01
    
    rad = 8 + 6*np.random.rand()
    deg = 361*np.random.rand()
    theta = deg*np.pi/180
    
    x = rad*np.cos(theta) + - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0]
    y = rad*np.sin(theta) - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0]
    z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0]
        
    return [x,y,z]


N = 500
for N in [100,300,500,1000,3000,5000,10000]:
    pt = np.array([torus() for i in range(N)])
    N = len(pt)
    col = ['red']*N
    a = [i for i in zip(pt,col)]
    np.random.shuffle(a)
    pts,colours = (np.array([i for i,j in a]), [j for i,j in a])
    
    #'''
    with open('/home/cfillmor/topology/medial/pt_sets/annulus_'+str(N) + '.json', 'w') as out:
        json.dump([pts.tolist(), colours], out)
#'''
'''
with open('/home/cfillmor/topology/medial/pt_sets/boro_3d_300.json') as file:
    pts,colours = json.load(file)
'''
'''
pts = np.array(pts)

delaunay = spa.Delaunay(pts)
voronoi = spa.Voronoi(pts)
new_dict = {tuple(sorted(tuple(i))):voronoi.ridge_dict[tuple(i)] for i in voronoi.ridge_points}

fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')
#ax.scatter(pts.T[0], pts.T[1], pts.T[2], color=colours)

v_verts = voronoi.vertices
bad_v = [-1]
#bad_v += [i for i,j in enumerate(v_verts) if np.sqrt(sum([k*k for k in j]))>30]
good = np.array([ j for i,j in enumerate(v_verts) if i not in bad_v])

ax.scatter(pts.T[0], pts.T[1], pts.T[2], color=colours)
#ax.scatter(good.T[0], good.T[1], good.T[2], color='gold')
temp = np.array([pole(i,pts,voronoi) for i in range(len(pts))])
pole_rad = []
for i in temp:
    pole_rad += i
#pole_rad = [i for i in pole_rad if dist(i[0],[0,0,0]) < 21]
poles = [i[0] for i in pole_rad]
poles = np.array(poles)
ax.scatter(poles.T[0], poles.T[1], poles.T[2], color='gold')


delauny2 = spa.Delaunay(poles)
tris = set([])
for tetra in delauny2.simplices:
    for triangle in it.combinations(tetra,3):
        blah = [(tuple([i,j])) for i,j in it.combinations(triangle,2) if dist(delauny2.points[i], delauny2.points[j]) < min([pole_rad[i][1], pole_rad[j][1]])]
        tris.update(blah)
        if len(blah)==3:
            tris.update([triangle])
plot_simp = a3.art3d.Poly3DCollection([delauny2.points[list(tri)] for tri in tris], alpha=0.1)
plot_simp.set_color('purple')
ax.add_collection3d(plot_simp)



for i in ["x", "y", "z"]:
    eval("ax.set_{:s}label('{:s}')".format(i, i))
plt.show()


ax.set_xlim3d(-20,20)
ax.set_ylim3d(-20,20)
ax.set_zlim3d(-20,20)
'''
