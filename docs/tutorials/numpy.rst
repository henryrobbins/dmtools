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

.. literalinclude:: scripts/numpy/numpy_array.py
   :language: python

Array Attributes
----------------

The three most common attributes of an array are the dimension ``ndim``, size
``size``, and shape ``shape``. The script below gives all three attributes of
two example arrays.

.. literalinclude:: scripts/numpy/array_attributes.py
   :language: python

Indexing and Slicing
--------------------

A common operation you will want to do is access part of an array. The
notation ``x[i:j]`` gives the ``i`` th through ``j`` th (not including ``j``)
values in the array ``x``. We can use ``x[i:]`` or ``x[:i]`` to get all the
values after or before the ``i`` th value respectively. It should be noted that
this notation also works with the Python list.

.. literalinclude:: scripts/numpy/indexing.py
   :language: python

Conditional Array
-----------------

Another way to slice an array is with a condition. The syntax for this is
``x[condition]``. If we just look at the result of the condition, it returns
an array of boolean values where the value is ``True`` if the corresponding
element satisfied the condition and ``False`` otherwise. Passing this boolean
array to the slicing notation indicates which values to keep.

.. literalinclude:: scripts/numpy/condition_array.py
   :language: python

Array Math
----------

The addition, subtraction, multiplication, and division operations for values
correspond to the element-wise operations for arrays. Element-wise meaning that
the operation is applied to corresponding elements in the two arrays. We can
also apply more advanced mathematical functions to an array using the NumPy
implmentation.

.. literalinclude:: scripts/numpy/array_math.py
   :language: python

Miscellaneous Operations
------------------------

There are some additional array operations that may be useful. ``.max()`` and
``.min()`` can be used to get the minimum or maximum element in an array
respectively. An array can be transposed (axes swapped) with ``.T``. Lastly,
``.vstack()`` and ``.hstack()`` can be used to vertically or horizontally stack
a pair of arrays.

.. literalinclude:: scripts/numpy/misc_operations.py
   :language: python

That concludes the tutorial! There is an endless amount to learn about the
NumPy Python package. Feel free to explore the `documentation`_ further to
learn more neat capabilities.

.. _documentation: https://numpy.org/doc/stable/user/absolute_beginners.html#