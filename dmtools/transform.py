import numpy as np
from math import floor, ceil, sqrt
from functools import partial
from enum import Enum
from collections import namedtuple
from typing import Union, List


class Loc(Enum):
    UPPER_LEFT = "upper_left"
    LOWER_LEFT = "lower_left"
    CENTER = "center"


def _box_weighting_function(x: float) -> float:
    return 1 if x <= 0.5 else 0


def _triangle_weighting_function(x: float) -> float:
    return max(1 - x, 0.0)


def _catmull_rom_weighting_function(x: float) -> float:
    if x <= 1:
        return (3*x**3 - 5*x**2 + 2) / 2
    elif x <= 2:
        return (-x**3 + 5*x**2 - 8*x + 4) / 2
    else:
        return 0


def _gaussian_weighting_function(x: float, sigma: float = 0.5,
                                 blur: float = 1.0) -> float:
    sigma = sigma * blur
    return (1 / sqrt(2*np.pi*sigma**2))*np.power(np.e, -x**2 / (2*sigma**2))


ResizeFilter = namedtuple('ResizeFilter', 'weighting_function support')
ResizeFilter.__doc__ = """\
Image resize filter.

To learn more about image resize filters, see the `ImageMagick`_ reference on
`Resampling Filters`_.

Parameters:
    weighting_function (Callable): Weighting function defined on [0, support].
    support (float): The ideal neighborhood size of the filter.

.. _ImageMagick: https://imagemagick.org/script/index.php
.. _Resampling Filters: https://legacy.imagemagick.org/Usage/filter/
"""


class ResizeFilterName(Enum):
    """An enumeration of supported resize filter names.

    The supported filters are a subset of `ImageMagick`_ filters.

    - `Point Filter`_ (POINT): Nearest-neighbor heuristic.
    - `Box Filter`_ (BOX): Average of neighboring pixels.
    - `Triangle Filter`_ (TRIANGLE): Linear decrease in pixel weight.
    - `Catmull-Rom Filter`_ (CATROM): Produces a sharper edge.
    - `Gaussian Filter`_ (GAUSSIAN): Blurs image. Useful as low pass filter.

    .. _ImageMagick: https://imagemagick.org/script/index.php
    .. _Point Filter: https://legacy.imagemagick.org/Usage/filter/#point
    .. _Box Filter: https://legacy.imagemagick.org/Usage/filter/#box
    .. _Triangle Filter: https://legacy.imagemagick.org/Usage/filter/#triangle
    .. _Catmull-Rom Filter: https://legacy.imagemagick.org/Usage/filter/#cubics
    .. _Gaussian Filter: https://legacy.imagemagick.org/Usage/filter/#gaussian
    """
    POINT = ResizeFilter(_box_weighting_function, 0.0)
    BOX = ResizeFilter(_box_weighting_function, 0.5)
    TRIANGLE = ResizeFilter(_triangle_weighting_function, 1.0)
    CATROM = ResizeFilter(_catmull_rom_weighting_function, 2.0)
    GAUSSIAN = ResizeFilter(_gaussian_weighting_function, 2.0)


