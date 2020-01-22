import numpy as np
from mpl_toolkits import mplot3d
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
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

def plot_voronoi(seeds,centroids):
    ax = plt.axes(projection='3d')
    ax.plot(seeds[:,0],seeds[:,1],'o')
    ax.plot(centroids[:,0],centroids[:,1],'o')

    for cell in cells:
        if len(cell) >= 3:
            vorhull = ConvexHull(cell)		
    #        plt.plot(cell[:,0],cell[:,1],'x')
            for simplex in vorhull.simplices:
                ax.plot(cell[simplex, 0],cell[simplex,1],'k-')

    #ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none', alpha=0.1)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.view_init(elev=90, azim=-90)
    plt.show()


def calc_centroids(regions):
    centroids = []
    for region in regions:
        length = region.shape[0]
        sum_x = np.sum(region[:, 0])
        sum_y = np.sum(region[:, 1])
        centroids.append([sum_x/length, sum_y/length])
    return np.array(centroids)

def init_phi(X, Y, centers, heights, sigmas):
    phi = np.ones((X.shape[0],X.shape[0]))
    for i, center in enumerate(centers):
        gau = heights[i]*np.exp((-((Y-center[1])**2/2)-((X-center[0])**2/2))/sigmas[i])
        phi += gau
    return phi

# boundary points, initial seed points
bnd = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
seeds = np.array([[0.1, 0.1], [0.42, 0.53], [0.8, 0.3]])

# parameter setup
heights = np.array([1, 2, 3])
sigmas = np.array([10, 20, 30])

# build meshgrid with extreme points of boundary
x_range = np.linspace(np.amin(bnd[:,0]),np.amax(bnd[:,0]),10)
y_range = np.linspace(np.amin(bnd[:,1]),np.amax(bnd[:,1]),10)
X, Y = np.meshgrid(x_range,y_range)

init_phi(X,Y,seeds,heights,sigmas)

# first iteration
cells = voronoi(seeds,bnd)
centroids = calc_centroids(cells)

i=0

# Perform LLoyd algorithm
while (not np.array_equal(seeds,centroids) and i<=9):

    i+=1
    print(i)

    # plot the result...
    plot_voronoi(seeds,centroids)

    # next iteration

    seeds = centroids
    cells = voronoi(seeds,bnd)
    areas = poly_areas(cells)
    centroids = calc_centroids(cells)
