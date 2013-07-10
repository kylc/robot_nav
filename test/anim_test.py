import sys
from collections import deque
from random import choice
import pygame
import numpy as np
from scipy.spatial import distance

from image_loader import load_image
from navigation import movement, skeleton

# Load the image
data = load_image(sys.argv[1])

EMPTY_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (0, 0, 0)
ROBOT_COLOR = (255, 0, 0,)

def draw_image(screen, img):
    for (y, x), v in np.ndenumerate(img):
        screen.fill((v, v, v), rect=(x, y, 1, 1))

# Set up pygame
pygame.init()
screen = pygame.display.set_mode((data.shape[1], data.shape[0]))

background = pygame.Surface(screen.get_size())
background = background.convert()
draw_image(background, data)

# Set up navigation
location = (1, 132)

def mask_fill_range(data, center, target_color, max_range):
    mask = np.zeros_like(data).astype(np.bool)

    q = deque()
    q.append(center)

    while q:
        (x, y) = q.pop()

        if data[y, x] == target_color and not mask[y, x] and distance.euclidean(center, (x, y)) < max_range:
            mask[y, x] = True
            q.append((x - 1, y))
            q.append((x + 1, y))
            q.append((x, y - 1))
            q.append((x, y + 1))

    return mask

masked = np.zeros_like(data)
mask = mask_fill_range(data, location, target_color=255, max_range=100)
masked = masked | np.where(mask, data, 0)

skel = skeleton.make_skeleton(masked, mindist=10)
navigator = movement.Navigator(location, skel)

# Iterate
clock = pygame.time.Clock()
while True:
    clock.tick(60)

    screen.blit(background, (0, 0))

    mask = mask_fill_range(data, location, target_color=255, max_range=100)
    masked = masked | np.where(mask, data, 0)
    for (y, x), v in np.ndenumerate(masked):
        # screen.fill((v, v, v), rect=(x, y, 1, 1))
        screen.set_at((x,  y), (v, v, v))

    # Draw the robot
    screen.fill(ROBOT_COLOR, rect=(location[0] - 5, location[1] - 5, 10, 10))

    # Calculate the next move
    location = navigator.advance(step=10)

    skel = skeleton.make_skeleton(masked, mindist=10)
    endpoints = skeleton.find_endpoints(skel)
    for (x, y) in endpoints:
        screen.fill((0, 255, 0), rect=(x - 3, y - 3, 3, 3))

    navigator.skeleton = skeleton
    navigator.regenerate_paths()

    pygame.display.flip()
