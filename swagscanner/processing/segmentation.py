import numpy as np
import os
import pcl

import swagscanner.visualization.viewer as viewer


def segment_plane(cloud):
    '''Take in a pointcloud and remove the ground plane

    Args:
        cloud (PointCloudXYZ): the cloud you want to segment

    Returns:
        The pointcloud without the ground plane

    '''

    seg = cloud.make_segmenter()
    # Optional
    seg.set_optimize_coefficients(True)
    # Mandatory
    seg.set_model_type(pcl.SACMODEL_PLANE)
    seg.set_method_type(pcl.SAC_RANSAC)
    seg.set_distance_threshold(0.005)

    inliers, model = seg.segment()

    # make the plane
    # plane = create_plane(indices=inliers, cloud=cloud)

    # delete the plane from the source cloud
    cloud_array = np.delete(cloud.to_array(), inliers, 0)
    cloud = pcl.PointCloud()
    cloud.from_array(cloud_array)
    print(cloud_array.shape)

    # viewer.visualize(source=cloud,  )
    return cloud


def get_plane(indices, cloud):
    '''Get the plane cloud from the input cloud

    '''

    # plane_list = np.zeros((len(indices), 3))
    indices = np.asarray(indices)
    plane_list = np.take(cloud_array, indices, axis=0)
    plane_list.astype(np.float32)

    plane = pcl.PointCloud()
    plane.from_array(plane_list)

    return plane


def delete_plane(cloud):
    '''Delete the plane from the source cloud

    Args:
        cloud (PointCloudXYZ): the source pointcloud

    Returns:
        the cloud without the ground plane

    '''
    pass


if __name__ == "__main__":
    cloud = pcl.load(
        '/Users/seanngpack/Programming Stuff/Projects/scanner_files/9/filtered/0.pcd')
    segment_plane(cloud)
