import os

# Paths to directories
source_dir = "/home/cephadrius/Desktop/git/arcanumpy/src/rst_files"
output_dir = "/home/cephadrius/Desktop/git/arcanumpy/src/"
output_module_file = os.path.join(output_dir, "functions.rst")

# Scan for all .rst files (exclude index.rst itself)
rst_files = [
    f for f in os.listdir(source_dir) if f.endswith(".rst") and f != "functions.rst"
]

# Write to index.rst
with open(output_module_file, "w") as module_file:
    module_file.write("=========\n")
    module_file.write("Functions\n")
    module_file.write("=========\n\n")
    module_file.write(".. toctree::\n")
    module_file.write("   :maxdepth: 3\n\n")
    for rst in sorted(rst_files):
        module_name = os.path.splitext(rst)[0]  # Remove the .rst extension
        # Remove "arcanumpy." from the module name
        # if module_name.startswith("arcanumpy."):
        #     module_name = module_name[len("arcanumpy.") :]

        module_file.write(f"   {module_name} <./rst_files/{module_name}.rst>\n")

        module_name = os.path.splitext(rst)[0]  # Remove the .rst extension
        module_rst_path = os.path.join(source_dir, rst)
