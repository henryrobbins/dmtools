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

    assert np.allclose(src, image, atol=2)


# TODO: Fix binary netpbm parser
@pytest.mark.parametrize("name",[
    ('color_matrix_ascii.pbm'),
    ('color_matrix_ascii.pgm'),
    ('color_matrix_ascii.ppm'),
    ('color_matrix_raw.pbm'),
    ('color_matrix_raw.pgm'),
    ('color_matrix_raw.ppm')])
def test_netpbm_io(name):
    # read image
    ext = name.split('.')[-1]
    src = read(os.path.join(RESOURCES_PATH, name))

    file_name = 'test.%s' % ext
    write_netpbm(src, 255, file_name)
    image = read(file_name)
    os.remove(file_name)

    assert np.allclose(src, image, atol=2)
