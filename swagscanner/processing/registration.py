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

    def __init__(self, file_saver=None, folder_path=None):
        if file_saver is None:
            self.file_saver = FileSaver(folder_path=folder_path)
            self.folder_path = folder_path
        else:
            self.file_saver = file_saver

    def merge_pair_clouds(self, source, target):
        '''Uses ICP algorithm to find correspondence between two clouds.
        Note: for incrementally iterating through pairs of clouds
        you want to transform the clouds with the first cloud frame,
        so set the estimated cloud to the source cloud in each iteration

        Args:
            source (PointCloud): input cloud
            target (PointCloud): target cloud

        Returns: the merge clouds

        '''

        icp = pcl.PointCloud().make_IterativeClosestPoint()
        print('made object')
        converged, transf, estimate, fitness = icp.icp(
            source, target, max_iter=100)

        print('has converged:' + str(converged) + ' score: ' + str(fitness))
        print(str(transf))
        print(estimate)

        return estimate

    def merge_all_clouds(self):
        def floatify_name(name):
            name = re.match(r'.*(?=\.)', name).group()
            return float(name)
        clouds = sorted([f for f in os.listdir(self.folder_path)
                         if f.endswith('.pcd')], key=floatify_name)
        cloud_list = []
        for cloud in clouds:
            cloud_list.append(os.path.join(self.folder_path, cloud))

        print(cloud_list)
        print('registration in progress...')
        
        source = pcl.load(cloud_list[0])
        for index in range(3):
            target = pcl.load(cloud_list[index+1])
            estimation = self.merge_pair_clouds(source, target)
            source = estimation
        viewer.visualize(source)
        self.file_saver.save_point_cloud(source,
                                    'registered',
                                    save_path='/Users/seanngpack/Programming Stuff/Projects/scanner_files/8/registered')


registration = Registration(
    folder_path='/Users/seanngpack/Programming Stuff/Projects/scanner_files/8/filtered')
registration.merge_all_clouds()
# source = pcl.load('/Users/seanngpack/Programming Stuff/Projects/scanner_files/8/filtered/0.pcd')
# print('loaded source')
# target = pcl.load('/Users/seanngpack/Programming Stuff/Projects/scanner_files/8/filtered/18.pcd')
# print('loaded target')
# registered = registration.merge_pair_clouds(source, target)

# target2 = pcl.load('/Users/seanngpack/Programming Stuff/Projects/scanner_files/8/filtered/36.pcd')
# registered = registration.merge_pair_clouds(registered, target2)

# viewer.visualize(registered)
