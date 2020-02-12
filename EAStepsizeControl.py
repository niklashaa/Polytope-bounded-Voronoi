from functions import allInside, allMoveSafeTowards, gauss_heights, init_phi, plot_voronoi, poly_area, poly_areas, uCentroids, wCentroids
from voronoi import voronoi

import numpy as np
from sys import maxsize
from matplotlib import path, pyplot as plt

# -----------------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------------

bnd = np.array([[0, 0], [9, 0], [9, 9], [0, 9]])
gran = 100
heighPar = 100
seedNum = 15
stepsize = 0.1
sigma = 40/2*np.sqrt(poly_area(bnd)/seedNum/np.pi)

seeds = [4*np.random.rand(2,) for num in range(seedNum)]
x_range = np.linspace(np.amin(bnd[:,0]),np.amax(bnd[:,0]),gran)
y_range = np.linspace(np.amin(bnd[:,1]),np.amax(bnd[:,1]),gran)
X, Y = np.meshgrid(x_range,y_range)

aimax = 10
ai = aimax
stdevs = []
stdevs.append(maxsize)
stepsize = 20 
decFactor = 0.5
minStepsize = 0.1

centroids = seeds
minSeeds = []
minstdev = maxsize

# -----------------------------------------------------------------------------------
# Algorithm
# -----------------------------------------------------------------------------------

# Introduces a mechanism of a decreasing step size 
# on top of additional iterations to the let the 
# algorithm converge
while True:

    if stepsize < minStepsize:
        break

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
    # print(allInsideCell(seeds,cells))
    
    print(ai)
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

plt.clf()
plt.ioff()
plt.plot(range(len(stdevs)-1),stdevs[1:])
plt.show()

