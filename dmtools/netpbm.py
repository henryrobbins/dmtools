import os
import time
import imageio
import numpy as np
from math import ceil
from collections import namedtuple
from skimage.transform import rescale
from typing import List, Callable
from .log import log_msg
import logging


# TODO: Improve this class defintion following conventions described in
# http://netpbm.sourceforge.net.
class Netpbm:
    """An object representing a Netpbm image.

    For more information about Netpbm images, see the
    `Netpbm Home Page <http://netpbm.sourceforge.net/>`_.
    """
    extension_to_magic_number = {"pbm": 1, "pgm": 2, "ppm": 3}
    magic_number_to_extension = {1: "pbm", 2: "pgm", 3: "ppm"}

    def __init__(self, P: int, k: int, w: int, h: int, M: np.ndarray):
        """Initialize a Netpbm image.

        Args:
            P (int): Magic number of the Netpbm image.
            k (int): Maximum gray/color value
            w (int): Width of the image
            h (int): Height of the image
            M (np.ndarray): A NumPy array representing the image pixels.
        """
        self.P = P
        self.w = w
        self.h = h
        self.k = k
        self.M = M

    def to_netpbm(self, path:str):
        """Write object to a Netpbm file (pbm, pgm, ppm).

        Uses the ASCII (plain) magic numbers.

        Args:
            path (str): String file path.
        """
        with open(path, "w") as f:
            f.write('P%d\n' % self.P)
            f.write("%s %s\n" % (self.w, self.h))
            if self.P != 1:
                f.write("%s\n" % (self.k))
            if self.P == 3:
                M = self.M.reshape(self.h, self.w * 3)
            else:
                M = self.M
            lines = M.clip(0,self.k).astype(int).astype(str).tolist()
            f.write('\n'.join([' '.join(line) for line in lines]))
            f.write('\n')

    def to_png(self, path:str, size:int):
        """Write object to a png file.

        Args:
            path (str): String file path.
            size (int): Target width.
        """
        # scale to desired size
        w = self.M.shape[1]
        image = enlarge(self, ceil(size / w))

        # reverse gradient if portable bit map image
        M = image.M
        if image.P == 1:
            M = np.where(M == 1, 0, 1)

        # scale gradient to 255
        M = M * (255 / image.k)
        M = M.astype(np.uint8)

        imageio.imwrite(path, M)


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
    return Netpbm(P, w, h, k, M)


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
    return Netpbm(P, w, h, k, M)


def read_netpbm(path:str) -> Netpbm:
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


def enlarge(image:Netpbm, k:int) -> Netpbm:
    """Enlarge the netpbm image by the multiplier k.

    Args:
        image (Netpbm): Netpbm image to enlarge.

    Returns:
       Netpbm: Enlarged Netpbm image.
    """
    # old implementation -- now using skimage for efficency
    # =====================================================
    # M = image.M
    # n,m = M.shape
    # expanded_rows = np.zeros((n*k,m))
    # for i in range(n*k):
    #     expanded_rows[i] = M[i // k]
    # expanded = np.zeros((n*k, m*k))
    # for j in range(m*k):
    #     expanded[:,j] = expanded_rows[:,j // k]
    # M_prime = expanded.astype(int)
    # =====================================================

    # NEAREST_NEIGHBOR (order=0)
    M = rescale(image.M, k,
                order=0, preserve_range=True, multichannel=(image.P == 3))
    w,h = image.w, image.h
    return Netpbm(P=image.P, w=w*k, h=h*k, k=image.k, M=M)


