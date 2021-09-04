import numpy as np
from typing import Callable

# Referenced colorconv.py from scikit-image for more efficient implementation
# of colorspace transformations. Will continue to maintain an independent
# implementation for educational purposes but scikit-image is the standard.

# https://en.wikipedia.org/wiki/Standard_illuminant
illuminants = \
    {'D50':(96.4212, 100.0, 82.5188),
     'D65':(95.0489, 100.0, 108.8840)}

# https://en.wikipedia.org/wiki/CIE_1931_color_space
b_21 = 0.17697
rgb_to_xyz = np.array([[0.49000, 0.31000, 0.20000],
                       [0.17697, 0.81240, 0.01063],
                       [0.00000, 0.01000, 0.99000]]) / b_21
xyz_to_rgb = np.linalg.inv(rgb_to_xyz)

# https://en.wikipedia.org/wiki/YUV
rgb_to_yuv = np.array([[+0.29900, +0.58700, +0.11400],
                       [-0.14713, -0.28886, +0.43600],
                       [+0.61500, -0.51499, -0.10001]])
yuv_to_rgb = np.linalg.inv(rgb_to_yuv)


def RGB_to_XYZ(pixels:np.ndarray) -> np.ndarray:
    """Convert a pixel matrix in RGB color space to XYZ color space.

    For details about the conversion from the CIE RGB space to XYZ space, see
    `CIE 1931 color space <https://en.wikipedia.org/wiki/CIE_1931_color_space>`_.

    Args:
        pixels (np.ndarray): Pixels in the RGB color space.

    Returns:
        np.ndarray: Pixel matrix in the XYZ color space.
    """
    return pixels @ rgb_to_xyz.T


def XYZ_to_RGB(pixels:np.ndarray) -> np.ndarray:
    """Convert a pixel matrix in XYZ color space to RGB color space.

    For details about the conversion from the CIE XYZ space to RGB space, see
    `CIE 1931 color space <https://en.wikipedia.org/wiki/CIE_1931_color_space>`_.

    Args:
        pixels (np.ndarray): Pixels in the XYZ color space.

    Returns:
        np.ndarray: Pixel matrix in the RGB color space.
    """
    return pixels @ xyz_to_rgb.T


def RGB_to_YUV(pixels:np.ndarray) -> np.ndarray:
    """Convert a pixel matrix in RGB color space to YUV color space.

    For details about the conversion from the RGB space to YUV space, see
    `YUV <https://en.wikipedia.org/wiki/YUV>`_.

    Args:
        pixels (np.ndarray): Pixels in the RGB color space.

    Returns:
        np.ndarray: Pixel matrix in the YUV color space.
    """
    pixels = normalize(pixels, 'RGB', True)
    return pixels @ rgb_to_yuv.T


def YUV_to_RGB(pixels:np.ndarray) -> np.ndarray:
    """Convert a pixel matrix in YUV color space to RGB color space.

    For details about the conversion from the RGB space to YUV space, see
    `YUV <https://en.wikipedia.org/wiki/YUV>`_.

    Args:
        pixels (np.ndarray): Pixels in the YUV color space.

    Returns:
        np.ndarray: Pixel matrix in the RGB color space.
    """
    pixels = pixels @ yuv_to_rgb.T
    return normalize(pixels, 'RGB', False)


def XYZ_to_Lab(pixels:np.ndarray,
               standard_illuminant:str = 'D65') -> np.ndarray:
    """Convert a pixel matrix in XYZ color space to Lab color space.

    For details about the conversion from the XYZ space to LAB space, see
    `CIELAB color space <https://en.wikipedia.org/wiki/CIELAB_color_space>`_.

    Args:
        pixels (np.ndarray): Pixels in the XYZ color space.
        standard_illuminant (str): Standard illuminant {D65, D50}

    Returns:
        np.ndarray: Pixel matrix in the Lab color space.
    """
    X_n, Y_n, Z_n = {'D50':(96.4212, 100.0, 82.5188),
                     'D65':(95.0489, 100.0, 108.8840)}[standard_illuminant]
    delta = 6 / 29

    def f(t):
        return t**(1/3) if t > delta**3 else (t/(3*delta**2)) + (4/29)

    def to_Lab(x):
        X, Y, Z = x
        L = 116*f(Y/Y_n) - 16
        a = 500*(f(X/X_n) - f(Y/Y_n))
        b = 200*(f(Y/Y_n) - f(Z/Z_n))
        return np.array([L,a,b])

    n,m,k = pixels.shape
    p = np.reshape(pixels, (n*m,3)).astype(float)
    p = np.apply_along_axis(to_Lab, 1, p)
    return np.reshape(p, (n,m,k))


