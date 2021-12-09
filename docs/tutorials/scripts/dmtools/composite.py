# composite.py
import dmtools
from dmtools import transform

blue_square = dmtools.read('blue_square.png')
orange_square = dmtools.read('orange_square.png')

blue_over_orange = transform.composite(blue_square, orange_square)
dmtools.write_png(blue_over_orange, 'blue_over_orange.png')

orange_over_blue = transform.composite(orange_square, blue_square)
dmtools.write_png(orange_over_blue, 'orange_over_blue.png')
