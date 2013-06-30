import numpy as np
from scipy import stats
from skimage import morphology

def make_skeleton(image, mindist=15):
    skel, distance = morphology.medial_axis(image, return_distance=True)

    dist_on_skel = distance * skel

    dist_on_skel = filter_skeleton_distances(dist_on_skel)
    normalized = normalize_skeleton(dist_on_skel)

    return normalized

def filter_skeleton_distances(dist_on_skel, mindist=10):
    # Threshold values too close to walls to -1
    return stats.threshold(dist_on_skel, threshmin=mindist, newval=-1)

def normalize_skeleton(dist_on_skel):
    """Return the skeleton with all values normalized to 1."""
    return np.where(dist_on_skel > 0, 1, -1)
