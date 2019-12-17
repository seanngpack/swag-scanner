import numpy as np
import pcl
from pcl import IterativeClosestPoint, GeneralizedIterativeClosestPoint
import os
from pathlib import Path
import re
from swagscanner.utils.file import FileSaver
import swagscanner.processing.segmentation as segmentation
import swagscanner.visualization.viewer as viewer
import open3d as o3d


class Registration():
    '''Provides tools for pointcloud registration

    '''

    def __init__(self, input_folder_path, write_folder_path, file_saver=None, generate_folder=True):
        if file_saver is None:
            self.input_folder_path = input_folder_path
            self.write_folder_path = write_folder_path
            self.file_saver = FileSaver(folder_path=self.write_folder_path, generate_folder=generate_folder)

        else:
            self.input_folder_path = input_folder_path
            self.file_saver = file_saver
            self.file_saver.folder_path = self.write_folder_path

    def register_pair_clouds(self, source, target):
        '''Uses ICP algorithm to find correspondence between two clouds.
        Note: for incrementally iterating through pairs of clouds
        you want to transform the clouds with the first cloud frame,
        so set the estimated cloud to the source cloud in each iteration

        Args:
            source (PointCloud): input cloud
            target (PointCloud): target cloud

        Returns: the registered clouds

        '''

        icp = source.make_IterativeClosestPoint()
        converged, transf, estimate, fitness = icp.icp(
            source, target, max_iter=1000)

        print('has converged:' + str(converged) + ' score: ' + str(fitness))

        print(str(transf))
        print(estimate)

        # apply transformation from target cloud to map back to source cloud frame
        result = self.map_cloud_operation(target, transf, np.dot)

        return result, transf

    def register_pair_clouds_o3d(self, source, target, threshold = 0.0001):
        '''Uses ICP algorithm to find correspondence between two clouds.
        Note: for incrementally iterating through pairs of clouds
        you want to transform the clouds with the first cloud frame,
        so set the estimated cloud to the source cloud in each iteration

        Args:
            source (PointCloud): input cloud
            target (PointCloud): target cloud

        Returns: the registered clouds

        '''      

        # convert PointCloudXYZ to PointCloud
        reg_p2p = o3d.registration.registration_icp(
                source, target, threshold, np.identity(4),
                o3d.registration.TransformationEstimationPointToPoint())

        transf = np.asarray(reg_p2p.transformation, dtype=np.float32)
        print(transf)
        
        return transf

    def register_all_clouds_o3d(self):
        '''register all the pointclouds found in the given folder

        Returns: the registered clouds

        '''

        cloud_list = self.file_saver.get_cloud_list(self.input_folder_path)

        print('registration in progress...')

        global_transform = np.identity(4)
        threshold = 0.001
        # perform iterative registration
        for index in range(len(cloud_list)-1):
            source = o3d.io.read_point_cloud(cloud_list[0])
            target = o3d.io.read_point_cloud(cloud_list[index+1])
            target_pcl = pcl.load(cloud_list[index+1])

            transf = self.register_pair_clouds_o3d(source, target)
            transf_inv = np.linalg.inv(transf)
            # print(transf_inv)

            result = self.map_cloud_operation(target_pcl, global_transform, np.dot)

            global_transform *= transf_inv
            print(global_transform)

            self.file_saver.save_point_cloud(point_cloud=result,
                                             file_name=str(index))
        return source

    def register_all_clouds(self):
        '''register all the pointclouds found in the given folder

        Returns: the registered clouds

        '''

        cloud_list = self.file_saver.get_cloud_list(self.input_folder_path)

        print('registration in progress...')

        global_transform = np.identity(4)
        # perform iterative registration
        for index in range(len(cloud_list)-1):
            source = pcl.load(cloud_list[0])
            target = pcl.load(cloud_list[index+1])

            estimation, pair_transform = self.register_pair_clouds(
                source, target)

            result = self.map_cloud_operation(estimation, global_transform, np.dot)


            # update the global transformation
            global_transform *= pair_transform
            # print(pair_transform)
            # print(global_transform)

            self.file_saver.save_point_cloud(point_cloud=result,
                                             file_name=str(index))
        return source

    def map_cloud_operation(self, cloud, matrix, func):
        '''Allows you to apply a matrix operation on a pointcloud

        Args:
            cloud(PointCloudXYZ): the pointcloud you want to modify
            matrix (array): the matrix you want to use to apply on the cloud
            func (function): the function you want to map

        Returns:
            the modified cloud

        '''

        cloud_array = cloud.to_array()
        # add ones column
        cloud_array = np.hstack(
            (cloud_array, np.ones((cloud_array.shape[0], 1))))
        
        # apply the function
        cloud_array = func(cloud_array, matrix)

        # trim off the last column and cast the array to float32
        cloud_array = cloud_array[:, :3]
        cloud_array = cloud_array.astype(np.float32)

        result = pcl.PointCloud()
        result.from_array(cloud_array)
        return result


def main():
    registration = Registration(
        input_folder_path='/Users/seanngpack/Programming Stuff/Projects/scanner_files/9/filtered',
        write_folder_path='/Users/seanngpack/Programming Stuff/Projects/scanner_files/9/registration')
    # registered = registration.register_all_clouds_o3d()
    
    source_pcl = pcl.load(
        '/Users/seanngpack/Programming Stuff/Projects/scanner_files/9/filtered/0.pcd')
    target_pcl = pcl.load(
        '/Users/seanngpack/Programming Stuff/Projects/scanner_files/9/filtered/18.pcd')
    source = o3d.io.read_point_cloud('/Users/seanngpack/Programming Stuff/Projects/scanner_files/9/filtered/0.pcd')
    target = o3d.io.read_point_cloud('/Users/seanngpack/Programming Stuff/Projects/scanner_files/9/filtered/18.pcd')
    # # print(target.size)
    print('registering...')
    transf = registration.register_pair_clouds_o3d(source, target)
    # print(transf)
    transf_inv = np.linalg.inv(transf)
    # print(transf_inv)

    registered = registration.map_cloud_operation(target_pcl, transf_inv, np.dot)
    viewer.visualize(source=source_pcl, registered=registered)
    

    # viewer.visualize_from_folder(
    #     '/Users/seanngpack/Programming Stuff/Projects/scanner_files/9/registration')


if __name__ == "__main__":
    main()
