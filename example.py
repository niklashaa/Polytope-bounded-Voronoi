import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from math import pi
from matplotlib import path
from mpl_toolkits import mplot3d
from scipy.spatial import ConvexHull
from voronoi import voronoi 

def poly_area(polytope):
    x = polytope[:,0]
    y = polytope[:,1]
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def poly_areas(polytopes):
    areas = []
    for poly in polytopes:
        areas.append(poly_area(poly))
    return np.asarray(areas)

def gauss_heights(areas,heighPar):
    return heighPar*(areas/np.mean(areas)-1)

def plot_voronoi(cells, seeds,centroids):
    ax = plt.axes(projection='3d')
    ax.plot(seeds[:,0],seeds[:,1],'o')
    ax.plot(centroids[:,0],centroids[:,1],'o')

    for cell in cells:
        if len(cell) >= 3:
            hull = ConvexHull(cell)		
            for simplex in hull.simplices:
                ax.plot(cell[simplex, 0],cell[simplex,1],'k-')

    ax.plot_surface(X, Y, phi, cmap='viridis', edgecolor='none', alpha=0.6)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.view_init(elev=90, azim=-90)
    plt.show()

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

def init_phi(X, Y, centers, heights, sigma):
    phi = np.ones((X.shape[0],X.shape[0]))
    for i, center in enumerate(centers):
        gau = heights[i]*np.exp((-((Y-center[1])**2/2)-((X-center[0])**2/2))/sigma)
        phi += gau
    return phi

# weighted centroid
def wCentroid(cell):
    centroid = []
    p = path.Path(cell)

    # Create binary matrix (flags) with ones and zeros that's one 
    # for the points that are in the cell
    all_points = np.vstack([X.flatten(), Y.flatten()]).T
    flags = p.contains_points(all_points)
    reflags = np.reshape(flags, X.shape) # reshaped flags
    
    # With X,Y,flags and phi calculate the weighted centroids:
    # (X.*flags.*phi)/sum(X.*flags) = centroid(0,0)
    # (Y.*flags.*phi)/sum(Y.*flags) = centroid(0,1)
    xin = np.multiply(X,reflags)
    yin = np.multiply(Y,reflags)

    centroid.append(np.sum(np.multiply(xin,phi))/np.sum(xin))
    centroid.append(np.sum(np.multiply(yin,phi))/np.sum(yin))

    return np.asarray(centroid)

def wCentroids(cells):
    centroids = []
    for cell in cells:
        centroids.append(wCentroid(cell))
    return np.asarray(centroids)



# parameter setup
heighPar = 1
sigPar = 1

# boundary points, initial seed points
bnd = np.array([[0, 0], [4, 0], [4, 4], [0, 4]])
seeds = np.array([[1, 1], [4, 4], [3, 2]])

# constants
mean_area = poly_area(bnd)/len(seeds)
sigma = sigPar/2*sqrt(mean_area/pi)

# build meshgrid with extreme points of boundary
gran = 100
x_range = np.linspace(np.amin(bnd[:,0]),np.amax(bnd[:,0]),gran)
y_range = np.linspace(np.amin(bnd[:,1]),np.amax(bnd[:,1]),gran)
X, Y = np.meshgrid(x_range,y_range)

# first iteration
cells = voronoi(seeds,bnd)
centroids = uCentroids(cells)

# initialize gauss functions
areas = poly_areas(cells)
heights = gauss_heights(areas, heighPar)
phi = init_phi(X, Y, seeds, heights, sigma)
centroids = wCentroids(cells)

i=0
# Perform LLoyd algorithm
while (not np.array_equal(seeds,centroids) and i<=5):

    i+=1
    print(i)
    print(centroids)

    # plot the result...
    plot_voronoi(cells, seeds,centroids)

    # next iteration
    seeds = centroids
    cells = voronoi(seeds,bnd)
    areas = poly_areas(cells)
    centroids = wCentroids(cells)

    # initialize gauss functions
    areas = poly_areas(cells)
    heights = gauss_heights(areas, heighPar)
    phi = init_phi(X, Y, seeds, heights, sigma)
