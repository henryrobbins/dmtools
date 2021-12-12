import numpy as np
from typing import List


def image_grid(images: List[np.ndarray], w: int, h: int, b: int,
               color: np.ndarray = None) -> np.ndarray:
    """Create a w * h grid of images with a border of width b.

    Args:
        images (List[np.ndarray]): images (of same dimension) for grid.
        w (int): number of images in each row of the grid.
        h (int): number of images in each column of the grid.
        b (int): width of the border/margin.
        color (np.ndarray): Pixel to use for bordering. Defaults to white.

    Returns:
        np.ndarray: grid layout of the images.
    """
    n,m,*k = images[0].shape
    if len(k) == 0:
        color = 1 if color is None else color
        h_border = np.full((b, w*m + (w+1)*b), color)
        v_border = np.full((n, b), color)
    else:
        k = k[0]
        color = np.ones(k) if color is None else color
        h_border = np.full((b, w*m + (w+1)*b, k), color)
        v_border = np.full((n, b, k), color)
    grid_layout = h_border
    for i in range(h):
        row = v_border
        for j in range(w):
            row = np.hstack((row, images[(i*w) + j]))
            row = np.hstack((row, v_border))
        grid_layout = np.vstack((grid_layout, row))
        grid_layout = np.vstack((grid_layout, h_border))
    return grid_layout


def border(image: np.ndarray, b: int, color: np.ndarray = None) -> np.ndarray:
    """Add a border of width b to the image.

    Args:
        image (Netpbm): Netpbm image to add a border to
        b (int): width of the border/margin.
        color (np.ndarray): Pixel to use for bordering. Defaults to white.

    Returns:
        np.ndarray: Image with border added.
    """
    return image_grid([image], w=1, h=1, b=b, color=color)
