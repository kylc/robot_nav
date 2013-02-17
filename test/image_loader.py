import Image
from navigation.world import *

def load_image(fname):
  data = []
  image = Image.open(fname)
  (width, height) = image.size
  for x in xrange(0, width):
    data.append([])
    for y in xrange(0, height):
      val = True if image.getpixel((x, y)) == (255, 255, 255) else False
      data[x].append(val)
  return World(data, width, height)
