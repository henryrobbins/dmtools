import pytest
import numpy as np
from dmtools.arrange import image_grid, border

# -----------
# TEST IMAGES
# -----------

# single white pixel
WHITE_PIXEL = np.array([[255]])

# single white pixel with 2 pixel black border
WHITE_PIXEL_BLACK_BORDER = \
    np.array([[  0,   0,   0,   0,   0],
              [  0,   0,   0,   0,   0],
              [  0,   0, 255,   0,   0],
              [  0,   0,   0,   0,   0],
              [  0,   0,   0,   0,   0]])

# four white pixels in 2x2 grid with 1 pixel black border
FOUR_WHITE_PIXEL_GRID = \
    np.array([[  0,   0,   0,   0,   0],
              [  0, 255,   0, 255,   0],
              [  0,   0,   0,   0,   0],
              [  0, 255,   0, 255,   0],
              [  0,   0,   0,   0,   0]])


@pytest.mark.parametrize("images,w,h,b,color,result",[
    ([WHITE_PIXEL], 1, 1, 2, 'black', WHITE_PIXEL_BLACK_BORDER),
    ([WHITE_PIXEL]*4, 2, 2, 1, 'black', FOUR_WHITE_PIXEL_GRID)])
def test_image_grid(images, w, h, b, color, result):
    assert np.array_equal(result, image_grid(images, w, h, b, color))


@pytest.mark.parametrize("image,b,color,result",[
    (WHITE_PIXEL, 2, 'black', WHITE_PIXEL_BLACK_BORDER)])
def test_border(image, b, color, result):
    assert np.array_equal(result, border(image, b, color))
