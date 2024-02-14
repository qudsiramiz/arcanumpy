import toml
from setuptools import setup, find_packages

# Read the pyproject.toml file
with open("pyproject.toml") as f:
    pyproject = toml.load(f)

# Extract the version number
version = pyproject["tool"]["poetry"]["version"]

# Extract the required packages
install_requires = pyproject["tool"]["poetry"]["dependencies"].keys()

setup(
    name="arcanumpy",
    version=version,
    description="Personal collection of various Python tools and utilities.",
    long_description=open("README.md").read(),
    url="https://github.com/qudsiramiz/arcanumpy",
    author="Qudsi, Ramiz",
    author_email="qudsiramiz@gmail.com",
    license="GNU GPLv3",
    keywords="packages",
    packages=find_packages(),
    package_data={
        "": ["*.toml"],
    },
    install_requires=install_requires,
    python_requires=">=3.10",
    include_package_data=True,
)
