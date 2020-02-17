from functions import allMoveSafeTowards, allInsideBnd, gauss_heights, init_phi, plot_voronoi, poly_area, poly_areas, uCentroids, wCentroids
from voronoi import voronoi

from sys import maxsize
import numpy as np

def eaStepsizeControl(seeds, sigma, heighpar, bnd, X, Y, plot):
    aimax = 10
    ai = aimax
    stepsize = 10 
    decFactor = 0.5
    minStepsize = 0.5

    print("Start equalizing areas with stepsize control")
    stdevs = [maxsize]
    centroids = seeds
    minseeds = seeds

    while True:

        if stepsize < minStepsize:
            break

        seeds = allMoveSafeTowards(seeds, centroids, stepsize, bnd)
        cells = voronoi(seeds,bnd)
        areas = poly_areas(cells)
        stdev = np.round(np.std(areas),4)
        heights = gauss_heights(areas, heighpar)
        phi = init_phi(X, Y, seeds, heights, sigma)
        centroids = wCentroids(cells, phi, X, Y)

        # plot the result
        if(plot):
            plot_voronoi(cells, seeds, centroids, X, Y, phi)

        if stdev >= min(stdevs):
            ai -= 1 
        else:
            ai = aimax
            minseeds = seeds
        if ai == 0:
            seeds = minseeds
            centroids = minseeds
            stdevs.append(min(stdevs))
            stepsize = decFactor*stepsize
            ai = aimax
            continue

        stdevs.append(stdev)
    return stdevs[1:]
