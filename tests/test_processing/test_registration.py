import numpy as np
import os
import pcl
import unittest
from swagscanner.processing.registration import Registration


class TestRegistration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registration = Registration(input_folder_path=os.getcwd(),
                                        write_folder_path=os.getcwd(),
                                        generate_folder=False)

    def test_map_cloud_operation(self):
        '''Test the mapping of functions to pointclouds

        '''

        dim = 99
        identity = np.identity(4)
        array = np.arange(dim, dtype=np.float32)
        array = array.reshape(-1, 3)
        
        cloud = pcl.PointCloud()
        cloud.from_array(array)

        result_cloud = self.registration.map_cloud_operation(cloud=cloud,
                                                             matrix=identity,
                                                             func=np.dot)

        self.assertTrue(np.all(np.equal(array, result_cloud.to_array())))


if __name__ == '__main__':
    unittest.main()
