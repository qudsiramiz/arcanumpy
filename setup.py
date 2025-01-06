from pathlib import Path
from setuptools import setup, find_packages
import toml

# Read the pyproject.toml file
pyproject_path = Path("pyproject.toml")
pyproject = toml.load(pyproject_path)

# Extract the version number
version = pyproject.get("tool", {}).get("poetry", {}).get("version", "0.0.1")

# Extract the required packages (excluding Python specifiers)
dependencies = pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {})
install_requires = [dep for dep in dependencies.keys() if dep.lower() != "python"]

setup(
    name="arcanumpy",
    version=version,
    description="Personal collection of various Python tools and utilities.",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://qudsiramiz.space/arcanumpy",
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
