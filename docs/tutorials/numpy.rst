.. _numpy_tutorial:

Working with Images in NumPy
============================

This tutorial will walk through a short introduction to NumPy with emphasis on
the tools that can be used for working with images. For more details, see
NumPy's excellent `documentation`_.

At their core, images are just two dimensional arrays or matrices of pixels.
These pixels might have one value representing their gray value where 0 is
black and some upper bound (usually 255) is white or they might have three
values representing their red, green, and blue values respectively. Hence, in
working with images, it is natural to want a tool that allows us to create and
manipulate large arrays of numbers. NumPy is the premier package in Python for
doing just that.

This tutorial is structured similarly to the Python tutorial in which each of
the follow sections corresponds to a script which introduces some concept. As
an important note, using NumPy in a script requires ``import numpy as np`` at
the beginning.

NumPy Array
-----------

The NumPy array is very similar to the list. To create a NumPy array, we can
pass a list to ``np.array()``. We can access values in the array the same way
we did in a list. However, the NumPy array does not have the ``.append()``
method. Additionally, the ``+`` operator has a different meaning when applied
to two NumPy arrays: if the arrays are of the same size, it adds arrays
together element-wise. Two other helpful methods for initializing arrays are
``np.zeros()`` and ``np.ones()`` which initializes arrays of all zeros or ones
in the shape given.

.. code-block:: python

    # numpy_array.py
    import numpy as np

    x = [1, 2, 3]
    y = np.array([1, 2, 3])

    print(x)     # [1, 2, 3]
    print(y)     # [1 2 3]
    print(x[0])  # 1
    print(y[0])  # 1

    print(x + x) # [1, 2, 3, 1, 2, 3]
    print(y + y) # [2 4 6]

    w = np.zeros(3)
    z = np.ones((2, 2))
    print(w)  # [0. 0. 0.]
    print(z)
    # [[1. 1.]
    #  [1. 1.]]

Array Attributes
----------------

The three most common attributes of an array are the dimension ``ndim``, size
``size``, and shape ``shape``. The script below gives all three attributes of
two example arrays.

.. code-block:: python

    # array_attributes.py
    import numpy as np

    A = np.array([[1, 2, 3],[4, 5, 6]])
    print(A)
    # [[1 2 3]
    #  [4 5 6]]

    print(A.ndim)   # 2
    print(A.size)   # 6
    print(A.shape)  # (2, 3)

    B = np.array([[[1,2],[3,4]],[[5,6],[7,8]]])
    print(B)
    # [[[1 2]
    #   [3 4]]
    #
    #  [[5 6]
    #   [7 8]]]

    print(B.ndim)   # 3
    print(B.size)   # 8
    print(B.shape)  # (2, 2, 2)

Indexing and Slicing
--------------------

A common operation you will want to do is access part of an array. The
notation ``x[i:j]`` gives the ``i`` th through ``j`` th (not including ``j``)
values in the array ``x``. We can use ``x[i:]`` or ``x[:i]`` to get all the
values after or before the ``i`` th value respectively. It should be noted that
this notation also works with the Python list.

.. code-block:: python

    # indexing.py
    import numpy as np

    A = np.array([0, 1, 2, 3, 4])

    print(A[2:4])  # [2 3]
    print(A[2:])   # [2 3 4]
    print(A[:2])   # [0 1]
    print(A[-2:])  # [3 4]

    B = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(B)
    # [[1 2 3]
    #  [4 5 6]
    #  [7 8 9]]

    print(B[1:])
    # [[4 5 6]
    #  [7 8 9]]
    print(B[:, 1:])
    # [[2 3]
    #  [5 6]
    #  [8 9]]
    print(B[0:2, 0:2])
    # [[1 2]
    #  [4 5]]

    C = np.zeros((3,3))
    C[0:2, 0:2] = np.ones((2,2))
    print(C)
    # [[1. 1. 0.]
    #  [1. 1. 0.]
    #  [0. 0. 0.]]


Conditional Array
-----------------


Array Operations
----------------


Miscellaneous Operations
------------------------

``.max()``, ``.min()`` ,  ``.vstack()``, ``.hstack``, ``.T``


.. _documentation: https://numpy.org/doc/stable/user/absolute_beginners.html#