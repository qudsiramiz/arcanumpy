# lexi/__init__.py

# Import the version from your setup.py file
from pkg_resources import get_distribution, DistributionNotFound

# Add the docstring to the package
__doc__ = """
Personal collection of various Python tools and utilities.
"""

try:
    __version__ = get_distribution("arcanumpy").version
except DistributionNotFound:
    # Package is not installed
    __version__ = "0.0.0"
