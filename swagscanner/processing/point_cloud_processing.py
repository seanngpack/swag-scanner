import datetime
import pcl


def save_pointcloud(pointcloud_xyz):
    current_time = datetime.datetime.now()
    save_path = (f'/Users/seanngpack/Programming Stuff/Projects/'
                 f'scanner_files/cloud{current_time.day}-'
                 f'{current_time.hour}-{current_time.minute}-{current_time.second}.pcd')
    pcl.save(pointcloud_xyz, save_path)
