# <img alt="dmtools" src="docs/branding/dmtools_dark.png" height="90">

[![PyPI pyversions](https://img.shields.io/pypi/pyversions/dmtools.svg)](https://pypi.python.org/pypi/dmtools/)
[![CircleCI](https://circleci.com/gh/henryrobbins/dmtools.svg?style=shield&circle-token=23cdbbfe0a606bd908e1a2a92bdff6f66d3e1c54)](https://app.circleci.com/pipelines/github/henryrobbins/dmtools)
[![Documentation Status](https://readthedocs.org/projects/dmtools/badge/?version=latest)](https://dmtools.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/henryrobbins/dmtools/branch/master/graphs/badge.svg)](https://codecov.io/gh/henryrobbins/dmtools)

dmtools (Digital Media Tools) is a Python package providing low-level tools for
working with digital media programmatically. It supports the PNG and [Netpbm][1]
image file formats as well as the MPEG-4 and [WAV][2] video and audio file
formats respectively.

The `transform` module provides image transformation tools such as rescale
(based on the [ImageMagick][3] implementation) and composite (based on the
[Cairo][4] implementation). The `adjustments` module provides a curves tool and
the `colorspace` module provides colorspace conversion tools. The `arrange`
module provides image layout tools. Lastly, the `animation` and `sound` modules
provide tools for working with video and sound respectively. For more details,
see the [Documentation][8].

# Installations

The quickest way to get started is with a pip install.

```
pip install dmtools
```

The `animation` module requires [ffmpeg][5] which you can install with a package
manager like [Homebrew][6]. Note that this may take some time to install.

```
brew install ffmpeg
```

For in-depth installation instructions see [Installation][7].

# Usage

The usage example below illustrates how an image can be read, manipulated,
and exported using dmtools. It features a change of color space, inversion of
the red channel, and blur. For more usage examples, see the
[Introduction to dmtools][9] in [Tutorials][10]. Both the input image
`checks_5.png` and output image `result.png` can be found in the [dmtools][11]
GitHub repository.

```python
import dmtools
from dmtools import colorspace, transform, adjustments, arrange

image = dmtools.read("checks_5.png")
image = colorspace.gray_to_RGB(image)
image = adjustments.apply_curve(image, lambda x: 1 - x, 0)
image = transform.blur(image, 5)
image = arrange.image_grid([image]*2, 2, 1, 15, color=1)

dmtools.write_png(image, "result.png")

```

![checks_5.png](checks_5.png)

*checks_5.png*

![result.png](result.png)

*result.png*

## License

Licensed under the [MIT License](https://choosealicense.com/licenses/mit/)

[1]: <http://netpbm.sourceforge.net/> "Netpbm"
[2]: <https://en.wikipedia.org/wiki/WAV> "WAV"
[3]: <https://legacy.imagemagick.org/Usage/resize/> "ImageMagick"
[4]: <https://cairographics.org/operators/> "Cairo"
[5]: <https://ffmpeg.org/about.html> "ffmpeg"
[6]: <https://brew.sh/> "Homebrew"
[7]: <https://dmtools.henryrobbins.com/en/latest/install/index.html> "Installation"
[8]: <https://dmtools.henryrobbins.com/en/latest/modules.html> "Documentation"
[9]: <https://dmtools.henryrobbins.com/en/latest/tutorials/dmtools.html> "Introduction"
[10]: <https://dmtools.henryrobbins.com/en/latest/tutorials/index.html> "Tutorials"
[11]: <https://github.com/henryrobbins/dmtools> "dmtools"
