#!/usr/bin/env python
import freenect
import cv2
import pcl
import numpy as np

from swagscanner.acquisition.grab_depth import grab_depth
import swagscanner.processing.point_cloud_tools as point_cloud_tools


def main():
    depth_map = grab_depth()
    print(depth_map[5][400])
    # print(depth.shape)
    # point_cloud = point_cloud_tools.create_pointcloudxyz(depth_map)
    
    # cloud = pcl.PointCloud()
    # print(type(cloud))
    # # cloud.from_array(np.array([[1,2,3],[3,4,5], [3,5,6]], dtype=np.float32))
    # print(cloud.height)
    # print(cloud.width)



if __name__ == "__main__":
    main()
