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

stdf = open("stdevs.csv","w+")
stdf.write("Lloyd;FWC;EASC\n")

iterations = 20
while iterations > 0:
    stdevs1 = Lloyd.lloyd(seeds, stepsize, bnd, X, Y, False)
    stdevs2 = FindWeightedCentroids.findWeightedCentroids(seeds, stepsize, sigma, heighpar, bnd, X, Y, False)
    stdevs3 = EAStepsizeControl.eaStepsizeControl(seeds, sigma, heighpar, bnd, X, Y, False)

    finalstd = []
    finalstd.append(stdevs1[-1])
    finalstd.append(stdevs2[-1])
    finalstd.append(stdevs3[-1])

    stdf.write(';'.join(map(str, finalstd)))
    stdf.write("\n")
    seeds = [9*np.random.rand(2,) for num in range(config.seednum)]
    iterations -= 1
