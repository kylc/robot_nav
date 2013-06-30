import numpy as np
from skimage import feature, graph

TEMPLATE_CENTER_OFFSET = 1
BASE_VERT_TEMPLATE = np.array([[0, 1, 0],
                               [0, 1, 0],
                               [0, 0, 0]])
BASE_DIAG_TEMPLATE = np.array([[1, 0, 0],
                               [0, 1, 0],
                               [0, 0, 0]])

def make_endpoint_templates():
    """Return the endpoint matching template matricies."""
    templates = []

    for i in xrange(0, 4):
        templates.append(np.rot90(BASE_VERT_TEMPLATE, k=i))
        templates.append(np.rot90(BASE_DIAG_TEMPLATE, k=i))

    return templates

def offset_template_point(p):
    return p + TEMPLATE_CENTER_OFFSET

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

        endpoints.extend(zip(*matches))

    return endpoints

def find_path(start, end, skel):
        # TODO: Why do matplotlib/skimage not agree on array shapes?
        route, cost = graph.route_through_array(skel,
                [start[1], start[0]],
                [end[0], end[1]],
                fully_connected=True)
        ys, xs = zip(*route)

        return [xs, ys]
