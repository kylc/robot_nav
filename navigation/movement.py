import math
import navigation.world as world
from navigation.world import World

def dist((ax, ay), (bx, by)):
    return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)

def contiguous_unknowns(wallmap, (x, y), max_range):
    unknowns = []

    is_cont = False
    start = end = None

    # Rotate around a full circle
    for t in range(0, 360, 5):
        # Trace out until we find an unknown or a wall
        for i in xrange(1, max_range):
            d = math.radians(t)
            (dx, dy) = (math.cos(d), math.sin(d))

            val = wallmap.get_value(world.nearest((x + dx * i, y + dy * i)))

            # If we find an unknown, set is_cont and mark the starting point
            if val == World.UNKNOWN:
                if not is_cont:
                    is_cont = True
                    start = (x + dx * i, y + dy * i)

                # We've found our goal, no need to search out further
                break
            # If we find a wall, set !is_cont and mark the ending point, then
            # append the start/end pair to the list of unknowns
            elif val == World.OCCUPIED:
                if is_cont:
                    is_cont = False

                    end = (x + dx * i, y + dy * i)
                    if dist(start, end) > 5:
                        (sx, sy) = start
                        (ex, ey) = end
                        if wallmap.is_within_bounds((sx, sy)) and wallmap.is_within_bounds((ex, ey)):
                            unknowns.append(world.nearest(((sx + ex) / 2, ((sy + ey) / 2))))

                # Don't try to look out beyond the wall
                break

    return unknowns

def threat_distance(wallmap, (x, y), (dx, dy), max_range):
    """Return the distance to an obstacle in a given direction."""
    for i in xrange(1, max_range):
        if wallmap.occupied(world.nearest((x + dx * i, y + dy * i))):
            return i
    return -1

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
            x_sum -= dist * x_dir
            y_sum -= dist * y_dir

    # Attract to targets

    # TODO: The farther the target, the stronger the attraction.  This needs
    # research.
    for (target_x, target_y) in targets:
        dx, dy = target_x - x, target_y - y

        # TODO: Find the proper multiplier for goals
        x_sum += 10 * dx
        y_sum += 10 * dy


    return (x_sum, y_sum)
