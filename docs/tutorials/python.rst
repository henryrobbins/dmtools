.. _python_tutorial:

Introduction to Python
======================

This tutorial will walk through a short introduction to Python with emphasis on
the necessary basics for using dmtools and working with images. To get the
most out of this tutorial, it is recommended to follow along by running all
the code snippets yourself.

Python Scripts
--------------

In the :ref:`installation` section, you saw how you can open up a Python prompt
in a terminal where you can enter Python commands and run them. Anything more
than a one line command is going to be bothersome to write in a prompt.
Furthermore, it will not be repeatable. The python script addresses these
issues. A Python script is a text file with the ``.py`` extension. We can write
these files in any text editor. This tutorial assumes you are using `VS Code`_
(see :ref:`vscode_tutorial`). After creating a Python script, you can run the
script from a terminal with ``python hello_world.py``. However, there is one
catch: you must be in the directory where the ``hello_world.py`` script is
located. Hence, we need to be able to navigate directories while in a terminal.

Navigating Directories in a Terminal
------------------------------------

When you open up a terminal, you will see a prompt like the following:

.. code-block:: bash

    (base) Name-Of-Machine:~ Name-Of-User$

Let's break down what information is contained in this prompt. The ``(base)``
let's us know that we are in the base Python environment. Don't worry too much
about what that means. The ``Name-Of-Machine`` and ``Name-Of-User`` tell us
(you guessed it) the name of the machine / computer and the user. The ``$`` is
just an indication that it is the end of the prompt and you can type your
command. Most pertinent is the ``~`` which indicates where in the file
structure we are located. This is called the current working directory.
The ``~`` indicates we are in the home directory.

We can navigate the file structure in a terminal the same way we would in
Finder on macOS. Run the command ``ls`` by typing ``ls`` after the prompt and
pressing ``Enter``. You should see a list of the files and directories in the
current working directory.

.. code-block:: bash

    (base) Name-Of-Machine:~ Name-Of-User$ ls
    Applications    Library
    Desktop         Movies
    Documents       Music
    Downloads       Public

We can go into one of these directories with the ``cd`` command. For example,
the command ``cd Desktop`` will change our working directory to the
``Desktop`` directory.

.. code-block:: bash

    (base) Name-Of-Machine:~ Name-Of-User$ cd Desktop
    (base) Name-Of-Machine:Desktop Name-Of-User$ ls
    DesktopItem1    DesktopItem3
    DesktopItem2    DesktopItem4

To go back one directory, use ``cd ..``. To go back all the way to the home
directory, use ``cd ~``. Lastly, you can specify a file path to avoid
running multiple ``cd`` commands.

.. code-block:: bash

    (base) Name-Of-Machine:~ Name-Of-User$ cd Music
    (base) Name-Of-Machine:Music Name-Of-User$ cd Artist
    (base) Name-Of-Machine:Artist Name-Of-User$ cd NewAlbum
    (base) Name-Of-Machine:NewAlbum Name-Of-User$ ls
    Song1   Song3
    Song2   Song4

.. code-block:: bash

    (base) Name-Of-Machine:~ Name-Of-User$ cd Music/Artist/NewAlbum
    (base) Name-Of-Machine:NewAlbum Name-Of-User$ ls
    Song1   Song3
    Song2   Song4

These few commands are really all you need to know to navigate directories
while in a terminal!


Hello World!
------------

In this section, we will create a directory where we will put our Python
scripts and create our first script.

First, open up a terminal. Run the command ``mkdir scripts`` to create a
directory called scripts. You can then ``cd`` into it a run ``ls`` to see that
there is nothing in it yet.

.. code-block:: bash

    (base) Name-Of-Machine:~ Name-Of-User$ ls
    Applications    Library
    Desktop         Movies
    Documents       Music
    Downloads       Public
    (base) Name-Of-Machine:~ Name-Of-User$ mkdir scripts
    (base) Name-Of-Machine:~ Name-Of-User$ ls
    Applications    Movies
    Desktop         Music
    Documents       Public
    Downloads       scripts
    Library
    (base) Name-Of-Machine:~ Name-Of-User$ cd scripts
    (base) Name-Of-Machine:scripts Name-Of-User$ ls
    (base) Name-Of-Machine:scripts Name-Of-User$

Now, let's create our first Python script! Rather than opening VS Code
in the traditional way you open applications, we will open it from the
terminal. This is because it will automatically put the files we create in the
working directory which will prevent us from running into issues when trying to
run our Python scripts. Make sure you are still in the ``scripts`` directory
and run ``code .`` to open VS Code (don't close your terminal because you will
need it to run the Python scripts). You will see a file navigation window on
the left. Create a new file called ``hello_world.py``.

