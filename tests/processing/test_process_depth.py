import unittest
import numpy.testing as npt

import swagscanner.processing.process_depth as pd

class ProcessDepthTests(unittest.TestCase):

    def test_depth_to_pointxyz(self):
        point1 = pd.depth_to_pointxyz(x = 1, y = 1, depth = 1000)
        point2 = pd.depth_to_pointxyz(x = 400, y = 300, depth = 2047)

        npt.assert_almost_equal(point1, [-2.19, -1.574, 3.848], 2)
        npt.assert_almost_equal(point2, [-0.034, -0.0327, -.338], 2)
        
        
if __name__ == '__main__':
    unittest.main()