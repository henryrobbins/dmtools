import os
import numpy as np
from imageio import imread, imwrite
from typing import List, Tuple
from ._log import _log_msg
import logging


def _continuous(image: np.ndarray, k: int) -> np.ndarray:
    """Make a discrete image continuous.

    Args:
        image (np.ndarray): Discrete image with values in [0,k].
        k (int): Maximum color/gray value.

    Returns:
        np.ndarray: Continuous image with values in [0,1].
    """
    return image / k


def _discretize(image: np.ndarray, k: int) -> np.ndarray:
    """Discretize a continuous image.

    Args:
        image (np.ndarray): Continuous image with values in [0,1].
        k (int): Maximum color/gray value.

    Returns:
        np.ndarray: Discrete image with values in [0,k].
    """
    # TODO: Is this the right way to discretize?
    return np.ceil(k*image - 0.5).astype(int)


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
    return _continuous(image, 255)


def write_png(image: np.ndarray, path: str):
    """Write NumPy array to a png file.

    The NumPy array should have values in the range [0, 1].
    Otherwise, this function has undefined behavior.

    Args:
        image (np.ndarray): NumPy array representing image.
        path (str): String file path.
    """
    im = _discretize(image, 255).astype(np.uint8)
    imwrite(im=im, uri=path, format='png')


def _parse_ascii_netpbm(f: List[str]) -> Tuple[np.ndarray, int]:
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
    M = _continuous(M, k)
    return (M, k)


# TODO: make the file reading code more robust
def _parse_binary_netpbm(path: str) -> Tuple[np.ndarray, int]:
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
    M = _continuous(M, k)
    return (M, k)


def read_netpbm(path: str) -> Tuple[np.ndarray, int]:
    """Read a Netpbm file (pbm, pgm, ppm) into a NumPy array.

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

    Args:
        path (str): String file path.

    Returns:
        image (np.ndarray): NumPy array representing image.
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


def write_netpbm(image: np.ndarray, k: int, path: str,
                 comment: List[str] = []):
    """Write object to a Netpbm file (pbm, pgm, ppm).

    Uses the ASCII (plain) magic numbers.

    Args:
        image (np.ndarray): NumPy array representing image.
        k (int): Maximum color/gray value.
        path (str): String file path.
        comment (str): List of comment lines to include in the file.
    """
    h, w, *_ = image.shape
    if len(image.shape) == 2:
        P = 1 if k == 1 else 2
    else:
        P = 3
    with open(path, "w") as f:
        f.write('P%d\n' % P)
        for line in comment:
            f.write('# %s\n' % line)
        f.write("%s %s\n" % (w, h))
        if P != 1:
            f.write("%s\n" % (k))
        if P == 3:
            image = image.reshape(h, w * 3)
        image = _discretize(image, k)
        lines = image.astype(str).tolist()
        f.write('\n'.join([' '.join(line) for line in lines]))
        f.write('\n')
        logging.info(_log_msg(path, os.stat(path).st_size))
