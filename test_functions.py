import unittest
import functions
import numpy as np

class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.bnd = np.array([[0, 0], [9, 0], [9, 9], [0, 9]])
        self.seeds = np.array([[1, 1],[2,1],[1,2],[3,4]])
        self.seeds = [np.array([0.93563851, 7.85080354]),
         np.array([0.89696547, 5.60573809]),
         np.array([7.68339449, 4.31291054]),
         np.array([5.67128713, 1.26333068]),
         np.array([3.34779595, 7.91012589])]

        self.triangle = np.array([[0, 0],[8,0],[4,6]])

        x_range = np.linspace(np.amin(self.bnd[:,0]),np.amax(self.bnd[:,0]),10)
        y_range = np.linspace(np.amin(self.bnd[:,1]),np.amax(self.bnd[:,1]),10)
        self.X, self.Y = np.meshgrid(x_range,y_range)

    def tearDown(self):
        pass

    def test_poly_area(self):
        area1 = functions.poly_area(np.array([[0, 0],[1,0],[1,1],[0,1]]))
        area2 = functions.poly_area(np.array([[0, 0],[1,0],[1,1],[0.5, 1],[0,1]]))
        area3 = functions.poly_area(np.array([[0, 0],[1,0],[1,1],[0,1],[0.5, 1]]))
        self.assertEqual(area1,1)
        self.assertEqual(area2,1)
        self.assertNotEqual(area3,1)

    def test_gauss_heights(self):
        areas = np.array([5, 6, 7])
        heighpar = 1
        res = np.round(functions.gauss_heights(areas, heighpar), 3)
        exp = np.array([-0.167, 0, 0.167])
        np.testing.assert_equal(res, exp)

    def test_uCentroid(self):
        centroid = np.array([4,2])
        np.testing.assert_equal(functions.uCentroid(self.triangle), centroid)

    def test_wCentroid(self):
        centroid = np.array([4,2])
        phi = np.ones((self.X.shape[0],self.X.shape[0]))
        wCentroid = np.round(functions.wCentroid(self.triangle,phi, self.X, self.Y))
        np.testing.assert_equal(wCentroid, centroid)

        phi = self.Y*phi
        centroid = np.array([4,3.290909])
        wCentroid = np.round(functions.wCentroid(self.triangle,phi, self.X, self.Y),6)
        np.testing.assert_equal(wCentroid, centroid)

        phi = (self.Y-1000)*phi
        centroid = np.array([4,3.288732])
        wCentroid = np.round(functions.wCentroid(self.triangle,phi, self.X, self.Y),6)
        np.testing.assert_equal(wCentroid, centroid)


        phi = (self.Y-1000)*phi
        centroid = np.array([4,3.286556])
        wCentroid = np.round(functions.wCentroid(self.triangle,phi, self.X, self.Y),6)
        np.testing.assert_equal(wCentroid, centroid)

if __name__ == '__main__':
    unittest.main()
