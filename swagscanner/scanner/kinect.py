import freenect
import numpy as np
import pcl
from swagscanner.scanner.camera import Camera


class Kinect(Camera):
    '''Kinect object

    '''

    def __init__(self):
        super()
        self.depth_to_meters_table = {
            num: (1.0 / (num * -0.0030711016 + 3.3309495161)) for num in range(2048)
        }
        self.intrinsics = self.get_instrinsics()

    def get_intrinsics(self):
        '''Grab the intrinsics from the camera

        '''

        intrinsics = {
            'width': 640,
            'height': 480,
            'fx': 5.9421434211923247e+02,
            'fy': 5.9104053696870778e+02,
            'ppx': 3.3930780975300314e+02,
            'ppy': 2.4273913761751615e+02,
            'model': None,
            'coeffs': None
        }

        return intrinsics

    def get_depth_frame(self):
        '''Get a depth frame the kinect

        Returns:
            A 2d numpy array of unit8 integers containing depth information mapped from 0->2047. 
            Need to use depth table to map those points to meters
        '''
    
        depth, timestamp = freenect.sync_get_depth()
        depth = depth.astype(np.uint16)
        return depth

    def get_depth_array(self):
        '''Get a 1D numpy depth array (307200, 1) from the depth frame
        with units in meter

        Returns:
            depth array

        '''

        depth_frame = self.get_depth_frame()
        depth_array = np.empty((307200, 3))
        depth_array = [self.depth_to_meters_table[depth_point]
                   for depth_point in depth_frame.ravel().tolist()]
        return depth_array


