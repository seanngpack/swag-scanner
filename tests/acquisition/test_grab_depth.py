import unittest
import timeit
import numpy as np
import numpy.testing as npt

import swagscanner.acquisition.grab_depth as gd

class GrabDepthTests(unittest.TestCase):

    def test_grab_depth(self):
        depth = gd.grab_depth()
        depth = depth.flatten()
        self.assertEqual(len(depth), 307200)
        
        
if __name__ == '__main__':
    unittest.main()