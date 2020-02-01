import numpy as np
import matplotlib.pyplot as plt
from math import sqrt,atan2, cos, sin
from mpl_toolkits import mplot3d
from scipy.spatial import ConvexHull
from matplotlib import path

from config import X, Y

def allInside(seeds, bnd):
    return path.Path(bnd).contains_points(seeds).all()

# Calculate the area of a polygon
def poly_area(polytope):
    x = polytope[:,0]
    y = polytope[:,1]
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def poly_areas(polytopes):
    areas = []
    for poly in polytopes:
        areas.append(poly_area(poly))
    return np.asarray(areas)

# Calculate the height of the gaussian bells
def gauss_heights(areas,heighPar):
    return heighPar*(areas/np.mean(areas)-1)

# unweighted centroid
def uCentroid(cell):
    length = cell.shape[0]
    sum_x = np.sum(cell[:, 0])
    sum_y = np.sum(cell[:, 1])   
    return [sum_x/length, sum_y/length] 

def uCentroids(cells):
    centroids = []
    for cell in cells:
        centroids.append(uCentroid(cell))
    return np.asarray(centroids)

# weighted centroid
def wCentroid(cell, phi):
    centroid = []
    p = path.Path(cell)

    # Create binary matrix (flags) with ones and zeros that's one 
    # for the points that are in the cell
    all_points = np.vstack([X.flatten(), Y.flatten()]).T
    flags = p.contains_points(all_points)
    reflags = np.reshape(flags, X.shape) # reshaped flags
    
    # With X,Y,flags and phi calculate the weighted centroids:
    # (X.*flags.*phi)/sum(phi*flags) = centroid(0,0)
    # (Y.*flags.*phi)/sum(phi*flags) = centroid(0,1)
    xin = np.multiply(X,reflags)
    yin = np.multiply(Y,reflags)
    pin = np.multiply(phi,reflags)

    centroid.append(np.sum(np.multiply(xin,phi))/np.sum(pin))
    centroid.append(np.sum(np.multiply(yin,phi))/np.sum(pin))

    return np.asarray(centroid)

def wCentroids(cells, phi):
    centroids = []
    for cell in cells:
        centroids.append(wCentroid(cell, phi))
    return np.asarray(centroids)

def moveTowards(seed, centroid, stepsize):
    dist = sqrt((centroid[0]-seed[0])**2 + (centroid[1]-seed[1])**2)
    if dist < stepsize:
        return centroid
    rad = atan2(centroid[1]-seed[1], centroid[0]-seed[0])
    new_x = seed[0] + stepsize*cos(rad)
    new_y = seed[1] + stepsize*sin(rad)
    return np.array([new_x, new_y])

def allMoveTowards(seeds, centroids, stepsize):
    new_centroids = []
    for i, seed in enumerate(seeds):
        new_centroids.append(moveTowards(seed, centroids[i], stepsize))
    return np.asarray(new_centroids)

def init_meshgrid(bnd, gran):
    return X, Y

def init_phi(X, Y, centers, heights, sigma):
    phi = np.ones((X.shape[0],X.shape[0]))
    for i, center in enumerate(centers):
        gau = heights[i]*np.exp((-((Y-center[1])**2/2)-((X-center[0])**2/2))/sigma)
        phi += gau
    return phi

# Plot weighted voronoi
def plot_voronoi(cells, seeds, centroids, phi):
    if not plt.fignum_exists(1):
        plt.ion()
        plt.show()
    ax = plt.axes(projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.view_init(elev=90, azim=-90)

    ax.plot(seeds[:,0],seeds[:,1],'.')
    ax.plot(centroids[:,0],centroids[:,1],'.')
    for cell in cells:
        if len(cell) >= 3:
            hull = ConvexHull(cell)		
            for simplex in hull.simplices:
                ax.plot(cell[simplex, 0],cell[simplex,1],'k-')
    ax.plot_surface(X, Y, phi, cmap='viridis', edgecolor='none', alpha=0.6)
    plt.draw()
    plt.pause(0.001)
