#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 13:11:32 2020

@author: cfillmor
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as mtri
from scipy.spatial import Delaunay


theta = np.array([i*360/50 for i in range(51)])
X = np.cos(theta)
Y = np.sin(theta)
Z = np.array([i for i in range(50)])

# u, v are parameterisation variables
u = np.array([0,0,0.5,1,1]) 
v = np.array([0,1,0.5,0,1]) 

x = u
y = v
z = np.array([0,0,1,0,0])

# Triangulate parameter space to determine the triangles
#tri = mtri.Triangulation(u, v)
tri = Delaunay(np.array([u,v]).T)
tri2 = Delaunay(np.array([theta]).T)

'''
print('polyhedron(faces = [')
#for vert in tri.triangles:
for vert in tri.simplices:
    print ('[%d,%d,%d],' % (vert[0],vert[1],vert[2]),)
print '], points = ['
for i in range(x.shape[0]):
    print '[%f,%f,%f],' % (x[i], y[i], z[i]),
print ']);'
'''

fig1 = plt.figure()
ax = fig1.add_subplot(1, 1, 1, projection='3d')

# The triangles in parameter space determine which x, y, z points are
# connected by an edge
#ax.plot_trisurf(x, y, z, triangles=tri.triangles, cmap=plt.cm.Spectral)
#ax.plot_trisurf(x, y, z, triangles=tri.simplices, cmap=plt.cm.Spectral)
#x.plot_trisurf(X, Y, Z, triangles=tri.simplices, cmap=plt.cm.Spectral)
ax.plot_trisurf(X, Y, Z, triangles=tri.simplices, cmap=plt.cm.Spectral)


plt.show()
