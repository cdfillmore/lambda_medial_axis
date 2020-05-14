#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 15:49:38 2020

@author: cfillmor
"""
from georg_miniball3d import circumsphere_3d
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

def triangulate(face):
    tris = []
    for i in range(1,len(face)-1):
        tris += [[face[0], face[i], face[i+1]]]
    #tris += [[face[0],face[-1],face[1]]]
    return tris

def delaunay_tri_2_voronoi_edge(triangle,ridge_dict):
    '''
    returns a vornoi edge with vertices indexed by voronoi vertices
    '''
    edges = [i for i in it.combinations(triangle,2)]
    dual_voro_faces = [ridge_dict[tuple(sorted(i))] for i in edges]
    return np.intersect1d(dual_voro_faces[0], dual_voro_faces[1], dual_voro_faces[2])

def approx_medial_axis(file, MAX, z_max, alpha, plot):
    
    with open(file) as f:
        pts,colours = json.load(f)
    pts = np.array(pts)
    
    delaunay = spa.Delaunay(pts)
    dtris = set([])
    for i in delaunay.simplices:
        dtris.update([ j for j in it.combinations(i,3) if circumsphere_3d(pts[i])[1] < alpha])
    dtris = np.array([list(i) for i in dtris], dtype=np.int32)
    
    voronoi = spa.Voronoi(pts)
    new_dict = {tuple(sorted(tuple(i))):voronoi.ridge_dict[tuple(i)] for i in voronoi.ridge_points}
    
    if plot==True:
        fig = plt.figure(1)
        ax = fig.add_subplot(111, projection='3d')
        #ax.scatter(pts.T[0], pts.T[1], pts.T[2], color=colours)
    
    v_verts = voronoi.vertices
    bad_v = [-1]
    #bad_v += [i for i,j in enumerate(v_verts) if np.sqrt(sum([k*k for k in j]))>30]
    good = np.array([ j for i,j in enumerate(v_verts) if i not in bad_v])
    
    if plot==True:
        ax.scatter(pts.T[0], pts.T[1], pts.T[2], color=colours)
    
    temp = np.array([pole(i,pts,voronoi) for i in range(len(pts))])
    pole_rad = []
    for i in temp:
        pole_rad += i
    
    if z_max:
        pole_rad = [i for i in pole_rad if (np.abs(i[0][2]) < z_max)]
    if MAX:
        pole_rad = [i for i in pole_rad if (dist(i[0],[0,0,0]) < MAX)]
    poles = [i[0] for i in pole_rad]
    poles = np.array(poles)
    #if plot==True:
        #ax.scatter(poles.T[0], poles.T[1], poles.T[2], color='gold')
    
    
    delauny2 = spa.Delaunay(poles)
    tris = set([])
    for tetra in delauny2.simplices:
        for triangle in it.combinations(tetra,3):
            blah = [(tuple([i,j])) for i,j in it.combinations(triangle,2) if dist(delauny2.points[i], delauny2.points[j]) < min([pole_rad[i][1], pole_rad[j][1]])]
            tris.update(blah)
            if len(blah)==3:
                tris.update([triangle])
    tris = list(tris)

    
    if plot==True:
        plot_simp = a3.art3d.Poly3DCollection([delauny2.points[list(tri)] for tri in tris], alpha=0.1)
        plot_simp.set_color('purple')
        ax.add_collection3d(plot_simp)
        
        for i in ["x", "y", "z"]:
            eval("ax.set_{:s}label('{:s}')".format(i, i))
        plt.show()
    
        '''
        ax.set_xlim3d(-1, 1)
        ax.set_ylim3d(-1, 1)
        ax.set_zlim3d(-1, 1)    
        
        ax.set_xlim3d(-5, 5)
        ax.set_ylim3d(-5, 5)
        ax.set_zlim3d(-5, 5)
       '''
        ax.set_xlim3d(-20, 20)
        ax.set_ylim3d(-20, 20)
        ax.set_zlim3d(-20, 20)
        #'''
    
    #return [pts, colours, [delauny2.points[list(tri)] for tri in tris], poles]
    return [pts, dtris, colours, delauny2.points, tris, poles]


def approx_medial_axis2(file, MAX, z_max, alpha, LAMBDA, exp_tris):
    with open(file) as f:
        pts,colours = json.load(f)
    pts = np.array(pts)
    
    voronoi = spa.Voronoi(pts)
    print("done voronoi")
    delaunay = spa.Delaunay(pts)
    print("done delaunay")
    
    dtris = set([])
    for i in delaunay.simplices:
        dtris.update([ j for j in it.combinations(i,3) if circumsphere_3d(pts[i])[1] < alpha])
    dtris = np.array([list(i) for i in dtris], dtype=np.int32)
    print("done alpha")
    
    '''
    new_dict = {tuple(sorted(tuple(i))):voronoi.ridge_dict[tuple(i)] for i in voronoi.ridge_points}
    inv_dict = {tuple(new_dict[i]):list(i) for i in new_dict}
    '''
    bad_v = []
    if MAX:
        bad_v += [i for i,j in enumerate(voronoi.vertices) if dist(j,[0,0,0])>MAX]
    if z_max:
        bad_v += [i for i,j in enumerate(voronoi.vertices) if (np.abs(j[2]) > z_max)]
    
    bad_v = list(set(bad_v))
    
    faces = []
    for i in voronoi.ridge_dict:
        if -1 in voronoi.ridge_dict[i]:
            continue
        elif circumsphere_3d([pts[i[0]], pts[i[1]]])[1] > LAMBDA:
            if len(np.intersect1d(voronoi.ridge_dict[i], bad_v, assume_unique = True)) == 0:
                if exp_tris:
                    faces += triangulate(voronoi.ridge_dict[i])
                else:
                    faces += [voronoi.ridge_dict[i]] 
    print("done lambda + limit")
    
    '''
    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')
    
    plot_simp = a3.art3d.Poly3DCollection([ voronoi.vertices[i] for i in faces], alpha=0.1)
    plot_simp.set_color('purple')
    ax.add_collection3d(plot_simp)
    
    ax.set_xlim3d(-4, 4)
    ax.set_ylim3d(-4, 4)
    ax.set_zlim3d(-4, 4)
    '''
    
    return [pts, dtris, voronoi.vertices, faces]










#approx_medial_axis('/home/cfillmor/topology/medial/pt_sets/boro_3d_500.json', False)
#approx_medial_axis('/home/cfillmor/topology/medial/pt_sets/boro_plane_500.json', False)
#approx_medial_axis('/home/cfillmor/topology/medial/pt_sets/L10a140_plane_500.json', False)
#approx_medial_axis('/home/cfillmor/topology/medial/pt_sets/square_plane_250.json', False)
#approx_medial_axis('/home/cfillmor/topology/medial/pt_sets/loop_plane_1000.json', False)
#approx_medial_axis('/home/cfillmor/topology/medial/pt_sets/elipse_plane_1000.json', False)
#approx_medial_axis('/home/cfillmor/topology/medial/pt_sets/hopf_3d_500.json', False)
#approx_medial_axis('/home/cfillmor/topology/medial/pt_sets/vase_2000.json', False)







