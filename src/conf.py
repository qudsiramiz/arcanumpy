import os
import sys
import subprocess

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../"))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


def get_git_versions():
    try:
        # Fetch tags
        tags = subprocess.check_output(
            ["git", "tag"], universal_newlines=True
        ).splitlines()
        # Fetch branches
        branches = subprocess.check_output(
            ["git", "branch", "-r"], universal_newlines=True
        ).splitlines()
        # Clean up branches (remove remote name, e.g., "origin/")
        branches = [
            branch.strip().replace("origin/", "")
            for branch in branches
            if "origin/HEAD" not in branch
        ]

        # Combine and sort
        versions = sorted(set(tags + branches), reverse=True)
        return versions
    except Exception as e:
        print(f"Error fetching Git versions: {e}")
        return ["latest", "main"]  # Fallback versions


# versions = get_git_versions()

# -- Project information -----------------------------------------------------
project = "ArcanumPy"
copyright = "@ Ramiz Qudsi, 2024"
author = "Ramiz Qudsi"

html_baseurl = "https://qudsiramiz.space/arcanumpy"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx_autodoc_typehints",
    "myst_parser",
    "jupyter_sphinx",
    "nbsphinx",
    "sphinx_togglebutton",
    "sphinx_copybutton",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]

autosummary_generate = True
autosummary_imported_members = True
autodoc_typehints = "description"

templates_path = ["_templates"]
html_static_path = ["_static"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "sphinx_rtd_theme"
# html_theme = "furo"
html_static_path = ["_static"]  # Ensure _static is in the static path
html_css_files = [
    "css/custom.css",  # Add custom.css to the list
]
html_logo = "_static/arcanumpy_logo.png"
html_favicon = "_static/arcanumpy_logo.png"

html_context = {
    "display_github": True,
    # "display_versions": True,
    # "versions": versions,
    "github_user": "qudsiramiz",
    "github_repo": "arcanumpy",
    "github_version": "main",
    "conf_py_path": "/src/",
}

# -- Options for autodoc -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#module-sphinx.ext.autodoc

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "exclude-members": "__weakref__",
}

# Disable autodoc typehints to simplify the output
autodoc_typehints = "none"

# -- Options for autodock mock imports ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_mock_imports

autodoc_mock_imports = [
    "numpy",
    "pandas",
    "matplotlib",
    "astropy",
    "scipy",
    "cdflib",
    "jupyter",
    "arcanumpy.__init__",
    "arcanumpy.__version__",
]

html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
    "titles_only": False,
    # "display_version": True,
    "prev_next_buttons_location": "both",
    "style_external_links": True,
    "style_nav_header_background": "#042444",
    # "style_nav_header_text": "#ffffff",
    # "flyout_display": "attached",
    # "version_selector": True,
    # "theme_switcher": False,
}
