import numpy as np

# Referenced colorconv.py from scikit-image for more efficient implementation
# of colorspace transformations. Will continue to maintain an independent
# implementation for educational purposes but scikit-image is the standard.

# https://wikipedia.org/wiki/Standard_illuminant
# These values assume the 2 degree point of view
illuminants = \
    {'D50': (96.4212, 100.0, 82.5188),
     'D65': (95.0489, 100.0, 108.8840)}

# http://poynton.ca/PDFs/ColorFAQ.pdf
rgb_to_gray = np.array([0.2125, 0.7154, 0.0721])

# https://wikipedia.org/wiki/CIE_1931_color_space
b_21 = 0.17697
rgb_to_xyz = np.array([[0.49000, 0.31000, 0.20000],
                       [0.17697, 0.81240, 0.01063],
                       [0.00000, 0.01000, 0.99000]]) / b_21
xyz_to_rgb = np.linalg.inv(rgb_to_xyz)

# https://wikipedia.org/wiki/YUV
rgb_to_yuv = np.array([[+0.29900, +0.58700, +0.11400],
                       [-0.14713, -0.28886, +0.43600],
                       [+0.61500, -0.51499, -0.10001]])
yuv_to_rgb = np.linalg.inv(rgb_to_yuv)

# Used to normalize an image in a colorspace to [0,1]
norm = \
    {'RGB': {'scale': (1.0, 1.0, 1.0),
             'shift': (0.0, 0.0, 0.0)},
     'Lab': {'scale': (1.0, 1.0, 1.0),
             'shift': (0.0, -0.5, -0.5)},
     'YUV': {'scale': (1.0, 1.0, 1.0),
             'shift': (0.0, -0.5, -0.5)}}


def RGB_to_gray(image: np.ndarray) -> np.ndarray:
    """Convert an image in CIE RGB space to grayscale.

    For details about the implemented conversion, see
    `FAQs about Color <http://poynton.ca/PDFs/ColorFAQ.pdf>`_.

    Args:
        image (np.ndarray): Image in CIE RGB space.

    Returns:
        np.ndarray: Image in grayscale.
    """
    image = np.copy(image)
    # TODO: this causes opacity of 4-channel images to be lost
    image = image[:,:,:3] @ rgb_to_gray.T
    return image


def gray_to_RGB(image: np.ndarray) -> np.ndarray:
    """Convert an image in grayscale to CIE RGB space.

    Args:
        image (np.ndarray): Image in grayscale.

    Returns:
        np.ndarray: Image in CIE RGB space.
    """
    return np.stack(3 * (image,), axis=-1)


def add_alpha(image: np.ndarray, a: float = 1) -> np.ndarray:
    """Add an alpha channel to a three color channel image.

    Args:
        image (np.ndarray): Image with three color channels.
        a (float): Alpha value to use in the image.

    Returns:
        np.ndarray: Four channel image with alpha channel.
    """
    n,m,*_ = image.shape
    return np.concatenate((image, a * np.ones((n,m,1))), axis=-1)


def RGB_to_XYZ(image: np.ndarray) -> np.ndarray:
    """Convert an image in CIE RGB space to XYZ space.

    For details about the implemented conversion, see
    `CIE 1931 color space <https://wikipedia.org/wiki/CIE_1931_color_space>`_.

    Args:
        image (np.ndarray): Image in CIE RGB space.

    Returns:
        np.ndarray: Image in CIE XYZ space.
    """
    image = np.copy(image)
    image[:,:,:3] = image[:,:,:3] @ rgb_to_xyz.T
    return image


def XYZ_to_RGB(image: np.ndarray) -> np.ndarray:
    """Convert an image in CIE XYZ space to RGB space.

    For details about the implemented conversion, see
    `CIE 1931 color space <https://wikipedia.org/wiki/CIE_1931_color_space>`_.

    Args:
        image (np.ndarray): Image in CIE XYZ space.

    Returns:
        np.ndarray: Image in CIE RGB space.
    """
    image = np.copy(image)
    image[:,:,:3] = image[:,:,:3] @ xyz_to_rgb.T
    return image


def RGB_to_YUV(image: np.ndarray) -> np.ndarray:
    """Convert an image in CIE RGB space to YUV space.

    For details about the implemented conversion, see
    `YUV <https://wikipedia.org/wiki/YUV>`_.

    Args:
        image (np.ndarray): Image in CIE RGB space.

    Returns:
        np.ndarray: Image in YUV space.
    """
    image = np.copy(image)
    image[:,:,:3] = image[:,:,:3] @ rgb_to_yuv.T
    return image


def YUV_to_RGB(image: np.ndarray) -> np.ndarray:
    """Convert an image in YUV space to CIE RGB space.

    For details about the implemented conversion, see
    `YUV <https://wikipedia.org/wiki/YUV>`_.

    Args:
        image (np.ndarray): Image in YUV space.

    Returns:
        np.ndarray: Image in CIE RGB space.
    """
    image = np.copy(image)
    image[:,:,:3] = image[:,:,:3] @ yuv_to_rgb.T
    return image


