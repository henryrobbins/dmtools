# curve.py
import dmtools
from dmtools import adjustments
import numpy as np

image = dmtools.read('pallette.png')

# apply identity to all channels
tmp = adjustments.apply_curve(image, lambda x: x)
dmtools.write_png(tmp, 'pallette_identity.png')

# apply clip from 0.25 to 0.75 to all channels
tmp = adjustments.apply_curve(image, lambda x: np.clip(2*(x-0.25), 0, 1))
dmtools.write_png(tmp, 'pallette_clip_25_75.png')

# apply clip from 0.4 to 0.6 to all channels
tmp = adjustments.apply_curve(image, lambda x: np.clip(5*(x-0.4), 0, 1))
dmtools.write_png(tmp, 'pallette_clip_40_60.png')

# apply clip from 0.4 to 0.6 to red channels
tmp = adjustments.apply_curve(image, lambda x: np.clip(5*(x-0.4), 0, 1), 0)
dmtools.write_png(tmp, 'pallette_clip_40_60_red.png')

# apply clip from 0.4 to 0.6 to blue channels
tmp = adjustments.apply_curve(image, lambda x: np.clip(5*(x-0.4), 0, 1), 2)
dmtools.write_png(tmp, 'pallette_clip_40_60_blue.png')

# apply parabola to all channels
tmp = adjustments.apply_curve(image, lambda x: 4*np.power(x - 0.5, 2))
dmtools.write_png(tmp, 'pallette_parabola.png')
