from functions import allMoveSafeTowards, gauss_heights, sumDist, init_phi, plot_voronoi, poly_area, poly_areas, uCentroids, wCentroids
from voronoi import voronoi

from sys import maxsize
import numpy as np

def findWeightedCentroids(seeds, stepsize, sigma, heighpar, bnd, X, Y, plot):
    aimax = 40
    ai = aimax
    stepsize = 10
    decFactor = 0.5

    print("Start finding weighted centroids")
    stdevs = [maxsize]
    sumdists = [maxsize]
    centroids = seeds
    minseeds = seeds

    while True:

        seeds = allMoveSafeTowards(seeds, centroids, stepsize, bnd)
        cells = voronoi(seeds,bnd)
        areas = poly_areas(cells)
        stdev = np.round(np.std(areas),4)
        heights = gauss_heights(areas, heighpar)
        phi = init_phi(X, Y, seeds, heights, sigma)
        centroids = wCentroids(cells, phi, X, Y)
        sumdist = sumDist(seeds,centroids)

        # plot the result
        if(plot):
            plot_voronoi(cells, seeds, centroids, X, Y, phi)

        if sumdist >= min(sumdists):
            ai -= 1 
        else:
            ai = aimax
            minseeds = seeds
        if ai == 0:
            seeds = minseeds
            centroids = minseeds
            stdevs.append(min(stdevs))
            sumdists.append(min(sumdists))
            stepsize = decFactor*stepsize
            ai = aimax
            continue

        if np.array_equal(np.round(seeds,2),np.round(centroids,2)):
            break

        stdevs.append(stdev)
        sumdists.append(sumdist)
    return stdevs[1:]
