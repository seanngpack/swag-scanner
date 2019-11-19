import unittest

import numpy as np
import numpy.testing as npt
import timeit

import swagscanner.acquisition.grab_depth as gd
import swagscanner.processing.depth_processing as dp

# depth_map = gd.grab_depth()
zeros_map = np.empty([480, 640])
random_map = np.random.randint(2048, size=(480, 640))


def flatten_depth(depth_map):
    depth_map = depth_map.flatten()
    [i+1 for i in depth_map.tolist()]


def enumerate_depth(depth_map):
    ''' enumeration is nice because we have access to the element indices
    However, we cannot perform the tolist() function on the ndenumerate object
    So we're missing out on 50% speed enhancements

    '''
    for index, value in np.ndenumerate(depth_map):
        value + 1


def ravel_depth(depth_map):
    depth_map = depth_map.ravel()
    [i+1 for i in depth_map.tolist()]


if __name__ == '__main__':

    flatten_depth_time = timeit.timeit(
        lambda: flatten_depth(zeros_map), number=500)
    print(
        f'the time to flatten the array and add 1 to each element is: {flatten_depth_time}')

    ravel_depth_timer = timeit.timeit(
        lambda: ravel_depth(zeros_map), number=500)
    print(
        f'the time to ravel the array and add 1 to each element is: {ravel_depth_timer}')
