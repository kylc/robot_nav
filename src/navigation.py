SEARCH_VECS = [
    (1, 0), (1, 1,), (0, 1), (-1, 1),
    (-1, 0), (-1, -1), (0, -1), (1, -1)
    ]

class WallMap(object):
  def __init__(self, data):
    self.data = data

  def set_occupied(self, (x, y), v):
    self.data[x][y] = v

  def occupied(self, (x, y)):
    if(x >= len(self.data) or y >= len(self.data[0])): return True
    return self.data[x][y]

def threat_distance(wallmap, (x, y), (dx, dy), max_range):
  for i in xrange(1, max_range):
    if wallmap.occupied((x + dx * i, y + dy * i)):
      return i
  return -1

def next_move(wallmap, (x, y), max_range):
  x_sum, y_sum = 0, 0
  for vec in SEARCH_VECS:
    dist = threat_distance(wallmap, (x, y), vec, max_range)
    x_sum += dist * vec[0]
    y_sum += dist * vec[1]
  return (x_sum, y_sum)

