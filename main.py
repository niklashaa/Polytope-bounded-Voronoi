import numpy as np
from math import sqrt, pi
from matplotlib import path
from functions import poly_area

# -----------------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------------

bnd = np.array([[0, 0], [9, 0], [9, 9], [0, 9]])
gran = 200
heighpar = 100
seedNum = 15
stepsize = 0.1
sigma = 40/2*sqrt(poly_area(bnd)/seedNum/pi)

seeds = [9*np.random.rand(2,) for num in range(seedNum)]
x_range = np.linspace(np.amin(bnd[:,0]),np.amax(bnd[:,0]),gran)
y_range = np.linspace(np.amin(bnd[:,1]),np.amax(bnd[:,1]),gran)
X, Y = np.meshgrid(x_range,y_range)
