import os
import sys
import re
import numpy as np
import pkgutil
from datetime import datetime
from imageio import imread, imwrite
from PIL import PngImagePlugin
from typing import List
from ._log import _log_msg
import logging


class Metadata:
    """Maintain metadata for an image. Based on the `PNG`_ format.

    .. _PNG: https://www.w3.org/TR/PNG/#11textinfo
    """

    def __init__(self,
                 title: str = None,
                 author: str = None,
                 description: str = None,
                 copyright: str = None,
                 creation_time: str = None,
                 software: str = None,
                 disclaimer: str = None,
                 warning: str = None,
                 source: str = None,
                 comment: str = None):
        """Initialize metadata.

        Args:
            title (str): Short (one line) title or caption for image. \
                Defaults to None
            author (str): Name of image's creator. \
                Defaults to None
            description (str): Description of image (possibly long). \
                Defaults to None
            copyright (str): Copyright notice. Defaults to None
            creation_time (str): Time of original image creation. \
                Defaults to the time of initialization.
            software (str): Software used to create the image. \
                Defaults to "dmtools".
            disclaimer (str): Legal disclaimer. Defaults to None.
            warning (str): Warning of nature of content. Defaults to None.
            source (str): Device used to create the image. \
                Defaults to the source code of the invoked script.
            comment (str): Miscellaneous comment. Defaults to None.
        """
        self.title = title
        self.author = author
        self.description = description
        self.copyright = copyright
        if creation_time is None:
            self.creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.creation_time = creation_time
        self.software = "dmtools" if software is None else software
        self.disclaimer = disclaimer
        self.warning = warning
        if source is None:
            if sys.argv[0] != "":
                self.source = open(sys.argv[0]).read()
            else:
                self.source = source
        self.comment = comment

    def _to_pnginfo(self) -> PngImagePlugin.PngInfo:
        """Return a PngInfo object with this metadata.

        Returns:
            PngImagePlugin.PngInfo: Corresponding PngInfo object.
        """
        info = PngImagePlugin.PngInfo()
        inst_var_to_attribute_name = {
            self.title: "Title",
            self.author: "Author",
            self.description: "Description",
            self.copyright: "Copyright",
            self.creation_time: "Creation Time",
            self.software: "Software",
            self.disclaimer: "Disclaimer",
            self.warning: "Warning",
            self.source: "Source",
            self.comment: "Comment"
        }
        for k,v in inst_var_to_attribute_name.items():
            if k is not None:
                info.add_text(v, k)
        return info

    def _to_comment_string(self) -> str:
        """Return a string representation of this metadata.

        Returns:
            str: String representation of metadata.
        """
        var_to_string = {
            self.title: "Title",
            self.author: "Author",
            self.description: "Description",
            self.copyright: "Copyright",
            self.creation_time: "Creation Time",
            self.software: "Software",
            self.disclaimer: "Disclaimer",
            self.warning: "Warning",
            self.source: "Source",
            self.comment: "Comment"
        }
        non_none = {k:v for k,v in var_to_string.items() if k is not None}
        lines = ["%s: %s\n" % (v,k) for k,v in non_none.items()]
        comment = "".join(lines)
        return "\n".join("# %s" % l for l in comment.split("\n")) + "\n"


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


def _get_next_version(path: str) -> str:
    """Return the name with the next highest version number.

    Args:
        name (str): String file path

    Returns:
        str: String file path with version number.
    """
    filenames = os.scandir(max(os.path.dirname(path), '.'))
    root, ext = os.path.splitext(path)
    basename = os.path.basename(root)
    # match if no extension or any of the dmtools supported file formats
    r = re.compile(f"{re.escape(basename)}_([0-9]+)(|.png|.pgm|.pbm|.ppm)")
    prev = (int(m[1]) for m in (r.match(f.name) for f in filenames) if m)
    i = 1 + max(prev, default=0)
    return f"{root}_{i:04}{ext}"


def read_png(path: str) -> np.ndarray:
    """Read a png file into a NumPy array.

    Args:
        path (str): String file path.

    Returns:
        np.ndarray: NumPy array representing the image.
    """
    image = imread(uri=path, format='png')
    return _continuous(image, 255)


def write_png(image: np.ndarray, path: str, versioning=False, metadata=None):
    """Write NumPy array to a png file.

    The NumPy array should have values in the range [0, 1].
    Otherwise, this function has undefined behavior.

    Args:
        image (np.ndarray): NumPy array representing image.
        path (str): String file path.
        versioning (bool): Version files (rather than overwrite).
        metadata (Metadata): Metadata for image. Defaults to Metadata().
    """
    if versioning:
        path = _get_next_version(path)
    im = _discretize(image, 255).astype(np.uint8)
    metadata = Metadata() if metadata is None else metadata
    imwrite(im=im, uri=path, format='png', pnginfo=metadata._to_pnginfo())


