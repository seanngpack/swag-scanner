import numpy as np
import pcl
import pyrealsense2 as rs
from swagscanner.scanner.d435 import D435
from swagscanner.scanner.kinect import Kinect
import swagscanner.visualization.viewer as viewer


class DepthProcessor():
    '''Factory object creator to send processing to either 'fast' or
    'slow' DepthProcessor objects

    '''

    def initialize_processor(self, camera=None, fast=True):
        if camera is None:
            raise ValueError('Error: must pass a camera to DepthProcessor')
        if fast == True:
            return DepthProcessorFast(camera)
        else:
            return DepthProcessorSlow(camera)

    def get_pointcloud(self):
        '''Use a depth frame to create a pointcloud

        '''

        pass

    def deproject_depth_frame(self):
        ''' Use a depth frame and camera intrinsics to deproject 2D pixels
        & depth values to real world coordinates

        '''

        pass

    def clip_depth(self, point_cloud_array):
        ''' Clip the points that are outside the field of the scan bed
        Clips the array after deprojection, can speed things up by
        clipping immediately after grabbing the depth frame.

        TODO: Put it there when I have more time.

        '''

        shape = point_cloud_array.shape
        width_clipping_percentage = 70
        height_clipping_percentage = 70

        point_cloud_array = point_cloud_array[(point_cloud_array[:, 0] > -.2) &
                                              (point_cloud_array[:, 0] < .2) &
                                              (point_cloud_array[:, 1] > -.3) &
                                              (point_cloud_array[:, 1] < .3) &
                                              (point_cloud_array[:, 2] < .7)]
        return point_cloud_array


class DepthProcessorFast(DepthProcessor):
    '''Uses fast vectorized operations to deproject depth frames

    '''

    def __init__(self, camera):
        self.camera = camera
        self.intrinsics = self.camera.depth_intrinsics

    def get_pointcloud(self):
        '''Use depth frame to create a pointcloud using vectorized
        operations for speed

        Returns:
            a pointcloud object

        '''

        pointcloud_array = self.deproject_depth_frame()
        # pointcloud_array = deproject_depth_frame_slow(depth_frame, depth_intrinsics)

        point_cloud = pcl.PointCloud()
        point_cloud.from_array(pointcloud_array)

        return point_cloud

    def deproject_depth_frame(self):
        '''Deproject 2D pixels & depth values to real world coordinates
        then shape into a (921600, 3) array
            [[x,y,d],
            [x,y,d],...]

        Returns:
            pointcloud_array (np.array): (921600, 3) array

        '''

        width = self.intrinsics['width']
        height = self.intrinsics['height']

        depth_array = self.camera.get_depth_array()
        x_array = np.tile(np.arange(width), height)
        y_array = np.repeat(np.arange(height), width)

        # perform calculations to convert to real world coordinates
        x_array = (x_array - self.intrinsics['ppx']) * \
            depth_array * (1/self.intrinsics['fx'])
        y_array = (y_array - self.intrinsics['ppy']) * \
            depth_array * (1/self.intrinsics['fy'])

        point_cloud_array = np.vstack((x_array, y_array, depth_array)).T
        point_cloud_array = np.asarray(point_cloud_array, dtype=np.float32)
        point_cloud_array = super().clip_depth(point_cloud_array)
        print(point_cloud_array.shape)
        return point_cloud_array


class DepthProcessorSlow(DepthProcessor):
    '''Uses slow nested for loops and librealsense libraries to
    deproject depth frames

    '''

    def __init__(self, camera):
        self.camera = camera
        self.intrinsics = self.camera.depth_intrinsics

    def get_pointcloud(self):
        '''Use depth frame to create a pointcloud using built in librealsense
        library methods

        Returns:
            a pointcloud object

        '''

        pc = rs.pointcloud()
        points = pc.calculate(self.camera.get_depth_frame())
        v, t = points.get_vertices(), points.get_texture_coordinates()
        verts = np.asanyarray(v).view(np.float32).reshape(-1, 3)  # xyz
        # texcoords = np.asanyarray(t).view(np.float32).reshape(-1, 2)  # uv

        point_cloud = pcl.PointCloud()
        point_cloud.from_array(verts)

        return point_cloud

    def deproject_depth_frame(self):
        '''Slow, naive approach to deproject using librealsense library methods

        Returns:
            pointcloud_array (np.array): (921600, 3) array

        '''

        width = self.intrinsics['width']
        height = self.intrinsics['height']

        depth_frame = self.camera.get_depth_frame()
        depth_array = np.empty((width * height, 3))

        intrin_object = self.camera.profile.get_stream(
            rs.stream.depth).as_video_stream_profile().get_intrinsics()

        counter = 0
        for i in range(depth_frame.get_height()):
            for j in range(depth_frame.get_width()):

                depth = depth_frame.get_distance(j, i)
                depth_point = np.asarray(rs.rs2_deproject_pixel_to_point(
                    intrin_object, [j, i], depth), dtype=np.float32)
                depth_array[counter] = depth_point
                counter += 1
        point_cloud_array = depth_array.astype(dtype=np.float32)
        return point_cloud_array
