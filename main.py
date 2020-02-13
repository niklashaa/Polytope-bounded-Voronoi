import numpy as np
from math import sqrt, pi
from matplotlib import path
from functions import poly_area

import config 
import Lloyd
import FindWeightedCentroids
import EAStepsizeControl
# -----------------------------------------------------------------------------------
# Choose algorithm
# -----------------------------------------------------------------------------------

initseeds = config.seeds

stdf = open("stdevs.csv","w+")
stdf.write("Lloyd;FWC;EASC\n")

iterations = 2
while iterations > 1:
    Lloyd
    seeds = initseeds
    FindWeightedCentroids
    seeds = initseeds
    EAStepsizeControl

    stdf.write(';'.join(map(str, config.finalstd)))
    stdf.write("\n")
    config.seeds = [9*np.random.rand(2,) for num in range(config.seedNum)]
    initseeds = config.seeds
    iterations -= 1
