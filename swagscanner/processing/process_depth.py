import freenect
import cv2
import pcl
import pcl.pcl_visualization
import numpy as np
import open3d

depth_to_meters_table = {
    num: (1.0 / (num * -0.0030711016 + 3.3309495161)) for num in range(2048)}


def depth_to_pointxyz(x: int, y: int, depth: int):

    # focal length x and y directions
    fx_d = 1.0 / 5.9421434211923247e+02
    fy_d = 1.0 / 5.9104053696870778e+02
    # principal points
    cx_d = 3.3930780975300314e+02
    cy_d = 2.4273913761751615e+02
    depth_meters = depth_to_meters_table[depth]

    point = np.empty([3], dtype=np.float32)

    point[0] = (x - cx_d) * depth_meters * fx_d  # x
    point[1] = (y - cy_d) * depth_meters * fy_d  # y
    point[2] = depth_meters                      # z
    return point


def create_pointcloudxyz(depth_map):

    point_cloud_array = np.empty((307200, 3), dtype=np.float32)
    for index, value in np.ndenumerate(depth_map):
        x = index[0]
        y = index[1]
        (x, y, z) = depth_to_pointxyz(x, y, value)
        point_cloud_array[sum(index)][0] = x
        point_cloud_array[sum(index)][1] = y
        point_cloud_array[sum(index)][2] = z

    print(point_cloud_array[1000:1001])
    print(point_cloud_array[15000:15003])
    
    point_cloud_xyz = pcl.PointCloud()
    point_cloud_xyz.from_array(point_cloud_array)


    # path = '/Users/seanngpack/Programming Stuff/Projects/scanner_files/'
    # pcl.save(point_cloud_xyz, path + 'cloud.pcd')

    viewer = pcl.pcl_visualization.PCLVisualizering('hello')
    pccolor = pcl.pcl_visualization.PointCloudColorHandleringCustom(
        point_cloud_xyz, 255, 255, 255)
    viewer.AddPointCloud_ColorHandler(point_cloud_xyz, pccolor)
    

    v = True
    while v:
        v = not(viewer.WasStopped())
        viewer.SpinOnce()
        # sleep(0.01)

    # pcd = open3d.io.read_point_cloud("/Users/seanngpack/Programming Stuff/Projects/scanner_files/cloud.pcd") # Read the point cloud
    # open3d.visualization.draw_geometries([pcd]) # Visualize the point cloud     
    