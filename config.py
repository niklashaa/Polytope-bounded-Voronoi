import numpy as np
from math import sqrt, pi
from matplotlib import path
from functions import poly_area
from sys import maxsize

bnd = np.array([[0, 0], [9, 0], [9, 9], [0, 9]])
gran = 200
heighpar = 10
seednum = 5
stepsize = 1
sigma = 40/2*sqrt(poly_area(bnd)/seednum/pi)

#seeds = [9*np.random.rand(2,) for num in range(seednum)]
seeds = [np.array([0.93563851, 7.85080354]),
 np.array([0.89696547, 5.60573809]),
 np.array([7.68339449, 4.31291054]),
 np.array([5.67128713, 1.26333068]),
 np.array([3.34779595, 7.91012589])]
centroids = seeds
x_range = np.linspace(np.amin(bnd[:,0]),np.amax(bnd[:,0]),gran)
y_range = np.linspace(np.amin(bnd[:,1]),np.amax(bnd[:,1]),gran)
X, Y = np.meshgrid(x_range,y_range)