def _safe_divide(n: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Divide NumPy arrays where divide by zero is zero.

    Args:
        n (np.ndarray): Numerator NumPy array.
        d (np.ndarray): Denominator NumPy array.

    Returns:
        np.ndarray: Numerator divided by denominator.
    """
    return np.divide(n, d, out=np.zeros_like(n), where=(d != 0))


def _over_alpha_composite(aA, aB) -> np.ndarray:
    return aA + aB * (1 - aA)


def _over_color_composite(xA, aA, xB, aB, xaA, xaB, aR) -> np.ndarray:
    return _safe_divide(xaA + xaB * (1 - aA), aR)


def _dest_over_alpha_composite(aA, aB) -> np.ndarray:
    return aB + aA * (1 - aB)


def _dest_over_color_composite(xA, aA, xB, aB, xaA, xaB, aR) -> np.ndarray:
    return _safe_divide(xaB + xaA * (1 - aB), aR)


def _add_alpha_composite(aA, aB) -> np.ndarray:
    return np.clip(aA + aB, 0, 1)


def _add_color_composite(xA, aA, xB, aB, xaA, xaB, aR) -> np.ndarray:
    return _safe_divide(xaA + xaB, aR)


CompositeOp = namedtuple('CompositeOp', 'alpha color')
CompositeOp.__doc__ = """\
Image alpha compositing operators.

To learn more about image alpha compositing, see `Alpha Compositing`_.

Parameters:
    alpha (Callable): The function producing the alpha of the resulting image.
    color (Callable): The function producing the color of the resulting image.

.. _Alpha Compositing: https://en.wikipedia.org/wiki/Alpha_compositing
"""


class CompositeOpName(Enum):
    """An enumeration of supported image alpha compositing operator names.

    The supported operators are a subset of `Cairo`_ operators.

    -  (OVER): two semi-transparent slides; source over dest.
    -  (DEST_OVER): two semi-transparent slides; dest over source.
    -  (ADD): Add source and dest.

    .. _Cairo: https://www.cairographics.org/operators
    """
    OVER = CompositeOp(_over_alpha_composite, _over_color_composite)
    DEST_OVER = CompositeOp(_dest_over_alpha_composite,
                            _dest_over_color_composite)
    ADD = CompositeOp(_add_alpha_composite, _add_color_composite)


EPSILON = 1.0e-6


def _rescale_axis(image: np.ndarray, axis: int, k: int,
                  filter: Union[ResizeFilterName, ResizeFilter],
                  **kwargs) -> np.ndarray:
    # set the weighting function and support
    if not isinstance(filter, ResizeFilter):
        filter = filter.value
    f = filter.weighting_function
    support = filter.support

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


def rescale(image: np.ndarray, k: int = -1, w: int = -1, h: int = -1,
            filter: Union[ResizeFilterName, ResizeFilter] =
            ResizeFilterName.POINT, **kwargs) -> np.ndarray:
    """Rescale the image.

    Provide either a global scale factor k or the desired dimensions (w,h) of
    the rescaled image. This image rescale implentation is largley based off of
    the `ImageMagick`_ impmenetation.

    .. _ImageMagick: https://imagemagick.org/script/index.php

    Args:
        image (np.ndarray): Image to rescale.
        k (int): Scaling factor.
        w (int): Desired width (in pixels).
        h (int): Desired height (in pixels).
        filter (Union[ResizeFilterName, ResizeFilter]): Resize filter to use.

    Returns:
        np.ndarray: Rescaled image.
    """
    if k != -1:
        w_scale = k
        h_scale = k
    elif w != -1 and h != -1:
        n,m,*_ = image.shape
        w_scale = w / m
        h_scale = h / n
    else:
        raise ValueError("Provide scale factor k or desired dimensions (w,h).")

    rescaled_image = _rescale_axis(image=image, axis=0, k=h_scale,
                                   filter=filter, **kwargs)
    rescaled_image = _rescale_axis(image=rescaled_image, axis=1, k=w_scale,
                                   filter=filter, **kwargs)
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
    filter = ResizeFilter(f, radius)
    return rescale(image, k=1, filter=filter)


def composite(source: np.ndarray, dest: np.ndarray,
              operator: Union[CompositeOpName, CompositeOp] =
              CompositeOpName.OVER) -> np.ndarray:
    """Return the image formed by compositing one image with another.

    For more information about alpha compositing, see `Alpha Compositing`_. The
    implementation is largely based on the `Cairo`_ implementation.

    .. _Alpha Compositing: https://en.wikipedia.org/wiki/Alpha_compositing
    .. _Cairo: https://www.cairographics.org/operators

    Args:
        source (np.ndarray): Image on top.
        dest (np.ndarray): Image on bottom.
        operator (Union[CompositeOpName, CompositeOp]): \
            The compositing operator to use.

    Returns:
        np.ndarray: The two images overlaid.
    """
    xA, aA = np.split(source, [3], axis=2)
    xB, aB = np.split(dest, [3], axis=2)
    xaA = xA * aA
    xaB = xB * aB

    if not isinstance(operator, CompositeOp):
        operator = operator.value

    alpha_composite = operator.alpha
    color_composite = operator.color

    aR = alpha_composite(aA, aB)
    xR = color_composite(xA, aA, xB, aB, xaA, xaB, aR)
    return np.append(xR, aR, axis=2)


def _standardize_selection(image: np.ndarray, x: float, y: float, w: float,
                           h: float, relative: bool, loc: Loc) -> List[float]:
    if relative:
        n,m,*_ = image.shape
        x = m * x
        y = n * y
        w = m * w
        h = n * h
    if loc == Loc.UPPER_LEFT:
        pass
    elif loc == Loc.LOWER_LEFT:
        y = image.shape[0] - y
    elif loc == Loc.CENTER:
        x = x - (w / 2)
        y = y - (h / 2)
    else:
        raise ValueError(f"{loc.value} is not a supported loc.")
    return int(x), int(y), int(w), int(h)


def substitute(image: np.ndarray, substitution: np.ndarray, x: float, y: float,
               relative: bool = False,
               loc: Loc = Loc.UPPER_LEFT) -> np.ndarray:
    """Substitute a portion of image with substitution.

    Args:
        image (np.ndarray): Base image.
        substitution (np.ndarray): Image to substitute into the base image.
        x (float): x coordinate of the point (relative to left of image).
        y (float): y coordinate of the point (relative to top of image).
        relative (bool): If True, x, y, w, and h are given relative to the \
            dimensions of the image. Defaults to False.
        loc (Loc): Location of (x,y) relative to substituted portion.

    Returns:
        np.ndarray: The image with substitution substituted in.
    """
    if relative:
        n,m,*_ = image.shape
        h,w,*_ = substitution.shape
        w = w / m
        h = h / n
    else:
        h,w,*_ = substitution.shape
    x, y, w, h = _standardize_selection(image, x, y, w, h, relative, loc)
    if len(image.shape) == 3:
        image[y:y+h, x:x+w, :] = substitution
    else:
        image[y:y+h, x:x+w] = substitution
    return image


def crop(image: np.ndarray, x: float, y: float, w: float, h: float,
         relative: bool = False, loc: Loc = Loc.UPPER_LEFT) -> np.ndarray:
    """Crop an image using an (x,y) point, width, and height.

    Args:
        image (np.ndarray): Image to be cropped.
        x (float): x coordinate of the point (relative to left of image).
        y (float): y coordinate of the point (relative to top of image).
        w (float): Width of the cropped portion.
        h (float): Height of the cropped portion.
        relative (bool): If True, x, y, w, and h are given relative to the \
            dimensions of the image. Defaults to False.
        loc (Loc): Location of (x,y) relative to substituted portion.

    Returns:
        np.ndarray: The cropped portion of the image.
    """
    x, y, w, h = _standardize_selection(image, x, y, w, h, relative, loc)
    if len(image.shape) == 3:
        return image[y:y+h, x:x+w, :]
    else:
        return image[y:y+h, x:x+w]


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