def _parse_ascii_netpbm(f: List[str]) -> np.ndarray:
    # adapted from code by Dan Torop
    vals = [v for line in f for v in line.split('#')[0].split()]
    P = int(vals[0][1])
    if P == 1:
        w, h, *vals = [v for v in vals[1:]]
        w = int(w)
        h = int(h)
        vals = [int(i) for i in list(''.join(vals))]
        k = 1
    else:
        w, h, k, *vals = [int(v) for v in vals[1:]]
    M = np.array(vals)
    if P == 1:
        M = -M + 1
    if P == 3:
        M = M.reshape(h, w, 3)
    else:
        M = M.reshape(h, w)
    return _continuous(M, k)


def _parse_binary_netpbm(path: str) -> np.ndarray:
    with open(path, "rb") as f:
        P = int(f.readline().decode()[1])
        # read lines until all tokens found
        num_tokens = 2 if P == 4 else 3
        tokens = []
        while len(tokens) < num_tokens:
            line_tokens = f.readline().decode()[:-1].split()
            i = 0
            while i < len(line_tokens) and line_tokens[i] != '#':
                tokens.append(line_tokens[i])
                i += 1
        tokens = [int(t) for t in tokens]
        w, h, *_ = tokens
        k = 1 if P == 4 else tokens[2]
        M = np.fromfile(f, 'uint8')
        if P == 4:
            # get bits from bytes
            M = np.unpackbits(M)
            m = int(np.ceil(w / 8)) * 8
            n = int(len(M) / m)
            M = np.reshape(M, (n,m))
            # ignore excess bits from each row
            M = M[:,:w]
            # inverse 0 and 1 so 0 is white
            M = -M + 1
        elif P == 5:
            M = M.reshape(h, w)
        else:
            M = M.reshape(h, w, 3)
    return _continuous(M, k)


def read_netpbm(path: str) -> np.ndarray:
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
                 versioning=False, metadata=None):
    """Write object to a Netpbm file (pbm, pgm, ppm).

    Uses the ASCII (plain) magic numbers.

    Args:
        image (np.ndarray): NumPy array representing image.
        k (int): Maximum color/gray value.
        path (str): String file path.
        versioning (bool): Version files (rather than overwrite).
        metadata (Metadata): Metadata for image. Defaults to Metadata().
    """
    if versioning:
        path = _get_next_version(path)
    metadata = Metadata() if metadata is None else metadata
    h, w, *_ = image.shape
    if len(image.shape) == 2:
        P = 1 if k == 1 else 2
    else:
        P = 3
    if P == 1:
        image = -image + 1
    with open(path, "w") as f:
        f.write('P%d\n' % P)
        f.write("%s %s\n" % (w, h))
        if P != 1:
            f.write("%s\n" % (k))
        if P == 3:
            image = image.reshape(h, w * 3)
        f.write(metadata._to_comment_string())
        image = _discretize(image, k)
        lines = image.astype(str).tolist()
        f.write('\n'.join([' '.join(line) for line in lines]))
        f.write('\n')
        logging.info(_log_msg(path, os.stat(path).st_size))


def write_ascii(image: np.ndarray, path: str, txt:str = False):
    """Write object to an ASCII art representation.

    Args:
        image (np.ndarray): NumPy array representing image.
        path (str): String file path.
        txt (str): True iff write to a txt file. Defaults to False.
    """
    char_map = "   -~:;=!*#$@"
    image = _discretize(image, len(char_map)-1)
    if not txt:
        # generate char map to small images of each character
        file = pkgutil.get_data(__name__, "resources/ascii.pgm")
        f = file.decode().split('\n')
        M = _parse_ascii_netpbm(f)
        char_ims = [np.pad(M,((0,0),(6,6))) for M in np.split(M, 13, axis=1)]
        char_image_map = dict(zip(list(" .,-~:;=!*#$@"), char_ims))

        # create image of ascii art and write to PNG
        A = np.copy(image)
        n,m = A.shape
        M = []
        for i in range(n):
            M.append([char_image_map[char_map[A[i,j]]] for j in range(m)])
        M = np.block(M)
        write_png(M, path)
        logging.info(_log_msg(path, os.stat(path).st_size))
    else:
        if path.split('.')[-1] != 'txt':
            path += '.txt'
        with open(path, "w") as f:
            lines = [[char_map[j] for j in row] for row in image]
            f.write('\n'.join([' '.join(line) for line in lines]))
        logging.info(_log_msg(path, os.stat(path).st_size))


def read(path: str) -> np.ndarray:
    """Read an image file into a NumPy array.

    Args:
        path (str): String file path with extention in {png, pbm, pgm, ppm}.

    Returns:
        np.ndarray: NumPy array representing the image.
    """
    _, ext = os.path.splitext(path)
    read_f = {'.png': read_png,
              '.pbm': read_netpbm,
              '.pgm': read_netpbm,
              '.ppm': read_netpbm}
    if ext not in read_f.keys():
        raise ValueError("File extension not supported.")
    else:
        return read_f[ext](path)


def recreate_script_from_png(image_path: str, script_path: str):
    """Recreate a script from the metadata of a PNG file.

    Args:
        image_path (str): String file path of PNG image.
        script_path (str): String file path of generated script.
    """
    with open(script_path, 'w') as f:
        print()
        f.write(imread(image_path).meta['Source'])
