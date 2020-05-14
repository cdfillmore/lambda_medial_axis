#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 13:55:36 2019

@author: cfillmor
"""


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm

x = np.arange(-2, 2, 0.1)
y = np.arange(-2, 2, 0.1)
mx, my = np.meshgrid(x, y, indexing='ij')
mz1 = np.abs(mx) + np.abs(my)
mz2 = mx ** 2 + my ** 2


def v2_mayavi(transparency):
    from mayavi import mlab
    fig = mlab.figure()

    ax_ranges = [-1.75, 1.75, -1.75, 1.75, -1.75, 1.75]
    ax_scale = [1.0, 1.0, 0.4]
    ax_extent = ax_ranges * np.repeat(ax_scale, 2)
    
    a1 = 0.25
    b1 = 1
    c1 = 1.5

    a2 = 0.25
    b2 = 2
    c2 = 0.5

    a3 = 0.25
    b3 = 1.5
    c3 = 0.5

    theta1 = [i*np.pi/180 for i in range(361)]
    theta2 = [i*np.pi/180 for i in range(361)]

    theta1, theta2 = np.meshgrid(theta1, theta2)

    x1 = (a1*np.cos(theta1)+b1)*c1*np.cos(theta2)
    y1 = (a1*np.cos(theta1)+b1)*np.sin(theta2)
    z1 = a1*np.sin(theta1)

    x2 = (a2*np.cos(theta1)+b2)*c2*np.cos(theta2)
    z2 = (a2*np.cos(theta1)+b2)*np.sin(theta2)
    y2 = a2*np.sin(theta1)

    z3 = (a3*np.cos(theta1)+b3)*c3*np.cos(theta2)
    y3 = (a3*np.cos(theta1)+b3)*np.sin(theta2)
    x3 = a3*np.sin(theta1)
    
    surf1 = mlab.surf(x1,y1,z1, colormap='Blues')
    #surf2 = mlab.surf(x2,y2,z2, colormap='Oranges')
    #surf3 = mlab.surf(x3,y3,z3, colormap='Greens')


    surf1.actor.actor.scale = ax_scale
    #surf2.actor.actor.scale = ax_scale
    #surf3.actor.actor.scale = ax_scale
    
    mlab.view(60, 74, 17, [-2.5, -4.6, -0.3])
    mlab.outline(surf1, color=(.7, .7, .7), extent=ax_extent)
    mlab.axes(surf1, color=(.7, .7, .7), extent=ax_extent,
              ranges=ax_ranges,
              xlabel='x', ylabel='y', zlabel='z')

    if transparency:
        surf1.actor.property.opacity = 0.5
        #surf2.actor.property.opacity = 0.5
        #surf3.actor.property.opacity = 0.5
        fig.scene.renderer.use_depth_peeling = 1



def v2_mayavi2(transparency):
    from mayavi import mlab
    fig = mlab.figure()

    ax_ranges = [-2, 2, -2, 2, 0, 8]
    ax_scale = [1.0, 1.0, 0.4]
    ax_extent = ax_ranges * np.repeat(ax_scale, 2)

    surf3 = mlab.surf(mx, my, mz1, colormap='Blues')
    surf4 = mlab.surf(mx, my, mz2, colormap='Oranges')

    surf3.actor.actor.scale = ax_scale
    surf4.actor.actor.scale = ax_scale
    mlab.view(60, 74, 17, [-2.5, -4.6, -0.3])
    mlab.outline(surf3, color=(.7, .7, .7), extent=ax_extent)
    mlab.axes(surf3, color=(.7, .7, .7), extent=ax_extent,
              ranges=ax_ranges,
              xlabel='x', ylabel='y', zlabel='z')

    if transparency:
        surf3.actor.property.opacity = 0.5
        surf4.actor.property.opacity = 0.5
        fig.scene.renderer.use_depth_peeling = 1


#%matplotlib notebook


a1 = 0.25
b1 = 1
c1 = 1.5

a2 = 0.25
b2 = 2
c2 = 0.5

a3 = 0.25
b3 = 1.5
c3 = 0.5

theta1 = [i*np.pi/180 for i in range(361)]
theta2 = [i*np.pi/180 for i in range(361)]




#r = 






theta1, theta2 = np.meshgrid(theta1, theta2)

x1 = (a1*np.cos(theta1)+b1)*c1*np.cos(theta2)
y1 = (a1*np.cos(theta1)+b1)*np.sin(theta2)
z1 = a1*np.sin(theta1)

x2 = (a2*np.cos(theta1)+b2)*c2*np.cos(theta2)
z2 = (a2*np.cos(theta1)+b2)*np.sin(theta2)
y2 = a2*np.sin(theta1)

z3 = (a3*np.cos(theta1)+b3)*c3*np.cos(theta2)
y3 = (a3*np.cos(theta1)+b3)*np.sin(theta2)
x3 = a3*np.sin(theta1)


'''
r⃗ (s,α)=γ⃗ (s)+ccosαn⃗ (s)+csinαb⃗ (s).
'''




fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([-1.75,1.75])
ax.set_ylim([-1.75,1.75])
ax.set_zlim([-1.75,1.75])
#ax.plot_surface(x,y,z, cmap = cm.jet)
ax.plot_surface(x1,y1,z1)
ax.plot_surface(x2,y2,z2)
ax.plot_surface(x3,y3,z3)


'''
surf1 = mlab.surf(x1,y1,z1)
surf2 = mlab.surf(x2,y2,z2)
surf3 = mlab.surf(x3,y3,z3)
'''



v2_mayavi2(True)











