#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 13:16:41 2020

@author: cfillmor
"""

import itertools as it
import numpy as np

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from ctypes import *
import sys
import math

lastPosX = 0
lastPosY = 0
zoomScale = 1.0
dataL = 0
xRot = 0
yRot = 0
zRot = 0

test = [[j for j in it.permutations(i)] for i in it.combinations_with_replacement([-1,1],3)]
verts = set([])
for i in test:
    verts.update(i)
verts = list(verts)
#print(verts)

edges = [i for i in it.combinations(verts,2)]
#print(edges)

def vect(p,q):
    return [ (p[i] - q[i]) for i in range(len(p))]

def dist(p,q):
    return np.sqrt( np.dot(vect(p,q), vect(p,q)) )

def angle(v,w):
    return np.arccos( np.dot(v,w) / (np.sqrt(np.dot(v,v))*np.sqrt(np.dot(w,w) ) ) )

'''
def normal(a, b, c):
    v1 = vect(a, b)
    v2 = vect(a, c)
    theta = angle(v1, v2)
    norm = [v1[1]*v2[2] - v1[2]*v2[1], v1[2]*v2[0] - v1[0]*v2[2], v1[0]*v2[1] - v1[1]*v2[0]]
    print(norm)
    return norm / (np.sqrt(np.dot(norm, norm)))
'''

def normal(a, b, c):
    p1 = np.array(a)
    p2 = np.array(b)
    p3 = np.array(c)

    N = np.cross(p2-p1, p3-p1)
    return N/N.sum()

def cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertex)
    glEnd()


def medial_plot(pts, pt_colours, tris, colours, shading):
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glBegin(GL_POINTS)
    for i in range(len(pts)):
        if False:
            glMaterialfv(GL_FRONT, GL_DIFFUSE, pt_colours[i]+[1.])
        glNormal3d(0., 0., 1.)
        glColor3fv(pt_colours[i])
        glVertex3fv(pts[i])
    glEnd()
        
    glLineWidth(1)
    glBegin(GL_TRIANGLES)
    for tri in tris:
#        if len(tri)<3:
#            continue
        '''
        if shading:
            glMaterialfv(GL_FRONT, GL_DIFFUSE, colours[1]+[1.])
        '''
        norm = normal(tri[0], tri[1], tri[2])
        glNormal3d(norm[0], norm[1], norm[2])
        for vertex in tri:
            glColor3fv(colours[1])
            glVertex3fv(vertex)
    glEnd()
    
    
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    glLineWidth(3)
    glBegin(GL_TRIANGLES)
    for tri in tris:
#        if len(tri)<3:
#            continue
        if False:
            glMaterialfv(GL_FRONT, GL_DIFFUSE, colours[2]+[1.])
        norm = normal(tri[0], tri[1], tri[2])
        glNormal3d(norm[0], norm[1], norm[2])
        for vertex in tri:
            glColor3fv(colours[2])
            glVertex3fv(vertex)
    glEnd()
    
def mouseMove(event):
    global lastPosX, lastPosY, zoomScale, xRot, yRot, zRot
 
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4: # wheel rolled up
        glScaled(1.05, 1.05, 1.05)
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5: # wheel rolled down
        glScaled(0.95, 0.95, 0.95)
 
    if event.type == pygame.MOUSEMOTION:
        x, y = event.pos
        dx = x - lastPosX
        dy = y - lastPosY
        
        mouseState = pygame.mouse.get_pressed()
        if mouseState[0]:

            modelView = (GLfloat * 16)()
            mvm = glGetFloatv(GL_MODELVIEW_MATRIX, modelView)
   
   # To combine x-axis and y-axis rotation
            temp = (GLfloat * 3)()
            temp[0] = modelView[0]*dy + modelView[1]*dx
            temp[1] = modelView[4]*dy + modelView[5]*dx
            temp[2] = modelView[8]*dy + modelView[9]*dx
            norm_xy = math.sqrt(temp[0]*temp[0] + temp[1]*temp[1] + temp[2]*temp[2])
            glRotatef(0.3*math.sqrt(dx*dx+dy*dy), temp[0]/norm_xy, temp[1]/norm_xy, temp[2]/norm_xy)

        lastPosX = x
        lastPosY = y
    

def main1():
    end = False
    runfile('/home/cfillmor/topology/medial/medial_axis_approx.py')
    pts, pt_cols, tris = approx_medial_axis('/home/cfillmor/topology/medial/pt_sets/boro_torus_500.json', 30, 0, False)
    col_dict = {'red':[1.,0.,0.], 'green':[0.,0.,1.], 'blue':[0.,1.,0.]}
    pt_colours = [col_dict[i] for i in pt_cols]
    tris = [i for i in tris if len(i)==3]
    colours = [[254/255, 0., 0.], [50/255, 50/255, 50/255], [255/255, 255/255, 100/250]]
    #colours = [[254/255, 0., 0.], [255/255, 255/255, 100/255.], [0/255, 0/255, 0/255]]
    pygame.init()
    display = (1920, 1080)
    window_width, window_height = display
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL|RESIZABLE)

    gluPerspective(45, (display[0]/display[1]), 0.001, 100.0)
    
    glTranslatef(0.0, 0.0, -5)
    
    glRotatef(0, 0, 0, 0)
    gluLookAt(20, 20, 20, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    #gluLookAt(1, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
    
    glEnable(GL_POINT_SMOOTH)
    glPointSize(5)
    glEnable(GL_LINE_SMOOTH)
    glLineWidth(3000)
    glEnable(GL_POLYGON_SMOOTH)
    
    white = [0.8, 0.8, 0.8, 1.0]
    cyan = [0., .8, .8, 1.]
    shininess = [1]
    
    specular_light = [1.0, 1.0, 0.0, 1.0]
    diffuse_light = [0.4, 0.4, 0.4, 1.0]
    specular_material = [1.0, 1.0, 1.0, 1.0]
    diffuse_material = [1.0, 1.0, 1.0, 1.0]
    
    shading = 0
    if shading:
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
        glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)
        glMaterialfv (GL_FRONT, GL_DIFFUSE, diffuse_material)
        glMaterialfv (GL_FRONT, GL_SPECULAR, specular_material)
        
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_DIFFUSE)
        glColorMaterial(GL_FRONT, GL_SPECULAR)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        #glEnable(GL_NORMALIZE)
        #glLightfv(GL_LIGHT0, GL_DIFFUSE, [-1.0, -1.0, -1.0, .4])
        
        #glMaterialfv(GL_FRONT, GL_DIFFUSE, cyan)
        #glMaterialfv(GL_FRONT, GL_SHININESS, shininess)
    
    glEnable(GL_DEPTH_TEST)
    glDepthMask(GL_TRUE)
    glDepthFunc(GL_LESS)
    glDepthRange(0.0, 1.0)
    
    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    #background_image = pygame.image.load("/home/cfillmor/topology/medial/galaxy.jpeg").convert()
    
    '''
    vbo1 = glGenBuffers(1)
    glBindBuffer (GL_ARRAY_BUFFER, vbo1)
    glBufferData (GL_ARRAY_BUFFER, len(pts)*4, (c_float*len(pts))(*pts), GL_STATIC_DRAW)    
    '''
    while True:
        for event in pygame.event.get():
            mouseMove(event)
            '''
            if event.type == pygame.MOUSEBUTTONDOWN:
                old_x, old_y = pygame.mouse.get_pos()
                #print(x,y)
            if event.type == pygame.MOUSEBUTTONUP:
                new_x, new_y = pygame.mouse.get_pos()
                #print(x,y)
            '''
            if event.type == pygame.QUIT:
                pygame.quit()
                #sys.exit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == 113:
                    end = True
                    pygame.quit()
                    #sys.exit()
                    quit()
            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), DOUBLEBUF|OPENGL|RESIZABLE)
        
        if end:
            return "done"
        
        #screen.blit(background_image, [0, 0])
        #glRotatef(np.random.randint(4), np.random.randint(4), np.random.randint(4), 1)
        #glRotatef(2, 2.5, 1, 1)
        #glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearColor(.35, .35, .35, 0.0)
        glClearDepth(1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        medial_plot(pts, pt_colours, tris, colours, shading)
        #cube()
        pygame.display.flip()
        #pygame.time.wait(0)

main1()




























