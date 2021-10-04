import numpy as np
from imageio import imread, imwrite


def read_png(path: str) -> np.ndarray:
    """Read a png file into a NumPy array.

    Args:
        path (str): String file path.

    Returns:
        np.ndarray: NumPy array representing the image.
    """
    image = imread(uri=path, format='png')
    # ignore the transparency channel when reading png files
    if len(image.shape) > 2 and image.shape[2] == 4:
        image = image[:,:,:3]
    return image


def write_png(image: np.ndarray, path: str):
    """Write NumPy array to a png file.

    The NumPy array should have integer values in the range [0, 255].
    Otherwise, this function has undefined behavior.

    Args:
        image (np.ndarray): NumPy array representing image.
        path (str): String file path.
    """
    imwrite(im=image, uri=path, format='png')
