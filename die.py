#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:35:46 2020

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


runfile('/home/cfillmor/topology/medial/medial_axis_approx.py')
pts, pt_cols, dpts, tris2, poles = approx_medial_axis('/home/cfillmor/topology/medial/pt_sets/boro_torus_1000.json', 35, 0, False)

tris2 = np.array([list(i) for i in tris2 if len(i)==3], dtype=np.int32)
dpts = np.array(dpts,dtype='f')


display = (800,600)
pygame.init()
screen = pygame.display.set_mode(display, pygame.OPENGL|pygame.DOUBLEBUF)

gluPerspective(45, (display[0]/display[1]), 0.001, 100.0)

glTranslatef(0.0, 0.0, -5)

glRotatef(0, 0, 0, 0)
gluLookAt(42, 42, 42, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

#Create the VBO
#vertices = np.array([[0,1,0],[-1,-1,0],[1,-1,0]], dtype='f')
vertexPositions = vbo.VBO(dpts, target=GL_ARRAY_BUFFER)
#vertexPositions = vbo.VBO(verts, target=GL_ARRAY_BUFFER)

#Create the index buffer object
#indices = np.array([[0,1,2]], dtype=np.int32)
indexPositions = vbo.VBO(tris2, target=GL_ELEMENT_ARRAY_BUFFER)
#indexPositions = vbo.VBO(TRIS, target=GL_ELEMENT_ARRAY_BUFFER)

glEnable(GL_DEPTH_TEST)
glDepthMask(GL_TRUE)
glDepthFunc(GL_LESS)
glDepthRange(0.0, 1.0)

glLineWidth(5)

#glBindVertexArray(0)
pygame.time.wait(100)

                
glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
#glRotatef(2, 2, 2, 1)

indexPositions.bind()
vertexPositions.bind()


glEnableVertexAttribArray(0);
glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
glColor3fv([0.45,0.45,0.45])

glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
#glDrawArrays(GL_TRIANGLES, 0, 3) #This line still works
glDrawElements(GL_TRIANGLES, len(tris2.flatten()), GL_UNSIGNED_INT, None) #This line does work too!
#glDrawElements(GL_TRIANGLES, len(TRIS.flatten()), GL_UNSIGNED_INT, None) #This line does work too!


glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
glColor3fv([0.,1.,0.])
glDrawElements(GL_TRIANGLES, len(tris2.flatten()), GL_UNSIGNED_INT, None)
#glDrawElements(GL_TRIANGLES, len(TRIS.flatten()), GL_UNSIGNED_INT, None)
# Show the screen
pygame.display.flip()
pygame.time.wait(4)












