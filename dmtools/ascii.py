import numpy as np
import os
import pkgutil
import copy
from .io import write_png, _parse_ascii_netpbm
from ._log import _log_msg
import logging


# Create a map from ascii characters to their image representation.
# Here are some scaled-down examples of the mappings in CHAR_TO_IMG.
#
#            0 0 0 0 0 0 0             0 0 1 0 1 0 0
#            0 0 1 0 0 0 0             0 1 1 1 1 1 0
#    ~  ->   0 1 0 1 0 1 0     #  ->   0 0 1 0 1 0 0
#            0 0 0 0 1 0 0             0 1 1 1 1 1 0
#            0 0 0 0 0 0 0             0 0 1 0 1 0 0

file = pkgutil.get_data(__name__, "resources/ascii.pgm").decode().split('\n')
ascii_M = _parse_ascii_netpbm(file)
char_images = [np.pad(M,((0,0),(6,6))) for M in np.split(ascii_M, 13, axis=1)]
CHAR_TO_IMG = dict(zip(list(" .,-~:;=!*#$@"), char_images))


class Ascii:
    """An object representing an ASCII image.

    For more information about ASCII, see
    `ASCII <https://wikipedia.org/wiki/ASCII>`_
    """
    def __init__(self, M: np.ndarray):
        """Initialize an ASCII image.

        Args:
            M (np.ndarray): A NumPy array of ASCII characters.
        """
        self.M = M

    def to_txt(self, path: str):
        """Write object to a txt file.

        Args:
            path (str): String file path.
        """
        with open(path, "w") as f:
            lines = self.M.astype(str).tolist()
            f.write('\n'.join([' '.join(line) for line in lines]))
            f.write('\n')
        logging.info(_log_msg(path, os.stat(path).st_size))

    def to_png(self, path: str):
        """Write object to a png file.

        Args:
            path (str): String file path.
        """
        A = self.M
        n,m = A.shape
        M = []
        for i in range(n):
            M.append([CHAR_TO_IMG[A[i,j]] for j in range(m)])
        M = np.block(M)
        write_png(M, path)
        logging.info(_log_msg(path, os.stat(path).st_size))


def image_to_ascii(image: np.ndarray) -> Ascii:
    """Return an ASCII representation of the given image.

    This function uses a particular style of
    `ASCII art <https://en.wikipedia.org/wiki/ASCII_art>`_
    in which "symbols with various intensities [are used for] creating
    gradients or contrasts."

    Args:
        image (np.ndarray): An image.

    Returns:
        Ascii: ASCII representation of image.
    """
    chars = "  -~:;=!*#$@"
    image = copy.copy((image))
    k = len(chars)-1
    image = (image * k).astype(int)
    M = image.astype(np.uint8)
    M = np.array([[chars[i] for i in row] for row in M])
    return Ascii(M=M)
