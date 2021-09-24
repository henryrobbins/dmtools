"""
dmtools
=======

dmtools (Digital Media Tools) is a Python package providing low-level tools for
working with digital media programmatically. The netpbm module allows one to
read and create Netpbm images. Color space transformations can be done with the
colorspace module. Using ffmpeg, the animation module can export .mp4 videos
formed from a list of images and the sound module can be used to add sound to
these videos as well. Lastly, ASCII art can be produced with the ascii module.
"""

__author__ = 'Henry Robbins'

from . import animation
from . import ascii
from . import colorspace
from . import netpbm
from . import sound
from . import arrange
from . import transform
from .io import read_png, write_png
