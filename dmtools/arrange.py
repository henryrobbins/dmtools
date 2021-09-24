import numpy as np
from typing import List


def image_grid(images: List[np.ndarray], w: int, h: int, b: int,
               color: int = "white", k: int = 255) -> np.ndarray:
    """Create a w * h grid of images with a border of width b.

    Args:
        images (List[np.ndarray]): images (of same dimension) for grid.
        w (int): number of images in each row of the grid.
        h (int): number of images in each column of the grid.
        b (int): width of the border/margin.
        color (int): color of border {'white', 'black'} (defaults to white).
        k (int): white point (defaults to 255).

    Returns:
        np.ndarray: grid layout of the images.
    """
    n,m = images[0].shape
    c = {'white': k, 'black': 0}[color]
    h_border = c*np.ones((b, w*m + (w+1)*b))
    v_border = c*np.ones((n, b))
    grid_layout = h_border
    p = 0
    for i in range(h):
        row = v_border
        for j in range(w):
            row = np.hstack((row, images[p]))
            row = np.hstack((row, v_border))
            p += 1
        grid_layout = np.vstack((grid_layout, row))
        grid_layout = np.vstack((grid_layout, h_border))
    return grid_layout.astype(int)


def border(image: np.ndarray, b: int,
           color: int = "white", k: int = 255) -> np.ndarray:
    """Add a border of width b to the image.

    Args:
        image (Netpbm): Netpbm image to add a border to
        b (int): width of the border/margin.
        color (int): color of border {'white', 'black'} (defaults to white).
        k (int): white point (defaults to 255).

    Returns:
        np.ndarray: Image with border added.
    """
    return image_grid([image], w=1, h=1, b=b, color=color, k=k)
