from setup import bnd, heighPar, seeds, sigma, stepsize, X, Y
from functions import allMoveTowards, gauss_heights, init_phi, plot_voronoi, poly_areas, uCentroids, wCentroids
from voronoi import voronoi

import numpy as np
from matplotlib import path

# -----------------------------------------------------------------------------------
# Algorithm
# -----------------------------------------------------------------------------------

if not path.Path(bnd).contains_points(seeds).all():
    raise Exception('Boundary does not contain all seeds:\n {}'.format(seeds))

# first iteration
cells = voronoi(seeds,bnd)
centroids = uCentroids(cells)

# initialize gauss functions
areas = poly_areas(cells)
heights = gauss_heights(areas, heighPar)
phi = init_phi(X, Y, seeds, heights, sigma)
centroids = wCentroids(cells, phi)

i=0
# Perform LLoyd algorithm
while not np.array_equal(np.round(seeds,3),np.round(centroids,3)):

    i+=1
    print(i)

    # plot the result...
    plot_voronoi(cells, seeds,centroids, phi)

    # next iteration
    seeds = allMoveTowards(seeds, centroids, stepsize)
    if not path.Path(bnd).contains_points(seeds).all():
        raise Exception('Boundary does not contain all seeds:\n {}'.format(seeds))
    cells = voronoi(seeds,bnd)
    areas = poly_areas(cells)
    centroids = uCentroids(cells)

    # initialize gauss functions
    areas = poly_areas(cells)
    heights = gauss_heights(areas, heighPar)
    phi = init_phi(X, Y, seeds, heights, sigma)
