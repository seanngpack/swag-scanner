'''Visualization tools

'''

import os
import pcl
import pcl.pcl_visualization
import re
import time


def visualize(point_cloud):
    '''Visualize a pointcloud

    Args:
        point_cloud (PointCloudXYZ): the pointcloud you want to visualize

    '''

    # Alternative:
    # viewer.visualize(point_cloud)

    viewer = pcl.pcl_visualization.PCLVisualizering('cloud visualizer yo')
    pccolor = pcl.pcl_visualization.PointCloudColorHandleringCustom(
        point_cloud, 255, 255, 255)
    viewer.AddPointCloud_ColorHandler(point_cloud, pccolor)

    v = True
    while v:
        v = not(viewer.WasStopped())
        viewer.SpinOnce()
        time.sleep(0.01)


def visualize_from_file(path, *args):
    '''Visualize a pointcloud given file path. Can handle multiple file inputs

    Args:
        path (str): path to the pointcloud you want to visualize

    '''

    point_cloud = pcl.load(path)
    viewer = pcl.pcl_visualization.PCLVisualizering('cloud visualizer yo')
    viewer.AddPointCloud(point_cloud, b'scene_cloud', 0)
    count = 0
    for arg in args:
        arg = pcl.load(arg)
        viewer.AddPointCloud(arg, b'%b' % bytes(count), 0)
        count += 1

    v = True
    while v:
        v = not(viewer.WasStopped())
        viewer.SpinOnce()
        time.sleep(0.01)


def visualize_from_folder(folder_path):
    '''Visualize all the pointclouds in a given folder 

    '''
    
    def floatify_name(name):
        name = re.match(r'.*(?=\.)', name).group()
        return float(name)
    clouds = sorted([f for f in os.listdir(folder_path)
                        if f.endswith('.pcd')], key=floatify_name)
    cloud_list = []
    for cloud in clouds:
        cloud_list.append(os.path.join(folder_path, cloud))

    viewer = pcl.pcl_visualization.PCLVisualizering('cloud visualizer yo')
    count = 0

    for cloud in cloud_list:
        cloud = pcl.load(cloud)
        viewer.AddPointCloud(cloud, b'%b' % bytes(count), 0)
        count += 1
    
    v = True
    while v:
        v = not(viewer.WasStopped())
        viewer.SpinOnce()
        time.sleep(0.01)


def main():
    visualize_from_folder('/Users/seanngpack/Programming Stuff/Projects/scanner_files/8/filtered')

if __name__ == "__main__":
    main()
