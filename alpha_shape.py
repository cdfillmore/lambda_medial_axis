#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 15:22:06 2020

@author: cfillmor
"""

import numpy as np
import itertools as it
import scipy.spatial as spa
import json


def circumsphere_3d_2(pointsf):
    '''Circumsphere of 2 points.
    Args:
        A list of the 2 input points.
    Returns:
        Pair of circumcenter and circumradius.
    '''

    points = np.array(pointsf)
    return list((points[0] + points[1]) / 2.0), \
           np.linalg.norm((points[0] - points[1]) / 2.0)

def circumsphere_3d_3(pointsf):
    '''Circumsphere of 3 points.
    Args:
        A list of the 3 input points.
    Returns:
        Pair of circumcenter and circumradius.
    '''

    points = np.array(pointsf)

    d1 = points[1] - points[0]
    d2 = points[2] - points[0]

    # compute normal vector
    n = normal([d1,d2])

    # Make system of 3 equations to solve for.
    # Third equation is: Circumcenter should be orthogonal to normal.
    genmat = np.array([d1, d2, n])
    normvec = np.array([np.linalg.norm(genmat[0])**2, 
                        np.linalg.norm(genmat[1])**2, 
                        0])
    # 0-based circumsphere is the solution to this equation system.
    cc = np.linalg.solve(2*genmat, normvec)

    return list(cc + points[0]), np.linalg.norm(cc)

def circumsphere_3d_4(pointsf):
    '''Circumsphere of 4 points.
    Args:
        A list of the 4 input points.
    Returns:
        Pair of circumcenter and circumradius.
    '''

    points = np.array(pointsf)

    # generator matrix D: Contains (as rows) the three direction vectors of
    # the tetrahedron spanned by the points with the first point as origin.
    genmat = np.array([points[i] - points[0] for i in range(1,4)])

    # vector n containing the square norms of the 3 vectors from genmat.
    normvec = np.array([np.linalg.norm(genmat[i])**2 for i in range(3)])

    # 0-based circumsphere is the solution x to 2Dx = n
    cc = np.linalg.solve(2*genmat, normvec)

    # Return translated circumcenter and 
    return list(cc + points[0]), np.linalg.norm(cc)

def circumsphere_3d(points):
    npoints = len(points)
    if npoints == 0:
        return None, 0
    elif npoints == 1:
        return points[0], 0
    elif npoints == 2:
        return circumsphere_3d_2(points)
    elif npoints == 3:
        return circumsphere_3d_3(points)
    elif npoints == 4:
        return circumsphere_3d_4(points)
    else:
        raise ValueError("Cannot have {} points on a sphere.".format(npoints))


def alpha(delaunay):
    simps = delaunay.simplices
    rads = [circumsphere_3d(i)[1] for i in delaunay.points[delaunay.simplices]]
    filt = sorted([(j,i) for i,j in enumerate(rads)])
    
    
    
    
    
    













#compute Alpha filtration values and intervals for current Delaunay triangulation
void Alpha_Complex::computeAlphaComplex()
{
    #initialize lists storing informations about simplices
    in_complex = std::vector<bool>(simplices.size(),false)
    filtration_values = std::vector<exact>(simplices.size(),-1)
    critical = std::vector<bool>(simplices.size(),true)
    interval_faces = std::vector<std::vector<int> >(simplices.size(),std::vector<int>(0))
    included = std::vector<bool>(simplices.size(),false)
    excluded = std::vector<bool>(simplices.size(),false)
    
    #compute Delaunay radius function values for all simplices, higher-dimensional ones first
    #----------------------------------------------------------------------------------------
    #compute Alpha for every tetrahedron
    for(std::vector<Simplex>::iterator it = simplices.begin() it<simplices.end() ++it){
        if((*it).getDim()==3){
            computeDelaunayRadius(&(*it),false,false)
        }
    }
    
    #compute Alpha for every triangle
    for(std::vector<Simplex>::iterator it = simplices.begin() it<simplices.end() ++it){
        if((*it).getDim()==2){
            computeDelaunayRadius(&(*it),false,false)
        }
    }       
    
    #if tetrahedron has two triangles in same interval, also common edge has to belong to interval
    #if it has three triangles in same interval, also  common point and 3 edges belong to (0,3)-interval (size 8)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    for(std::vector<Simplex>::iterator it = simplices.begin() it<simplices.end() ++it){
        if((*it).getDim()==3){
            Simplex tetrahedron = *it
            if(!(tetrahedron.isDeleted())){
                std::vector<int> tetra_interval_faces = interval_faces[tetrahedron.getIndex()]
                if(tetra_interval_faces.size()==2){
                    Simplex triangle1 = simplices[tetra_interval_faces[0]]
                    Simplex triangle2 = simplices[tetra_interval_faces[1]]
                    std::vector<int> triangle2_edges = triangle2.getFacetIndices()
                    int common_edge_index
                    std::vector<int> triangle1_edges = triangle1.getFacetIndices()
                    for(std::vector<int>::iterator it2 = triangle1_edges.begin() it2<triangle1_edges.end() ++it2){
                        common_edge_index = *it2 
                        if(common_edge_index == triangle2_edges[0]  or  common_edge_index == triangle2_edges[1]  or  common_edge_index == triangle2_edges[2]){
                            break
                        }               
                    }
                    #set common edge of two interval triangles to be in interval as well
                    critical[common_edge_index]=false
                    exact edgeradius2 = filtration_values[tetrahedron.getIndex()]
                    filtration_values[common_edge_index]=edgeradius2
                    filtration_current.appendElement(edgeradius2,common_edge_index) 
                    #add edge to interval faces of tetrahedron
                    interval_faces[it->getIndex()].push_back(common_edge_index)
                    critical[it->getIndex()]=false
                }else if(tetra_interval_faces.size()==3){
                    Simplex triangle1 = simplices[tetra_interval_faces[0]]
                    Simplex triangle2 = simplices[tetra_interval_faces[1]]
                    Simplex triangle3 = simplices[tetra_interval_faces[2]]
                    int common_point_index = triangle1.getVertex(0)
                    if(!triangle2.hasVertex(common_point_index) or !triangle3.hasVertex(common_point_index)){
                        common_point_index = triangle1.getVertex(1)
                        if(!triangle2.hasVertex(common_point_index) or !triangle3.hasVertex(common_point_index)){
                            common_point_index = triangle1.getVertex(2)
                            if(!triangle2.hasVertex(common_point_index) or !triangle3.hasVertex(common_point_index)){
                                std::cerr << "Error(Alpha_Complex::setPoints): no common point found in (0,3)-interval" << std::endl
                                continue
                            }
                        }
                    }
                    #triangle edges that have common point as vertex are in interval
                    std::set<int> interval_edges_ind
                    std::vector<int> triangle_edges = triangle1.getFacetIndices()
                    for(int i=0 i<triangle_edges.size() i++){
                        if(simplices[triangle_edges[i]].hasVertex(common_point_index)){
                            interval_edges_ind.insert(triangle_edges[i])
                        }
                    }
                    triangle_edges = triangle2.getFacetIndices()
                    for(int i=0 i<triangle_edges.size() i++){
                        if(simplices[triangle_edges[i]].hasVertex(common_point_index)){
                            interval_edges_ind.insert(triangle_edges[i])
                        }
                    }
                    #we do not need to check triangle3, shares relevant edges with other two triangles
                    #mark edges as noncritical, add to interval faces of tetrahedron
                    for(std::set<int>::iterator it2 = interval_edges_ind.begin() it2 != interval_edges_ind.end() ++it2){
                        int edge_index = (*it2)
                        critical[edge_index]=false
                        exact edgeradius2 = filtration_values[tetrahedron.getIndex()]
                        filtration_values[edge_index]=edgeradius2
                        filtration_current.appendElement(edgeradius2,edge_index) 
                        #add edge to interval faces of tetrahedron
                        interval_faces[it->getIndex()].push_back(edge_index)
                        critical[it->getIndex()]=false
                    }
                    #mark common point as noncritical, add as interval face of tetrahedron
                    critical[data_points_simplex_indices[common_point_index]]=false
                    exact pointradius2 = filtration_values[tetrahedron.getIndex()]
                    filtration_values[data_points_simplex_indices[common_point_index]]=pointradius2
                    
                    filtration_current.appendElement(pointradius2,data_points_simplex_indices[common_point_index])
                    #add point to interval faces of triangle
                    interval_faces[it->getIndex()].push_back(data_points_simplex_indices[common_point_index])
                    critical[it->getIndex()]=false
                }
            }
        }
    }
        
    #compute Alpha for every edge
    for(std::vector<Simplex>::iterator it = simplices.begin() it<simplices.end() ++it){
        Simplex edge = *it
        if(edge.getDim()==1){
            if(critical[edge.getIndex()]){ #edge was not already put in interval of size 4
                computeDelaunayRadius(&(*it),false,false)
            }
        }
    } 

    #if triangle has two edges in same interval, also common point has to belong to interval
    for(std::vector<Simplex>::iterator it = simplices.begin() it != simplices.end() ++it){
        Simplex triangle = *it
        if(triangle.getDim()==2){
            if(!(triangle.isDeleted())){
                std::vector<int> interval_faces_triangle = interval_faces[triangle.getIndex()]
                if(interval_faces_triangle.size()==2){
                    Simplex edge1 = simplices[interval_faces_triangle[0]]
                    Simplex edge2 = simplices[interval_faces_triangle[1]]
                    int common_point_index = edge1.getVertex(0)
                    if(common_point_index!=edge2.getVertex(0) && common_point_index!=edge2.getVertex(1)){
                        common_point_index = edge1.getVertex(1)
                        if(common_point_index!=edge2.getVertex(0) && common_point_index!=edge2.getVertex(1)){
                            std::cerr << "Error(Alpha_Complex::setPoints): no common point found in (0,2)-interval" << std::endl
                            continue
                        }
                    }
                    #set common point of two interval edges to be noncritical, add as interval face of triangle
                    critical[data_points_simplex_indices[common_point_index]]=false
                    exact pointradius2 = filtration_values[triangle.getIndex()]
                    filtration_values[data_points_simplex_indices[common_point_index]]=pointradius2
                    filtration_current.appendElement(pointradius2,data_points_simplex_indices[common_point_index])
                    #add point to interval faces of triangle
                    interval_faces[triangle.getIndex()].push_back(data_points_simplex_indices[common_point_index])
                    critical[triangle.getIndex()]=false
                }
            }
        }
    }

    #compute Alpha for every point
    for(int i=0 i<data_points->size() i++){
        if(!(data_points->at(i)).isHidden()){
            if(critical[data_points_simplex_indices[i]]){
                computeDelaunayRadius(&simplices[data_points_simplex_indices[i]],false,false)
            }
        }
    }
    
    #store pointers to lists
    critical_ptr = &critical
    
    #sort filtration simplices
    filtration_current.sort(&simplices,&critical,&included,&inclusion_values_and_counter)
    
}