#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 14:40:18 2020

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


def elip0():
    a=16
    b=4
    
    lift = 0.2
    rand_const = 0.01
    
    x0 = 0
    y0 = 0
    
    deg = 361*np.random.rand()
    theta = deg*np.pi/180
    x = a*np.cos(theta) - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + x0
    y = b*np.sin(theta) - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + y0
    
    
    #0 int 2 a
    if (deg > (308 - 7)%360) & (deg < 308%360):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + ((deg - 308 + 7))*lift
    elif (deg >= 308%360) & (deg < (308 + 7)%360):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + ((308 + 7 - deg))*lift
    #0 int 2 b
    elif (deg > (235 - 7)%360) & (deg < 235):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + (deg - 235 + 7)*lift
    elif (deg >= 235) & (deg < (235 + 7)%360):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + (235 + 7 - deg)*lift
    #0 int 1 a
    elif (deg > (77 - 7)%360) & (deg < 77%360):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + ((deg - 77 + 7))*lift
    elif (deg >= 77%360) & (deg < (77 + 7)%360):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + ((77 + 7 - deg))*lift
    #0 int 1 b
    elif (deg > (283 - 7)%360) & (deg < 283):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + (deg - 283 + 7)*lift
    elif (deg >= 283) & (deg < (283 + 7)%360):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + (283 + 7 - deg)*lift
    #normal
    else:
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0]
        
        
    return [x,y,z]

def elip1():
    a=4
    b=16
    
    lift = 0.2
    rand_const = 0.01
    
    x0 = 0
    y0 = 0
    
    deg = 361*np.random.rand()
    theta = deg*np.pi/180
    x = a*np.cos(theta) - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + x0
    y = b*np.sin(theta) - 0.005 + rand_const*np.random.rand(1,1)[0][0] + y0
    
    
    
    #1 int 2 a
    if (deg > (38 - 7)%360) & (deg < 38):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + (deg - 38 + 7)*lift
    elif (deg >= 38) & (deg < (38 + 7)%360):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + (38 + 7 - deg)*lift
    #1 int 2 b
    elif (deg > (322 - 7)%360) & (deg < 322):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + (deg - 322 + 7)*lift
    elif (deg >= 322) & (deg < (322 + 7)%360):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + (322 + 7 - deg)*lift
    #1 int 0 a
    elif (deg > (165 - 7)%360) & (deg < 165%360):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + ((deg - 165 + 7))*lift
    elif (deg >= 165%360) & (deg < (165 + 7)%360):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + ((165 + 7 - deg))*lift
    #1 int 0 b
    elif (deg > (195 - 7)%360) & (deg < 195):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + (deg - 195 + 7)*lift
    elif (deg >= 195) & (deg < (195 + 7)%360):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + (195 + 7 - deg)*lift
    #normal
    else:
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0]
    
    
    return [x,y,z]

def elip2():
    a=10
    b=10
    
    lift = 0.2
    rand_const = 0.01
    
    x0 = 0
    y0 = 0
    
    deg = 361*np.random.rand()
    theta = deg*np.pi/180
    x = a*np.cos(theta) - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + x0
    y = b*np.sin(theta) - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + y0
    
    
    #2 int 0 a
    if (deg > (18 - 7)%360) & (deg < 18):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + (deg - 18 + 7)*lift
    elif (deg >= 18) & (deg < (18 + 7)%360):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + (18 + 7 - deg)*lift
    #2 int 0 b
    elif (deg > (162 - 7)%360) & (deg < 162):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + (deg - 162 + 7)*lift
    elif (deg >= 162) & (deg < (162 + 7)%360):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + (162 + 7 - deg)*lift
    #2 int 1 a
    elif (deg > (110 - 7)%360) & (deg < 110%360):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + ((deg - 110 + 7))*lift
    elif (deg >= 110%360) & (deg < (110 + 7)%360):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + ((110 + 7 - deg))*lift
    #2 int 1 b
    elif (deg > (250 - 7)%360) & (deg < 250):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + (deg - 250 + 7)*lift
    elif (deg >= 250) & (deg < (250 + 7)%360):
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0] + (250 + 7 - deg)*lift
    #normal
    else:
        z = 0 - 0.5*rand_const + rand_const*np.random.rand(1,1)[0][0]
    
    
    return [x,y,z]

N = 5000
for N in [100,300,500,1000,3000,5000,10000]:
    pt = np.array([elip0() for i in range(N)] + [elip1() for i in range(N)] +[elip2() for i in range(N)])
    col = ['red']*N + ['green']*N + ["blue"]*N
    a = [i for i in zip(pt,col)]
    np.random.shuffle(a)
    pts,colours = (np.array([i for i,j in a]), [j for i,j in a])
    
    with open('/home/cfillmor/topology/medial/pt_sets/L10a140_plane_'+str(N) + '.json', 'w') as out:
        json.dump([pts.tolist(), colours], out)



'''
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
pole_rad = [i for i in pole_rad if dist(i[0],[0,0,0]) < 21]
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





