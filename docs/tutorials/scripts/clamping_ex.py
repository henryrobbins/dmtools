# clamping_ex.py
import dmtools
from dmtools import transform
import numpy as np

def f(x):
    return np.sin(x)

image = dmtools.read_png('checks_10.png')
scaled_image = transform.rescale(image, k=10, weighting_function=f, support=7)

clip_image = transform.clip(scaled_image).astype(np.uint8)
dmtools.write_png(clip_image, 'checks_10_clip.png')

normalize_image = transform.normalize(scaled_image).astype(np.uint8)
dmtools.write_png(normalize_image, 'checks_10_normalize.png')

wraparound_image = transform.wraparound(scaled_image).astype(np.uint8)
dmtools.write_png(wraparound_image, 'checks_10_wraparound.png')
