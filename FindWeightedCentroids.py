from functions import allMoveSafeTowards, gauss_heights, init_phi, plot_voronoi, poly_area, poly_areas, uCentroids, wCentroids
from voronoi import voronoi

from sys import maxsize
import numpy as np

def findWeightedCentroids(seeds, stepsize, sigma, heighpar, bnd, X, Y):

    print("Start finding weighted centroids")
    stdevs = [maxsize]
    centroids = seeds

    while True:

        seeds = allMoveSafeTowards(seeds, centroids, stepsize, bnd)
        cells = voronoi(seeds,bnd)
        for cell in cells:
            if cell.shape[1] != 2:
                print(cell)
        areas = poly_areas(cells)
        heights = gauss_heights(areas, heighpar)
        phi = init_phi(X, Y, seeds, heights, sigma)
        centroids = wCentroids(cells, phi, X, Y)

        # plot the result
        # plot_voronoi(cells, seeds, centroids, X, Y, phi)

        stdev = np.round(np.std(areas),4)
        if np.array_equal(np.round(seeds,3),np.round(centroids,3)):
            break
        if len(stdevs) > 6 and len(set(stdevs[-6:])) < 3:
            break
        stdevs.append(stdev)
    return stdevs[1:]
