from config import seeds, seednum, bnd, heighpar, stepsize, sigma, seeds, X, Y
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi
from matplotlib import path
from functions import poly_area

import config 
import Lloyd
import FindWeightedCentroids
import EAStepsizeControl

#stdevs = Lloyd.lloyd(seeds, stepsize, bnd, X, Y, True)
stdevs = FindWeightedCentroids.findWeightedCentroids(seeds, stepsize, sigma, heighpar, bnd, X, Y, True)
#stdevs = EAStepsizeControl.eaStepsizeControl(seeds, sigma, heighpar, bnd, X, Y, True)
plt.close()
plt.plot(range(len(stdevs)-1),stdevs[1:])
plt.show()
