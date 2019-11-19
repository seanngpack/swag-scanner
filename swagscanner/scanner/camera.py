import numpy as np

class Camera():
    '''Camera object

    '''

    def __init__(self, rotation_matrix=None):
        self.rotation_matrix = rotation_matrix

    def get_depth(self):
        '''Get a depth frame (1280 x 720) from D435 camera

        Args:
            None

        Returns:
            A numpy array shape=(1280 x 720) of the depth frame
            with values from 0->2047

        '''
        
        # TODO: write code to get the depth map from the camera
