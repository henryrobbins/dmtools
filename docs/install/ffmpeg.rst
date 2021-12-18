Installing FFmpeg (Optional)
============================

#. This section is not optional of you wish to create videos with dmtools
#. Currently, these installation instructions focus on macOS users. For
   installation instructions on other operating systems, see `Download FFmpeg`_.

In order to install FFmpeg, we will first need to install a
`package manager`_. A package manager functions similarly to an app store--it
provides a way of installing and managing computer programs "in a consistent
manner." `Homebrew`_ is a package manager for macOS. It is the one we will use
to install FFmpeg. To install it, paste the following line in macOS Terminal.

.. code-block:: bash

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

When running the above line, you will likely be prompted to install Command
Line Tools (CLT) for Xcode. This can be installed with

.. code-block:: bash

    xcode-select --install

To verify Homebrew was installed properly, run ``brew`` in Terminal and
you should receive a help page on various Homebrew commands. With Homebrew now
installed, you can easily install FFmpeg with

.. code-block:: bash

    brew install ffmpeg

This installation may take some time. Once complete, verify it was installed
properly by running ``ffmpeg`` in Terminal. It should return some FFmpeg
version information.

Congratulations! You have now installed a package manager and FFmpeg. You will
now be able to create videos using dmtools.

.. _Download FFmpeg: https://www.ffmpeg.org/download.html
.. _package manager: https://wikipedia.org/wiki/Package_manager
.. _Homebrew: https://brew.sh/