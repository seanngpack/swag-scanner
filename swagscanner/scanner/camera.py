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
        # TODO: Add intrinsics ehre

    def get_depth(self):
        '''Get a depth frame (1280 x 720) from D435 camera

        Args:
            None

        Returns:
            A numpy array shape=(1280 x 720) of the depth frame
            with values from 0->2047

        '''
        print("lol")

    def get_pointcloud(self):
        '''Use depth frame to create a pointcloud using vectorized
        operations for speed

        Args:
            None

        Returns:
            a pointcloud object

        '''

        clipping_distance_in_meters = 1
        clipping_distance = clipping_distance_in_meters / self.depth_scale

        try:
            frames = self.pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()

            if not depth_frame:
                raise RuntimeError("Could not acquire depth frame")

            pointcloud_array = self.get_pointcloud_array_vectorized(
                depth_frame, self.depth_scale)

            point_cloud_xyz = pcl.PointCloud()
            point_cloud_xyz.from_array(pointcloud_array)
            viewer.visualize(point_cloud_xyz)


        finally:
            self.pipeline.stop()

    def get_pointcloud_array_vectorized(self, depth_frame, depth_scale):
        '''Convert depth frame to a (921600, 3) array of real-world coordinates
        [[x,y,d],
        [x,y,d],...]

        Args:
            depth_frame (depth_frame): depth captured by the camera

        Returns:
            pointcloud_array (np.array): (921600, 3) array

        '''

        depth_image = np.asarray(depth_frame.get_data())
        depth_image = np.asarray(depth_image, dtype=np.float32) * self.depth_scale
        depth_image = depth_image.flatten()

        depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
        fx_d = 1.0 / depth_intrin.fx
        cx_d = depth_intrin.ppx
        fy_d = 1.0 / depth_intrin.fy
        cy_d = depth_intrin.ppy

        depth_array = np.empty((921600, 3))
        x_array = np.tile(np.arange(1280), 720)
        y_array = np.repeat(np.arange(720), 1280)

        # perform calculations to convert to real world coordinates
        depth_array = depth_image # TODO: double check this
        x_array = (x_array - cx_d) * depth_array * fx_d
        y_array = (y_array - cy_d) * depth_array * fy_d

        point_cloud_array = np.vstack((x_array, y_array, depth_array)).T
        point_cloud_array = np.asarray(point_cloud_array, dtype=np.float32)

        return point_cloud_array


def main():
    camera = Camera()
    camera.get_pointcloud()

if __name__ == "__main__":
    main()