# Test file for arcanumpy

import os
import builtins
import runpy
from pathlib import Path


def test_update_modules_rst_file_cosmere(tmp_path, monkeypatch):
    """Ensure the documentation index is generated correctly."""

    rst_dir = tmp_path / "rst_files"
    rst_dir.mkdir()
    for name in ("alpha.rst", "beta.rst"):
        (rst_dir / name).write_text("")

    output_file = tmp_path / "functions.rst"

    original_listdir = os.listdir
    monkeypatch.setattr(os, "listdir", lambda _:
                        original_listdir(rst_dir))

    original_open = builtins.open

    def fake_open(file, mode="r", *args, **kwargs):
        if "w" in mode:
            return original_open(output_file, mode, *args, **kwargs)
        return original_open(file, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)

    script_path = Path(__file__).resolve().parents[2] / "src" / "update_modules_rst_file_cosmere.py"
    runpy.run_path(str(script_path))

    assert output_file.exists()
    content = output_file.read_text()
    assert "alpha <./rst_files/alpha.rst>" in content
    assert "beta <./rst_files/beta.rst>" in content