def change_gradient(image:Netpbm, k:int) -> Netpbm:
    """Change the max gradient value of the netpbm image M to n.

    Args:
        image (Netpbm): Netpbm image to change gradient for.
        k (int): New max gradient value.

    Returns:
       Netpbm: Netpbm image with changed gradient.
    """
    M_prime = np.array(list(map(lambda x: x // int(image.k / k), image.M)))
    return Netpbm(P=image.P, w=image.w, h=image.h, k=k, M=M_prime)


def image_grid(images:List[Netpbm], w:int, h:int, b:int,
               color:int = "white") -> Netpbm:
    """Create a w * h grid of images with a border of width b.

    Args:
        images (List[Netpbm]): images to be put in the grid (same dimensions).
        w (int): number of images in each row of the grid.
        h (int): number of images in each column of the grid.
        b (int): width of the border/margin.
        color (int): color of border {'white', 'black'} (defaults to white).

    Returns:
        Netpbm: grid layout of the images.
    """
    n,m = images[0].M.shape
    k = images[0].k
    c = {'white':k, 'black':0}[color]
    h_border = c*np.ones((b, w*m + (w+1)*b))
    v_border = c*np.ones((n, b))
    grid_layout = h_border
    p = 0
    for i in range(h):
        row = v_border
        for j in range(w):
            row = np.hstack((row, images[p].M))
            row = np.hstack((row, v_border))
            p += 1
        grid_layout = np.vstack((grid_layout, row))
        grid_layout = np.vstack((grid_layout, h_border))
    return Netpbm(P=images[0].P,
                  w=w*m + (w+1)*b,
                  h=h*n + (h+1)*b,
                  k=k, M=grid_layout.astype(int))


def border(image:Netpbm, b:int, color:int = "white") -> Netpbm:
    """Add a border of width b to the image

    Args:
        image (Netpbm): Netpbm image to add a border to
        b (int): width of the border/margin.
        color (int): color of border {'white', 'black'} (defaults to white).

    Returns:
        Netpbm: Image with border added.
    """
    return image_grid([image], w=1, h=1, b=b, color=color)


def transform(in_path:str, out_path:str, f:Callable, scale:int = -1, **kwargs):
    """Apply f to the image at in_path and write result to out_path.

    Args:
        in_path (str): Path of the image to be transformed.
        out_path (str): Path the transformed image is written to.
        f (Callable): Function to apply to the netpbm image.
        scale (int): Scale the image to this dimension. Defaults to -1.
        magic_number (int): "Magic number" {1,2,3}. Defaults to None.
    """
    then = time.time()

    image = read_netpbm(in_path)
    new_image = f(image=image, **kwargs)
    if scale != -1:
        m = ceil(scale / max(new_image.w,new_image.h))
        new_image = enlarge(new_image, m)
    new_image.to_netpbm(out_path)

    t = time.time() - then
    size = os.stat(out_path).st_size
    name = out_path.split('/')[-1]
    logging.info(log_msg(name, t, size))


def generate(path:str, f:Callable, scale:int = -1, **kwargs):
    """Generate a Netpbm image using f and write the image to the path.

    Args:
        path (str): Path to write the generated Netpbm image to.
        f (Callable): Function used to generate the image.
        scale (int): Scale the image to this dimension. Defaults to -1.
    """
    then = time.time()

    image = f(**kwargs)
    if scale != -1:
        m = ceil(scale / max(image.M.shape))
        image = enlarge(image, m)
    write(path, image)

    t = time.time() - then
    size = os.stat(path).st_size
    name = path.split('/')[-1]
    logging.info(log_msg(name, t, size))

# TODO: Comment to write in file should be provided as optional argument
# def netpbm_comment(file_name:str):
#     """Comment to be written in the

#     Args:
#         file_name (str): Name of the Netpbm file to be written.
#     """
#     name = file_name.split('/')[-1]
#     lines = ["Title: %s\n" % name,
#              "Compiled on: %s\n" % datetime.datetime.now(), "\n"]
#     readme_path = "/".join(file_name.split('/')[:-1]) + "/README.md"
#     with open(readme_path) as f:
#         readme = f.readlines()
#         indices = [i for i in range(len(readme)) if readme[i] == '\n']
#         lines = lines + readme[:indices[1]]
#     lines = ["# " + line for line in lines]
#     return lines


def animate(pattern:str, out_path:str, fps:int):
    """Creates an animation by calling the ffmpeg commmand line tool.

    Args:
        pattern (str): Pattern of the input frame.
        out_path (str): Path to write the output file to.
        fps (int): Frames per second.
    """
    # -r   set frame rate
    # -i   pattern of image frame file names
    # -y   overwrite output files
    # -an  disable audio
    # -vb  video bitrate
    # -sn  disable subtitle
    then = time.time()
    command = ("ffmpeg -r %d -i %s -y -an -vb 20M -sn %s"
               % (fps, pattern, out_path))
    os.system(command)
    t = time.time() - then
    size = os.stat(out_path).st_size
    name = out_path.split('/')[-1]
    logging.info(log_msg(name, t, size))
