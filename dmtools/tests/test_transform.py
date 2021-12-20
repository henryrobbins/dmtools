import os
import pytest
import numpy as np
from dmtools.transform import (rescale, blur, composite, clip, normalize,
                               wraparound, _over_alpha_composite,
                               _over_color_composite, crop, substitute)
from dmtools.colorspace import gray_to_RGB
from dmtools.io import read

RESOURCES_PATH = os.path.join(os.path.dirname(__file__), 'resources')

# These tests are derived from ImageMagick example images which can be found in
# https://legacy.imagemagick.org/Usage/filter/
#
# Links test imagery used for each filter
#
# Point filter: https://legacy.imagemagick.org/Usage/filter/#point
# Box filter: https://legacy.imagemagick.org/Usage/filter/#box
# Triangle filter: https://legacy.imagemagick.org/Usage/filter/#triangle
# Gaussian filter: https://legacy.imagemagick.org/Usage/filter/#gaussian


@pytest.mark.parametrize("image,filter,k,new_name",[
    ('checks_10', 'point', 0.9, 'point_0.9'),
    ('checks_10', 'point', 0.8, 'point_0.8'),
    ('checks_10', 'point', 0.7, 'point_0.7'),
    ('checks_10', 'point', 0.6, 'point_0.6'),
    ('checks_10', 'point', 0.5, 'point_0.5'),
    ('checks_10', 'box', 0.9, 'box_0.9'),
    # ('checks_10', 'box', 0.8, 'box_0.8'), strangely differs from ImageMagick
    ('checks_10', 'box', 0.7, 'box_0.7'),
    ('checks_10', 'box', 0.6, 'box_0.6'),
    ('checks_10', 'box', 0.5, 'box_0.5'),
    ('checks_5', 'box', 1.2, 'box_1.2'),
    ('checks_5', 'point', 1.2, 'box_1.2'),
    ('checks_5', 'box', 1.4, 'box_1.4'),
    ('checks_5', 'point', 1.4, 'box_1.4'),
    ('checks_5', 'box', 1.6, 'box_1.6'),
    ('checks_5', 'point', 1.6, 'box_1.6'),
    ('checks_5', 'box', 1.8, 'box_1.8'),
    ('checks_5', 'point', 1.8, 'box_1.8'),
    ('checks_5', 'box', 2.0, 'box_2.0'),
    ('checks_5', 'point', 2.0, 'box_2.0'),
    ('checks_10', 'triangle', 0.9, 'triangle_0.9'),
    ('checks_10', 'triangle', 0.8, 'triangle_0.8'),
    ('checks_10', 'triangle', 0.7, 'triangle_0.7'),
    ('checks_10', 'triangle', 0.6, 'triangle_0.6'),
    ('checks_10', 'triangle', 0.5, 'triangle_0.5'),
    ('checks_5', 'triangle', 1.2, 'triangle_1.2'),
    ('checks_5', 'triangle', 1.4, 'triangle_1.4'),
    ('checks_5', 'triangle', 1.6, 'triangle_1.6'),
    ('checks_5', 'triangle', 1.8, 'triangle_1.8'),
    ('checks_5', 'triangle', 2.0, 'triangle_2.0'),
    ('checks_10', 'catrom', 0.9, 'catrom_0.9'),
    ('checks_10', 'catrom', 0.8, 'catrom_0.8'),
    ('checks_10', 'catrom', 0.7, 'catrom_0.7'),
    ('checks_10', 'catrom', 0.6, 'catrom_0.6'),
    ('checks_10', 'catrom', 0.5, 'catrom_0.5'),
    ('checks_5', 'catrom', 1.2, 'catrom_1.2'),
    ('checks_5', 'catrom', 1.4, 'catrom_1.4'),
    ('checks_5', 'catrom', 1.6, 'catrom_1.6'),
    ('checks_5', 'catrom', 1.8, 'catrom_1.8'),
    ('checks_5', 'catrom', 2.0, 'catrom_2.0')])
def test_rescale(image, filter, k, new_name):
    # single channel
    src = read(os.path.join(RESOURCES_PATH, image, 'src.png'))
    new = read(os.path.join(RESOURCES_PATH, image, new_name + '.png'))
    assert np.allclose(new, clip(rescale(src, k=k, filter=filter)), atol=0.01)

    # three channel
    src = gray_to_RGB(src)
    new = gray_to_RGB(new)
    assert np.allclose(new, clip(rescale(src, k=k, filter=filter)), atol=0.01)


@pytest.mark.parametrize("image,k,blur,new_name",[
    ('pixel_5', 300, 0.5, 'blur_0.5'),
    ('pixel_5', 300, 1.0, 'blur_1.0'),
    ('pixel_5', 300, 1.5, 'blur_1.5')])
def test_gaussian_blur(image, k, blur, new_name):
    src = read(os.path.join(RESOURCES_PATH, image, 'src.png'))
    new = read(os.path.join(RESOURCES_PATH, image, new_name + '.png'))
    assert np.allclose(new, rescale(src, k=k, filter='gaussian', blur=blur),
                       atol=0.01)