def Lab_to_XYZ(pixels:np.ndarray, illuminant:str = 'D65') -> np.ndarray:
    """Convert a pixel matrix in Lab color space to XYZ color space.

    For details about the conversion from the XYZ space to LAB space, see
    `CIELAB color space <https://en.wikipedia.org/wiki/CIELAB_color_space>`_.

    Args:
        pixels (np.ndarray): Pixels in the Lab color space.
        illuminant (str): Standard illuminant {D65, D50}

    Returns:
        np.ndarray: Pixel matrix in the XYZ color space.
    """
    # See the following link for the implemented conversion
    # https://en.wikipedia.org/wiki/CIELAB_color_space
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

    n,m,k = pixels.shape
    p = np.reshape(pixels, (n*m,3)).astype(float)
    p = np.apply_along_axis(to_XYZ, 1, p)
    return np.reshape(p, (n,m,k))


def RGB_to_Lab(pixels:np.ndarray, illuminant:str = 'D65') -> np.ndarray:
    """Convert a pixel matrix in RGB color space to Lab color space.

    Args:
        pixels (np.ndarray): Pixels in the RGB color space.
        illuminant (str): Standard illuminant {D65, D50}

    Returns:
        np.ndarray: Pixel matrix in the Lab color space.
    """
    return XYZ_to_Lab(RGB_to_XYZ(pixels), illuminant)


def Lab_to_RGB(pixels:np.ndarray, illuminant:str = 'D65') -> np.ndarray:
    """Convert a pixel matrix in Lab color space to RGB color space.

    Args:
        pixels (np.ndarray): Pixels in the Lab color space.
        illuminant (str): Standard illuminant {D65, D50}

    Returns:
        np.ndarray: Pixel matrix in the RGB color space.
    """
    return XYZ_to_RGB(Lab_to_XYZ(pixels, illuminant))


def apply_to_channels(pixels:np.ndarray,
                      f_1:Callable,
                      f_2:Callable,
                      f_3:Callable) -> np.ndarray:
    """Return the pixel matrix with the functions applied to each channel.

    Args:
        pixels (np.ndarray): Pixel matrix
        f_1 (Callable): Function to apply to the first channel.
        f_2 (Callable): Function to apply to the second channel.
        f_3 (Callable): Function to apply to the third channel.

    Returns:
        np.ndarray: Pixel matrix with functions applied to each channel.
    """
    n,m,k = pixels.shape
    p = np.reshape(pixels, (n*m,3)).astype(float)
    p[:,0] = f_1(p[:,0])
    p[:,1] = f_2(p[:,1])
    p[:,2] = f_3(p[:,2])
    return np.reshape(p, (n,m,k))


def normalize(pixels:np.ndarray, color_space:str, norm:bool) -> np.ndarray:
    """Normalize / unnormalize the pixel matrix of the given color space.

    Args:
        pixels (np.ndarray): Pixel matrix in the given color space.
        color_space (str): Color space {RGB, Lab, YUV}
        norm (bool): Normalize if true. Otherwise, unnormalize.

    Returns:
        np.ndarray: Pixel matrix in the normalized / unnormalize color space.
    """
    r = {'RGB':[[0,255],[0,255],[0,255]],
         'Lab':[[0,255],[-128,127],[-128,127]],
         'YUV':[[0,1],[-0.436,0.436],[-0.615,0.615]]}[color_space]
    if norm:
        def f(i):
            return lambda x: (x - r[i][0]) / (r[i][1] - r[i][0])
    else:
        def f(i):
            return lambda x: (x * (r[i][1] - r[i][0])) + r[i][0]
    return apply_to_channels(pixels, f(0), f(1), f(2))
