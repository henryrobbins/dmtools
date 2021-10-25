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
    # transform range of image from [0,255] to [0,1]
    image = image / 255
    return image


def write_png(image: np.ndarray, path: str):
    """Write NumPy array to a png file.

    The NumPy array should have values in the range [0, 1].
    Otherwise, this function has undefined behavior.

    Args:
        image (np.ndarray): NumPy array representing image.
        path (str): String file path.
    """
    # TODO: Is this the right way to discretize?
    im = np.ceil(255*image - 0.5).astype(np.uint8)
    imwrite(im=im, uri=path, format='png')
