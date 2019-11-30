'''Visualization tools

'''

import pcl
import pcl.pcl_visualization
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


def visualize_from_file(path):
    '''Visualize a pointcloud given file path

    Args:
        path (str): path to the pointcloud you want to visualize

    '''

    point_cloud = pcl.load(path)
    viewer = pcl.pcl_visualization.PCLVisualizering('cloud visualizer yo')
    pccolor = pcl.pcl_visualization.PointCloudColorHandleringCustom(
        point_cloud, 255, 255, 255)
    viewer.AddPointCloud_ColorHandler(point_cloud, pccolor)

    v = True
    while v:
        v = not(viewer.WasStopped())
        viewer.SpinOnce()
        time.sleep(0.01)
