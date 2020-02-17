import numpy as np
from math import sqrt, pi
from matplotlib import path
from functions import poly_area
from sys import maxsize

bnd = np.array([[0, 0], [9, 0], [9, 9], [0, 9]])
gran = 200
heighpar = 10
seednum = 15
stepsize = 1
sigma = 40/2*sqrt(poly_area(bnd)/seednum/pi)

seeds = [9*np.random.rand(2,) for num in range(seednum)]
#seeds = [np.array([1.95534202, 1.96299316]),
# np.array([7.04207485, 1.95492166]),
# np.array([7.04187283, 7.04545893]),
# np.array([4.5154923,  4.49890175]),
# np.array([1.95643911, 7.03662142])]
#
#seeds = [np.array([1.76537519, 1.76522898]),
# np.array([07.23481697, 1.76530735]),
# np.array([7.2348233,  7.23467715]),
# np.array([4.50006725, 4.49999457]),
# np.array([1.76536887, 7.23475551])]
centroids = seeds
x_range = np.linspace(np.amin(bnd[:,0]),np.amax(bnd[:,0]),gran)
y_range = np.linspace(np.amin(bnd[:,1]),np.amax(bnd[:,1]),gran)
X, Y = np.meshgrid(x_range,y_range)
