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


def visualize_from_file(path, *args):
    '''Visualize a pointcloud given file path

    Args:
        path (str): path to the pointcloud you want to visualize

    '''

    point_cloud = pcl.load(path)
    viewer = pcl.pcl_visualization.PCLVisualizering('cloud visualizer yo')
    viewer.AddPointCloud(point_cloud, b'scene_cloud', 0)
    count=0
    for arg in args:
        arg = pcl.load(arg)
        viewer.AddPointCloud(arg, b'%b' %bytes(count), 0)
        count+=1

    v = True
    while v:
        v = not(viewer.WasStopped())
        viewer.SpinOnce()
        time.sleep(0.01)


# visualize_from_file('/Users/seanngpack/Programming Stuff/Projects/scanner_files/5/0.pcd',
#                     '/Users/seanngpack/Programming Stuff/Projects/scanner_files/5/10.pcd',
#                     '/Users/seanngpack/Programming Stuff/Projects/scanner_files/5/20.pcd',
#                     '/Users/seanngpack/Programming Stuff/Projects/scanner_files/5/30.pcd',
#                     '/Users/seanngpack/Programming Stuff/Projects/scanner_files/5/40.pcd',
#                     '/Users/seanngpack/Programming Stuff/Projects/scanner_files/5/50.pcd',
#                     '/Users/seanngpack/Programming Stuff/Projects/scanner_files/5/60.pcd',
#                     '/Users/seanngpack/Programming Stuff/Projects/scanner_files/5/70.pcd',
#                     '/Users/seanngpack/Programming Stuff/Projects/scanner_files/5/80.pcd')

# visualize_from_file('/Users/seanngpack/Programming Stuff/Projects/scanner_files/8/registered.pcd')
# visualize_from_file('/Users/seanngpack/Programming Stuff/Projects/scanner_files/8/clipped/0.pcd')