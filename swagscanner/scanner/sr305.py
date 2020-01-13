import numpy as np
import pyrealsense2 as rs
import pcl
from swagscanner.scanner.camera import Camera


class SR305(Camera):
    '''Camera object

    '''

    def __init__(self):
        # Configure depth stream
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(
            rs.stream.depth, 640, 480, rs.format.z16, 30)

        # Start streaming
        self.profile = self.pipeline.start(self.config)
        self.device = self.profile.get_device()
        self.depth_sensor = self.device.first_depth_sensor()
        # self.depth_sensor.set_option(rs.option.visual_preset, 3)

        # Grab camera information
        self.depth_scale = self.depth_sensor.get_depth_scale()
        self.depth_intrinsics = self.get_intrinsics()

    def get_intrinsics(self):
        '''Grab the intrinsics from the camera

        '''

        intrin = (self.profile.get_stream(rs.stream.depth).
                  as_video_stream_profile().get_intrinsics())

        intrinsics = {
            'width': intrin.width,
            'height': intrin.height,
            'fx': intrin.fx,
            'fy': intrin.fy,
            'ppx': intrin.ppx,
            'ppy': intrin.ppy,
            'model': intrin.model,
            'coeffs': intrin.coeffs
        }

        return intrinsics

    def get_depth_frame(self):
        '''Get a depth frame (640 x 480) from SR305 camera

        Args:
            None

        Returns:
            A numpy array shape=(640 x 480) of the depth frame

        '''

        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            raise RuntimeError("Could not acquire depth frame")
        return depth_frame

    def get_depth_array(self):
        '''Get a 1D numpy depth array (307200, 1) from the depth frame
        with units in meters

        Returns:
            depth array

        '''

        depth_frame = self.get_depth_frame()
        depth_array = np.asarray(depth_frame.get_data())
        depth_array = np.asarray(depth_array, dtype=np.float32) * self.depth_scale
        depth_array = depth_array.flatten()

        return depth_array

    def stop_pipeline(self):
        '''Stop camera pipeline

        '''
        
        self.pipeline.stop()
