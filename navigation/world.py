import math

class World(object):
    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height

    def set_occupied(self, (x, y), v):
        self.data[x][y] = v

    def occupied(self, (x, y)):
        if(x >= len(self.data) or y >= len(self.data[0])):
            return True
        return self.data[x][y]

def threat_distance(wallmap, (x, y), (dx, dy), max_range):
    for i in xrange(1, max_range):
        if wallmap.occupied((int(round(x + dx * i)), int(round(y + dy * i)))):
            return i
    return -1

def repulsive_force((x0, y0), (xi, yi), const, dist, active, width):
      if not active: return (0, 0)
      f = const * width / dist;
      return ((xi - x0) * f, (yi - y0) * f)

def next_move(wallmap, (x, y), max_range):
    x_sum, y_sum = 0, 0
    for t in range(0, 360, 5):
        d = math.radians(t)
        x_dir, y_dir = math.cos(d), math.sin(d)
        dist = threat_distance(wallmap, (x, y), (x_dir, y_dir), max_range)
        if dist > 0:
            x_sum += dist * x_dir
            y_sum += dist * y_dir
    return (x_sum, y_sum)
