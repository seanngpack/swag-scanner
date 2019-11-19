import cv2
import freenect
import numpy as np
import open3d
import pcl

depth_to_meters_table = {
    num: (1.0 / (num * -0.0030711016 + 3.3309495161)) for num in range(2048)
}


def depth_to_real_world_vectorized(depth_map):
    '''Takes in raw depth data from the kinect (480, 640) and performs calculations
    to map it to three different arrays for real-world x, y, and depth values in meters

    Args:
        depth_map (array): (480, 640) depth data collected from kinect

    Returns:
        three arrays containing the mapped transformations of the x, y, and 
        depth values (307200, 1) each

    '''

    fx_d = 1.0 / 5.9421434211923247e+02
    cx_d = 3.3930780975300314e+02
    fy_d = 1.0 / 5.9104053696870778e+02
    cy_d = 2.4273913761751615e+02

    depth_array = np.empty((307200, 3))
    x_array = np.tile(np.arange(640), 480)
    y_array = np.repeat(np.arange(480), 640)

    # perform calculations to convert to real world coordinates
    depth_array = [depth_to_meters_table[depth]
                   for depth in depth_map.ravel().tolist()]
    x_array = (x_array - cx_d) * depth_array * fx_d
    y_array = (y_array - cy_d) * depth_array * fy_d

    return x_array, y_array, depth_array


def create_pointcloudxyz_vectorized(depth_map):
    '''Creates a pointcloud object by calculating real-world coordinates, mapping them
    to a single (307200, 3) array, and constructing a pointcloud

    Args:
        depth_map (array): (480, 640) depth data collected from kinect

    Returns:
        PointCloud object

    '''

    x_array, y_array, depth_array = depth_to_real_world_vectorized(depth_map)

    # combine the three arrays into a (307200, 3) array
    point_cloud_array = np.vstack((x_array, y_array, depth_array)).T
    point_cloud_array = np.asarray(point_cloud_array, dtype=np.float32)

    # Make the pointcloud
    point_cloud_xyz = pcl.PointCloud()
    point_cloud_xyz.from_array(point_cloud_array)
    return point_cloud_xyz

    # pcd = open3d.io.read_point_cloud("/Users/seanngpack/Programming Stuff/Projects/scanner_files/cloud.pcd") # Read the point cloud
    # open3d.visualization.draw_geometries([pcd]) # Visualize the point cloud
