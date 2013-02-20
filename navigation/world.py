class World(object):
    OCCUPIED = 1
    EMPTY = 2
    UNKNOWN = 3

    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height

    def set_empty(self, (x, y), v):
        self.data[x][y] = World.EMPTY

    def set_occupied(self, (x, y), v):
        self.data[x][y] = World.OCCUPIED

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
