import os
import pcl
import swagscanner.processing.segmentation as segmentation
from swagscanner.utils.file import FileSaver


class Filtering():
    ''' provide the tools for filtering

    '''

    def __init__(self, input_folder_path, write_folder_path, file_saver=None):
        self.input_folder_path = input_folder_path
        if file_saver is None:
            self.write_folder_path = write_folder_path
            self.file_saver = FileSaver(folder_path=self.write_folder_path)

        else:
            self.write_folder_path = write_folder_path
            self.file_saver = file_saver
            self.file_saver.write_folder_path = write_folder_path

    def voxel_grid_filtering(self, point_cloud, file_name, leaf_size=0.0005):
        '''Apply voxel grid filtering to downsample point cloud to more manageable size

        Args:
            point_cloud (PointCloud): cloud you want to downsample
            file_name (str): path to the cloud you want to downsample
            leaf_size (float): leaf size for downsampling

        '''

        sor = point_cloud.make_voxel_grid_filter()
        sor.set_leaf_size(leaf_size, leaf_size, leaf_size)
        point_cloud_filtered = sor.filter()

        # TODO: THIS IS HACKY, PUT THE SEGMENTATION IN ITS OWN THING!!
        # TODO: log this
        point_cloud_filtered = segmentation.segment_plane(point_cloud_filtered)

        # save dis
        self.file_saver.save_point_cloud(point_cloud=point_cloud_filtered,
                                         file_name=file_name)

    def filter_all(self):
        '''Filter all the pointcloud files inside the clipped folder
        then save them to the filtered folder

        '''

        cloud_list = self.file_saver.get_cloud_list(self.input_folder_path)

        # filter everything
        for cloud in cloud_list:
            file_name = os.path.splitext(os.path.basename(cloud))[0]
            cloud = pcl.load(cloud)
            self.voxel_grid_filtering(cloud, file_name)


def main():
    filtering = Filtering(input_folder_path='/Users/seanngpack/Programming Stuff/Projects/scanner_files/9/',
                          write_folder_path='/Users/seanngpack/Programming Stuff/Projects/scanner_files/9/filtered')
    filtering.filter_all()


if __name__ == "__main__":
    main()
