import pyrealsense2 as rs
import pcl


class Camera():
    '''Camera object

    '''

    def __init__(self):
        self.depth_intrinsics = self.get_intrinsics()


    def get_intrinsics(self):
        '''Grab the intrinsics from the camera

        Returns:
            width: width of image in pixels
            height: height of image in pixels
            fx: focal length of the image, as a multiple of pixel width and height
            fy: focal length of the image, as a multiple of pixel width and height
            ppx: pixel coordinates of the principal point (center of projection) 
            ppy: pixel coordinates of the principal point (center of projection)
            model: model used to calibrate the image (none for kinect, make my own)
            coeffs: coefficients describing the distortion model

        '''

        raise Exception ("Not Implemented")



    def get_depth_frame(self):
        '''Get a depth frame from the camera

        Returns:
            A numpy array of the depth frame

        '''

        raise Exception ("Not Implemented")
    

    def get_depth_array(self):
        '''Get a 1D numpy depth array from the depth frame
        with units in meters

        Returns:
            depth array

        '''
        
