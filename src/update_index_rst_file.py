import os

# Paths to directories
source_dir = "/home/vetinari/Desktop/git/arcanumpy/src/rst_files"
output_dir = "/home/vetinari/Desktop/git/arcanumpy/src/"
output_index_file = os.path.join(output_dir, "index.rst")

# Scan for all .rst files (exclude index.rst itself)
rst_files = [
    f for f in os.listdir(source_dir) if f.endswith(".rst") and f != "index.rst"
]

# Write to index.rst
with open(output_index_file, "w") as index_file:
    # Header section with additional information
    index_file.write(":tocdepth: 3\n\n")
    index_file.write(".. _ArcanumPy-documentation:\n\n")
    index_file.write(".. image:: _static/arcanumpy_logo.png\n")
    index_file.write("    :alt: arcanum logo\n")
    index_file.write("    :align: right\n")
    index_file.write("    :Scale: 20%\n\n")
    index_file.write("=======================\n")
    index_file.write("ArcanumPy Documentation\n")
    index_file.write("=======================\n\n")
    index_file.write(".. _arpy: https://qudsiramiz.space/arcanumpy/\n\n")
    index_file.write(
        "ArcanumPy is a Python package that provides a set of tools that I have developed for my research or\n"
        "have found useful in my research. The package is named after the Ars Arcanum, in the Stormlight\n"
        "Archive series by Brandon Sanderson. The Ars Arcanum is a collection of information about the magic\n"
        "systems in the world of Roshar.\n\n"
    )
    index_file.write(
        ".. note::\n\n"
        "    The package is still under development and might be a bit buggy to use. Please report any bug\n"
        "    that you might find to us. The documentation is also a work in progress and is being continuously updated.\n\n"
    )

    # Main table of contents
    index_file.write("Contents\n")
    index_file.write("========\n\n")

    # Add additional sections (static)
    index_file.write("About ArcanumPy\n")
    index_file.write("===============\n")
    index_file.write(".. toctree::\n")
    index_file.write("   :maxdepth: 2\n\n")
    index_file.write("   About ArcanumPy <about>\n\n")

    index_file.write("Installation\n")
    index_file.write("============\n")
    index_file.write(".. toctree::\n")
    index_file.write("   :maxdepth: 5\n\n")
    index_file.write("   Installation <install>\n\n")

    # Dynamically add all `.rst` files as part of the main TOC
    index_file.write("\nModules\n")
    index_file.write("=======\n")
    index_file.write(".. toctree::\n")
    index_file.write("   :maxdepth: 5\n\n")
    for rst in sorted(rst_files):
        module_name = os.path.splitext(rst)[0]  # Remove the .rst extension
        index_file.write(f"   {module_name} <./rst_files/{module_name}.rst>\n")

        module_name = os.path.splitext(rst)[0]  # Remove the .rst extension
        module_rst_path = os.path.join(source_dir, rst)

        print(f"Processing {module_name} from {module_rst_path}")

        """
        # Read the module .rst file to extract functions
        with open(module_rst_path, "r") as module_file:
            lines = module_file.readlines()
            for line in lines:
                if line.startswith(".. autofunction::"):
                    # Extract function name from the line
                    function_name = line.replace(".. autofunction::", "").strip()
                    index_file.write(f"   {module_name}.{function_name}\n")

        """

    index_file.write("Citation and Acknowledgements\n")
    index_file.write("=============================\n")
    index_file.write(".. toctree::\n")
    index_file.write("   :maxdepth: 2\n\n")
    index_file.write("   Citation and Acknowledgements <citation>\n\n")

    # Footer for additional references
    index_file.write("\nIndices and tables\n")
    index_file.write("==================\n\n")
    index_file.write("* :ref:`genindex`\n")
    index_file.write("* :ref:`modindex`\n")
    index_file.write("* :ref:`search`\n")
