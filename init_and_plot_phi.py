from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from math import exp


def plot_phi(X,Y,Z):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z');
    ax.view_init(elev=80, azim=0)
    plt.show()

def init_phi(centers, heights, sigmas):
    x_centers = centers[:,0]
    y_centers = centers[:,1]
    x = 100*np.linspace(0, 1, 100)
    y = 100*np.linspace(0, 1, 100)

    phi = 0
    X, Y = np.meshgrid(x,y)
    phi = np.ones((100,100))
    for i, obj in enumerate(centers):
        gau = heights[i]*np.exp((-((Y-y_centers[i])**2/2)-((X-x_centers[i])**2/2))/sigmas[i])
        phi += gau
    return X,Y,phi

centers = np.array([[40, 50], [50, 40], [60, 60]])
heights = np.array([1, 2, 3])
sigmas = np.array([10, 20, 30])


X,Y,phi = init_phi(centers, heights, sigmas)
plot_phi(X,Y,phi)
