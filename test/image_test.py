import sys
import time
import pygame
import image_loader
from navigation import world as w

BG_COLOR = (0, 0, 0)
WALL_COLOR = (255, 255, 255)
OBJ_COLOR = (255, 0, 0)

# Load the world from image data
world = image_loader.load_image(sys.argv[1])

# Set our initial x and y coordinates
(x, y) = (10, 50)

pygame.init()
screen = pygame.display.set_mode((world.width, world.height))
pygame.display.set_caption("Visualization")

background = pygame.Surface(screen.get_size())
background = background.convert()

clock = pygame.time.Clock()
while True:
  clock.tick(60)

  # Draw the map
  for i, row in enumerate(world.data):
    for j, col in enumerate(row):
      if col:
        background.fill(WALL_COLOR, rect=(i, j, 1, 1))
      else:
        background.fill(BG_COLOR, rect=(i, j, 1, 1))

  # Draw the robot
  background.fill(OBJ_COLOR, rect=((x - 5), (y - 5), 10, 10))

  world.set_occupied((x, y), True)

  # Make the next movement
  (dx, dy) = w.next_move(world, (x, y), 200)
  if dx > 0: x += 1
  elif dx < 0: x -= 1
  if dy > 0: y += 1
  elif dy < 0: y -= 1


  screen.blit(background, (0, 0))
  pygame.display.flip()
