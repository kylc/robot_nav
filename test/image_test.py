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

clock = pygame.time.Clock()
while True:
    clock.tick(5)

    screen.blit(background, (0, 0))

    # Draw the robot
    locx, locy = location
    screen.fill(ROBOT_COLOR, rect=(locx - 5, locy - 5, 10, 10))

    closest_path = movement.find_closest_path(location, paths)
    print "Location:", location
    print "PathL:", zip(*closest_path.path)
    path_as_points = zip(*closest_path.path)
    for idx, point in enumerate(path_as_points):
        # If this is our current location in the path, move to the next point
        if location == point:
            print "found match at", idx
            location = path_as_points[idx + 1]
            break

    pygame.display.flip()
    print "Tick!"
