import numpy as np
from math import floor, ceil, sqrt
from functools import partial
from typing import Callable


def _box_weighting_function(x: float) -> float:
    """Box filter's weighting function.

    For more information about the Box filter, see
    `Box <https://legacy.imagemagick.org/Usage/filter/#box>`_.

    Args:
        x (float): distance to source pixel.

    Returns:
        float: weight on the source pixel.
    """
    return 1 if x <= 0.5 else 0


def _triangle_weighting_function(x: float) -> float:
    """Triangle filter's weighting function.

    For more information about the Triangle filter, see
    `Triangle <https://legacy.imagemagick.org/Usage/filter/#triangle>`_.

    Args:
        x (float): distance to source pixel.

    Returns:
        float: weight on the source pixel.
    """
    return max(1 - x, 0.0)


def _catmull_rom_weighting_function(x: float) -> float:
    """Catmull-Rom filter's weighting function.

    For more information about the Catmull-Rom filter, see
    `Cubic Filters <https://legacy.imagemagick.org/Usage/filter/#cubics>`_.

    Args:
        x (float): distance to source pixel.

    Returns:
        float: weight on the source pixel.
    """
    if x <= 1:
        return (3*x**3 - 5*x**2 + 2) / 2
    elif x <= 2:
        return (-x**3 + 5*x**2 - 8*x + 4) / 2
    else:
        return 0


def _gaussian_weighting_function(x: float,
                                 sigma: float = 0.5,
                                 blur: float = 1.0) -> float:
    """Gaussian blur function.

    For information about Gaussian blur, see
    `Gaussian <https://legacy.imagemagick.org/Usage/filter/#gaussian>`_.

    Args:
        x (float): Distance to source pixel.
        sigma (float): Determines the "neighborhood" of blur. Defaults to 0.5.
        blur (float): Scale sigma by some multiplier. Defaults to 1.0.

    Returns:
        float: weight on the source pixel.
    """
    sigma = sigma * blur
    return (1 / sqrt(2*np.pi*sigma**2))*np.power(np.e, -x**2 / (2*sigma**2))


RESIZE_FILTERS = \
    {'point':    (_box_weighting_function,          0.0),
     'box':      (_box_weighting_function,          0.5),
     'triangle': (_triangle_weighting_function,     1.0),
     'catrom':   (_catmull_rom_weighting_function,  2.0),
     'gaussian': (_gaussian_weighting_function,     2.0)}

EPSILON = 1.0e-6


def _rescale_axis(image: np.ndarray,
                  axis: int,
                  k: int,
                  filter: str,
                  weighting_function: Callable = None,
                  support: Callable = None,
                  **kwargs) -> np.ndarray:
    # set the weighting function and support
    if weighting_function is not None:
        if support is None:
            raise ValueError('Weighting function provided without support.')
        f = weighting_function
        support = support
    else:
        f, support = RESIZE_FILTERS[filter]

    # scale support if blur keyword argument is passed
    if 'blur' in kwargs:
        support = support * kwargs['blur']

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

        def x(i):
            """Return distance to source pixel."""
            return abs((i+0.5) - (bisect / k))

        # use weighting function to weight rows
        if k <= 1:
            weights = np.array([f(x(i) * k, **kwargs) for i in range(a,b)])
        else:
            weights = np.array([f(x(i), **kwargs) for i in range(a,b)])

        # TODO: This is the numerically stable way to implement this.
        #       Need to decide if this implementation should be used.
        # weights = weights / max(np.sum(weights), EPSILON) # normalize weights
        # row = np.dot(weights, np.swapaxes(row,0,1))
        row = np.average(row, axis=0, weights=weights)

        # set row of rescaled image
        rescaled_image[i,:] = row

    if axis == 1:
        rescaled_image = np.swapaxes(rescaled_image,0,1)

    return rescaled_image


