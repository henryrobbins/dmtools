from dmtools import netpbm
from dmtools import colorspace

def transform(image, color_space, f1, f2, f3):
    M = image.M

    if color_space == 'RGB':
        M = colorspace.normalize(M, 'RGB')
        M = colorspace.apply_to_channels(M, f1, f2, f3)
        M = colorspace.denormalize(M, 'RGB')
    elif color_space == 'Lab':
        M = colorspace.RGB_to_Lab(M)
        M = colorspace.normalize(M, 'Lab')
        M = colorspace.apply_to_channels(M, f1, f2, f3)
        M = colorspace.denormalize(M, 'Lab')
        M = colorspace.Lab_to_RGB(M)
    elif color_space == 'YUV':
        M = colorspace.RGB_to_YUV(M)
        M = colorspace.normalize(M, 'YUV')
        M = colorspace.apply_to_channels(M, f1, f2, f3)
        M = colorspace.denormalize(M, 'YUV')
        M = colorspace.YUV_to_RGB(M)

    return netpbm.Netpbm(P=image.P, k=image.k, M=M)

identity = (lambda x: x, "x")
invert = (lambda x: 1 - x, "1-x")
zero = (lambda x: 0, "0")
half = (lambda x: 0.5, "0.5")
one = (lambda x: 1, "1")

def multiply(p):
    return (lambda x: x*p, "%0.1fx" % p)

transformations = ([
    (identity, zero, zero),
    (zero, identity, zero),
    (zero, zero, identity),
    (identity, half, half),
    (zero, identity, half),
    (zero, half, identity),
    (multiply(1.5), identity, identity),
    (identity, multiply(1.5), identity),
    (identity, identity, multiply(1.5))])

for t1, t2, t3 in transformations:
    f1, s1 = t1
    f2, s2 = t2
    f3, s3 = t3
    image = netpbm.read_netpbm("barn.ppm")
    for color_space in ['RGB', 'Lab', 'YUV']:
        image = transform(image,color_space, f1, f2, f3)
        path = "barn_%s_%s_%s_%s.ppm" % (color_space, s1, s2, s3)
        image.to_netpbm(path)
