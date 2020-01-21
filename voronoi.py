#!/usr/bin/python

import numpy as np
import random, itertools, collections


from scipy.spatial import Delaunay
from scipy.spatial import ConvexHull

from interLine import interLine
from perpBisector2d import perpBisector2d
from inHull import inHull

"""
Input:
    seeds: Voronoi seed points
    bnd: Boundary

Output:
    seeds: Voronoi seed points
    cells: Voronoi polygons
"""


def voronoi(seeds,bnd):

    if all(x == seeds[0,0] for x in seeds[:,0]) or all(x == seeds[0,1] for x in seeds[:,1]):
        raise Exception('seeds have the same value for x or y:\n {}'.format(seeds))

    # Delaunay triangulation
    tri = Delaunay(seeds)

    # find voronoi neighbors for each generater point
    neibs = [ [] for row in seeds]
    # iterate over seeds
    for j, obj in enumerate(seeds):
        neibs[j]=[]
        i = 0
        # check if simplice contains seed
        for row in tri.simplices:
            i = i + 1
            tmp = np.intersect1d(tri.simplices[i-1],[j])
            if tmp.size !=0:
                # add points of simplice that are not the seed
                neibs[j].append(np.setdiff1d(tri.simplices[i-1],j))
        # get rid of duplicates
        neibs[j] = np.unique(neibs[j])

    # linear equations for the boundary
    bndhull = ConvexHull(bnd)
    bndTmp = bndhull.equations
    bndMat = np.matrix(bndTmp)
    Abnd = bndMat[:,0:2]
    bbnd = bndMat[:,2]

    # find linear equations for perpendicular bisectors
    mylistA = [] # Contains vectors between seeds to their neighbours
    mylistb = [] # Contains dot products of vectors in listA to centre between seeds

    for i, obj in enumerate(seeds):
        A = []
        b = []
        for j in range(0,len(neibs[i])):
            Altmp, bltmp = perpBisector2d(seeds[i],seeds[neibs[i][j]])
            A.append(Altmp)
            b.append(bltmp)
        mylistA.append(np.matrix(A))
        mylistb.append(np.matrix(b))

    # obtain voronoi vertices
    cells = [ [] for row in seeds]
    for j in range(0,len(mylistA)):
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
        cells[j] = np.asarray(cells[j])
    cells = np.asarray(cells)


    return cells
