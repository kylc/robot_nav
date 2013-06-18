import sys
import matplotlib.pyplot as plt
from image_loader import load_image
from navigation.movement import make_skeleton, find_path

# Load the image
data = load_image(sys.argv[1])

# Generate the path
skel = make_skeleton(data, mindist=10)
path = find_path(skel)

# Draw!
plt.figure()
plt.subplot(121)
plt.imshow(data, cmap=plt.cm.gray, interpolation='nearest')
plt.subplot(122)
plt.imshow(skel, cmap=plt.cm.spectral, interpolation='nearest')
plt.contour(data, [0.5], colors='w')

plt.plot(*zip(*path), color='r')

plt.show()
