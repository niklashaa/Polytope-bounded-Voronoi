from config import bnd, heighPar, seeds, sigma, X, Y
from functions import allInside, allMoveSafeTowards, gauss_heights, init_phi, plot_voronoi, poly_areas, uCentroids, wCentroids
from voronoi import voronoi

import numpy as np
from sys import maxsize
from matplotlib import path, pyplot as plt

aimax = 10
ai = aimax
stdevs = []
stdevs.append(maxsize)
stepsize = 20 # max stepsize
decFactor = 0.5
minStepsize = 0.01

centroids = seeds
minSeeds = []
minstdev = maxsize

# Introduces a mechanism of a decreasing step size 
# on top of additional iterations to the let the 
# algorithm converge
while True:

    if stepsize < minStepsize:
        break

    # iteration
    seeds = allMoveSafeTowards(seeds, centroids, stepsize)
    cells = voronoi(seeds,bnd)
    areas = poly_areas(cells)
    stdev = np.round(np.std(areas),4)
    heights = gauss_heights(areas, heighPar)
    phi = init_phi(X, Y, seeds, heights, sigma)
    centroids = wCentroids(cells, phi)

    # plot the result
    # plot_voronoi(cells, seeds,centroids, phi)
    # print(allInsideCell(seeds,cells))
    
    print(ai)
    if stdev >= minstdev:
        ai -= 1 
    else:
        ai = aimax
        minSeeds = seeds
        minstdev = stdev
    if ai == 0:
        seeds = minSeeds
        centroids = minSeeds
        stdevs.append(minstdev)
        stepsize = decFactor*stepsize
        ai = aimax
        continue

    stdevs.append(stdev)

plt.clf()
plt.ioff()
plt.plot(range(len(stdevs)-1),stdevs[1:])
plt.show()

