import numpy as np
from skimage import feature, graph
import movement

TEMPLATE_CENTER_OFFSET = 1
BASE_VERT_TEMPLATE = np.array([[0, 1, 0],
                               [0, 1, 0],
                               [0, 0, 0]])
BASE_DIAG_TEMPLATE = np.array([[1, 0, 0],
                               [0, 1, 0],
                               [0, 0, 0]])

class Path:
    def __init__(self, start, end, points, cost):
        self.start = start
        self.end = end
        self.points = points
        self.cost = cost

    def as_tuples(self):
        return zip(*self.points)

    def advance(self, current, n=1):
        path_as_points = self.as_tuples()

        for idx, point in enumerate(path_as_points):
            # If this is our current location in the path, move to the next point
            if current == point:
                # If there are any more points in the path, move to them
                if len(path_as_points) > idx + n:
                    return path_as_points[idx + n]
                else:
                    return path_as_points[-1]

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

def find_path(start, end, skel):
    """Find the shortest path along the skeleton from point to point."""
    # TODO: Why do matplotlib/skimage not agree on array shapes?
    route, cost = graph.route_through_array(skel,
            [start[1], start[0]],
            [end[1], end[0]],
            fully_connected=True)
    ys, xs = zip(*route)
    xs, ys = np.asarray(xs), np.asarray(ys)

    return xs, ys, cost

def find_all_paths(start, skel):
    paths = []

    endpoints = find_endpoints(skel)
    for endpoint in endpoints:
        xs, ys, cost = movement.find_path(start, endpoint, skel)

        path = Path(start, endpoint, [xs, ys], cost)
        paths.append(path)

    return paths

def find_closest_path(start, paths, visited=[]):
    paths = filter(lambda path: path.end not in visited, paths)
    return sorted(paths, key=lambda path: path.cost)[0]
