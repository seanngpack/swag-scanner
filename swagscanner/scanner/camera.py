import numpy as np
import pyrealsense2 as rs
import pcl
import swagscanner.visualization.viewer as viewer


class Camera():
    '''Camera object

    '''

    def __init__(self, rotation_matrix=None):
        self.rotation_matrix = rotation_matrix

        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

        # Start streaming
        self.pipeline.start(config)

        # Get stream profile and camera intrinsics
        profile = self.pipeline.get_active_profile()
        depth_profile = rs.video_stream_profile(
            profile.get_stream(rs.stream.depth))
        self.depth_intrinsics = depth_profile.get_intrinsics()

        self.depth_sensor = profile.get_device().first_depth_sensor()
        self.depth_sensor.set_option(
            rs.option.visual_preset, 3
        )  # Set high accuracy for depth sensor
        self.depth_scale = self.depth_sensor.get_depth_scale()

    def get_depth_frame(self):
        '''Get a depth frame (1280 x 720) from D435 camera

        Args:
            None

        Returns:
            A numpy array shape=(1280 x 720) of the depth frame
            with values from 0->2047

        '''

        clipping_distance_in_meters = 1
        clipping_distance = clipping_distance_in_meters / self.depth_scale

        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            raise RuntimeError("Could not acquire depth frame")
        return depth_frame

    def stop_pipeline(self):
        self.pipeline.stop()
