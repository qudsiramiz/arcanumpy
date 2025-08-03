from __future__ import annotations

import os
from pathlib import Path


def update_functions_rst_file(source_dir: Path | str | None = None,
                              output_dir: Path | str | None = None) -> Path:
    """Generate ``functions.rst`` from the RST files in ``source_dir``.

    Parameters
    ----------
    source_dir:
        Directory containing individual ``.rst`` files.  When ``None`` the
        ``rst_files`` directory located next to this script is used.
    output_dir:
        Directory in which to place the generated ``functions.rst`` file.  When
        ``None`` the directory containing this script is used.

    Returns
    -------
    Path
        Path to the generated ``functions.rst`` file.
    """

    base_dir = Path(__file__).resolve().parent
    source_path = Path(source_dir) if source_dir is not None else base_dir / "rst_files"
    output_path = Path(output_dir) if output_dir is not None else base_dir
    output_module_file = output_path / "functions.rst"

    rst_files = [
        f for f in os.listdir(source_path) if f.endswith(".rst") and f != "functions.rst"
    ]

    with open(output_module_file, "w") as module_file:
        module_file.write("=========\n")
        module_file.write("Functions\n")
        module_file.write("=========\n\n")
        module_file.write(".. toctree::\n")
        module_file.write("   :maxdepth: 3\n\n")
        for rst in sorted(rst_files):
            module_name = os.path.splitext(rst)[0]
            module_file.write(
                f"   {module_name} <./rst_files/{module_name}.rst>\n"
            )

    return output_module_file


if __name__ == "__main__":  # pragma: no cover - script entry point
    update_functions_rst_file()
