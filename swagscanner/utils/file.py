import pcl
import os
from pathlib import Path
import re
from swagscanner.utils.config import Config


class FileSaver():
    '''Provides tools for saving pointcloud files

    '''

    def __init__(self, folder_path=None):
        if folder_path is None:
            self.folder_path = self.get_default_folder_path()
        else:
            self.folder_path = folder_path
            if not os.path.exists(folder_path):
                os.makedirs(self.folder_path)
        self.saved_files = []

    def get_default_folder_path(self):
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

    def get_cloud_list(self, folder_path):
        '''Get the paths of all the pointclouds in the folder

        Args:
            folder_path (str): path to the folder containing the pointclouds

        Returns:
            List of paths of the pointclouds in the folder
            
        '''

        def floatify_name(name):
            name = re.match(r'.*(?=\.)', name).group()
            return float(name)
        clouds = sorted([f for f in os.listdir(folder_path)
                         if f.endswith('.pcd')], key=floatify_name)

        cloud_list = []
        for cloud in clouds:
            cloud_list.append(os.path.join(folder_path, cloud))
        
        return cloud_list

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

        if save_path is None:
            save_path = f'{self.folder_path}/{file_name}.pcd'
        else:
            save_path=f'{save_path}.pcd'
        pcl.save(point_cloud, save_path)
        self.saved_files.append(save_path)
        return save_path