def XYZ_to_Lab(image: np.ndarray, illuminant: str = 'D65') -> np.ndarray:
    """Convert an image in CIE XYZ space to Lab space.

    For details about the implemented conversion, see
    `CIELAB color space <https://wikipedia.org/wiki/CIELAB_color_space>`_.

    Args:
        image (np.ndarray): Image in CIE XYZ space.
        illuminant (str): Standard illuminant {D65, D50}

    Returns:
        np.ndarray: Image in Lab space.
    """
    X_n, Y_n, Z_n = illuminants[illuminant]
    delta = 6 / 29

    def f(t):
        return t**(1/3) if t > delta**3 else (t/(3*delta**2)) + (4/29)

    def to_Lab(x):
        X, Y, Z = x
        L = 116*f(Y/Y_n) - 16
        a = 500*(f(X/X_n) - f(Y/Y_n))
        b = 200*(f(Y/Y_n) - f(Z/Z_n))
        return np.array([L,a,b])

    image = np.copy(image)
    n,m,k = image.shape
    p = np.reshape(image[:,:,:3], (n*m,3)).astype(float)
    p = np.apply_along_axis(to_Lab, 1, p)
    image[:,:,:3] = np.reshape(p, (n,m,3))
    return image


def Lab_to_XYZ(image: np.ndarray, illuminant: str = 'D65') -> np.ndarray:
    """Convert an image in Lab space to CIE XYZ space.

    For details about the implemented conversion, see
    `CIELAB color space <https://wikipedia.org/wiki/CIELAB_color_space>`_.

    Args:
        image (np.ndarray): Image in Lab space.
        illuminant (str): Standard illuminant {D65, D50}

    Returns:
        np.ndarray: Image in CIE XYZ space.
    """
    X_n, Y_n, Z_n = illuminants[illuminant]
    delta = 6 / 29

    def f_inv(t):
        return t**3 if t > delta else 3*delta**2*(t-(4/29))

    def to_XYZ(x):
        L, a, b = x
        X = X_n*f_inv(((L + 16)/116) + a/500)
        Y = Y_n*f_inv((L + 16)/116)
        Z = Z_n*f_inv(((L + 16)/116) - b/200)
        return np.array([X,Y,Z])

    image = np.copy(image)
    n,m,k = image.shape
    p = np.reshape(image[:,:,:3], (n*m,3)).astype(float)
    p = np.apply_along_axis(to_XYZ, 1, p)
    image[:,:,:3] = np.reshape(p, (n,m,3))
    return image


def RGB_to_Lab(image: np.ndarray, illuminant: str = 'D65') -> np.ndarray:
    """Convert an image in CIE RGB space to Lab space.

    For details about the implemented conversion, see
    `CIE 1931 color space <https://wikipedia.org/wiki/CIE_1931_color_space>`_
    and
    `CIELAB color space <https://wikipedia.org/wiki/CIELAB_color_space>`_.

    Args:
        image (np.ndarray): Image in CIE RGB space.
        illuminant (str): Standard illuminant {D65, D50}

    Returns:
        np.ndarray: Image in Lab space.
    """
    return XYZ_to_Lab(RGB_to_XYZ(image), illuminant)


def Lab_to_RGB(image: np.ndarray, illuminant: str = 'D65') -> np.ndarray:
    """Convert an image in Lab space to CIE RGB space.

    For details about the implemented conversion, see
    `CIE 1931 color space <https://wikipedia.org/wiki/CIE_1931_color_space>`_
    and
    `CIELAB color space <https://wikipedia.org/wiki/CIELAB_color_space>`_.

    Args:
        image (np.ndarray): Image in Lab space.
        illuminant (str): Standard illuminant {D65, D50}

    Returns:
        np.ndarray: Image in CIE RGB space.
    """
    return XYZ_to_RGB(Lab_to_XYZ(image, illuminant))


def normalize(image: np.ndarray, color_space: str) -> np.ndarray:
    """Normalize the image in the given color space.

    Args:
        image (np.ndarray): Image in the given color space.
        color_space (str): Color space {RGB, Lab, YUV}.

    Returns:
        np.ndarray: Normalized image with values in [0,1].
    """
    scale = norm[color_space]['scale']
    shift = norm[color_space]['shift']
    shift_mat = np.ones(image.shape) @ np.diag(shift)
    normalized_image = (image - shift_mat) @ np.diag(1 / np.array(scale))
    return normalized_image.clip(0,1)


def denormalize(image: np.ndarray, color_space: str) -> np.ndarray:
    """Denormalize the image in the given color space.

    Args:
        image (np.ndarray): Normalized image in the given color space.
        color_space (str): Color space {RGB, Lab, YUV}.

    Returns:
        np.ndarray: Denormalized image in the given color space.
    """
    scale = norm[color_space]['scale']
    shift = norm[color_space]['shift']
    shift_mat = np.ones(image.shape) @ np.diag(shift)
    return (image @ np.diag(scale)) + shift_mat
