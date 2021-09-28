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

Another way to slice an array is with a condition. The syntax for this is
``x[condition]``. If we just look at the result of the condition, it returns
an array of boolean values where the value is ``True`` if the corresponding
element satisfied the condition and ``False`` otherwise. Passing this boolean
array to the slicing notation indicates which values to keep.

.. code-block:: python

    # condition_array.py
    import numpy as np

    A = np.array([1, 2, 3, 4, 5])

    print(A > 2)     # [False False True True True]
    print(A[A > 2])  # [3 4 5]

    B = np.array([[1, 2], [3, 4]])

    print(B < 4)
    # [[ True  True]
    #  [ True False]]
    print(B[B < 4])  # [1 2 3]

Array Math
----------

The addition, subtraction, multiplication, and division operations for values
correspond to the element-wise operations for arrays. Element-wise meaning that
the operation is applied to corresponding elements in the two arrays. We can
also apply more advanced mathematical functions to an array using the NumPy
implmentation.

.. code-block:: python

    # array_math.py
    import numpy as np

    A = np.array([1, 2, 3])
    B = np.array([4, 5, 6])

    print(A + B)  # [5 7 9]
    print(B - A)  # [3 3 3]
    print(A * B)  # [ 4 10 18]
    print(B / A)  # [4.  2.5 2. ]

    print(np.power(A,2))  # [1 4 9]
    print(np.sin(A))      # [0.84147098 0.90929743 0.14112001]

Miscellaneous Operations
------------------------

There are some additional array operations that may be useful. ``.max()`` and
``.min()`` can be used to get the minimum or maximum element in an array
respectively. An array can be transposed (axes swapped) with ``.T``. Lastly,
``.vstack()`` and ``.hstack()`` can be used to vertically or horizontally stack
a pair of arrays.

.. code-block:: python

    # misc_operations.py
    import numpy as np

    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])

    print(A.min())  # 1
    print(A.max())  # 4
    print(A.T)
    # [[1 3]
    #  [2 4]]
    print(np.hstack((A,B)))
    # [[1 2 5 6]
    #  [3 4 7 8]]
    print(np.vstack((A,B)))
    # [[1 2]
    #  [3 4]
    #  [5 6]
    #  [7 8]]

That concludes the tutorial! There is an endless amount to learn about the
NumPy Python package. Feel free to explore the `documentation`_ further to
learn more neat capabilities.

.. _documentation: https://numpy.org/doc/stable/user/absolute_beginners.html#