def rescale(image: np.ndarray,
            k: int,
            filter: str = 'point',
            weighting_function: Callable = None,
            support: Callable = None,
            **kwargs) -> np.ndarray:
    """Rescale the image by the given scaling factor.

    This image rescale implentation is largley based off of the `ImageMagick`_
    impmenetation. The following filters are built-in:

    - `Point Filter`_ ("point"): Nearest-neighbor heuristic.
    - `Box Filter`_ ("box"): Average of neighboring pixels.
    - `Triangle Filter`_ ("triangle"): Linear decrease in pixel weight.
    - `Catmull-Rom Filter`_ ("catrom"): Produces a sharper edge.
    - `Gaussian Filter`_ ("gaussian"): Blurs image. Useful as low pass filter.

    Additionally, advanced users can specify a custom filter by providing a
    weighting function and a support.

    .. _ImageMagick: https://imagemagick.org/script/index.php
    .. _Point Filter: https://legacy.imagemagick.org/Usage/filter/#point
    .. _Box Filter: https://legacy.imagemagick.org/Usage/filter/#box
    .. _Triangle Filter: https://legacy.imagemagick.org/Usage/filter/#triangle
    .. _Catmull-Rom Filter: https://legacy.imagemagick.org/Usage/filter/#cubics
    .. _Gaussian Filter: https://legacy.imagemagick.org/Usage/filter/#gaussian

    Args:
        image (np.ndarray): Image to rescale.
        k (int): Scaling factor.
        filter (str): {point, box, triangle, catrom, gaussian}.
        weighting_function (Callable): Weighting function to use.
        support (float): Support of the provided weighting function.

    Returns:
        np.ndarray: Rescaled image.
    """
    rescaled_image = _rescale_axis(image=image, axis=0, k=k, filter=filter,
                                   weighting_function=weighting_function,
                                   support=support, **kwargs)
    rescaled_image = _rescale_axis(image=rescaled_image, axis=1, k=k,
                                   filter=filter,
                                   weighting_function=weighting_function,
                                   support=support, **kwargs)
    return rescaled_image


def blur(image: np.ndarray, sigma: float, radius: float = 0) -> np.ndarray:
    """Blur the image.

    This image blur implentation is largley based off of the `ImageMagick`_
    impmenetation. It uses a `Gaussian Filter`_ with parameter ``sigma`` and
    a support of ``radius`` to blur the image.

    .. _ImageMagick: https://imagemagick.org/script/index.php
    .. _Gaussian Filter: https://legacy.imagemagick.org/Usage/filter/#gaussian

    Args:
        image (np.ndarray): Image to be blurred.
        sigma (float): "Neighborhood" of the blur. A larger value is blurrier.
        radius (float): Limit of the blur. Defaults to 4 x sigma.

    Returns:
        np.ndarray: Blurred image.
    """
    if radius == 0:
        radius = 4 * sigma
    f = partial(_gaussian_weighting_function, sigma=sigma)
    return rescale(image, k=1, weighting_function=f, support=radius)


def clip(image: np.ndarray) -> np.ndarray:
    """Clip gray/color values that are out of bounds.

    Every value less than 0 is mapped to 0 and every value more than 1 is
    mapped to 1. Values in [0,1] are untouched.

    Args:
        image (np.ndarray): Image to clip.

    Returns:
        np.ndarray: Clipped image.
    """
    return np.clip(image, 0, 1)


def normalize(image: np.ndarray) -> np.ndarray:
    """Normalize the image to bring all gray/color values into bounds.

    Normalize the range of values in the image to [0,1]. If applied to a
    three channel image, normalizes each channel by the same amount.

    Args:
        image (np.ndarray): Image to normalize.

    Returns:
        np.ndarray: Normalized image.
    """
    if np.max(image) == np.min(image):
        # every value in the image is the same--fall back to clip
        return clip(image)
    image = image - np.min(image)
    return image * (1 / (np.max(image)))


def wraparound(image: np.ndarray) -> np.ndarray:
    """Wraparound gray/color values that are out of bounds.

    Each value x is mapped to x mod 1 such that values outside of [0,1]
    wraparound until they fall in the desired range.

    Args:
        image (np.ndarray): Image to wraparound

    Returns:
        np.ndarray: Wraparound image.
    """
    # TODO: Is there a quicker way to implement this?
    # TODO: Is this the right implementation?
    image = np.where(image > 1, np.modf(image)[0], image)
    image = np.where(image < 0, np.modf(image)[0] + 1, image)
    return image
