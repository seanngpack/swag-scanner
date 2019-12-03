import os
import pcl
from swagscanner.utils.file import FileSaver


class Filtering():
    ''' provide the tools for filtering

    '''

    def __init__(self, raw_depth_path, folder_path, file_saver=None):
        self.raw_depth_path = raw_depth_path
        if file_saver is None:
            self.folder_path = folder_path
            self.file_saver = FileSaver(folder_path=self.folder_path)

        else:
            self.folder_path = folder_path
            self.file_saver = file_saver
            self.file_saver.folder_path = folder_path

    def voxel_grid_filtering(self, point_cloud, file_name):

        sor = point_cloud.make_voxel_grid_filter()
        sor.set_leaf_size(0.001, 0.001, 0.001)
        point_cloud_filtered = sor.filter()

        self.file_saver.save_point_cloud(point_cloud=point_cloud_filtered,
                                         file_name=file_name)
        # TODO: log this

    def filter_all(self):
        '''Filter all the pointcloud files inside the clipped folder
        then save them to the filtered folder

        '''

        cloud_list = self.file_saver.get_cloud_list(self.raw_depth_path)

        # filter everything
        for cloud in cloud_list:
            file_name = os.path.splitext(os.path.basename(cloud))[0]
            cloud = pcl.load(cloud)
            self.voxel_grid_filtering(cloud, file_name)


def main():
    filtering = Filtering(raw_depth_path='/Users/seanngpack/Programming Stuff/Projects/scanner_files/8/clipped',
                          folder_path='/Users/seanngpack/Programming Stuff/Projects/scanner_files/8/filtered')
    filtering.filter_all()


if __name__ == "__main__":
    main()
