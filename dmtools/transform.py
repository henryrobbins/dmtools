import numpy as np
from math import floor, ceil


def _rescale_axis(image: np.ndarray, axis: int, k: int) -> np.ndarray:
    # TODO: provide different resizing algorithms
    def f(x : float):
        return max(1-x, 0)
    support = 1.0

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
            # determine where the majority of the interval lies
            if ceil(a) - a > ((b - a) / 2.0):
                a = floor(a)
            else:
                a = ceil(a)
            b = a + 1
        a = round(a)
        b = round(b)
        row = image[a:b,:]

        # use weighting function to weight rows
        if row.shape[0] > 1:
            weights = [f(abs((i+0.5) - (bisect / k)) * k) for i in range(a,b)]
            density = np.sum(weights)
            row = np.dot(weights, row) / density

        # set row of rescaled image
        rescaled_image[i,:] = row

    if axis == 1:
        rescaled_image = np.swapaxes(rescaled_image,0,1)

    return rescaled_image


def rescale(image: np.ndarray, k: int) -> np.ndarray:
    """Rescale the image by the given scaling factor.

    Args:
        image (np.ndarray): Image to rescale.
        k (int): Scaling factor.

    Returns:
        np.ndarray: Rescaled image.
    """
    rescaled_image = _rescale_axis(image=image, axis=0, k=k)
    rescaled_image = _rescale_axis(image=rescaled_image, axis=1, k=k)
    return rescaled_image
