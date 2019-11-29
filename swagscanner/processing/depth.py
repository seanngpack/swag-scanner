import numpy as np
import pcl
import pyrealsense2 as rs
from swagscanner.scanner.d435 import D435
from swagscanner.scanner.kinect import Kinect
import swagscanner.visualization.viewer as viewer


class DepthProcessor():
    '''Takes in a camera object and performs processing on the
    depth frame it generates

    '''

    def __init__(self, camera=None, fast=True):
        if camera is None:
            raise ValueError('Error: must pass a camera to DepthProcessor')
        self.camera = camera
        self.intrinsics = self.camera.depth_intrinsics



    def get_pointcloud(self):
        '''Use depth frame to create a pointcloud using vectorized
        operations for speed

        Args:
            None

        Returns:
            a pointcloud object

        '''

        pointcloud_array = self.deproject_depth_frame()
        # pointcloud_array = deproject_depth_frame_slow(depth_frame, depth_intrinsics)

        point_cloud_xyz = pcl.PointCloud()
        point_cloud_xyz.from_array(pointcloud_array)
        
        # let's look at our new pointcloud
        viewer.visualize(point_cloud_xyz)

        return point_cloud_xyz

    def get_pointcloud_2(self, depth_frame):
        pc = rs.pointcloud()
        points = pc.calculate(depth_frame)
        v, t = points.get_vertices(), points.get_texture_coordinates()
        verts = np.asanyarray(v).view(np.float32).reshape(-1, 3)  # xyz
        # texcoords = np.asanyarray(t).view(np.float32).reshape(-1, 2)  # uv
                
        pc2 = pcl.PointCloud()
        pc2.from_array(verts)

        viewer.visualize(pc2)
        print('pc2222')
        return pc2

    def deproject_depth_frame(self):
        '''Deproject 2D pixels & depth values to real world coordinates 
        then shape into a (921600, 3) array
            [[x,y,d],
            [x,y,d],...]

        Args:
            depth_frame (depth_frame): depth captured by the camera
            depth_intrinsics (depth_intrinsics): camera intrinsics
            depth_scale (float): conversion from camera depth mapping to meters irl

        Returns:
            pointcloud_array (np.array): (921600, 3) array

        '''

        width = self.intrinsics['width']
        height = self.intrinsics['height']

        depth_array = self.camera.get_depth_array()
        x_array = np.tile(np.arange(width), height)
        y_array = np.repeat(np.arange(height), width)

        # perform calculations to convert to real world coordinates
        x_array = (x_array - self.intrinsics['ppx']) * depth_array * (1/self.intrinsics['fx'])
        y_array = (y_array - self.intrinsics['ppy']) * depth_array * (1/self.intrinsics['fy'])

        point_cloud_array = np.vstack((x_array, y_array, depth_array)).T
        point_cloud_array = np.asarray(point_cloud_array, dtype=np.float32)

        return point_cloud_array

    def deproject_depth_frame_slow(self, depth_frame, depth_intrinsics):
        '''Slow, naive approach

        Args:
            depth_frame (depth_frame): depth captured by the camera
            depth_intrinsics (depth_intrinsics): camera intrinsics

        Returns:
            pointcloud_array (np.array): (921600, 3) array

        '''

        depth_array = np.empty((921600, 3))
        counter = 0
        for i in range(depth_frame.get_height()):
            for j in range(depth_frame.get_width()):

                depth = depth_frame.get_distance(j, i)
                depth_point = np.asarray(rs.rs2_deproject_pixel_to_point(
                                    depth_intrinsics, [j, i], depth), dtype=np.float32)       
                depth_array[counter] = depth_point
                counter +=1
        point_cloud_array = depth_array.astype(dtype=np.float32)
        return point_cloud_array

swag = DepthProcessor(D435())
swag.get_pointcloud()