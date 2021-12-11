.. _dmtools_tutorial:

Introduction to dmtools
=======================

This tutorial will walk through a short introduction to dmtools. The tutorial
is divided into sections which each focus on a certain module of dmtools.
Note that this documentation is under development.

io (input / output)
-------------------

The first step in manipulating images programmatically with dmtools is loading
in an image. This is done using :py:func:`dmtools.io.read_png`. Similarly,
after manipulating the image, you can export it to a PNG file with
:py:func:`dmtools.io.write_png`. Here is a short example script with no
manipulations. Note that this example script assumes that the script
``io_ex.py`` and ``checks_10.png`` are in the same directory.

.. literalinclude:: scripts/dmtools/io_ex.py
   :language: python

.. list-table::
    :align: center

    * - .. figure:: images/checks_10.png
            :alt: checks_10.png
            :align: center

            checks_10.png

      - .. figure:: images/checks_10_clone.png
            :alt: checks_10_clone.png
            :align: center

            checks_10_clone.png

Both :py:func:`dmtools.io.write_png` and :py:func:`dmtools.io.write_netpbm`
write additional metadata to the file automatically. This includes the
creation time of the image, the software ("dmtools") used to create the image,
and the source code of the script that created the image. We can also use the
:py:class:`dmtools.io.Metadata` class to provide additional information. In
the example below, we export the ``checks_10.png`` file to Netpbm so we can view
the metadata in plaintext. The example shows the default metadata and an
example of providing custom metadata.

.. literalinclude:: scripts/dmtools/metadata.py
   :language: python

checks_10_default_metadata.pbm

.. literalinclude:: scripts/dmtools/checks_10_default_metadata.pbm

checks_10_custom_metadata.pbm

.. literalinclude:: scripts/dmtools/checks_10_custom_metadata.pbm

In addition to writing the source code to an image's metadata by default, the
function :py:func:`dmtools.io.recreate_script_from_png` allows one to recover
the script that created a PNG image.

transform
---------

The transform module contains many functions for manipulating images. The full
API reference can be found here: :py:mod:`dmtools.transform`. In this section,
we will highlight some of the functionality.

Currently, the transform module is mainly focused on image manipulations
related to rescaling an image. Frequently, the first step in image rescaling is
blurring the image. This provides a good removal of "noise" from the image.
The :py:func:`dmtools.transform.blur` functions does just that. It takes a
parameter called ``sigma`` which indicates how much to blur the image.
Usually, ``sigma=0.5`` is a good default. The example script below reads
``red_blue_square.png`` and then blurs the image with two different values of
``sigma``. You can see the resulting images below where the larger ``sigma``
results in a blurrier image.

.. literalinclude:: scripts/dmtools/simple_blur.py
   :language: python

.. list-table::
    :align: center

    * - .. figure:: images/red_blue_square.png
            :height: 100
            :alt: red_blue_square.png
            :align: center

            red_blue_square.png

      - .. figure:: images/red_blue_square_blur_5.png
            :height: 100
            :alt: red_blue_square_blur_5.png
            :align: center

            red_blue_square_blur_5.png

      - .. figure:: images/red_blue_square_blur_10.png
            :height: 100
            :alt: red_blue_square_blur_10.png
            :align: center

            red_blue_square_blur_10.png

After blurring, we can actually rescale the image. This step is also called
"resampling." This is done with :py:func:`dmtools.transform.rescale`. This
takes a parameter ``k`` which specifies by what factor to scale the image.
Hence, ``k=2`` would double the width and height of the image.

When scaling down an image, we have more than one source pixel for each new
pixel and we must decide how to assign a color to that new pixel. Similarly,
when scaling up an image, we have many pixels in the new image for which there
are no corresponding source pixels. Again, we must decide how to assign these
pixels a color based on their proximity to the source pixels. A filter is a
combination of a weighting function and support which determine how we choose.

In the dmtools rescale implementation, there are multiple built-in filters.
A comprehensive list of them is given in the documentation:
:py:func:`dmtools.transform.rescale`. Depending on the use case, one or more of
the filters may be applicable. The exciting feature of this implementation is
the ability to provide one's own weighting function and support to define
custom filters. The weighting function (blue) and supports (red) of some common
filters are given below. The weighting function tells us how much to weight the
color of a source pixel as a function of its distance to the new pixel. The
support defines the "neighborhood" of pixels. In most cases, that is the
furthest a source pixel can be while still contributing some weight.

.. list-table::
    :align: center

    * - .. figure:: images/box_filter.png
            :alt: box_filter.png
            :align: center

            Box Filter

      - .. figure:: images/triangle_filter.png
            :alt: triangle_filter.png
            :align: center

            Triangle Filter

      - .. figure:: images/custom_filter.png
            :alt: custom_filter.png
            :align: center

            Custom Filter

In the example script below, we load the 10x10 checkerboard image and scale it
up using three different filters: "point" or "nearest neighbor", "triangle",
and a custom filter. You can ignore ``transform.clip`` and
``transform.normalize`` for now. The resulting images are also shown.

.. literalinclude:: scripts/dmtools/rescale_ex.py
   :language: python

.. list-table::
    :align: center

    * - .. figure:: images/checks_10_point.png
            :alt: checks_10_point.png
            :align: center

            checks_10_point.png

      - .. figure:: images/checks_10_triangle.png
            :alt: checks_10_triangle.png
            :align: center

            checks_10_triangle.png

      - .. figure:: images/checks_10_custom.png
            :alt: checks_10_custom.png
            :align: center

            checks_10_custom.png

