.. _dmtools_tutorial:

Introduction to dmtools
=======================

This tutorial will walk through a short introduction to dmtools. The tutorial
is divided into sections which each focus on a certain module of dmtools.
Note that this documentation is under development.

io (input / output)
-------------------

The first step in manuipulating images programtically with dmtools is loading
in an image. This is done using :py:func:`dmtools.io.read_png`. Similarly,
after manuipulating the image, you can export it to a PNG file with
:py:func:`dmtools.io.write_png`. Here is a short example script with no
manipulations. Note that this example script assumes that the script
``io_ex.py`` and ``checks_10.png`` are in the same directory.

.. code-block:: python

    # io_ex.py
    import dmtools

    image = dmtools.read_png('checks_10.png')
    dmtools.write_png(image, 'checks_10_clone.png')

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

transform
---------

The transform module contains many functions for manuipulating images. The full
API reference can be found here: :py:mod:`dmtools.transform`. In this section,
we will highlight some of the functionality.

.. code-block:: python

    # simple_blur.py
    import dmtools
    from dmtools import transform

    image = dmtools.read_png('red_blue_square.png')
    blurred_image = transform.blur(image, sigma=5)
    dmtools.write_png(blurred_image, 'red_blue_square_blur_5.png')

    blurred_image = transform.blur(image, sigma=10)
    dmtools.write_png(blurred_image, 'red_blue_square_blur_10.png')

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


.. code-block:: python

    # rescale_ex.py
    import dmtools
    from dmtools import transform
    import numpy as np

    image = dmtools.read_png('checks_10.png')
    scaled_image = transform.rescale(image, k=10, filter='point')
    scaled_image = transform.clip(scaled_image).astype(np.uint8)
    dmtools.write_png(scaled_image, 'checks_10_point.png')

    scaled_image = transform.rescale(image, k=10, filter='triangle')
    scaled_image = transform.clip(scaled_image).astype(np.uint8)
    dmtools.write_png(scaled_image, 'checks_10_triangle.png')

    def f(x):
        return np.sin(x)

    # use a custom weighting function and support
    scaled_image = transform.rescale(image, k=10, weighting_function=f, support=5)
    scaled_image = transform.normalize(scaled_image).astype(np.uint8)
    dmtools.write_png(scaled_image, 'checks_10_custom.png')


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
