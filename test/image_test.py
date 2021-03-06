import sys
from random import choice
import numpy as np
import matplotlib.pyplot as plt
from image_loader import load_image
from navigation import movement, skeleton

# Load the image
print "Loading image..."
data = load_image(sys.argv[1])

print "Generating skeleton..."
skel = skeleton.make_skeleton(data, mindist=10)

# Draw!
plt.figure()
plt.imshow(data, cmap=plt.cm.gray, interpolation='nearest')

# Compute the paths
print "Finding paths..."
start = (1, 132)

paths = movement.find_all_paths(start, skel)
closest_path = movement.find_closest_path(start, paths)

print "Plotting!"
for path in paths:
    color = np.random.rand(3)

    plt.plot(*path.end, color=color, marker='o')
    plt.plot(*path.points, color=color, marker=',')

plt.plot(*closest_path.points, color='r', linewidth=5)

plt.show()
