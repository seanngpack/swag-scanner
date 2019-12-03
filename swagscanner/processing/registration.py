import pcl
from pcl import IterativeClosestPoint, GeneralizedIterativeClosestPoint
import os
from pathlib import Path
import re
from swagscanner.utils.file import FileSaver
import swagscanner.visualization.viewer as viewer


class Registration():
    '''Provides tools for pointcloud registration

    '''

    def __init__(self, folder_path, file_saver=None):
        if file_saver is None:
            self.folder_path = folder_path
            self.file_saver = FileSaver(folder_path=self.folder_path)
            
        else:
            self.folder_path = folder_path
            self.file_saver = file_saver
            self.file_saver.folder_path = folder_path

    def register_pair_clouds(self, source, target):
        '''Uses ICP algorithm to find correspondence between two clouds.
        Note: for incrementally iterating through pairs of clouds
        you want to transform the clouds with the first cloud frame,
        so set the estimated cloud to the source cloud in each iteration

        Args:
            source (PointCloud): input cloud
            target (PointCloud): target cloud

        Returns: the merge clouds

        '''

        icp = source.make_IterativeClosestPoint()
        print('made object')
        converged, transf, estimate, fitness = icp.icp(
            source, target, max_iter=3)

        print('has converged:' + str(converged) + ' score: ' + str(fitness))
        print(str(transf))
        print(estimate)

        return estimate

    def register_all_clouds(self):
        '''register all the pointclouds found in the given folder

        '''

        cloud_list = self.file_saver.get_cloud_list(self.folder_path)

        print('registration in progress...')

        # perform iterative registration
        source = pcl.load(cloud_list[0])
        for index in range(len(cloud_list)-1):
            target = pcl.load(cloud_list[index+1])
            estimation = self.register_pair_clouds(source, target)
            source = estimation
        viewer.visualize(source)
        self.file_saver.save_point_cloud(source,
                                         'registered',
                                         save_path='/Users/seanngpack/Programming Stuff/Projects/scanner_files/8/registered')


def main():
    registration = Registration(
        folder_path='/Users/seanngpack/Programming Stuff/Projects/scanner_files/8/filtered')
    registration.register_all_clouds()


if __name__ == "__main__":
    main()
