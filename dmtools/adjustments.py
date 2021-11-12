import numpy as np
from typing import Callable


def apply_curve(image: np.ndarray, f: Callable, c: int = -1) -> np.ndarray:
    """Apply a curve f to an  image or channel of an image.

    Args:
        image (np.ndarray): Image on which to apply curve.
        f (Callable): Curve to apply. f: [0,1] -> [0,1].
        c (int): Channel to apply curve to. Apply to all channels if -1.

    Returns:
        np.ndarray: Image with curve applied.
    """
    if c == -1:
        return f(image)
    else:
        image = np.copy(image)
        n,m,k = image.shape
        channels = np.reshape(image, (n*m,k))
        channels[:,c] = f(channels[:,c])
        return np.reshape(channels, (n,m,k))
