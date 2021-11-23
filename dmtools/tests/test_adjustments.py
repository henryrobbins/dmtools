import pytest
import numpy as np
from dmtools.adjustments import apply_curve


# test curve
def clip(x):
    return np.clip(2*(x - 0.25), 0, 1)


# -----------
# TEST IMAGES
# -----------

# single channel gradient
ONE_CHANNEL_GRADIENT = np.array([[0.0, 0.25, 0.50, 0.75, 1.0]])
ONE_CHANNEL_GRADIENT_CLIPPED = np.array([[0.0, 0.0, 0.50, 1.0, 1.0]])
ONE_CHANNEL_GRADIENT_ONE_COLOR = np.array([[0.5, 0.5, 0.5, 0.5, 0.5]])

# three channel gradient
THREE_CHANNEL_GRADIENT = np.array([[[0.0, 0.0, 1.0],
                                    [0.75, 0.1, 0.2],
                                    [0.23, 0.6, 1.0]]])
THREE_CHANNEL_GRADIENT_CLIPPED = np.array([[[0.0, 0.0, 1.0],
                                            [1.0, 0.0, 0.0],
                                            [0.0, 0.7, 1.0]]])
THREE_CHANNEL_GRADIENT_CLIPPED_1 = np.array([[[0.0, 0.0, 1.0],
                                              [0.75, 0.0, 0.2],
                                              [0.23, 0.7, 1.0]]])

# three chroma channels + alpha channel
THREE_CHANNEL_WITH_ALPHA = np.array([[[0.0, 0.0, 1.0, 1.0],
                                      [0.75, 0.1, 0.2, 1.0],
                                      [0.23, 0.6, 1.0, 1.0]]])
THREE_CHANNEL_WITH_ALPHA_CLIPPED = np.array([[[0.0, 0.0, 1.0, 1.0],
                                              [1.0, 0.0, 0.0, 1.0],
                                              [0.0, 0.7, 1.0, 1.0]]])
THREE_CHANNEL_WITH_ALPHA_CLIPPED_1 = np.array([[[0.0, 0.0, 1.0, 1.0],
                                                [0.75, 0.0, 0.2, 1.0],
                                                [0.23, 0.7, 1.0, 1.0]]])


@pytest.mark.parametrize("image,f,c,result",[
    (ONE_CHANNEL_GRADIENT, clip, -1, ONE_CHANNEL_GRADIENT_CLIPPED),
    (THREE_CHANNEL_GRADIENT, clip, -1, THREE_CHANNEL_GRADIENT_CLIPPED),
    (THREE_CHANNEL_GRADIENT, clip, 1, THREE_CHANNEL_GRADIENT_CLIPPED_1),
    (THREE_CHANNEL_WITH_ALPHA, clip, -1, THREE_CHANNEL_WITH_ALPHA_CLIPPED),
    (THREE_CHANNEL_WITH_ALPHA, clip, 1, THREE_CHANNEL_WITH_ALPHA_CLIPPED_1)])
def test_image_grid(image, f, c, result):
    assert np.array_equal(result, apply_curve(image, f, c))
