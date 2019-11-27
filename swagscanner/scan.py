'''Entry point into the application

'''

import cv2
import numpy as np
import pcl
import swagscanner.processing.depth as depth
from swagscanner.scanner.arduino import Arduino
from swagscanner.scanner.camera import Camera


def main():
    # TODO: instantiate arduino
    # TODO: grab depth
    # TODO: convert to pointcloud
    # TODO: keep rotating arduino
    # TODO: keep grabbing depth
    # TODO: continue converting to pointcloud
    # TODO: stitch them together

    d435 = Camera()
    depth_intrinsics = d435.depth_intrinsics
    depth_scale = d435.depth_scale
    depth_frame = d435.get_depth_frame()
    depth.get_pointcloud(depth_frame, depth_intrinsics, depth_scale)


if __name__ == "__main__":
    main()
