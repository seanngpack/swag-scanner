import unittest
import timeit
import numpy as np
import numpy.testing as npt

import swagscanner.acquisition.grab_depth as gd


class GrabDepthTests(unittest.TestCase):
    def setUp(self):
        self.depth_map = depth = gd.grab_depth()

    def test_grab_depth(self):
        self.assertEqual(len(self.depth_map.flatten()), 307200)



if __name__ == '__main__':
    unittest.main()
