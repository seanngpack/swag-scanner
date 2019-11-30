'''Tools to deal with file handling and processing

'''

import pcl
import os
from pathlib import Path

from swagscanner.utils.config import Config


class FileSaver():
    '''Provides tools for saving pointcloud files

    '''

    def __init__(self):
        self.folder_path = self.get_folder_path()
        self.saved_files = []

    def get_folder_path(self):
        '''Get the folder path we should save our scan to and make the directory

        Returns:
            The folder path

        '''

        folder_path = Config.consts("PATHS", "SAVE_PATH")
        # print only the folders in the folder path
        dirs = next(os.walk(folder_path))[1]
        # name the folder to store the scan (1 + the latest folder name)
        folder_name = str(len(dirs) + 1)
        folder_path = Path(folder_path) / folder_name

        # make the folder path
        os.makedirs(folder_path)

        return folder_path

    def save_point_cloud(self, point_cloud, file_name, save_path=None):
        '''Save the pointcloud to a hardcoded location, otherwise specified
        by function argument

        Args:
            point_cloud (PointcloudXYZ): a pointcloud
            file_name (str): file name of the thing you want to save
            save_path (str): optional argument if you want to save somewhere else

        Returns:
            The path of the file saved

        '''

        save_path = f'{self.folder_path}/{file_name}.pcd'
        pcl.save(point_cloud, save_path)
        self.saved_files.append(save_path)
        return save_path
