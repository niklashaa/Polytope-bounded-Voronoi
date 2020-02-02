#!/usr/bin/python

import numpy as np
import random, itertools, collections

from math import atan2
from math import degrees
from numpy import linalg as la
from scipy.spatial import Delaunay
from scipy.spatial import ConvexHull



def perpBisector2d(v1, v2):
    vm = np.array([(v1[0] + v2[0])/2,(v1[1] + v2[1])/2]) # Mittelpunkt zwischen v1 und v2
    v3 = np.array([v2[0] - v1[0],v2[1]-v1[1]]) # Richtungsvektor v1 -> v2 

    Ad = np.array([v3[0]/ la.norm(v3,2),v3[1]/la.norm(v3,2)]) # Normierter Richtungsvektor
    bd = np.dot(Ad,vm) # Skalarprodukt aus Richtungsvektor und Mittelpunktsvektor

    if np.dot(Ad,v1) <= bd:
        return Ad, bd
    return np.negative(Ad), np.negative(bd)

"""
#lineA = [0.1, 0.2, 0.1]
#lineB = [0.4, -0.2, 0.3]

# A = [[0.1, 0.2], 
#      [0.4, -0.2]]

# b = [[0.1],
#      [0.3]]
"""
def interLine(lineA,lineB):
    if (lineA[0]*lineB[1] - lineB[0]*lineA[1] != 0): # Check if lines are parallel
        A = np.array([[lineA[0],lineA[1]],[lineB[0],lineB[1]]])
        b = np.array([[lineA[2]],[lineB[2]]])
        res = np.dot(la.inv(A),b) # Returns nested matrix
        return np.array([res.item(0),res.item(1)])
    return False

"""
Input:
    seeds: Voronoi seed points
    bnd: Boundary

Output:
    cells: Voronoi polygons
"""
def voronoi(seeds,bnd):

    if seeds.shape[0] == 1:
        return None
    
    if seeds.shape[0] == 2:
        return None

    if all(x == seeds[0,0] for x in seeds[:,0]) or all(x == seeds[0,1] for x in seeds[:,1]):
        raise Exception('seeds have the same value for x or y:\n {}'.format(seeds))

    # Delaunay triangulation
    tri = Delaunay(seeds)

    # find  neighbor indices for each seed point
    neib_inices = [ [] for seed in seeds]
    # iterate over seeds
    for j, seed in enumerate(seeds):
        neib_inices[j]=[]
        # check if simplice contains seed
        for simplex in tri.simplices:
            intersect = np.intersect1d(simplex,j)
            if intersect.size > 0:
                # add points of simplice that are not the seed
                neib_inices[j].append(np.setdiff1d(simplex,j))
        # get rid of duplicates
        neib_inices[j] = np.unique(neib_inices[j])

    # linear equations for the boundary
    bndhull = ConvexHull(bnd)
    bndTmp = bndhull.equations
    bndMat = np.matrix(bndTmp)
    Abnd = bndMat[:,0:2]
    bbnd = bndMat[:,2]

    # find linear equations for perpendicular bisectors
    mylistA = [] # Contains vectors between seeds to their neighbours
    mylistb = [] # Contains dot products of vectors in listA to centre between seeds

    for i, seed in enumerate(seeds):
        A = []
        b = []
        for ind in neib_inices[i]:
            Altmp, bltmp = perpBisector2d(seed,seeds[ind])
            A.append(Altmp)
            b.append(bltmp)
        mylistA.append(np.matrix(A))
        mylistb.append(np.matrix(b))

    # obtain voronoi vertices
    cells = []
    for j in range(len(mylistA)):
        cell = []
        Atmp = np.concatenate((mylistA[j],Abnd))
        btmp = np.concatenate((mylistb[j].transpose(),-bbnd))
        combinations = itertools.combinations(range(Atmp.shape[0]),2)
        for tupl in combinations:
            lineA = [Atmp[tupl[0]][0,0],Atmp[tupl[0]][0,1],btmp[tupl[0]][0,0]]
            lineB = [Atmp[tupl[1]][0,0],Atmp[tupl[1]][0,1],btmp[tupl[1]][0,0]]
            vertex = interLine(lineA,lineB)
            if type(vertex) != type(False):
                if (np.round(np.dot(Atmp,vertex),6)<=np.round(btmp.transpose(),6)).all():
                    if not any((vertex == x).all() for x in cell):
                        cell.append(vertex)
        cell = np.asarray(counterClockwise(seeds[j], cell))
        cells.append(cell)
    return cells

# Arrange the vertices of a cell in counterclockwise order
def counterClockwise(seed,cell):
    vertex_radians = [atan2(vertex[1]-seed[1], vertex[0]-seed[0]) for vertex in cell]
    scell = [vertex for _,vertex in sorted(zip(vertex_radians,cell))]
    return scell