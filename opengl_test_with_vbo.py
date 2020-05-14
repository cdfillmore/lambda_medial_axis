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
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

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


def medial_plot(pts, pt_colours, tris, colours):
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glBegin(GL_POINTS)
    for i in range(len(pts)):
        glColor3fv(pt_colours[i])
        glVertex3fv(pts[i])
    glEnd()
        
    glBegin(GL_TRIANGLES)
    for tri in tris:
        for vertex in tri:
            glColor3fv(colours[1])
            glVertex3fv(vertex)
    glEnd()
    
    
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    glBegin(GL_TRIANGLES)
    for tri in tris:
        for vertex in tri:
            glColor3fv(colours[2])
            glVertex3fv(vertex)
    glEnd()
    
def medial_plot2(pts2, pt_colours2, tris3, colours, vbo1, vbo1_ids, vbo2, vbo2_ids, vao2):
    #drawpoints
    
    glBindBuffer(GL_ARRAY_BUFFER, vbo1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vbo1_ids)
    
    
    #enable vertex arrays
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    
    glVertexPointer(3, GL_FLOAT, 0, None)
    glColorPointer(3, GL_FLOAT, 0, len(pts2))
    
    glDrawElements(GL_POINTS, len(pts2), GL_UNSIGNED_BYTE, None)
    #disable vertex arrays
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)

    #unbind VBOs
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    
    ########################################################
    #draw triangles
    '''
    glBindVertexArray(vao2)
    glBindBuffer(GL_ARRAY_BUFFER, vbo2)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vbo2_ids)
    
    #enable vertex arrays
    #glEnableClientState(GL_VERTEX_ARRAY)
    
    #glVertexPointer(3, GL_FLOAT, 0, None)
    glColor3f(1.0, 0.0, 0.0)
    #glDrawElements(GL_TRIANGLES, len(tris3), GL_UNSIGNED_BYTE, None)
    #disable vertex arrays
    #glDisableClientState(GL_VERTEX_ARRAY)

    #unbind VBOs
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    '''
    
def medial_plot3(pts2, pt_colours2, tris3, colours, indexPositions, vertexPositions):
    indexPositions.bind()
    vertexPositions.bind()
    
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
    
    #glDrawArrays(GL_TRIANGLES, 0, 3) #This line still works
    glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_BYTE, None) #This line does work too!
    
    indexPositions.unbind()
    vertexPositions.unbind()
    
    
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
    pts, pt_cols, dpts, tris2 = approx_medial_axis('/home/cfillmor/topology/medial/pt_sets/hopf_torus_500.json', 30, 0, False)
    
    
    tris2 = np.array([list(i) for i in tris2 if len(i)==3])
    tris = np.array([dpts[list(tri)] for tri in tris2])
    tris3 = tris.flatten()
    
    col_dict = {'red':[1.,0.,0.], 'green':[0.,0.,1.], 'blue':[0.,1.,0.]}
    pt_colours = np.array([col_dict[i] for i in pt_cols])
    colours = [[254/255, 0., 0.], [75/255, 75/255, 75/255], [255/255, 255/255, 100/250]]
    #colours = [[254/255, 0., 0.], [255/255, 255/255, 100/255.], [0/255, 0/255, 0/255]]
    pts2 = pts.flatten()
    pt_colours2 = pt_colours.flatten()
    
    
    pygame.init()
    display = (1920, 1080)
    window_width, window_height = display
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL|RESIZABLE)
    
    gluPerspective(45, (display[0]/display[1]), 0.001, 100.0)
    
    glTranslatef(0.0, 0.0, -5)
    
    glRotatef(0, 0, 0, 0)
    gluLookAt(42, 42, 42, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    #gluLookAt(1, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
    
    #glEnable(GL_POINT_SMOOTH)
    glPointSize(5)
    #glEnable(GL_LINE_SMOOTH)
    glLineWidth(5)
    #glEnable(GL_POLYGON_SMOOTH)
    
    glEnable(GL_DEPTH_TEST)
    glDepthMask(GL_TRUE)
    glDepthFunc(GL_LESS)
    glDepthRange(0.0, 1.0)
    
    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    
    #Create the VBO
    vertexPositions = vbo.VBO(dpts, target=GL_ARRAY_BUFFER)
    
    #Create the index buffer object
    #indexPositions = vbo.VBO(np.array([[i] for (i,j) in enumerate(pts)]), target=GL_ELEMENT_ARRAY_BUFFER)
    indexPositions = vbo.VBO(tris2, target=GL_ELEMENT_ARRAY_BUFFER)
    
    
    '''
    #create vertex buffer and ids for point set
    vbo1 = glGenBuffers(1)
    vbo1_ids = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo1)
    glBufferData(GL_ARRAY_BUFFER, len(pts2) + len(pt_colours2), np.append(pts2, pt_colours2), GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vbo1_ids)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(pts), np.array([i for (i,j) in enumerate(pts)]), GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    
    #create vertex buffer and ids for medial axis
    vbo2 = glGenBuffers(1)
    vbo2_ids = glGenBuffers(1)
    vao2 = glGenVertexArrays(1)
    glBindVertexArray(vao2)
    glBindBuffer(GL_ARRAY_BUFFER, vbo2)
    glBufferData(GL_ARRAY_BUFFER, len(dpts), dpts, GL_STATIC_DRAW)
    
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vbo2_ids)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(tris2.flatten()), tris2.flatten(), GL_STATIC_DRAW)
    
    glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    '''
    
    
    
    while True:
        for event in pygame.event.get():
            mouseMove(event)
            if event.type == pygame.QUIT:
                end = True
                pygame.quit()
                #sys.exit()
                #quit()
            if event.type == pygame.KEYDOWN:
                if event.key == 113:
                    end = True
                    pygame.quit()
                    #sys.exit()
                    #quit()
            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), DOUBLEBUF|OPENGL|RESIZABLE)
        
        if end:
            return "done"
        
        #screen.blit(background_image, [0, 0])
        #glRotatef(np.random.randint(4), np.random.randint(4), np.random.randint(4), 1)
        #glRotatef(2, 2.5, 1, 1)
        #glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearColor(.5, .5, .5, 0.0)
        glClearDepth(1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #medial_plot3(pts2, pt_colours2, tris3, colours, indexPositions, vertexPositions)
        
        vertexPositions.bind()
        indexPositions.bind()
        
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        
        #glDrawArrays(GL_TRIANGLES, 0, 3) #This line still works
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_BYTE, None) #This line does work too!
        
        indexPositions.unbind()
        vertexPositions.unbind()
        
        
        #medial_plot2(pts2, pt_colours2, tris3, colours, vbo1, vbo1_ids, vbo2, vbo2_ids, vao2)
        #medial_plot(pts, pt_colours, tris, colours)
        #cube()
        pygame.display.flip()
        #pygame.time.wait(0)

main1()



















