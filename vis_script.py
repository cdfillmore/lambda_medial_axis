#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 13:05:31 2020

@author: cfillmor
"""

from medial_axis_approx import approx_medial_axis2, approx_medial_axis, write_obj
from stupid_opengl import run2



waiter = 0.4
#run(pts, dtris, pt_cols, dpts, tris2, poles)


####################### Choose your triangulation

pts, dtris, vpts, faces = approx_medial_axis2('/home/cfillmor/topology/medial/pt_sets/' + 'boro_torus_1000' + '.json', 30, 0, 1, 1.5, True)
'''
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









################ run visualisation


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





################ write .obj file for blender
write_obj("./out.obj", vpts, faces)
