import sys
import pygame
import image_loader
from navigation import movement
from navigation.world import World

EMPTY_COLOR = (0, 0, 0)
UNKNOWN_COLOR = (128, 128, 128)
OCCUPIED_COLOR = (255, 255, 255)

PATH_COLOR = (0, 255, 0)
OBJ_COLOR = (255, 0, 0)

# Load the world from image data.  We load the entire map (full_wallmap), but
# only calculate our next move based on what we have seen (wallmap).
full_wallmap = image_loader.load_image(sys.argv[1])
wallmap = World.make_unknown_map(full_wallmap.width, full_wallmap.height)

# Set our initial x and y coordinates
(x, y) = (10, 50)
(finish_x, finish_y) = (20, 280)
targets = [(finish_x, finish_y)]

pygame.init()
screen = pygame.display.set_mode((wallmap.width, wallmap.height))
pygame.display.set_caption("Visualization")

background = pygame.Surface(screen.get_size())
background = background.convert()

def draw_pixel((x, y), v):
    if v == World.OCCUPIED:
        background.fill(OCCUPIED_COLOR, rect=(i, j, 1, 1))
    elif v == World.EMPTY:
        background.fill(EMPTY_COLOR, rect=(i, j, 1, 1))
    elif v == World.UNKNOWN:
        background.fill(UNKNOWN_COLOR, rect=(i, j, 1, 1))

# Draw the map
for i, row in enumerate(wallmap.data):
    for j, col in enumerate(row):
        draw_pixel((i, j), wallmap.data[i][j])

clock = pygame.time.Clock()
while True:
    clock.tick(60)

    # Reveal the area around the robot
    for i in xrange(x - 40, x + 40):
        for j in xrange(y - 40, y + 40):
            val = full_wallmap.get_value((i, j))
            wallmap.set_value((i, j), val)

            # Redraw the area
            draw_pixel((i, j), val)

    # Draw the robot
    screen.blit(background, (0, 0))
    screen.fill(OBJ_COLOR, rect=((x - 5), (y - 5), 10, 10))

    # Find the unknown regions so we can target them.
    unknowns = movement.contiguous_unknowns(wallmap, (x, y), 100)
    for (ux, uy) in unknowns:
        pygame.draw.circle(screen, PATH_COLOR, (ux, uy), 2)
    targets = unknowns # TODO: TODO: TODO:

    # Make the next movement
    # TODO: Need to figure out how to move in each direction independently.
    # This allows only for moving up/down, left/right, or diagonal, preventing
    # the robot from following it's true desired path.
    (dx, dy) = movement.next_move(wallmap, (x, y), 40, targets)
    if dx > 0: x += 1
    elif dx < 0: x -= 1
    if dy > 0: y += 1
    elif dy < 0: y -= 1

    pygame.draw.aaline(screen, PATH_COLOR, (x, y), (x + dx, y + dy))

    wallmap.set_occupied((x, y))
    background.fill(OCCUPIED_COLOR, rect=(x, y, 1, 1))

    pygame.display.flip()
