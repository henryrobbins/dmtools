import os
import imageio
import numpy as np
from .transform import rescale
from typing import List
from ._log import _log_msg
import logging


class Netpbm:
    """An object representing a Netpbm image.

    Netpbm is a package of graphics programs and a programming library. These
    programs work with a set of graphics formats called the "netpbm" formats.
    Each format is identified by a "magic number" which is denoted as :code:`P`
    followed by the number identifier. This class works with the following
    formats.

    - `pbm`_: Pixels are black or white (:code:`P1` and :code:`P4`).
    - `pgm`_: Pixels are shades of gray (:code:`P2` and :code:`P5`).
    - `ppm`_: Pixels are in full color (:code:`P3` and :code:`P6`).

    Each of the formats has two "magic numbers" associated with it. The lower
    number corresponds to the ASCII (plain) format while the higher number
    corresponds to the binary (raw) format. This class can handle reading both
    the plain and raw formats though it can only export Netpbm images in the
    plain formats (:code:`P1`, :code:`P2`, and :code:`P3`).

    The plain formats for all three of pbm, pgm, and ppm are quite similar.
    Here is an example pgm format.

    .. code-block:: text

        P2
        5 3
        4
        1 1 0 1 0
        2 0 3 0 1
        2 2 3 1 0

    The first row of the file contains the "magic number". In this example, the
    file is a grayscale pgm image. The second row gives the file
    dimensions (width by height) separated by whitespace. The third row gives
    the maximum gray/color value. In this case, it is the maximum gray value
    since this is a grayscale pgm image. Essentially, this number encodes how
    many different gradients there are in the image. Lastly, the remaining
    lines of the file encode the actual pixels of the image. In a pbm image,
    the third line is not needed since pixels have binary (black or white)
    values. In a ppm full-color image, each pixels has three values represeting
    it--the values of the red, green, and blue channels.

    This descriptions serves as a brief overview of the Netpbm formats with the
    relevant knowledge for using this class. For more information about Netpbm,
    see the `Netpbm Home Page`_.

    .. _pbm: http://netpbm.sourceforge.net/doc/pbm.html
    .. _pgm: http://netpbm.sourceforge.net/doc/pgm.html
    .. _ppm: http://netpbm.sourceforge.net/doc/ppm.html
    .. _Netpbm Home Page: http://netpbm.sourceforge.net

    """
    extension_to_magic_number = {"pbm": 1, "pgm": 2, "ppm": 3}
    magic_number_to_extension = {1: "pbm", 2: "pgm", 3: "ppm"}

    def __init__(self, P: int, k: int, M: np.ndarray):
        """Initialize a Netpbm image.

        Args:
            P (int): Magic number of the Netpbm image.
            k (int): Maximum gray/color value
            M (np.ndarray): A NumPy array representing the image pixels.
        """
        self.P = P
        self.h, self.w, *_ = M.shape
        self.k = k
        self.M = M

    def __copy__(self):
        return Netpbm(P=self.P, k=self.k, M=self.M)

    def set_max_color_value(self, k: int):
        """Set the maximum gray/color value of this Netpbm image.

        Args:
            k (int): Maximum gray/color value.
        """
        if k == 1:
            self.M = ((self.M / self.k) > 0.5).astype(int)
            if self.P == 2:
                self.P == 1
        else:
            step = int(self.k / k)
            self.M = np.floor_divide(self.M, step)

    def rescale(self, k: int):
        """Rescale the image by the desired scaling factor.

        Uses Nearest-neighbor interpolation as the image scaling algorithm.
        Read more about image scaling algorithms at
        `Image scaling <https://wikipedia.org/wiki/Image_scaling>`_.

        Args:
            k (int): Scale factor
        """
        # Note that order=0 is equivalent to the nearest neighbor algorithm
        self.M = rescale(self.M, k, filter='point')
        self.h, self.w, *_ = self.M.shape

    def to_netpbm(self, path: str, comment: List[str] = []):
        """Write object to a Netpbm file (pbm, pgm, ppm).

        Uses the ASCII (plain) magic numbers.

        Args:
            path (str): String file path.
            comment (str): List of comment lines to include in the file.
        """
        with open(path, "w") as f:
            f.write('P%d\n' % self.P)
            for line in comment:
                f.write('# %s\n' % line)
            f.write("%s %s\n" % (self.w, self.h))
            if self.P != 1:
                f.write("%s\n" % (self.k))
            if self.P == 3:
                M = self.M.reshape(self.h, self.w * 3)
            else:
                M = self.M
            lines = M.clip(0, self.k).astype(int).astype(str).tolist()
            f.write('\n'.join([' '.join(line) for line in lines]))
            f.write('\n')
        logging.info(_log_msg(path, os.stat(path).st_size))

    def to_png(self, path: str):
        """Write object to a png file.

        Args:
            path (str): String file path.
        """
        M = self.M
        if self.P == 1:
            M = np.where(M == 1, 0, 1)
        M = np.array(M * (255 / self.k), dtype=np.uint8)
        imageio.imwrite(path, M)
        logging.info(_log_msg(path, os.stat(path).st_size))


def _parse_ascii_netpbm(f: List[str]) -> Netpbm:
    # adapted from code by Dan Torop
    vals = [v for line in f for v in line.split('#')[0].split()]
    P = int(vals[0][1])
    if P == 1:
        w, h, *vals = [int(v) for v in vals[1:]]
        k = 1
    else:
        w, h, k, *vals = [int(v) for v in vals[1:]]
    if P == 3:
        M = np.array(vals).reshape(h, w, 3)
    else:
        M = np.array(vals).reshape(h, w)
    return Netpbm(P=P, k=k, M=M)


# TODO: make the file reading code more robust
def _parse_binary_netpbm(path: str) -> Netpbm:
    # adapted from https://www.stackvidhya.com/python-read-binary-file/
    with open(path, "rb") as f:
        P = int(f.readline().decode()[1])
        # change to corresponding ASCII magic number
        P = int(P / 2)
        w = int(f.readline().decode()[:-1])
        h = int(f.readline().decode()[:-1])
        if P == 1:
            k = 1
        else:
            k = int(f.readline().decode()[:-1])
        dtype = np.dtype('B')
        M = np.fromfile(f, dtype)
        if P == 3:
            M = M.reshape(h, w, 3)
        else:
            M = M.reshape(h, w)
    return Netpbm(P=P, k=k, M=M)


def read_netpbm(path: str) -> Netpbm:
    """Read Netpbm file (pbm, pgm, ppm) into Netpbm.

    Args:
        path (str): String file path.

    Returns:
        Netpbm: A Netpbm image
    """
    with open(path, "rb") as f:
        magic_number = f.read(2).decode()
    if int(magic_number[1]) <= 3:
        # P1, P2, P3 are the ASCII (plain) formats
        with open(path) as f:
            return _parse_ascii_netpbm(f)
    else:
        # P4, P5, P6 are the binary (raw) formats
        return _parse_binary_netpbm(path)
