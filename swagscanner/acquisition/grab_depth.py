import freenect
import numpy as np

def grab_depth() -> list:
    '''Capture a single frame as a depth map

    Returns: 
        A 2d numpy array of unit8 integers containing depth information mapped from 0->2047. 

    '''
    
    depth, timestamp = freenect.sync_get_depth()
    depth = depth.astype(np.uint16)
    return depth
