import cv2

import numpy as np
import pyrealsense2 as rs
import os
import pcl
import shutil


def make_clean_folder(path_folder):
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)
    else:
        user_input = input("%s not empty. Overwrite? (y/n) : " % path_folder)
        if user_input.lower() == "y":
            shutil.rmtree(path_folder)
            os.makedirs(path_folder)
        else:
            exit()


def record_rgbd():
    # make_clean_folder("../data/realsense/")

    pipeline = rs.pipeline()

    config = rs.config()
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

    profile = pipeline.start(config)

    depth_sensor = profile.get_device().first_depth_sensor()
    depth_sensor.set_option(
        rs.option.visual_preset, 3
    )  # Set high accuracy for depth sensor
    depth_scale = depth_sensor.get_depth_scale()

    clipping_distance_in_meters = 1
    clipping_distance = clipping_distance_in_meters / depth_scale


    try:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        if not depth_frame:
            raise RuntimeError("Could not acquire depth frame")

        depth_image = np.asanyarray(depth_frame.get_data())
        
        # convert to meters using depth scale
        depth_image = depth
        print(depth_image.shape)
        print(np.amax(depth_image))
        print(type(depth_image[0][0]))

        

        point_cloud_xyz = pcl.PointCloud()
        point_cloud_xyz.from_array(depth_image)
        print(point_cloud_xyz)

        # imageio.imwrite("../data/realsense/depth.png", depth_image)
        # imageio.imwrite("../data/realsense/rgb.png", color_image)

    finally:
        pipeline.stop()

    return depth_image


if __name__ == "__main__":
    record_rgbd()