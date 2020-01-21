import numpy as np
from numpy import linalg as LA

def perpBisector2d(v1, v2):
    vm = np.array([(v1[0] + v2[0])/2,(v1[1] + v2[1])/2]) # Mittelpunkt zwischen v1 und v2
    v3 = np.array([v2[0] - v1[0],v2[1]-v1[1]]) # Richtungsvektor v1 -> v2 

    Ad = np.array([v3[0]/ LA.norm(v3,2),v3[1]/LA.norm(v3,2)]) # Normierter Richtungsvektor
    bd = np.dot(Ad,vm) # Skalarprodukt aus Richtungsvektor und Mittelpunktsvektor

    if np.dot(Ad,v1) <= bd:
        return Ad, bd
    return np.negative(Ad), np.negative(bd)