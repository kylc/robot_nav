import numpy as np
from scipy import stats, signal
from skimage import feature, morphology

import util

# Convolution matrix for detecting endpoints.  Points surrounding the center are
# weighed so we can count how many connecting edges are present.
ENDPOINT_CONVOLUTION_MATRIX = [[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]]

def make_skeleton(image, mindist):
    """Return a skeletonization of the image, filtered and normalized."""
    skel, distance = morphology.medial_axis(image, return_distance=True)

    dist_on_skel = distance * skel

    dist_on_skel = filter_skeleton_distances(dist_on_skel)
    normalized = normalize_skeleton(dist_on_skel)

    return normalized

def filter_skeleton_distances(dist_on_skel, mindist=10, newval=0):
    """Threshold values too close to obstacles to a new value."""
    return stats.threshold(dist_on_skel, threshmin=mindist, newval=newval)

def normalize_skeleton(dist_on_skel):
    """Return the skeleton with all values normalized to 1."""
    return np.where(dist_on_skel > 0, 1, 0)

def find_endpoints(skel):
    """Return all matched endpoints in the image."""
    
    # Convolving the skeleton with the defined matrix essentially returns the
    # sum of the points surrounding the center point.  As all points along the
    # path are 1 and all points off the path are 0, this gives us the number of
    # edges connecting to the center point.  If that number is 1, this is an
    # endpoint.
    endpoints = signal.convolve2d(skel, ENDPOINT_CONVOLUTION_MATRIX, mode='same') == 1

    # Mask out the areas that are not part of the path
    endpoints = np.where(skel & endpoints)

    return zip(endpoints[1], endpoints[0])
