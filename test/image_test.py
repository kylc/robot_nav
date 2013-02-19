import sys
import pygame
import image_loader
from navigation import movement

BG_COLOR = (0, 0, 0)
PATH_COLOR = (0, 255, 0)
WALL_COLOR = (255, 255, 255)
OBJ_COLOR = (255, 0, 0)

# Load the world from image data
wallmap = image_loader.load_image(sys.argv[1])

# Set our initial x and y coordinates
(x, y) = (10, 50)

pygame.init()
screen = pygame.display.set_mode((wallmap.width, wallmap.height))
pygame.display.set_caption("Visualization")

background = pygame.Surface(screen.get_size())
background = background.convert()

# Draw the map
for i, row in enumerate(wallmap.data):
    for j, col in enumerate(row):
        if col:
            background.fill(WALL_COLOR, rect=(i, j, 1, 1))
        else:
            background.fill(BG_COLOR, rect=(i, j, 1, 1))

clock = pygame.time.Clock()
while True:
    clock.tick(60)

    # Draw the robot
    screen.blit(background, (0, 0))
    screen.fill(OBJ_COLOR, rect=((x - 5), (y - 5), 10, 10))

    # Make the next movement
    # TODO: Need to figure out how to move in each direction independently.
    # This allows only for moving up/down, left/right, or diagonal, preventing
    # the robot from following it's true desired path.
    (dx, dy) = movement.next_move(wallmap, (x, y), 200)
    if dx > 0: x += 1
    elif dx < 0: x -= 1
    if dy > 0: y += 1
    elif dy < 0: y -= 1

    pygame.draw.aaline(screen, PATH_COLOR, (x, y), (x + dx, y + dy))

    wallmap.set_occupied((x, y), True)
    background.fill(WALL_COLOR, rect=(x, y, 1, 1))

    pygame.display.flip()
