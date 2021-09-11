Installing dmtools
==================

In this section, we will install the dmtools Python package. But first,
what is a Python package? A Python package is essentially pre-bundled Python
code that provides some functionality. For example, `NumPy`_ is a Python
package (one you will get more familiar with in :ref:`numpy_tutorial`) that
allows for easy manipulation of arrays. Python packages are your friend! They
allow you to easily use other people's code so you never have to re-invent the
wheel and can spend more time being creative.

In installing anaconda, you should now have a program called `pip`_ which stands
for Pip Installs Packages. It is a Python package manager and it is the tool
we will use to install dmtools. Just run the following line.

.. code-block:: bash

    pip install dmtools

To the verify the installation worked correctly, open a Python prompt by typing
``python`` and then type ``from dmtools import netpbm.`` If you don't get any
error messages, the instllation was a success!

.. code-block:: bash

    python
    Python 3.8.8 (default, Apr 13 2021, 12:59:45)
    [Clang 10.0.0 ] :: Anaconda, Inc. on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from dmtools import netpbm
    >>> quit()

.. _NumPy: https://numpy.org/
.. _pip: https://pip.pypa.io/en/stable/installation/