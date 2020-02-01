from config import bnd, heighPar, seeds, sigma, stepsize, X, Y
from functions import allInside, allMoveTowards, gauss_heights, init_phi, plot_voronoi, poly_areas, uCentroids, wCentroids
from voronoi import voronoi

import numpy as np
from sys import maxsize
from matplotlib import path, pyplot as plt

# -----------------------------------------------------------------------------------
# Algorithm
# -----------------------------------------------------------------------------------

stdevs = []
stdevs.append(maxsize)
centroids = seeds

# Perform equalization of areas
while True:

    # iteration
    seeds = allMoveTowards(seeds, centroids, stepsize)
    cells = voronoi(seeds,bnd)
    if not allInside(seeds,bnd):
        raise Exception('Boundary does not contain all seeds:\n {}'.format(seeds))

    areas = poly_areas(cells)
    stdev = np.round(np.std(areas),4)
    heights = gauss_heights(areas, heighPar)
    phi = init_phi(X, Y, seeds, heights, sigma)
    centroids = wCentroids(cells, phi)

    # plot the result
    plot_voronoi(cells, seeds,centroids, phi)

    if stdev >= stdevs[-1]:
        break
    stdevs.append(stdev)

plt.clf()
plt.ioff()
plt.plot(range(len(stdevs)-1),stdevs[1:])
plt.show()

