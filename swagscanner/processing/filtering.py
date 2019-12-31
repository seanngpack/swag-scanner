import os
import pcl
import swagscanner.processing.segmentation as segmentation
from swagscanner.utils.file import FileSaver


class Filtering():
    ''' provide the tools for filtering

    '''

    def __init__(self, input_folder_path, write_folder_path, file_saver=None, leaf_size=.0005):
        self.input_folder_path = input_folder_path
        self.leaf_size = leaf_size
        if file_saver is None:
            self.write_folder_path = write_folder_path
            self.file_saver = FileSaver(folder_path=self.write_folder_path)

        else:
            self.write_folder_path = write_folder_path
            self.file_saver = file_saver
            self.file_saver.write_folder_path = write_folder_path

    def segment_plane(self, point_cloud):
        '''Remove plane from target cloud and return the cloud

        Args:
            point_cloud (PointCloud): the target cloud you want to remove plane from

        Returns:
            The cloud without the plane

        '''

        segmented_cloud = segmentation.segment_plane(point_cloud)
        return segmented_cloud

    def voxel_grid_filtering(self, point_cloud, file_name):
        '''Apply voxel grid filtering to downsample point cloud to more manageable size

        Args:
            point_cloud (PointCloud): cloud you want to downsample
            file_name (str): path to the cloud you want to downsample
            leaf_size (float): leaf size for downsampling

        '''

        sor = point_cloud.make_voxel_grid_filter()
        sor.set_leaf_size(self.leaf_size, self.leaf_size, self.leaf_size)
        point_cloud_filtered = sor.filter()

        return point_cloud_filtered

    def filter_all(self):
        '''Filter all the pointcloud files inside the main folder
        then save them to the filtered folder

        '''

        cloud_list = self.file_saver.get_cloud_list(self.input_folder_path)

        # filter everything
        for cloud in cloud_list:
            file_name = os.path.splitext(os.path.basename(cloud))[0]
            cloud = pcl.load(cloud)
            filtered_cloud = self.voxel_grid_filtering(cloud, file_name)
            segmented_cloud = self.segment_plane(filtered_cloud)

            # save dis
            self.file_saver.save_point_cloud(point_cloud=segmented_cloud,
                                             file_name=file_name)


def main():
    filtering = Filtering(input_folder_path='/Users/seanngpack/Programming Stuff/Projects/scanner_files/9/',
                          write_folder_path='/Users/seanngpack/Programming Stuff/Projects/scanner_files/9/filtered',
                          leaf_size=.0005)
    filtering.filter_all()


if __name__ == "__main__":
    main()