@pytest.mark.parametrize("image,sigma,new_name",[
    ('red_blue_square', 2, 'blur_2'),
    ('red_blue_square', 3, 'blur_3'),
    ('red_blue_square', 5, 'blur_5'),
    ('red_blue_square', 10, 'blur_10'),
    ('red_blue_square', 20, 'blur_20')])
def test_blur(image, sigma, new_name):
    src = read(os.path.join(RESOURCES_PATH, image, 'src.png'))
    new = read(os.path.join(RESOURCES_PATH, image, new_name + '.png'))
    new = new[:,:,:3]  # drop the alpha channel to compare
    assert np.allclose(new, blur(src, sigma=sigma), atol=0.01)


@pytest.mark.parametrize("operator,result",[
    ('over', 'over.png'),
    ('dest_over', 'dest_over.png'),
    ('add', 'add.png')])
def test_composite(operator, result):
    A = read(os.path.join(RESOURCES_PATH, 'composite_tests', 'blue.png'))
    B = read(os.path.join(RESOURCES_PATH, 'composite_tests', 'red.png'))
    result = read(os.path.join(RESOURCES_PATH, 'composite_tests', result))
    assert np.allclose(result, composite(A, B, operator), atol=0.01)


def test_composite_functions():
    A = read(os.path.join(RESOURCES_PATH, 'composite_tests', 'blue.png'))
    B = read(os.path.join(RESOURCES_PATH, 'composite_tests', 'red.png'))
    result = read(os.path.join(RESOURCES_PATH, 'composite_tests', 'over.png'))
    image = composite(A, B, alpha_composite_function=_over_alpha_composite,
                      color_composite_function=_over_color_composite)
    assert np.allclose(result, image, atol=0.01)


@pytest.mark.parametrize("path,sub_path,x,y,relative,loc,exp_path",[
    ('red_box', 'blue_box', 100, 200, False, 'upper-left', 'red_blue_box'),
    ('red_box', 'blue_box', 100, 100, False, 'lower-left', 'red_blue_box'),
    ('red_box', 'blue_box', 150, 150, False, 'center', 'red_blue_box'),
    ('red_box', 'blue_box', 0.5, 0.5, True, 'center', 'red_blue_box')])
def test_substitute(path, sub_path, x, y, relative, loc, exp_path):
    image = read(f"{RESOURCES_PATH}/substitute_tests/{path}.png")
    sub_image = read(f"{RESOURCES_PATH}/substitute_tests/{sub_path}.png")
    exp = read(f"{RESOURCES_PATH}/substitute_tests/{exp_path}.png")
    result = substitute(image, sub_image, x, y, relative=relative, loc=loc)
    assert np.allclose(exp, result, atol=0.01)


@pytest.mark.parametrize("path,x,y,w,h,relative,loc,exp_path",[
    ('black_square', 0, 125, 125, 125, False, 'upper-left', 'black_square'),
    ('red_square', 0, 0, 125, 125, False, 'lower-left', 'red_square'),
    ('black_square', 25, 50, 25, 25, False, 'upper-left', 'black_box'),
    ('red_square', 25, 50, 25, 25, False, 'upper-left', 'red_box'),
    ('black_square', 0.2, 0.2, 0.2, 0.2, True, 'lower-left', 'black_box'),
    ('red_square', 0.2, 0.8, 0.2, 0.2, True, 'upper-left', 'red_box'),
    ('black_square', 0.5, 0.5, 0.6, 0.6, True, 'center', 'black_corner'),
    ('red_square', 0.5, 0.5, 0.6, 0.6, True, 'center', 'red_corner')])
def test_crop(path, x, y, w, h, relative, loc, exp_path):
    image = read(os.path.join(RESOURCES_PATH, "crop_tests", f"{path}.png"))
    exp = read(os.path.join(RESOURCES_PATH, "crop_tests", f"{exp_path}.png"))
    result = crop(image, x, y, w, h, relative=relative, loc=loc)
    assert np.allclose(exp, result, atol=0.01)


@pytest.mark.parametrize("src,new",[
    (np.array([[1,1],[1,1]]), np.array([[1,1],[1,1]])),
    (np.array([[1.25,1.25],[1.25,1.25]]), np.array([[1,1],[1,1]])),
    (np.array([[-0.25,1.25],[1.25,-0.25]]), np.array([[0,1],[1,0]]))])
def test_clip(src, new):
    assert np.allclose(new, clip(src), atol=0)


@pytest.mark.parametrize("src,new",[
    (np.array([[1,1],[1,1]]), np.array([[1,1],[1,1]])),
    (np.array([[0,0.1],[0.25,0.5]]), np.array([[0,0.2],[0.5,1]])),
    (np.array([[0,0.5],[1,2]]), np.array([[0,0.25],[0.5,1]]))])
def test_normalize(src, new):
    assert np.allclose(new, normalize(src), atol=0)


@pytest.mark.parametrize("src,new",[
    (np.array([[1.25,1.25],[1.25,1.25]]), np.array([[0.25,0.25],[0.25,0.25]])),
    (np.array([[0,0.1],[0.25,0.5]]), np.array([[0,0.1],[0.25,0.5]])),
    (np.array([[0,-0.25],[1.25,1]]), np.array([[0,0.75],[0.25,1]]))])
def test_wraparound(src, new):
    assert np.allclose(new, wraparound(src), atol=0)
