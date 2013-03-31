import math

def threat_distance(wallmap, (x, y), (dx, dy), max_range):
    """Return the distance to an obstacle in a given direction."""
    for i in xrange(1, max_range):
        if wallmap.occupied((int(round(x + dx * i)), int(round(y + dy * i)))):
            return i
    return -1

def repulsive_force((x0, y0), (xi, yi), const, dist, active, width):
    """Return the magnitude and direction of the repulsive force for a given
    cell."""
    if not active:
        return (0, 0)
    f = const * width / dist
    return ((xi - x0) * f, (yi - y0) * f)

def next_move(wallmap, (x, y), max_range, targets):
    """Return the direction of the next move.  This is accomplished by summing
    all of the repulsive forces within the given max range."""
    (x_sum, y_sum) = (0, 0)

    # Repel from obstacles
    for t in range(0, 360, 5):
        d = math.radians(t)
        (x_dir, y_dir) = (math.cos(d), math.sin(d))
        dist = threat_distance(wallmap, (x, y), (x_dir, y_dir), max_range)
        if dist != -1:
            x_sum += dist * x_dir
            y_sum += dist * y_dir

    # Attract to targets

    # TODO: The farther the target, the stronger the attraction.  This needs
    # research.
    for (target_x, target_y) in targets:
        dx, dy = target_x - x, target_y - y
        x_sum += dx
        y_sum += dy


    return (x_sum, y_sum)
