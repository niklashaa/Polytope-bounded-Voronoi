from config import bnd, centroids, gran, heighpar, stepsize, sigma, seeds, X, Y
from config import finalstd, stdevs
from functions import allMoveSafeTowards, gauss_heights, init_phi, plot_voronoi, poly_area, poly_areas, uCentroids, wCentroids
from voronoi import voronoi

from sys import maxsize
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------------------------------------
# Algorithm
# -----------------------------------------------------------------------------------

print("Start finding weighted centroids")
# Continues until the seeds lie in the weigthed centroids of their cells
while True:

    # iteration
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
        finalstd.append(stdev)
        break
    if len(stdevs) > 6 and len(set(stdevs[-6:])) < 3:
        finalstd.append(stdev)
        break
    stdevs.append(stdev)

#plt.clf()
#plt.ioff()
#plt.plot(range(len(stdevs)-1),stdevs[1:])
#plt.show()
