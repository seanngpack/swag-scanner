import os
import pcl
import re
from swagscanner.utils.file import FileSaver


class Filtering():
    ''' provide the tools for filtering

    '''

    def __init__(self, raw_depth_path, file_saver=None, folder_path=None):
        if file_saver is None:
            self.file_saver = FileSaver(folder_path=folder_path)
            self.folder_path = folder_path
        else:
            self.file_saver = file_saver
        self.raw_depth_path = raw_depth_path

    def voxel_grid_filtering(self, point_cloud, file_name):

        sor = point_cloud.make_voxel_grid_filter()
        sor.set_leaf_size(0.01, 0.01, 0.01)
        point_cloud_filtered = sor.filter()

        print(self.file_saver.save_point_cloud(point_cloud=point_cloud_filtered,
                                               file_name=file_name))

    def filter_all(self):
        '''Filter all the pointcloud files inside the clipped folder
        then save them to the filtered folder

        '''

        def floatify_name(name):
            name = re.match(r'.*(?=\.)', name).group()
            return float(name)
        clouds = sorted([f for f in os.listdir(self.raw_depth_path)
                         if f.endswith('.pcd')], key=floatify_name)

        cloud_list = []
        for cloud in clouds:
            cloud_list.append(os.path.join(self.raw_depth_path, cloud))

        # filter everything
        for cloud in cloud_list:
            file_name = os.path.splitext(os.path.basename(cloud))[0]
            # print(file_name)
            cloud = pcl.load(cloud)
            self.voxel_grid_filtering(cloud, file_name)


def main():
    filtering = Filtering(raw_depth_path='/Users/seanngpack/Programming Stuff/Projects/scanner_files/8/clipped',
                          folder_path='/Users/seanngpack/Programming Stuff/Projects/scanner_files/8/filtered')
    filtering.filter_all()


if __name__ == "__main__":
    main()
