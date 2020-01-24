#!/usr/bin/python

import numpy as np
import random, itertools, collections

from math import atan2
from math import degrees
from scipy.spatial import Delaunay
from scipy.spatial import ConvexHull

from interLine import interLine
from perpBisector2d import perpBisector2d

"""
Input:
    seeds: Voronoi seed points
    bnd: Boundary

Output:
    cells: Voronoi polygons
"""
def voronoi(seeds,bnd):

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
    cells = [ [] for seed in seeds]
    for j in range(len(mylistA)):
        Atmp = np.concatenate((mylistA[j],Abnd))
        btmp = np.concatenate((mylistb[j].transpose(),-bbnd))
        combinations = itertools.combinations(range(Atmp.shape[0]),2)
        for tupl in combinations:
            lineA = [Atmp[tupl[0]][0,0],Atmp[tupl[0]][0,1],btmp[tupl[0]][0,0]]
            lineB = [Atmp[tupl[1]][0,0],Atmp[tupl[1]][0,1],btmp[tupl[1]][0,0]]
            output = interLine(lineA,lineB)
            if type(output) != type(False):
                if (np.round(np.dot(Atmp,output),6)<=np.round(btmp.transpose(),6)).all():
                   if not any((output == x).all() for x in cells[j]):
                        cells[j].append(output)
        cells[j] = np.asarray(counterClockwise(seeds[j], cells[j]))
    cells = np.asarray(cells)


    return cells

# Arrange the vertices of a cell in counterclockwise order
def counterClockwise(seed,cell):
    vertex_radians = [atan2(vertex[1]-seed[1], vertex[0]-seed[0]) for vertex in cell]
    scell = [vertex for _,vertex in sorted(zip(vertex_radians,cell))]
    return scell