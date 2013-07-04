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

    path_as_points = closest_path.as_tuples()
    for idx, point in enumerate(path_as_points):
        # If this is our current location in the path, move to the next point
        if location == point:
            # If there are any more points in the path, move to them
            if len(path_as_points) > idx + 1:
                location = path_as_points[idx + 1]

                # Draw the vector
                if len(path_as_points) > idx + 10:
                    vec_end = path_as_points[idx + 10]
                else:
                    vec_end = path_as_points[-1]

                pygame.draw.aaline(screen, (0, 255, 0), location, vec_end)

                break
            # If this is the end, we've now visited the endpoint, so mark it as
            # so
            else:
                visited.append((location[1], location[0]))

                # Now figure out how to get to all the other endpoints
                paths = movement.find_all_paths(location, skel)

    pygame.display.flip()
