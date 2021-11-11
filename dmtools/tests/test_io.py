import os
import pytest
import numpy as np
from dmtools.io import read, write_netpbm, write_png

RESOURCES_PATH = os.path.join(os.path.dirname(__file__), 'resources/io_tests')


@pytest.mark.parametrize("name",[
    ('color_matrix.png')])
def test_png_io(name):
    # read image
    ext = name.split('.')[-1]
    src = read(os.path.join(RESOURCES_PATH, name))

    file_name = 'text.%s' % ext
    write_png(src, file_name)
    image = read(file_name)
    os.remove(file_name)

    assert np.array_equal(src, image)


@pytest.mark.parametrize("name,k",[
    ('color_matrix_ascii.pbm', 1),
    ('color_matrix_ascii.pbm', 255),
    ('color_matrix_ascii.pgm', 255),
    ('color_matrix_ascii.ppm', 255),
    ('color_matrix_raw.pbm', 1),
    ('color_matrix_raw.pbm', 255),
    ('color_matrix_raw.pgm', 255),
    ('color_matrix_raw.ppm', 255)])
def test_netpbm_io(name, k):
    # read image
    ext = name.split('.')[-1]
    src = read(os.path.join(RESOURCES_PATH, name))

    file_name = 'test.%s' % ext
    write_netpbm(src, k, file_name, comment=["comment test"])
    image = read(file_name)
    os.remove(file_name)

    assert np.array_equal(src, image)
