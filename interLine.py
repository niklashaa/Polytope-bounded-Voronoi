#!/usr/bin/python

import numpy as np
from numpy.linalg import inv

#lineA = [0.1, 0f.2, 0.1]
#lineB = [0.4, -0.2, 0.3]

# A = [[0.1, 0.2], 
#      [0.4, -0.2]]

# b = [[0.1],
#      [0.3]]

def interLine(lineA,lineB):
    if (lineA[0]*lineB[1] - lineB[0]*lineA[1] != 0): # Check if lines are parallel
        A = np.array([[lineA[0],lineA[1]],[lineB[0],lineB[1]]])
        b = np.array([[lineA[2]],[lineB[2]]])
        res = np.dot(inv(A),b) # Returns nested matrix
        return np.array([res.item(0),res.item(1)])
    return False
