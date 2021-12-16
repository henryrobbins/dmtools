import os
import sys
import shutil
import pytest
import numpy as np
from imageio import imread
from dmtools.io import (Metadata, read, write_netpbm, write_png, write_ascii,
                        recreate_script_from_png, _get_next_version)

RESOURCES_PATH = os.path.join(os.path.dirname(__file__), 'resources/io_tests')


def test_get_next_version():
    image = np.array([[[1,1,1]]])  # white pixel image

    # test PNG versioning
    for i in range(1,10):
        expected = f"white_pixel_{i:04}.png"
        assert expected == _get_next_version("white_pixel.png")
        write_png(image, "white_pixel.png", versioning=True)

    for i in range(1,10):
        os.remove(f"white_pixel_{i:04}.png")

    # test Netpbm versioning
    for i in range(1,10):
        expected = f"white_pixel_{i:04}.ppm"
        assert expected == _get_next_version("white_pixel.ppm")
        write_netpbm(image, 255, "white_pixel.ppm", versioning=True)

    for i in range(1,10):
        os.remove(f"white_pixel_{i:04}.ppm")

    # test directory prefix
    dir_name = "dir_for_version_testing"
    os.makedirs(dir_name, exist_ok=True)
    for i in range(1,10):
        expected = f"{dir_name}/white_pixel_{i:04}.png"
        assert expected == _get_next_version(f"{dir_name}/white_pixel.png")
        write_png(image, f"{dir_name}/white_pixel.png", versioning=True)
    shutil.rmtree(dir_name)


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


@pytest.mark.parametrize("name,k,new_ext",[
    ('color_matrix_ascii.pbm', 1, 'pbm'),
    ('color_matrix_ascii.pbm', 255, 'pgm'),
    ('color_matrix_ascii.pgm', 255, 'pgm'),
    ('color_matrix_ascii.ppm', 255, 'ppm'),
    ('color_matrix_raw.pbm', 1, 'pbm'),
    ('color_matrix_raw.pbm', 255, 'pgm'),
    ('color_matrix_raw.pgm', 255, 'pgm'),
    ('color_matrix_raw.ppm', 255, 'ppm')])
def test_netpbm_io(name, k, new_ext):
    # read image
    src = read(os.path.join(RESOURCES_PATH, name))

    file_name = 'test.%s' % new_ext
    write_netpbm(src, k, file_name)
    image = read(file_name)
    os.remove(file_name)

    assert np.array_equal(src, image)


@pytest.mark.parametrize("src,txt_expected_path,png_expected_path",[
    ('12_gradient.pgm', '12_gradient.txt', '12_gradient.png')])
def test_ascii_io(src, txt_expected_path, png_expected_path):
    image = read(os.path.join(RESOURCES_PATH, src))

    # test writing to ASCII txt
    write_ascii(image, 'test.txt', txt=True)
    txt_actual = ""
    with open('test.txt', mode='r') as f:
        txt_actual = f.read()
    txt_expected = ""
    with open(os.path.join(RESOURCES_PATH, txt_expected_path), mode='r') as f:
        txt_expected = f.read()
    os.remove('test.txt')
    assert txt_actual == txt_expected

    # test writing to ASCII PNG
    write_ascii(image, 'test.png')
    png_actual = read('test.png')
    png_expected = read(os.path.join(RESOURCES_PATH, png_expected_path))
    os.remove('test.png')
    assert np.array_equal(png_actual, png_expected)


def test_metadata_io():
    metadata = Metadata()
    src = read(os.path.join(RESOURCES_PATH, "color_matrix.png"))

    write_png(src, "color_matrix_metadata.png", metadata=metadata)
    write_netpbm(src, 255, "color_matrix_metadata.ppm", metadata=metadata)
    png_metadata = imread("color_matrix_metadata.png").meta
    os.remove("color_matrix_metadata.png")
    os.remove("color_matrix_metadata.ppm")

    assert png_metadata['Creation Time'] == metadata.creation_time
    assert png_metadata['Software'] == metadata.software
    assert png_metadata['Source'] == metadata.source


def test_recreate_script_from_png():

    source = open(sys.argv[0]).read()
    image = read(os.path.join(RESOURCES_PATH, "color_matrix.png"))
    write_png(image, "color_matrix_metadata.png")

    recreate_script_from_png("color_matrix_metadata.png", "test_recreate.py")
    source_from_file = open("test_recreate.py").read()
    os.remove("color_matrix_metadata.png")
    os.remove("test_recreate.py")

    assert source == source_from_file