You can see how "point" is the best filter for maintaining the pixels of the
original image. Here, the "triangle" filter causes the image to be blurred
since it is takes the average of surrounding white and black pixels causing the
gray space between them. Any reasonable filter will mostly decrease the weight
as the distance gets further. Furthermore, they will not have significant
negative weights. For that reason, the custom filter used here does all sorts
of strange things to the image.

After rescaling the image, we would like to write it to a PNG file. However,
the rescaling step results in pixels having non-integer values which can also
be outside of the [0, 255] range (especially when using strange filters). The
transform module provides three different functions to adjust values back into
the [0, 255] range: :py:func:`dmtools.transform.clip`,
:py:func:`dmtools.transform.normalize`, :py:func:`dmtools.transform.wraparound`.
It is recommended to use ``.astype(np.uint8)`` to round. The example script
below shows how the choice of which of these you use affects the resulting image.

.. literalinclude:: scripts/dmtools/clamping_ex.py
   :language: python

.. list-table::
    :align: center

    * - .. figure:: images/checks_10_clip.png
            :alt: checks_10_clip.png
            :align: center

            checks_10_clip.png

      - .. figure:: images/checks_10_normalize.png
            :alt: checks_10_normalize.png
            :align: center

            checks_10_normalize.png

      - .. figure:: images/checks_10_wraparound.png
            :alt: checks_10_wraparound.png
            :align: center

            checks_10_wraparound.png

In ``checks_10_wraparound.png``, we can see harsh contrast between gradients
where a gradient progressively gets darker until it switches white. This is
arising from dark values above 255 (black) wrapping around to 0 (white) and
vice versa. In ``checks_10_clip.png``, these are the darkest and whitest areas
in the image since values above or below just get clipped to 0 and 255
respectively. Lastly, ``checks_10_normalize.png`` normalizes the minimum and
largest value to 0 and 255 causing this image to loose contrast in the center
when compared to the clipping algorithm.

Another function provided by the transform module is
:py:func:`dmtools.transform.composite`. It allows for layering two images. In the
case of fully opaque images, the function is uninteresting as the top image
will completely obfuscate the below image. However, when images have lower
opacities, this function handles what is called `Alpha Compositing`_. In the
example script below, we input two images at half opacity and view the result of
overlaying in both possible orientations. Note how the composite function creates
the effect of the top image being placed over the bottom image.

.. literalinclude:: scripts/dmtools/composite.py
   :language: python

.. list-table::
    :align: center

    * - .. figure:: images/blue_square.png
            :alt: blue_square.png
            :align: center

            blue_square.png

      - .. figure:: images/orange_square.png
            :alt: orange_square.png
            :align: center

            orange_square.png

.. list-table::
    :align: center

    * - .. figure:: images/blue_over_orange.png
            :alt: blue_over_orange.png
            :align: center

            blue_over_orange.png

      - .. figure:: images/orange_over_blue.png
            :alt: orange_over_blue.png
            :align: center

            orange_over_blue.png


adjustments
-----------

The adjustments module currently contains an equivalent to a curves tool. The
full API reference can be found here: :py:mod:`dmtools.adjustments`. In this
section, we will give a more detailed explanation of how the curve tool can
be used.

A curves tool is a comprehensive tool for changing the colors of an image. It
can be used to achieve a variety of effects. It works by specifying a function
for remapping the tones of an image. This function can be applied to the image
as a whole or to an individual channel (examples of both are given below). As
dmtools works with images normalized to [0,1], the curve function should be
a function with a domain and range of [0,1].

Let us walk through the example script below. Aside from the identity function
(the straight line from (0,0) to (1,1) in which every tone maps to itself),
all of the functions it uses are given below.

.. list-table::
    :align: center

    * - .. figure:: images/clip_25_75.png
            :alt: clip_25_75.png
            :align: center

            Clip to [0.25, 0.75]

      - .. figure:: images/clip_40_60.png
            :alt: clip_40_60.png
            :align: center

            Clip to [0.40, 0.60]

      - .. figure:: images/parabola.png
            :alt: parabola.png
            :align: center

            Parabola

In this script, we apply a variety of different curves to the `pallette.png`
image. Some curves are applied to all channels of an image (when no channel
is given) and some are applied to individual channels. As we are working in the
RGB (Red, Green, Blue) colorspace, the red channel is channel 0 and the blue
channel is channel 2.

.. literalinclude:: scripts/dmtools/curve.py
   :language: python

.. list-table::
    :align: center

    * - .. figure:: images/pallette.png
            :alt: pallette.png
            :align: center

            pallette.png

      - .. figure:: images/pallette_identity.png
            :alt: pallette_identity.png
            :align: center

            pallette_identity.png

    * - .. figure:: images/pallette_clip_25_75.png
            :alt: pallette_clip_25_75.png
            :align: center

            pallette_clip_25_75.png

      - .. figure:: images/pallette_clip_40_60.png
            :alt: pallette_clip_40_60.png
            :align: center

            pallette_clip_40_60.png

    * - .. figure:: images/pallette_clip_40_60_red.png
            :alt: pallette_clip_40_60_red.png
            :align: center

            pallette_clip_40_60_red.png

      - .. figure:: images/pallette_clip_40_60_blue.png
            :alt: pallette_clip_40_60_blue.png
            :align: center

            pallette_clip_40_60_blue.png

.. figure:: images/pallette_parabola.png
      :alt: pallette_parabola.png
      :align: center

      pallette_parabola.png

All of the images generated by the script are shown above. You should make a
few important observations. The identity function does not alter the image.
The clip functions reduce contrast at either end of the tonal range but
increase it in the center of the range. The clip to [0.40, 0.60] has a more
pronounced effect that the clip to [0.25, 0.75]. Lastly, when the curve is
applied to a single channel, the colors of other channels are unaffected.

.. _Alpha Compositing: https://en.wikipedia.org/wiki/Alpha_compositing