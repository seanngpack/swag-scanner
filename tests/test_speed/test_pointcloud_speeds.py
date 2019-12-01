import unittest

import pcl
import timeit
import numpy as np
import numpy.testing as npt

# import swagscanner.acquisition.grab_depth as gd
# import swagscanner.processing.depth_processing as dp


depth_to_meters_table = {
    num: (1.0 / (num * -0.0030711016 + 3.3309495161)) for num in range(2048)}
zeros_map = np.empty([720, 1280])
random_map = np.random.randint(2048, size=(720, 1280))


def depth_to_real_world_vectorized(depth_map):
    fx_d = 1.0 / 5.9421434211923247e+02
    cx_d = 3.3930780975300314e+02
    fy_d = 1.0 / 5.9104053696870778e+02
    cy_d = 2.4273913761751615e+02

    depth_array = np.empty((921600, 3))
    x_array = np.tile(np.arange(1280), 720)
    y_array = np.repeat(np.arange(720), 1280)

    # perform calculations to convert to real world coordinates
    depth_array = [depth_to_meters_table[depth]
                   for depth in depth_map.ravel().tolist()]
    x_array = (x_array - cx_d) * depth_array * fx_d
    y_array = (y_array - cy_d) * depth_array * fy_d

    return x_array, y_array, depth_array


def create_pointcloudxyz_vectorized(depth_map):

    x_array, y_array, depth_array = depth_to_real_world_vectorized(depth_map)

    # combine the three arrays into a (307200, 3) array
    point_cloud_array = np.vstack((x_array, y_array, depth_array)).T
    point_cloud_array = np.asarray(point_cloud_array, dtype=np.float32)

    # Make the pointcloud
    point_cloud_xyz = pcl.PointCloud()
    point_cloud_xyz.from_array(point_cloud_array)
    return point_cloud_xyz


def depth_to_pointxyz(x: int, y: int, depth: int):

    # focal length x and y directions
    fx_d = 1.0 / 5.9421434211923247e+02
    fy_d = 1.0 / 5.9104053696870778e+02
    # principal points
    cx_d = 3.3930780975300314e+02
    cy_d = 2.4273913761751615e+02
    depth_meters = depth_to_meters_table[depth]

    point = np.empty([3], dtype=np.float32)

    point[0] = (x - cx_d) * depth_meters * fx_d  # x
    point[1] = (y - cy_d) * depth_meters * fy_d  # y
    point[2] = depth_meters                      # z
    return point


def create_pointcloudxyz(depth_map):

    point_cloud_array = np.empty((921600, 3), dtype=np.float32)
    i = 0
    for index, value in np.ndenumerate(depth_map):
        y = index[0]
        x = index[1]

        (x, y, z) = depth_to_pointxyz(x, y, value)
        point_cloud_array[i][0] = x
        point_cloud_array[i][1] = y
        point_cloud_array[i][2] = z

        i += 1

    point_cloud_xyz = pcl.PointCloud()
    point_cloud_xyz.from_array(point_cloud_array)
    return point_cloud_xyz


if __name__ == '__main__':

    flatten_create_pointcloudxyz_time = timeit.timeit(
        lambda: create_pointcloudxyz(zeros_map), number=40)
    print(
        f'the time to create one pointcloud is: {flatten_create_pointcloudxyz_time/40} seconds')

    vectorized_create_pointcloudxyz_time = timeit.timeit(
        lambda: create_pointcloudxyz_vectorized(zeros_map), number=40)
    print(
        f'the time to create one pointcloud with vectorization is: {vectorized_create_pointcloudxyz_time/40} seconds')
