# io_ex.py
import dmtools

image = dmtools.read_png('checks_10.png')
dmtools.write_png(image, 'checks_10_clone.png')
