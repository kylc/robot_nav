import math
from navigation.world import World

def dist((ax, ay), (bx, by)):
    return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)

def contiguous_unknowns(wallmap, (x, y), max_range):
    unknowns = []

    is_cont = False
    start = end = None

    # Trace out until we find an unkown or a wall
    for i in xrange(1, max_range):
        # Rotate around a full circle
        for t in range(0, 360, 5):
            d = math.radians(t)
            (dx, dy) = (math.cos(d), math.sin(d))

            val = wallmap.get_value((int(round(x + dx * i)), int(round(y + dy * i))))

            if val == World.UNKNOWN:
                # If !is_cont and found unknown, set is_cont and mark starting
                # point
                if not is_cont:
                    is_cont = True
                    start = (x + dx * i, y + dy * i)
            elif val == World.OCCUPIED or val == World.EMPTY:
                # If is_cont and found wall, set !is_cont and mark ending point
                if is_cont:
                    is_cont = False

                    end = (x + dx * i, y + dy * i)
                    if dist(start, end) > 5:
                        (sx, sy) = start
                        (ex, ey) = end
                        if wallmap.is_within_bounds((sx, sy)) and wallmap.is_within_bounds((ex, ey)):
                            unknowns.append((int((sx + ex) / 2), int((sy + ey) / 2)))

    return unknowns

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
