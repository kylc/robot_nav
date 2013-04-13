class World(object):
    OCCUPIED = 1
    EMPTY = 2
    UNKNOWN = 3

    @classmethod
    def make_unknown_map(cls, width, height):
        data = []
        for x in xrange(0, width):
            data.append([])
            for y in xrange(0, height):
                data[x].append(World.UNKNOWN)
        return World(data, width, height)

    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height

    def set_empty(self, (x, y)):
        self.data[x][y] = World.EMPTY

    def set_occupied(self, (x, y)):
        self.data[x][y] = World.OCCUPIED

    def set_unknown(self, (x, y)):
        self.data[x][y] = World.UNKNOWN

    def occupied(self, (x, y)):
        return self.get_value((x, y)) == World.OCCUPIED

    def empty(self, (x, y)):
        return self.get_value((x, y)) == World.EMPTY

    def unknown(self, (x, y)):
        return self.get_value((x, y)) == World.UNKNOWN

    def get_value(self, (x, y)):
        """Return whether or not the cell is occupied.  Return true if the given
        cell is out of bounds."""
        if(x >= len(self.data) or y >= len(self.data[0])):
            # We assume all out-of-bounds regions are occupied.
            return World.OCCUPIED
        return self.data[x][y] 

    def set_value(self, (x, y), v):
        if(x >= len(self.data) or y >= len(self.data[0])):
            return

        self.data[x][y] = v

    def is_within_bounds(self, (x, y)):
        return x > 0 and x < self.width and y > 0 and y < self.height

def nearest((x, y)):
    return (int(round(x)), int(round(y)))
