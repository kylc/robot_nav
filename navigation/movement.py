import numpy as np
from skimage import graph

import skeleton

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

class Navigator:
    def __init__(self, start, skel):
        self.location = start
        self.visited = []
        self.skel = skel

        self.regenerate_paths()

    def regenerate_paths(self):
        self.paths = find_all_paths(self.location, self.skel, omit=self.visited)

    def advance(self, step=1):
        closest_path = find_closest_path(self.location, self.paths)

        # Move to the next location along the path
        self.location = closest_path.advance(self.location, n=step)

        # If we have reached the end, mark the point as visited
        if self.location == closest_path.end:
            self.visited.append(closest_path.end)

            # Now figure out how to get to all the other endpoints
            self.regenerate_paths()

        return self.location

def find_path(start, end, skel):
    """Find the shortest path along the skeleton from point to point."""
    # route_through_array treats zeros as having zero cost.  In our case, zeros
    # are points off the path.  Mark them as -1 so route_through_array ignores
    # them.
    skel = np.where(skel > 0, 1, -1)

    # TODO: Why do matplotlib/skimage not agree on array shapes?
    route, cost = graph.route_through_array(skel,
            [start[1], start[0]],
            [end[1], end[0]],
            fully_connected=True)
    ys, xs = zip(*route)
    xs, ys = np.asarray(xs), np.asarray(ys)

    return xs, ys, cost

def find_all_paths(start, skel, omit=[]):
    paths = []

    endpoints = skeleton.find_endpoints(skel)
    for endpoint in filter(lambda e: not e in omit, endpoints):
        xs, ys, cost = find_path(start, endpoint, skel)

        path = Path(start, endpoint, [xs, ys], cost)
        paths.append(path)

    return paths

def find_closest_path(start, paths):
    return sorted(paths, key=lambda path: path.cost)[0]
