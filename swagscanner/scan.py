'''Entry point into the application

'''

import cv2
import numpy as np
import pcl
import swagscanner.visualization.viewer as viewer
from swagscanner.utils.file import FileSaver
from swagscanner.processing.depth import DepthProcessor
from swagscanner.processing.filtering import Filtering
from swagscanner.processing.registration import Registration
from swagscanner.scanner.arduino import Arduino
from swagscanner.scanner.d435 import D435
from swagscanner.scanner.kinect import Kinect
import threading
import time


class SwagScanner():
    '''Scanner system

    '''

    def __init__(self, camera=D435(), fast=True, interval=10):
        self.file_saver = FileSaver()
        self.arduino = Arduino()
        self.camera = camera
        self.depth_processor = DepthProcessor().initialize_processor(
            camera=self.camera, fast=fast)
        self.filtering = Filtering(input_folder_path=self.file_saver.folder_path,
                                   write_folder_path=f'{self.file_saver.folder_path}/filtered')
        self.registration = Registration(input_folder_path=f'{self.file_saver.folder_path}/filtered',
                                         write_folder_path=f'{self.file_saver.folder_path}/registration')
        self.interval = interval
        self.latest_point_cloud = None
        self.scanned = {}

    def get_point_cloud(self):
        '''Fetch a pointcloud

        '''

        point_cloud = self.depth_processor.get_pointcloud()
        self.latest_point_cloud = point_cloud
        return point_cloud

    def save_point_cloud(self):
        '''Save the pointcloud to file

        Returns:
            The path of the file saved

        '''

        current_scan = len(self.scanned) * self.interval

        saved = self.file_saver.save_point_cloud(self.latest_point_cloud,
                                                 str(current_scan))

        # deallocate pointcloud stored in memory
        self.latest_point_cloud = None
        self.scanned.update({str(current_scan): saved})
        return saved

    def filter_all_clouds(self):
        '''Filters all the scanned point clouds and writes
        them to a /filtered directory

        '''

        self.filtering.filter_all()

    def register_all_clouds(self):
        '''Register all the point clouds and writes the output
        to a /registered folder

        '''

        self.registration.register_all_clouds_o3d()

    def rotate_table(self):
        ''' rotate the bed

        Returns:
            The amount rotated
            Current position?

        '''

        self.arduino.rotate_table(self.interval)


def main():
    '''Initialize arduino, camera, and scanner objects,
    then grab images, save them, rotate table, and continue until
    fully rotated.

    '''

    scanner = SwagScanner(fast=True, interval=9)

    rotations = int(360/scanner.interval)
    for i in range(rotations):
        scanner.get_point_cloud()
        scanner.save_point_cloud()
        scanner.rotate_table()
        time.sleep(4)
    scanner.filter_all_clouds()
    scanner.register_all_clouds()

    # scanner.get_point_cloud()
    # scanner.save_point_cloud()
    # scanner.rotate_table()

    # viewer.visualize_from_file(scanner.scanned['0'])


if __name__ == "__main__":
    main()
