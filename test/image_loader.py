from PIL import Image
import numpy as np

def load_image(fname):
    """Load an image as a numpy array."""
    image = Image.open(fname)
    image = image.convert("L")

    return np.asarray(image)
