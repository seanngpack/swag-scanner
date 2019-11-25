'''Visualization tools

'''

import pcl
import pcl.pcl_visualization
import time

def visualize(point_cloud_xyz):
    '''Visualize a pointcloud 

    '''
    
    viewer = pcl.pcl_visualization.PCLVisualizering('hello')
    pccolor = pcl.pcl_visualization.PointCloudColorHandleringCustom(
        point_cloud_xyz, 255, 255, 255)
    viewer.AddPointCloud_ColorHandler(point_cloud_xyz, pccolor)

    v = True
    while v:
        v = not(viewer.WasStopped())
        viewer.SpinOnce()
        time.sleep(0.01)