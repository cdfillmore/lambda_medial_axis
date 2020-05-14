#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 18:09:31 2020

@author: cfillmor
"""

from OpenGL.GL import shaders
from OpenGL.arrays import vbo
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray

import pygame

import numpy as np
import itertools as it

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
    

def run():
    
    
    
    runfile('/home/cfillmor/topology/medial/medial_axis_approx.py')
    pts, pt_cols, dpts, tris2, poles = approx_medial_axis('/home/cfillmor/topology/medial/pt_sets/hopf_torus_500.json', 30, 0, False)
    
    tris2 = np.array([list(i) for i in tris2 if len(i)==3], dtype=np.int32)
    tris = np.array([dpts[list(tri)] for tri in tris2])
    tris3 = tris.flatten()
    
    col_dict = {'red':[1.,0.,0.], 'green':[0.,0.,1.], 'blue':[0.,1.,0.]}
    pt_colours = np.array([col_dict[i] for i in pt_cols])
    colours = [[254/255, 0., 0.], [75/255, 75/255, 75/255], [255/255, 255/255, 100/250]]
    #colours = [[254/255, 0., 0.], [255/255, 255/255, 100/255.], [0/255, 0/255, 0/255]]
    dpts = np.array(dpts,dtype='f')
    
    
    
    
    
    
    
    
    
    
    #'''
    test = [[j for j in it.permutations(i)] for i in it.combinations_with_replacement([-1,1],3)]
    verts = set([])
    for i in test:
        verts.update(i)
    verts = np.array([list(i) for i in verts], dtype='f')
    #print(verts)
    
    tris = np.array([i for i in it.combinations([i for i,j in enumerate(verts)],3)], dtype=np.int32)
    #'''
    
    
    
    
    
    display = (800,600)
    pygame.init()
    screen = pygame.display.set_mode(display, pygame.OPENGL|pygame.DOUBLEBUF)
    
    gluPerspective(45, (display[0]/display[1]), 0.001, 100.0)
    
    glTranslatef(0.0, 0.0, -5)
    
    glRotatef(0, 0, 0, 0)
    gluLookAt(42, 42, 42, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    #Create the VBO
    vertices = np.array([[0,1,0],[-1,-1,0],[1,-1,0]], dtype='f')
    #vertexPositions = vbo.VBO(dpts)
    vertexPositions = vbo.VBO(vertices)
    
    #Create the index buffer object
    indices = np.array([[0,1,2]], dtype=np.int32)
    #indexPositions = vbo.VBO(tris2, target=GL_ELEMENT_ARRAY_BUFFER)
    indexPositions = vbo.VBO(indices, target=GL_ELEMENT_ARRAY_BUFFER)
    
    glEnable(GL_DEPTH_TEST)
    glDepthMask(GL_TRUE)
    glDepthFunc(GL_LESS)
    glDepthRange(0.0, 1.0)
    
    glLineWidth(5)
    
    #The draw loop
    while True:
        for event in pygame.event.get():
            mouseMove(event)
            if event.type == pygame.QUIT:
                end = True
                pygame.quit()
                #sys.exit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == 113:
                    end = True
                    pygame.quit()
                    #sys.exit()
                    quit()
                    
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #glRotatef(2, 2, 2, 1)
        
        indexPositions.bind()
        vertexPositions.bind()
        
        glEnableVertexAttribArray(0);
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        glColor3fv([0.45,0.45,0.45])
    
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        #glDrawArrays(GL_TRIANGLES, 0, 3) #This line still works
        #glDrawElements(GL_TRIANGLES, len(tris2.flatten()), GL_UNSIGNED_INT, None) #This line does work too!
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None) #This line does work too!
        
        
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        glColor3fv([0.,1.,0.])
        #glDrawElements(GL_TRIANGLES, len(tris2.flatten()), GL_UNSIGNED_INT, None)
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None)
        # Show the screen
        pygame.display.flip()

run()