import sys
from random import choice
import pygame
import numpy as np

from image_loader import load_image
from navigation import movement, skeleton

# Load the image
print "Loading image..."
data = load_image(sys.argv[1])

print "Generating skeleton..."
skel = skeleton.make_skeleton(data, mindist=10)

# Compute the paths
print "Finding paths..."
location = (1, 132)

paths = movement.find_all_paths(location, skel)

EMPTY_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (0, 0, 0)
ROBOT_COLOR = (255, 0, 0,)

def draw_image(screen, img):
    for (y, x), v in np.ndenumerate(img):
        screen.fill((v, v, v), rect=(x, y, 1, 1))

pygame.init()
screen = pygame.display.set_mode((data.shape[1], data.shape[0]))

background = pygame.Surface(screen.get_size())
background = background.convert()
draw_image(background, data)

# The visited endpoints, so we know not to go back to them
visited = []

clock = pygame.time.Clock()
while True:
    clock.tick(60)

    screen.blit(background, (0, 0))

    # Draw the robot
    locx, locy = location
    screen.fill(ROBOT_COLOR, rect=(locx - 5, locy - 5, 10, 10))

    closest_path = movement.find_closest_path(location, paths, visited)

    # Move to the next location along the path
    location = closest_path.advance(location, n=1)

    # If we have reached the end, mark the point as visited
    if location == closest_path.end:
        visited.append(closest_path.end)

        # Now figure out how to get to all the other endpoints
        paths = movement.find_all_paths(location, skel)

    pygame.display.flip()
