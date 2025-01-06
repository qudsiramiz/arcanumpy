"""Print the version number for the current installation."""

import logging


def version():
    """
    Print the ArcanumPy version number.

    Returns
    -------
    None.

    """
    from importlib.metadata import version

    ver = version("arcanumpy")
    logging.info("arcanumpy version: " + ver)
