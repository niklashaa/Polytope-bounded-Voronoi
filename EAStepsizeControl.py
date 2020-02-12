from main import bnd, gran, heighpar, sigma, seeds, X, Y
from functions import allMoveSafeTowards, gauss_heights, init_phi, plot_voronoi, poly_area, poly_areas, uCentroids, wCentroids
from voronoi import voronoi

import numpy as np
from sys import maxsize
from matplotlib import path, pyplot as plt

# -----------------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------------

aimax = 10
ai = aimax
stdevs = []
stdevs.append(maxsize)
stepsize = 10 
decFactor = 0.5
minStepsize = 0.5

centroids = seeds
minSeeds = []
minstdev = maxsize

# -----------------------------------------------------------------------------------
# Algorithm
# -----------------------------------------------------------------------------------

# Introduces a mechanism of a decreasing step size 
# on top of additional iterations to the let the 
# algorithm converge
while True:

    if stepsize < minStepsize:
        break

    # iteration
    seeds = allMoveSafeTowards(seeds, centroids, stepsize, bnd)
    cells = voronoi(seeds,bnd)
    areas = poly_areas(cells)
    stdev = np.round(np.std(areas),4)
    heights = gauss_heights(areas, heighpar)
    phi = init_phi(X, Y, seeds, heights, sigma)
    centroids = wCentroids(cells, phi, X, Y)

    # plot the result
    # plot_voronoi(cells, seeds,centroids, phi)
    
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

