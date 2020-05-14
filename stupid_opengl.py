#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 13:45:58 2020

@author: cfillmor
"""
from medial_axis_approx import approx_medial_axis2, approx_medial_axis
from georg_miniball3d import circumsphere_3d

from OpenGL.GL import shaders
from OpenGL.arrays import vbo
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, glBindVertexArray

import pygame

from scipy.spatial import Delaunay

import numpy as np
import itertools as it

from ctypes import *
import sys
import math
import time

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
        
        try:
            mouseState = pygame.mouse.get_pressed()
        except:
            return
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

def write_obj(fname, V, F):
    F = [[v + 1 for v in f] for f in F]
    with open(fname, 'w') as fout:
        fout.write('\n'.join('v ' + ' '.join(list(map(str, v))) for v in V) + '\n')
        fout.write('\n'.join('f ' + ' '.join(list(map(str, f))) for f in F) + '\n')

def drawer(indexPositions, vertexPositions, surfaceDexPositions, surfacePositions, surfaceTriPositions, surfacePositions2, pts, dtris, tris2, draw_surface, draw_medial):
    
    if draw_surface == 0:
        surfaceDexPositions.bind()
        surfacePositions.bind()
        
    elif draw_surface == 1:
        surfaceDexPositions.bind()
        surfacePositions.bind()
    
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        glColor3fv([30/255,145/255,188/255])
        glPolygonMode(GL_FRONT_AND_BACK,GL_POINT)
        glDrawElements(GL_POINTS, len(pts), GL_UNSIGNED_INT, None) #This line does work too!
        
        surfaceDexPositions.unbind()
        surfacePositions.unbind()

    elif draw_surface == 2:
        surfaceTriPositions.bind()
        surfacePositions2.bind()
        
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        
        glColor3fv([30/255,145/255,188/255])
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        glDrawElements(GL_TRIANGLES, len(surfaceTriPositions.flatten()), GL_UNSIGNED_INT, None) #This line does work too!
        
        glColor3fv([1.,1.,1.0])
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        glDrawElements(GL_TRIANGLES, len(surfaceTriPositions.flatten()), GL_UNSIGNED_INT, None) #This line does work too!
        
        surfaceTriPositions.unbind()
        surfacePositions2.unbind()
    
    if draw_medial == 0:
        indexPositions.bind()
        vertexPositions.bind()
    elif draw_medial == 2:
        indexPositions.bind()
        vertexPositions.bind()
        
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        #glColor3fv([0.45,0.45,0.45])
        #glColor3fv([0.,0.,0.])
        glColor3fv([0.,0.,0.])
        #glDrawArrays(GL_TRIANGLES, 0, 3) #This line still works
        glDrawElements(GL_TRIANGLES, len(tris2.flatten()), GL_UNSIGNED_INT, None) #This line does work too!
        #glDrawElements(GL_TRIANGLES, len(TRIS.flatten()), GL_UNSIGNED_INT, None) #This line does work too!
    
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        #glColor3fv([0.,1.,0.])
        glColor3fv([225/255, 132/255, 173/255])
        glDrawElements(GL_TRIANGLES, len(tris2.flatten()), GL_UNSIGNED_INT, None)
        #glDrawElements(GL_TRIANGLES, len(TRIS.flatten()), GL_UNSIGNED_INT, None)
    else:
        indexPositions.bind()
        vertexPositions.bind()
        
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        
        glPolygonMode(GL_FRONT_AND_BACK,GL_POINT)
        #glColor3fv([0.45,0.45,0.45])
        glColor3fv([0.,0.,0.])
        #glDrawArrays(GL_TRIANGLES, 0, 3) #This line still works
        #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        glColor3fv([225/255, 132/255, 173/255])
        glDrawElements(GL_TRIANGLES, len(tris2.flatten()), GL_UNSIGNED_INT, None)   
    
    indexPositions.unbind()
    vertexPositions.unbind()

def run(pts, dtris, pt_cols, dpts, tris2, poles):
    
    tris2 = np.array([list(i) for i in tris2 if len(i)==3], dtype = np.int32)
    dpts = np.array(dpts,dtype='f')
    
    pts = np.array(pts,dtype='f')
    indices = np.array([[i] for i,j in enumerate(pts)], dtype = np.int32)
    
    
    display = (1920,1080)
    pygame.init()
    screen = pygame.display.set_mode(display, pygame.OPENGL|pygame.DOUBLEBUF)
    
    gluPerspective(45, (display[0]/display[1]), 0.001, 100.0)
    
    glTranslatef(0.0, 0.0, -5)
    
    glRotatef(0, 0, 0, 0)
    gluLookAt(42, 42, 42, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    
    surfacePositions = vbo.VBO(pts, target=GL_ARRAY_BUFFER)
    surfaceDexPositions = vbo.VBO(indices, target=GL_ELEMENT_ARRAY_BUFFER)
    surfaceDexPositions.bind()
    surfacePositions.bind()
    surfaceDexPositions.unbind()
    surfacePositions.unbind()
    
    surfacePositions2 = vbo.VBO(pts, target=GL_ARRAY_BUFFER)
    surfaceTriPositions = vbo.VBO(dtris, target=GL_ELEMENT_ARRAY_BUFFER)
    surfaceTriPositions.bind()
    surfacePositions2.bind()
    surfaceTriPositions.unbind()
    surfacePositions.unbind()
    
    #Create the VBO
    #vertices = np.array([[0,1,0],[-1,-1,0],[1,-1,0]], dtype='f')
    vertexPositions = vbo.VBO(dpts, target=GL_ARRAY_BUFFER)
    #vertexPositions = vbo.VBO(verts, target=GL_ARRAY_BUFFER)
    
    #Create the index buffer object
    #indices = np.array([[0,1,2]], dtype=np.int32)
    indexPositions = vbo.VBO(tris2, target=GL_ELEMENT_ARRAY_BUFFER)
    #indexPositions = vbo.VBO(TRIS, target=GL_ELEMENT_ARRAY_BUFFER)
    
    indexPositions.bind()
    vertexPositions.bind()
    indexPositions.unbind()
    vertexPositions.unbind()
    
    '''
    #lighting junk
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [-100,-100,-100,0.])
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, [100,100,100,0.])
    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_BLEND)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    '''
    
    glEnable(GL_DEPTH_TEST)
    glDepthMask(GL_TRUE)
    glDepthFunc(GL_LESS)
    glDepthRange(0.0, 1.0)
    
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    
    glLineWidth(5)
    glPointSize(3)
    
    
    breaker = False
    rotater = 0
    draw_surface = 1
    draw_medial = 1
    
    #The draw loop
    while True:
        for event in pygame.event.get():
            mouseMove(event)
            if event.type == pygame.QUIT:
                end = True
                pygame.display.quit()
                #sys.exit()
                #quit()
                breaker = True
            if event.type == pygame.KEYDOWN:
                if event.key == 113:
                    end = True
                    pygame.display.quit()
                    #sys.exit()
                    #quit()
                    breaker = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rotater = (rotater + 1) % 2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    draw_surface = (draw_surface + 1) % 3
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    draw_medial= (draw_medial + 1) % 3
        
        if breaker:
            break
        #glClearColor(1., 1., 1., 0.0)
        glClearColor(0., 0., .15, 0.0)
        glClearDepth(1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        if rotater:
            glRotatef(1, 2, 3, 1)
        
        #lighting junk
        
        drawer(indexPositions, vertexPositions, surfaceDexPositions, surfacePositions, surfaceTriPositions, surfacePositions2, pts, dtris, tris2, draw_surface, draw_medial)
        
        
        # Show the screen
        pygame.display.flip()
        pygame.time.wait(10)


def drawer2(indexPositions, vertexPositions, surfaceDexPositions, surfacePositions, surfaceTriPositions, surfacePositions2, pts, dtris, faces, draw_surface, draw_medial):
    
    if draw_surface == 0:
        surfaceDexPositions.bind()
        surfacePositions.bind()
        surfaceDexPositions.unbind()
        surfacePositions.unbind()
        
    elif draw_surface == 1:
        surfaceDexPositions.bind()
        surfacePositions.bind()
    
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        glColor3fv([30/255,145/255,188/255])
        glPolygonMode(GL_FRONT_AND_BACK,GL_POINT)
        glDrawElements(GL_POINTS, len(pts), GL_UNSIGNED_INT, None) #This line does work too!
        
        surfaceDexPositions.unbind()
        surfacePositions.unbind()

    elif draw_surface == 2:
        surfaceTriPositions.bind()
        surfacePositions2.bind()
        
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        
        glColor3fv([30/255,145/255,188/255])
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        glDrawElements(GL_TRIANGLES, len(surfaceTriPositions.flatten()), GL_UNSIGNED_INT, None) #This line does work too!
        
        glColor3fv([0.,0.,0.])
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        glDrawElements(GL_TRIANGLES, len(surfaceTriPositions.flatten()), GL_UNSIGNED_INT, None) #This line does work too!
        
        surfaceTriPositions.unbind()
        surfacePositions2.unbind()
        
    if draw_medial == 0:
        indexPositions.bind()
        vertexPositions.bind()
    elif draw_medial == 2:
        indexPositions.bind()
        vertexPositions.bind()
        
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        #glColor3fv([0.45,0.45,0.45])
        #glColor3fv([0.,0.,0.])
        glColor3fv([0.7,.3,0.2])
        #glDrawArrays(GL_TRIANGLES, 0, 3) #This line still works
        glDrawElements(GL_TRIANGLES, sum([len(i) for i in faces]), GL_UNSIGNED_INT, None) #This line does work too!
        #glDrawElements(GL_TRIANGLES, len(TRIS.flatten()), GL_UNSIGNED_INT, None) #This line does work too!
    
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        glColor3fv([0.,0.,0.])
        #glColor3fv([225/255, 132/255, 173/255])
        glDrawElements(GL_TRIANGLES, sum([len(i) for i in faces]), GL_UNSIGNED_INT, None)
        #glDrawElements(GL_TRIANGLES, len(TRIS.flatten()), GL_UNSIGNED_INT, None)
    else:
        indexPositions.bind()
        vertexPositions.bind()
        
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        
        glPolygonMode(GL_FRONT_AND_BACK,GL_POINT)
        #glColor3fv([0.45,0.45,0.45])
        glColor3fv([0.,0.,0.])
        #glDrawArrays(GL_TRIANGLES, 0, 3) #This line still works
        #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        #glColor3fv([225/255, 132/255, 173/255])
        glColor3fv([0.7,.3,0.15])
        glDrawElements(GL_TRIANGLES, sum([len(i) for i in faces]), GL_UNSIGNED_INT, None)   
    
    indexPositions.unbind()
    vertexPositions.unbind()

def run2(pts, dtris, vpts, faces):
    
    #faces = np.array([np.array(i, dtype = np.int32) for i in faces])
    faces = np.array(faces, dtype=np.int32)
    #faces = np.array([faces[1900]], dtype = np.int32)
    vpts = np.array(vpts,dtype='f')
    
    pts = np.array(pts,dtype='f')
    indices = np.array([[i] for i,j in enumerate(pts)], dtype = np.int32)
    
    
    display = (1920,1080)
    pygame.init()
    screen = pygame.display.set_mode(display, pygame.OPENGL|pygame.DOUBLEBUF)
    
    gluPerspective(45, (display[0]/display[1]), 0.001, 100.0)
    
    glTranslatef(0.0, 0.0, -5)
    
    glRotatef(0, 0, 0, 0)
    gluLookAt(42, 42, 42, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    
    surfacePositions = vbo.VBO(pts, target=GL_ARRAY_BUFFER)
    surfaceDexPositions = vbo.VBO(indices, target=GL_ELEMENT_ARRAY_BUFFER)
    surfaceDexPositions.bind()
    surfacePositions.bind()
    surfaceDexPositions.unbind()
    surfacePositions.unbind()
    
    surfacePositions2 = vbo.VBO(pts, target=GL_ARRAY_BUFFER)
    surfaceTriPositions = vbo.VBO(dtris, target=GL_ELEMENT_ARRAY_BUFFER)
    surfaceTriPositions.bind()
    surfacePositions2.bind()
    surfaceTriPositions.unbind()
    surfacePositions.unbind()
    
    #Create the VBO
    #vertices = np.array([[0,1,0],[-1,-1,0],[1,-1,0]], dtype='f')
    vertexPositions = vbo.VBO(vpts, target=GL_ARRAY_BUFFER)
    #vertexPositions = vbo.VBO(verts, target=GL_ARRAY_BUFFER)
    
    #Create the index buffer object
    #indices = np.array([[0,1,2]], dtype=np.int32)
    indexPositions = vbo.VBO(faces, target=GL_ELEMENT_ARRAY_BUFFER)
    #indexPositions = vbo.VBO(TRIS, target=GL_ELEMENT_ARRAY_BUFFER)
    
    indexPositions.bind()
    vertexPositions.bind()
    indexPositions.unbind()
    vertexPositions.unbind()
    
    '''
    #lighting junk
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [-100,-100,-100,0.])
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, [100,100,100,0.])
    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_BLEND)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    '''
    
    glEnable(GL_DEPTH_TEST)
    glDepthMask(GL_TRUE)
    glDepthFunc(GL_LESS)
    glDepthRange(0.0, 1.0)
    
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    
    glLineWidth(5)
    glPointSize(3)
    
    
    breaker = False
    rotater = 0
    draw_surface = 1
    draw_medial = 1
    
    #The draw loop
    while True:
        for event in pygame.event.get():
            mouseMove(event)
            if event.type == pygame.QUIT:
                end = True
                pygame.display.quit()
                #sys.exit()
                #quit()
                breaker = True
            if event.type == pygame.KEYDOWN:
                if event.key == 113:
                    end = True
                    pygame.display.quit()
                    #sys.exit()
                    #quit()
                    breaker = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rotater = (rotater + 1) % 2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    draw_surface = (draw_surface + 1) % 3
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    draw_medial= (draw_medial + 1) % 3
        
        if breaker:
            break
        #glClearColor(1., 1., 1., 0.0)
        glClearColor(0., 0., .25, 0.0)
        glClearDepth(1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        if rotater:
            glRotatef(1/2, 2/2, 3/2, 1)
        
        #lighting junk
        
        drawer2(indexPositions, vertexPositions, surfaceDexPositions, surfacePositions, surfaceTriPositions, surfacePositions2, pts, dtris, faces, draw_surface, draw_medial)
        
        
        # Show the screen
        #print('hi')
        pygame.display.flip()
        pygame.time.wait(10)



#pts, pt_cols, dpts, tris2, poles = approx_medial_axis('/home/cfillmor/topology/medial/pt_sets/' + 'boro_torus_10000' + '.json', 21, 0, False)

#run('L10a140_plane_5000', 30 ,5)
#run('mobius_10000', 30, 0)
#run('boro_torus_10000', 21, 0)
#run('boro_plane_10000', 30, 5)




waiter = 0.4
#run(pts, dtris, pt_cols, dpts, tris2, poles)


'''

pts, dtris, vpts, faces = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'boro_torus_1000' + '.json', 30, 0, 1, 1.5, True)
pts2, dtris2, vpts2, faces2 = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'knot_torus_1000' + '.json', 15, 0, .5, .5, True)
pts3, dtris3, vpts3, faces3 = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'mobius_3000' + '.json', 60, 0, 10, 5, True)
pts4, dtris4, vpts4, faces4 = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'hopf_torus_1000' + '.json', 30, 0, 5, 4, True)
pts5, dtris5, vpts5, faces5 = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'genus_2_1000' + '.json', 30, 0, 5, 3, True)



pts6, dtris6, vpts6, faces6 = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'knot_2_3_1000' + '.json', 30, 0, 5, 3, True)
pts7, dtris7, vpts7, faces7 = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'knot_2_5_1000' + '.json', 30, 0, 5, 3, True)
pts8, dtris8, vpts8, faces8 = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'knot_3_5_1000' + '.json', 30, 0, 5, 3, True)

run2(pts, dtris, vpts, faces)                 #borromean
time.sleep(waiter)
run2(pts2, dtris2, vpts2, faces2)             #trefoil
time.sleep(waiter)
run2(pts3, dtris3, vpts3, faces3)             #mobius
time.sleep(waiter)
run2(pts4, dtris4, vpts4, faces4)             #hopf link
time.sleep(waiter)
run2(pts5, dtris5, vpts5, faces5)             #dragon
'''

#################################  knots (3,2), (5,2), (4,3), (5,3), (9,2)

#timea = time.time()
#pts, dtris, vpts, faces = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'boro_torus_1000' + '.json', 30, 0, 1, 1.5, True)
'''
pts2, dtris2, vpts2, faces2 = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'knot_torus_1000' + '.json', 15, 0, .5, .5, True)
pts6, dtris6, vpts6, faces6 = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'knot_3_2_3000' + '.json', 15, 0, .5, .5, True)
pts7, dtris7, vpts7, faces7 = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'knot_5_2_3000' + '.json', 15, 0, .5, .5, True)
pts8, dtris8, vpts8, faces8 = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'knot_4_3_3000' + '.json', 15, 0, .5, .5, True)
pts9, dtris9, vpts9, faces9 = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'knot_5_3_3000' + '.json', 15, 0, .5, .5, True)
pts10, dtris10, vpts10, faces10 = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'knot_9_2_3000' + '.json', 15, 0, .5, .5, True)
pts11, dtris11, vpts11, faces11 = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'knot_figure8_3000' + '.json', 15, 0, .45, .45, True)
#timeb = time.time()
#print(timeb - timea)
'''
run2(pts, dtris, vpts, faces)
'''
time.sleep(waiter)
run2(pts2, dtris2, vpts2, faces2)
time.sleep(waiter)
run2(pts6, dtris6, vpts6, faces6)
time.sleep(waiter)
run2(pts7, dtris7, vpts7, faces7)
time.sleep(waiter)
run2(pts8, dtris8, vpts8, faces8)
time.sleep(waiter)
run2(pts9, dtris9, vpts9, faces9)
time.sleep(waiter)
run2(pts10, dtris10, vpts10, faces10)
time.sleep(waiter)
run2(pts11, dtris11, vpts11, faces11)
'''




