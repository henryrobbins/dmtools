# rescale_ex.py
import dmtools
from dmtools import transform
import numpy as np

image = dmtools.read_png('checks_10.png')
scaled_image = transform.rescale(image, k=10, filter='point')
scaled_image = transform.clip(scaled_image)
dmtools.write_png(scaled_image, 'checks_10_point.png')

scaled_image = transform.rescale(image, k=10, filter='triangle')
scaled_image = transform.clip(scaled_image)
dmtools.write_png(scaled_image, 'checks_10_triangle.png')

def f(x):
    return np.sin(x)

# use a custom weighting function and support
scaled_image = transform.rescale(image, k=10, weighting_function=f, support=5)
scaled_image = transform.normalize(scaled_image)
dmtools.write_png(scaled_image, 'checks_10_custom.png')
