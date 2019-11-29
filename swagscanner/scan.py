'''Entry point into the application

'''

import cv2
import numpy as np
import pcl
import swagscanner.visualization.viewer as viewer
from swagscanner.processing.depth import DepthProcessor
from swagscanner.scanner.arduino import Arduino
from swagscanner.scanner.d435 import D435
from swagscanner.scanner.kinect import Kinect
import threading


class SwagScanner():
    '''Scanner system

    '''

    def __init__(self, camera=D435()):
        # self.arduino = Arduino()
        self.camera = camera
        self.depth_processor = DepthProcessor().initialize_processor(
            camera=self.camera, fast=True)

    def get_pointcloud(self):
        '''Fetch a pointcloud

        '''

        pointcloud = self.depth_processor.get_pointcloud()
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
    point_cloud = scanner.get_pointcloud()
    viewer.visualize(point_cloud)


if __name__ == "__main__":
    main()
