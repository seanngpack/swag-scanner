import numpy as np
import pyrealsense2 as rs

class Camera():
    '''Camera object

    '''

    def __init__(self, rotation_matrix=None):
        self.rotation_matrix = rotation_matrix
        self.pipeline = rs.pipeline()
        self.config = rs.config()

    def get_depth(self):
        '''Get a depth frame (1280 x 720) from D435 camera

        Args:
            None

        Returns:
            A numpy array shape=(1280 x 720) of the depth frame
            with values from 0->2047

        '''
        
        # TODO: write code to get the depth map from the camera
        # Setup:
        pipe = rs.pipeline()
        cfg = rs.config()
        cfg.enable_device_from_file("stairs.bag")
        profile = pipe.start(cfg)

        # Skip 5 first frames to give the Auto-Exposure time to adjust
        for x in range(5):
            pipe.wait_for_frames()
            
        
        # Store next frameset for later processing:
        frameset = pipe.wait_for_frames()
        depth_frame = frameset.get_depth_frame()

        # Cleanup:
        pipe.stop()
        print("Frames Captured")
