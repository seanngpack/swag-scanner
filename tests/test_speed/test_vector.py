import timeit

from swagscanner.scanner.d435 import D435
from swagscanner.processing.depth import DepthProcessor

trials=40

fast_deproject = DepthProcessor().initialize_processor(camera=D435(), fast=True)
time = timeit.Timer(fast_deproject.deproject_depth_frame).timeit(number=400)
print(time/400)

# slow_deproject = DepthProcessor().initialize_processor(camera=D435(), fast=False)
# time = timeit.Timer(slow_deproject.deproject_depth_frame).timeit(number=10)
# print(time/10)
