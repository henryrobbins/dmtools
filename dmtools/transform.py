import numpy as np
from math import floor, ceil


def box_resize_weighting_function(x: float) -> float:
    """Box filter's weighting function.

    For more information about the Box filter, see
    `Box <https://legacy.imagemagick.org/Usage/filter/#box>`_.

    Args:
        x (float): distance to source pixel.

    Returns:
        float: weight on the source pixel.
    """
    return 1 if x <= 0.5 else 0


def triangle_resize_weighting_function(x: float) -> float:
    """Triangle filter's weighting function.

    For more information about the Triangle filter, see
    `Triangle <https://legacy.imagemagick.org/Usage/filter/#triangle>`_.

    Args:
        x (float): distance to source pixel.

    Returns:
        float: weight on the source pixel.
    """
    return max(1 - x, 0.0)


RESIZE_FILTERS = \
    {'point':    (box_resize_weighting_function,      0.0),
     'box':      (box_resize_weighting_function,      0.5),
     'triangle': (triangle_resize_weighting_function, 1.0)}


def _rescale_axis(image: np.ndarray, axis: int, k: int, filter: str) -> np.ndarray:
    f, support = RESIZE_FILTERS[filter]
    if k > 1:
        support = support * k

    if axis == 1:
        image = np.swapaxes(image,0,1)

    n, *_ = image.shape
    new_shape = list(image.shape)
    new_shape[0] = int(new_shape[0] * k)
    rescaled_image = np.zeros(new_shape)
    for i in range(new_shape[0]):
        # get range of rows in the support
        bisect = i + 0.5
        a = max((bisect - support) / k, 0.0)
        b = min((bisect + support) / k, n)
        if (b-a < 1):
            # fall back to nearest neighbor heuristic
            if ceil(a) - a > ((b - a) / 2.0):
                a = floor(a)
            else:
                a = ceil(a)
            b = a + 1
        a = round(a)
        b = round(b)
        row = image[a:b,:]

        # use weighting function to weight rows
        if k <= 1:
            weights = [f(abs((i+0.5) - (bisect / k)) * k) for i in range(a,b)]
        else:
            weights = [f(abs((i+0.5) - (bisect / k))) for i in range(a,b)]
        density = np.sum(weights)
        row = np.dot(weights, row) / density

        # set row of rescaled image
        rescaled_image[i,:] = row

    if axis == 1:
        rescaled_image = np.swapaxes(rescaled_image,0,1)

    return rescaled_image


def rescale(image: np.ndarray, k: int, filter: str='point') -> np.ndarray:
    """Rescale the image by the given scaling factor.

    Args:
        image (np.ndarray): Image to rescale.
        k (int): Scaling factor.
        filter (str): {point, box, triangle}. Defaults to point.

    Returns:
        np.ndarray: Rescaled image.
    """
    rescaled_image = _rescale_axis(image=image, axis=0, k=k, filter=filter)
    rescaled_image = _rescale_axis(image=rescaled_image, axis=1, k=k, filter=filter)
    return rescaled_image
