import sys
from random import choice
import numpy as np
import matplotlib.pyplot as plt
from image_loader import load_image
from navigation import movement, skeleton

# Load the image
data = load_image(sys.argv[1])

print "Generating skeleton..."
skel = skeleton.make_skeleton(data, mindist=10)

# Draw!
plt.figure()
plt.imshow(data, cmap=plt.cm.gray, interpolation='nearest')

# Compute the paths
print "Finding endpoints..."
endpoints = movement.find_endpoints(skel)

print "Finding paths..."
startpoint = (1, 132)
for endpoint in endpoints:
    color = np.random.rand(3)

    plt.plot(endpoint[1], endpoint[0], color=color, marker='o')

    print "Finding path from: ", startpoint, " to: ", endpoint

    xs, ys = movement.find_path(startpoint, endpoint, skel)
    plt.plot(xs, ys, color=color, marker=',')


plt.show()
