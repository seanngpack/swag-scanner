import numpy as np
import os
import pcl


def segment_plane(cloud, threshold=0.005):
    '''Take in a pointcloud and remove the ground plane

    Args:
        cloud (PointCloudXYZ): the cloud you want to segment
        theshold (float): the distance threshold of ransac segmentation

    Returns:
        The pointcloud without the ground plane

    '''

    seg = cloud.make_segmenter()
    # Optional
    seg.set_optimize_coefficients(True)
    # Mandatory
    seg.set_model_type(pcl.SACMODEL_PLANE)
    seg.set_method_type(pcl.SAC_RANSAC)
    seg.set_distance_threshold(threshold)

    inliers, model = seg.segment()

    # make the plane
    # plane = create_plane(indices=inliers, cloud=cloud)

    # delete the plane from the source cloud
    cloud_array = np.delete(cloud.to_array(), inliers, 0)
    cloud = pcl.PointCloud()
    cloud.from_array(cloud_array)

    return cloud


if __name__ == "__main__":
    cloud = pcl.load(
        '/Users/seanngpack/Programming Stuff/Projects/scanner_files/9/filtered/0.pcd')
    segment_plane(cloud)
