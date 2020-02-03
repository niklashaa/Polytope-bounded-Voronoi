from config import bnd, heighPar, seeds, sigma, stepsize, X, Y
from functions import allInside, allMoveSafeTowards, gauss_heights, init_phi, plot_voronoi, poly_areas, uCentroids, wCentroids
from voronoi import voronoi

import numpy as np
from sys import maxsize
from matplotlib import path, pyplot as plt

initai = 10
ai = initai
stdevs = []
stdevs.append(maxsize)

centroids = seeds
minSeeds = []
minstdev = maxsize

# Introduces a mechanism of additional iterations to improve the chances to 
# find a better local minimum
while True:

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
        ai = ai - 1 
    else:
        ai = initai
        minSeeds = seeds
        minstdev = stdev
    if ai == 0:
        seeds = minSeeds
        stdevs.append(minstdev)
        break

    stdevs.append(stdev)

plt.clf()
plt.ioff()
plt.plot(range(len(stdevs)-1),stdevs[1:])
plt.show()

