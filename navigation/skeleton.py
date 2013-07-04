import numpy as np
from scipy import stats
from skimage import feature, morphology

TEMPLATE_CENTER_OFFSET = 1
BASE_VERT_TEMPLATE = np.array([[0, 1, 0],
                               [0, 1, 0],
                               [0, 0, 0]])
BASE_DIAG_TEMPLATE = np.array([[1, 0, 0],
                               [0, 1, 0],
                               [0, 0, 0]])

def make_skeleton(image, mindist):
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

def make_endpoint_templates():
    """Return the endpoint matching template matricies."""
    templates = []

    for i in xrange(0, 4):
        templates.append(np.rot90(BASE_VERT_TEMPLATE, k=i))
        templates.append(np.rot90(BASE_DIAG_TEMPLATE, k=i))

    return templates

def offset_template_point(p):
    return p + TEMPLATE_CENTER_OFFSET

def swap_axes((x, y)):
    return (y, x)

def find_endpoints(skel):
    """Return all matched endpoints in the image."""
    endpoints = []

    for template in make_endpoint_templates():
        matches = feature.match_template(skel, template)

        # Filter to only those that match with an 80% probability
        matches = np.where(matches > 0.80)

        # skimage matches on the top left of the template, so shift it to the
        # center point
        matches = map(offset_template_point, matches)

        endpoints.extend(map(swap_axes, zip(*matches)))

    return endpoints
