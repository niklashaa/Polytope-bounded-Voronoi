from functions import allInside, allMoveSafeTowards, gauss_heights, init_phi, plot_voronoi, poly_area, poly_areas, uCentroids, wCentroids
from voronoi import voronoi

import numpy as np
from sys import maxsize
from matplotlib import path, pyplot as plt

# -----------------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------------

bnd = np.array([[0, 0], [9, 0], [9, 9], [0, 9]])
gran = 200
heighPar = 100
seedNum = 15
stepsize = 0.1
sigma = 40/2*np.sqrt(poly_area(bnd)/seedNum/np.pi)

seeds = [4*np.random.rand(2,) for num in range(seedNum)]
x_range = np.linspace(np.amin(bnd[:,0]),np.amax(bnd[:,0]),gran)
y_range = np.linspace(np.amin(bnd[:,1]),np.amax(bnd[:,1]),gran)
X, Y = np.meshgrid(x_range,y_range)

initai = 10
ai = initai
stdevs = []
stdevs.append(maxsize)

centroids = seeds
minSeeds = []
minstdev = maxsize

# -----------------------------------------------------------------------------------
# Algorithm
# -----------------------------------------------------------------------------------

# Introduces a mechanism of additional iterations to improve the chances to 
# find a better local minimum
while True:

    # iteration
    seeds = allMoveSafeTowards(seeds, centroids, stepsize, bnd)
    cells = voronoi(seeds,bnd)
    areas = poly_areas(cells)
    stdev = np.round(np.std(areas),4)
    heights = gauss_heights(areas, heighPar)
    phi = init_phi(X, Y, seeds, heights, sigma)
    centroids = wCentroids(cells, phi, X, Y)

    # plot the result
    # plot_voronoi(cells, seeds,centroids, phi)
    
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

