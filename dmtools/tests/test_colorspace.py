import pytest
import numpy as np
from dmtools.colorspace import \
    gray_to_RGB, RGB_to_gray, RGB_to_XYZ, XYZ_to_RGB, RGB_to_YUV, YUV_to_RGB, \
    RGB_to_Lab, Lab_to_RGB, add_alpha

# -----------
# TEST IMAGES
# -----------

# single white pixel (single channel)
ONE_CHANNEL_WHITE_PIXEL = np.array([[1.0]])

# single white pixel (three channels)
THREE_CHANNEL_WHITE_PIXEL = np.array([[[1.0, 1.0, 1.0]]])

# single color pixel
COLOR_PIXEL = np.array([[[0.45, 0.33, 0.98]]])

# opaque pixel
OPAQUE_PIXEL = np.array([[[0.45, 0.33, 0.98, 0.50]]])


@pytest.mark.parametrize("f,source,new",[
    (gray_to_RGB, ONE_CHANNEL_WHITE_PIXEL, THREE_CHANNEL_WHITE_PIXEL),
    (RGB_to_gray, THREE_CHANNEL_WHITE_PIXEL, ONE_CHANNEL_WHITE_PIXEL)])
def test_colorspace_transformation(f, source, new):
    assert np.allclose(new, f(source), atol=1e-6)


@pytest.mark.parametrize("f,f_inv,image",[
    (gray_to_RGB, RGB_to_gray, ONE_CHANNEL_WHITE_PIXEL),
    (RGB_to_XYZ, XYZ_to_RGB, COLOR_PIXEL),
    (RGB_to_XYZ, XYZ_to_RGB, THREE_CHANNEL_WHITE_PIXEL),
    (RGB_to_XYZ, XYZ_to_RGB, OPAQUE_PIXEL),
    (RGB_to_YUV, YUV_to_RGB, COLOR_PIXEL),
    (RGB_to_YUV, YUV_to_RGB, THREE_CHANNEL_WHITE_PIXEL),
    (RGB_to_YUV, YUV_to_RGB, OPAQUE_PIXEL),
    (RGB_to_Lab, Lab_to_RGB, COLOR_PIXEL),
    (RGB_to_Lab, Lab_to_RGB, THREE_CHANNEL_WHITE_PIXEL),
    (RGB_to_Lab, Lab_to_RGB, OPAQUE_PIXEL)])
def test_colorspace_inverse(f, f_inv, image):
    print(image)
    print(f(image))
    print(f_inv(f(image)))
    assert np.allclose(image, f_inv(f(image)), atol=1e-6)


def test_add_alpha():
    assert np.allclose(COLOR_PIXEL, add_alpha(COLOR_PIXEL)[:,:,:3], atol=1e-6)
