import pytest
import numpy as np
from dmtools.arrange import image_grid, border

# -----------
# TEST IMAGES
# -----------

# single white pixel
WHITE_PIXEL = np.array([[1]])

# single white pixel with 2 pixel black border
WHITE_PIXEL_BLACK_BORDER = \
    np.array([[  0,   0,   0,   0,   0],
              [  0,   0,   0,   0,   0],
              [  0,   0,   1,   0,   0],
              [  0,   0,   0,   0,   0],
              [  0,   0,   0,   0,   0]])

# four white pixels in 2x2 grid with 1 pixel black border
FOUR_WHITE_PIXEL_GRID = \
    np.array([[  0,   0,   0,   0,   0],
              [  0,   1,   0,   1,   0],
              [  0,   0,   0,   0,   0],
              [  0,   1,   0,   1,   0],
              [  0,   0,   0,   0,   0]])

# single color pixel
COLOR_PIXEL = np.array([[[0.1, 0.5, 0.8]]])

# single color pixel with 1 pixel black border
COLOR_PIXEL_BLACK_BORDER = \
    np.array([[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
              [[0.0, 0.0, 0.0], [0.1, 0.5, 0.8], [0.0, 0.0, 0.0]],
              [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]])

# opaque pixel
OPAQUE_PIXEL = np.array([[[0.1, 0.5, 0.8, 0.5]]])

# single opaque pixel with 1 pixel black border
OPAQUE_PIXEL_BLACK_BORDER = \
    np.array([[[1, 1, 1, 1], [1.0, 1.0, 1.0, 1.0], [1, 1, 1, 1]],
              [[1, 1, 1, 1], [0.1, 0.5, 0.8, 0.5], [1, 1, 1, 1]],
              [[1, 1, 1, 1], [1.0, 1.0, 1.0, 1.0], [1, 1, 1, 1]]])


@pytest.mark.parametrize("images,w,h,b,color,result",[
    ([WHITE_PIXEL], 1, 1, 2, np.array([0]), WHITE_PIXEL_BLACK_BORDER),
    ([WHITE_PIXEL]*4, 2, 2, 1, np.array([0]), FOUR_WHITE_PIXEL_GRID),
    ([COLOR_PIXEL], 1, 1, 1, np.array([0,0,0]), COLOR_PIXEL_BLACK_BORDER),
    ([OPAQUE_PIXEL], 1, 1, 1, None, OPAQUE_PIXEL_BLACK_BORDER)])
def test_image_grid(images, w, h, b, color, result):
    assert np.array_equal(result, image_grid(images, w, h, b, color))


@pytest.mark.parametrize("image,b,color,result",[
    (WHITE_PIXEL, 2, np.array([0]), WHITE_PIXEL_BLACK_BORDER),
    (COLOR_PIXEL, 1, np.array([0,0,0]), COLOR_PIXEL_BLACK_BORDER),
    (OPAQUE_PIXEL, 1, None, OPAQUE_PIXEL_BLACK_BORDER)])
def test_border(image, b, color, result):
    assert np.array_equal(result, border(image, b, color))
