from functions import allMoveSafeTowards, gauss_heights, init_phi, plot_voronoi, poly_area, poly_areas, uCentroids
from voronoi import voronoi

from sys import maxsize
import numpy as np

def lloyd(seeds,stepsize, bnd, X, Y, plot):

    print("Start Lloyd algorithm")
    stdevs = [maxsize]
    centroids = seeds

    while True:
        seeds = allMoveSafeTowards(seeds, centroids, stepsize, bnd)
        cells = voronoi(seeds,bnd)
        areas = poly_areas(cells)
        centroids = uCentroids(cells)

        # plot the result
        if(plot):
            plot_voronoi(cells, seeds, centroids, X, Y, phi)

        stdev = np.round(np.std(areas),4)
        if np.array_equal(np.round(seeds,3),np.round(centroids,3)):
            break
        if len(stdevs) > 6 and len(set(stdevs[-6:])) < 3:
            break
        stdevs.append(stdev)
    return stdevs[1:]
