import numpy as np
from scipy import ndimage
from scipy.stats import threshold
from skimage.graph import route_through_array
from skimage.morphology import medial_axis

def make_skeleton(data, mindist=15):
    skel, distance = medial_axis(data, return_distance=True)

    dist_on_skel = distance * skel

    # Filter the points too close to walls
    dist_on_skel = threshold(dist_on_skel, threshmin=mindist, newval=-1)

    return dist_on_skel

def find_path(skeleton):
    # TODO: Make these arguments
    start = (139, 38)
    end = (88, 430)

    path, cost = route_through_array(skeleton, start, end, fully_connected=True)
    path = np.asarray(path)

    # TODO: Why are the coordinates flipped?
    # TODO: numpy probably has some kind of rot90 function...
    for i in range(len(path)):
        (x, y) = path[i]
        path[i] = (y, x)

    return path
