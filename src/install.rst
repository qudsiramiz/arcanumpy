Installation Guide
==================

The next section of this document will guide you through the installation process of `arcanumpy`.

Though it is not necessary, we strongly recommend that you install `arcanumpy` in a virtual environment.
This will prevent any conflicts with other Python packages you may have installed.

A virtual environment is a self-contained directory tree that contains a Python installation for a
particular version of Python, plus a number of additional packages. You can install packages into a
virtual environment without affecting the system Python installation. This is especially useful when
you need to install packages that might conflict with other packages you have installed.

Creating a Virtual Environment
------------------------------

There are several ways to create a virtual environment. We recommend using `python3` to do so.

For this exercise, we will assume that you have a directory called `Documents/arcanumpy` where you will
install `arcanumpy` and create your virtual environment. Please replace `Documents/arcanumpy` with the actual
path to the directory where you want to install `arcanumpy` and create your virtual environment.

- Navigate to the `Documents/arcanumpy` directory.

Using python3
~~~~~~~~~~~~~

You can create a virtual environment called `arcanumpy_venv` (or any other name you might like) using 
`python3` by running the following command:

.. code-block:: bash

    python3 -m venv arcanumpy_venv

You can activate the virtual environment by running the following command:

On Linux/MacOS:
^^^^^^^^^^^^^^^

.. code-block:: bash

    source arcanumpy_venv/bin/activate

On Windows:
^^^^^^^^^^^

.. code-block:: bash

    .\arcanumpy_venv\Scripts\activate

You can deactivate the virtual environment by running the following command:

.. code-block:: bash

    deactivate

Installing `arcanumpy`
---------------
There are three ways to install `arcanumpy`: from pypi, from source, and from a local copy.

Installing from PyPI
~~~~~~~~~~~~~~~~~~~~~

After you have created and activated your virtual environment, you can install `arcanumpy` from PyPI by
running the following command:

.. code-block:: bash

    pip install arcanumpy


Installing from Source
~~~~~~~~~~~~~~~~~~~~~~

After you have created and activated your virtual environment, you can install `arcanumpy` directly from
GitHub by running the following command:

.. code-block:: bash

    pip install git+https://github.com/qudsiramiz/arcanumpy

.. note::
    This will install the latest version of `arcanumpy` from the main branch. If you want to install a specific version, please append the version number to the URL.
    For example, if you want to install version `0.3.1`, you can run the following command:

    .. code-block:: bash

        pip install git+https://github.com/qudsiramiz/arcanumpy@0.3.1


Verifying the Installation
==========================

You can verify that `arcanumpy` was installed by running the following command:

.. code-block:: bash

    pip show arcanumpy

This should produce output similar to the following:

.. code-block::

    Name: arcanumpy
    Version: 0.1.0
    Summary: Personal selection of random functions and codes in Python
    Home-page: https://qudsiramiz.space/arcanumpy/
    Author: Ramiz Qudsi
    Author-email: qudsiramiz@gmail.com
    License: GPL V3
    Location: /home/cephadrius/Desktop/arcanum_test/arcanum_test/lib/python3.10/site-packages
    Requires: cdflib, imageio, pandas, scikit-learn, seaborn
    Required-by: 


You can also verify that `arcanumpy` was installed by running the following command:

.. code-block:: bash

    pip list

This should produce output similar to the following:

.. code-block:: bash

    Package         Version
    --------------- -------
    .....................
    kiwisolver      1.4.5
    arcanumpy       0.0.1
    matplotlib      3.8.2
    numpy           1.26.4
    .....................

You can open a Python shell and import `arcanumpy` by running the following commands:

.. code-block:: bash

    python
    import arcanumpy
    arcanumpy.__version__

This should produce output similar to the following:

.. code-block::

    '0.0.1'

If that worked, congratulations! You have successfully installed `arcanumpy`.

Using `arcanumpy` Software
===================

.. note::
   We will add more examples and tutorials in the future. For now, we will use a Jupyter Notebook
   to demonstrate how to use `arcanumpy`.
