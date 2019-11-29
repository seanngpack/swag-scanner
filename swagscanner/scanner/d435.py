import numpy as np
import pyrealsense2 as rs
import pcl
from swagscanner.scanner.camera import Camera


class D435(Camera):
    '''Camera object

    '''

    def __init__(self):
        # Configure depth stream
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(
            rs.stream.depth, 1280, 720, rs.format.z16, 30)

        # Start streaming
        self.profile = self.pipeline.start(self.config)
        self.device = self.profile.get_device()
        self.depth_sensor = self.device.first_depth_sensor()
        self.depth_sensor.set_option(rs.option.visual_preset, 3)

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
        '''Get a depth frame (1280 x 720) from D435 camera

        Args:
            None

        Returns:
            A numpy array shape=(1280 x 720) of the depth frame

        '''

        clipping_distance_in_meters = 1
        clipping_distance = clipping_distance_in_meters / self.depth_scale

        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            raise RuntimeError("Could not acquire depth frame")
        return depth_frame

    def get_depth_array(self):
        '''Get a 1D numpy depth array (921600, 1) from the depth frame
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
        self.pipeline.stop()
