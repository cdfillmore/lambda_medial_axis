#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 13:07:18 2020

@author: cfillmor
"""

pindex = 71
tetra = delaunay.simplices[pindex]

tris = [i for i in it.combinations(tetra,3)]

triangle = tris[0]
print(len([voronoi.regions[i] for i in tetra if -1 in voronoi.regions[i] ]))



chs = [spa.ConvexHull(voronoi.vertices[voronoi.regions[voronoi.point_region[i]]]) for i in tetra]

fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')

'''
for ch in chs:
    plot_ch = a3.art3d.Poly3DCollection([ch.points[i] for i in ch.simplices], alpha=0.2)
    plot_ch.set_color('brown')
    ax.add_collection3d(plot_ch)
'''

dual_voro_edge = delaunay_tri_2_voronoi_edge(triangle, new_dict)

plot_tris = a3.art3d.Poly3DCollection([pts[list(i)] for i in tris[1:]], alpha=0.2)
plot_tris.set_color('purple')
ax.add_collection3d(plot_tris)

plot_tri = a3.art3d.Poly3DCollection([pts[list(triangle)]], alpha=0.2)
plot_tri.set_color('yellow')
ax.add_collection3d(plot_tri)

plot_edge = a3.art3d.Poly3DCollection([voronoi.vertices[list(dual_voro_edge)]], alpha=0.2)
plot_edge.set_color('red')
ax.add_collection3d(plot_edge)


ax.set_xlim3d(-5,5)
ax.set_ylim3d(-5,5)
ax.set_zlim3d(-5,5)






