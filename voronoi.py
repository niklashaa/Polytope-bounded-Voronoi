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
    pins: Voronoi seed points
    bnd: Boundary

Output:
    seeds: Voronoi seed points
    cells: Voronoi polygons
"""


def voronoi(pins,bnd):

        seeds = inHull(pins,bnd)

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
        mylistA = []
        mylistb = []

        for i, obj in enumerate(seeds):
            A = np.array([[0, 0]])
            b = np.array([0])
            for j in range(0,len(neibs[i])):
                Altmp, blt = perpBisector2d(seeds[i],seeds[neibs[i][j]])
                Al = np.array([Altmp])
                bl = np.array([blt])
                A = np.concatenate((A,Al),axis=0)
                b = np.concatenate((b,bl),axis=0)
            Amat = np.matrix(A)
            bmat = np.matrix(b)
            mylistA.append(Amat[1:np.shape(Amat)[0]])
            mylistb.append(bmat[:,1:np.shape(bmat)[1]])

        # obtain voronoi vertices
        cells = [ [] for row in seeds]
        for j in range(0,len(mylistA)):
            Atmp = np.concatenate((mylistA[j],Abnd))
            btmp = np.concatenate((mylistb[j].transpose(),-bbnd))
            k =0
            for comb in list(itertools.combinations(range(1,np.shape(Atmp)[0]+1),2)):
                k = k+1
                if k <= len(list(itertools.combinations(range(1,np.shape(Atmp)[0]+1),2))):
                    lineA = [Atmp[comb[0]-1].item(0,0),Atmp[comb[0]-1].item(0,1),btmp[comb[0]-1].item(0,0)]
                    lineB = [Atmp[comb[1]-1].item(0,0),Atmp[comb[1]-1].item(0,1),btmp[comb[1]-1].item(0,0)]
                    output = interLine(lineA,lineB)
                    if type(output) != type(False):
                        if (np.round(np.dot(Atmp,np.array([output.item(0,0),output.item(1,0)])),7)<=np.round(btmp.transpose(),7)).all():
                           if [output.item(0,0),output.item(1,0)] not in cells[j]:
                                cells[j].append([output.item(0,0),output.item(1,0)])
#            cells[j] = np.asarray(cells[j])
        cells = np.asarray(cells)


        return seeds,cells
