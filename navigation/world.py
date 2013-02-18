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
