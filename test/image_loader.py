import Image
from navigation import world

def load_image(fname):
    """Load a World from an image file."""
    data = []
    image = Image.open(fname)
    (width, height) = image.size
    for x in xrange(0, width):
        data.append([])
        for y in xrange(0, height):
            # TODO: Handle RGB and RGBA images
            val = image.getpixel((x, y)) == (255, 255, 255, 255)
            if val:
                data[x].append(world.World.OCCUPIED)
            else:
                data[x].append(world.World.EMPTY)
    return world.World(data, width, height)
