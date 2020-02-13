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
stepsize = 1
sigma = 40/2*sqrt(poly_area(bnd)/seedNum/pi)

seeds = [9*np.random.rand(2,) for num in range(seedNum)]
seeds = [np.array([2.28282306, 8.2307008 ]), np.array([8.18527049, 6.50520956]),
np.array([2.60915053, 8.62384755]), np.array([5.10121156, 1.7441158 ]),
np.array([6.27438546, 7.77531027]), np.array([6.1559009 , 0.59289757]),
np.array([8.85379385, 2.40520028]), np.array([8.23961065, 4.94294113]),
np.array([3.60354836, 2.73230573]), np.array([4.96989575, 0.14903545]),
np.array([2.93935512, 7.39421625]), np.array([4.42100026, 2.9731659 ]),
np.array([2.92559434, 1.61967565]), np.array([2.05321745, 2.64976749]),
np.array([5.33633283, 4.20027221])]
x_range = np.linspace(np.amin(bnd[:,0]),np.amax(bnd[:,0]),gran)
y_range = np.linspace(np.amin(bnd[:,1]),np.amax(bnd[:,1]),gran)
X, Y = np.meshgrid(x_range,y_range)

# -----------------------------------------------------------------------------------
# Choose algorithm
# -----------------------------------------------------------------------------------

import EAStepsizeControl
#import FindWeightedCentroids
#import Lloyd
