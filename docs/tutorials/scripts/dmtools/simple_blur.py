# simple_blur.py
import dmtools
from dmtools import transform

image = dmtools.read_png('red_blue_square.png')
blurred_image = transform.blur(image, sigma=5)
dmtools.write_png(blurred_image, 'red_blue_square_blur_5.png')

blurred_image = transform.blur(image, sigma=10)
dmtools.write_png(blurred_image, 'red_blue_square_blur_10.png')
