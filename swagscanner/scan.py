'''Entry point into the application

'''

import cv2
import numpy as np
import pcl
import swagscanner.processing.depth as process_depth
from swagscanner.scanner.arduino import Arduino
from swagscanner.scanner.camera import Camera
import threading


class SwagScanner():
    '''Scanner system

    '''

    def __init__(self):
        self.arduino = Arduino()
        self.camera = Camera()

    def get_pointcloud(self):
        '''Fetch a pointcloud

        '''

        pointcloud = process_depth.get_pointcloud(self.camera.get_depth_frame(),
                                                  self.camera.depth_intrinsics,
                                                  self.camera.depth_scale)
        return pointcloud


def main():
    # TODO: instantiate arduino
    # TODO: grab depth
    # TODO: convert to pointcloud
    # TODO: keep rotating arduino
    # TODO: keep grabbing depth
    # TODO: continue converting to pointcloud
    # TODO: stitch them together

    scanner = SwagScanner()
    scanner.get_pointcloud()


if __name__ == "__main__":
    main()
