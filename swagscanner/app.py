#!/usr/bin/env python
import cv2
import freenect
import numpy as np
import pcl

from swagscanner.acquisition.grab_depth import grab_depth
import swagscanner.processing.depth_processing as dp
import swagscanner.visualization.visualization_tools as vt


def main():
    depth_map = grab_depth()
    point_cloud = dp.create_pointcloudxyz_vectorized(depth_map)
    vt.visualize(point_cloud)


if __name__ == "__main__":
    main()