.. literalinclude:: scripts/python/hello_world.py
   :language: python

The lines with ``#`` at the beginning are just comments in the Python code. You
do not need to include them but they can give helpful information! Save the
file and try running ``python hello_world.py`` in the terminal.

.. code-block:: bash

    (base) Name-Of-Machine:scripts Name-Of-User$ python hello_world.py
    Hello World!

You just created your first Python script! The remainder of this tutorial will
walk you through the basics of Python through multiple example Python
`scripts`_ . Again, it is recommended you follow along by creating and running
these scripts. Even better, try modifying them to see if the output changes as
you would expect!

Math
----

We can add, multipy, subtract, and divide numbers quite easily. What if we
want to use some more complex math functions like the sine function? A lot of
these are provided by a package called NumPy (which we will look at much
closer in :ref:`numpy_tutorial`). To access these functions, we first need to
import the package with ``import numpy as np``. We can then use ``np.sin()``
to apply the sine function to some value. The math package also
provides some useful functions you may want to use like the floor and ceiling
function.

.. literalinclude:: scripts/python/simple_math.py
   :language: python

Variables
---------

It is often helpful to assign a name to a value. This is called a variable.
In the script below, we set the variable ``x`` to be ``1`` and  ``y`` to be
``2``. We can then use these variables just like they were the values we
assigned them to.

.. literalinclude:: scripts/python/variables.py
   :language: python

Loops
-----

If we want to do the same command multiple times, we can use a loop. A loop has
the syntax ``for i in range(n)`` where ``n`` is the number of times we will run
through this loop. The variable ``i`` starts at zero and is incremented by one
every time we run through the loop. The lines of code that are run in every
iteration of the loop make up the loop body. We indent the lines that are in
the loop body.

.. literalinclude:: scripts/python/loops.py
   :language: python

Conditional Statements
----------------------

What if we want to run a line of code only if a certain condition holds?
These are called conditional statements. To compare values, we can use ``==``
for equals and ``!=`` for not equals. Note that ``x = 2`` assigns variable ``x``
the value ``2`` while ``x == 2`` returns if ``x`` has value ``2`` or not. Next,
we need the syntax for boolean operators like and, or, and not. The operator
``x & y`` returns ``True`` if both ``x`` and ``y`` are ``True``. The operator
``x | y`` returns ``True`` if at least one of ``x`` or ``y`` are ``True``.
Lastly, we have the syntax for the conditional statement which is ``if x:``
where the body of the conditional statement runs if ``x`` is ``True``. The
body of the conditional statement is denoted with indentation like the
loop body.

.. literalinclude:: scripts/python/condition.py
   :language: python

Lists
-----

Sometimes we have a list of values we care about and not just a single value.
We can represent these as a list. For example, ``x = [1,2,3]`` is a list of
three integers. We can then access the value at a certain index with the
notation ``x[i]`` where ``i`` is the index of the value we want. Python is
zero-indexed which means that the first value in a list has index zero. We can
add values to lists with ``.append()``. We can also add lists together.

.. literalinclude:: scripts/python/lists.py
   :language: python

List Comprehension
------------------

One of the many nice features in Python is called list comprehension. It allows
us to initialize a list. It essentially combines the syntax for a list with
the syntax for a loop allowing us to define a list with less code.

.. literalinclude:: scripts/python/list_comprehension.py
   :language: python

Functions
---------

One of the most important concepts in programming is the function. Functions
allow us to avoid writing the same code multiple times. A function has
parameters or inputs. Sometimes it has an output and other times, it does not.
The notation for a function declaration in Python is ``def f(x, y, ...):`` where
``f`` is the name of the function and ``x, y, ...`` are the function parameters.
Like we have seen before, we use indentation in Python to denote the function
body. This is the code that will be run every time the function is called.
If the function will return a value, we use the keyword ``return``. Lastly,
when we want to call the function, we use the notation ``f(x, y, ...)`` where
``f`` is the name of the function and ``x, y, ...`` are the arguments or actual
values we are assigning the parameters of that function.

.. literalinclude:: scripts/python/functions.py
   :language: python

That concludes the tutorial! If you want to do something in Python but don't
know the syntax, `Stack Overflow`_ is a great resource. It is also a great
resource if you get an error message when trying to run your Python script.

.. _VS Code: https://code.visualstudio.com/
.. _Notepad++: https://notepad-plus-plus.org/
.. _Vim: https://www.vim.org/
.. _scripts: https://github.com/henryrobbins/dmtools/tree/master/docs/tutorials/scripts
.. _Stack Overflow: https://stackoverflow.com/