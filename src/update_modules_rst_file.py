from __future__ import annotations

import os
from pathlib import Path


def update_modules_rst_file(source_dir: Path | str | None = None,
                            output_dir: Path | str | None = None) -> Path:
    """Generate ``modules.rst`` from RST files in ``source_dir``.

    Parameters
    ----------
    source_dir:
        Directory containing individual ``.rst`` files.  Defaults to the
        ``rst_files`` directory next to this script.
    output_dir:
        Destination directory for the resulting ``modules.rst`` file.  Defaults
        to the ``rst_files`` directory.

    Returns
    -------
    Path
        Path to the generated ``modules.rst`` file.
    """

    base_dir = Path(__file__).resolve().parent
    source_path = Path(source_dir) if source_dir is not None else base_dir / "rst_files"
    output_path = Path(output_dir) if output_dir is not None else base_dir / "rst_files"
    output_module_file = output_path / "modules.rst"

    rst_files = [
        f for f in os.listdir(source_path) if f.endswith(".rst") and f != "modules.rst"
    ]

    with open(output_module_file, "w") as module_file:
        module_file.write(".. toctree::\n")
        module_file.write("   :maxdepth: 3\n\n")
        for rst in sorted(rst_files):
            module_name = os.path.splitext(rst)[0]
            module_file.write(
                f"   {module_name} <./rst_files/{module_name}.rst>\n"
            )

    return output_module_file


if __name__ == "__main__":  # pragma: no cover - script entry point
    update_modules_rst_file()
