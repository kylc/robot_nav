import sys
from random import choice
import pygame
import numpy as np

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

skel = skeleton.make_skeleton(data, mindist=10)
navigator = movement.Navigator(location, skel)

# Iterate
clock = pygame.time.Clock()
while True:
    clock.tick(60)

    screen.blit(background, (0, 0))

    # Draw the robot
    screen.fill(ROBOT_COLOR, rect=(location[0] - 5, location[1] - 5, 10, 10))

    # Calculate the next move
    location = navigator.advance(step=1)

    pygame.display.flip()
