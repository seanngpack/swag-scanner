import numpy as np
import pcl
import swagscanner.visualization.viewer as viewer

'''This module provides tools for processing the depth frame
captured by the Camera object

'''


def get_pointcloud(depth_frame, depth_intrinsics, depth_scale):
    '''Use depth frame to create a pointcloud using vectorized
    operations for speed

    Args:
        None

    Returns:
        a pointcloud object

    '''

    pointcloud_array = deproject_depth_frame(
        depth_frame, depth_intrinsics ,depth_scale)

    point_cloud_xyz = pcl.PointCloud()
    point_cloud_xyz.from_array(pointcloud_array)
    
    # let's look at our new pointcloud
    # viewer.visualize(point_cloud_xyz)


    return point_cloud_xyz

def deproject_depth_frame(depth_frame, depth_intrinsics, depth_scale):
    '''Deproject 2D pixels & depth values to real world coordinates 
    then shape into a (921600, 3) array
        [[x,y,d],
        [x,y,d],...]

    Args:
        depth_frame (depth_frame): depth captured by the camera

    Returns:
        pointcloud_array (np.array): (921600, 3) array

    '''

    depth_image = np.asarray(depth_frame.get_data())
    depth_image = np.asarray(depth_image, dtype=np.float32) * depth_scale
    depth_image = depth_image.flatten()

    fx_d = 1.0 / depth_intrinsics.fx
    cx_d = depth_intrinsics.ppx
    fy_d = 1.0 / depth_intrinsics.fy
    cy_d = depth_intrinsics.ppy

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
