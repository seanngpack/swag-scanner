'''Tools to deal with file handling and processing

'''

import pcl
import datetime

from swagscanner.utils.config import Config


def save_pointcloud(pointcloud_xyz):
    '''Save the pointcloud to a hardcoded location

    Args:
        pointcloud_xyz (PointcloudXYZ): a pointcloud

    Returns:
        None

    '''

    current_time = datetime.datetime.now()
    save_path = ('{Config.consts("PATHS", "SAVE_PATH")}cloud{current_time.day}-'
                 f'{current_time.hour}-{current_time.minute}-{current_time.second}.pcd')
    pcl.save(pointcloud_xyz, save_path)