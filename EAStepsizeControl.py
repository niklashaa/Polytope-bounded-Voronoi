from functions import allMoveSafeTowards, allInsideBnd, gauss_heights, init_phi, plot_voronoi, poly_area, poly_areas, uCentroids, wCentroids
from voronoi import voronoi

from sys import maxsize
import numpy as np

# Introduces a mechanism of a decreasing step size 
# on top of additional iterations to the let the 
# algorithm converge
def eaStepsizeControl(seeds, sigma, heighpar, bnd, X, Y):
    aimax = 10
    ai = aimax
    stepsize = 10 
    decFactor = 0.5
    minStepsize = 0.5
    minstdev = maxsize

    print("Start equalizing areas with stepsize control")
    stdevs = [maxsize]
    centroids = seeds

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
    return stdevs[1:]
