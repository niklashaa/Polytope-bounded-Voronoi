import numpy as np
import random
from scipy.spatial import ConvexHull

def inHull(pnts,bnd):
    k=0
    pout = []
    for j, obj in enumerate(pnts):
        bndhull = ConvexHull(bnd)
        bndTmp = bndhull.equations
        bndMat = np.matrix(bndTmp)
        Abnd = bndMat[:,0:2]
        bbnd = bndMat[:,2]
        if (np.round(np.dot(Abnd,pnts[j].transpose()),7) <= np.round(-bbnd.transpose(),7)).all():
            k = k+1
            pout.append(pnts[j])
    return np.array(pout)
