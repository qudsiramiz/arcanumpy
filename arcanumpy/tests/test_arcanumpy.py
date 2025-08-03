from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_update_module() -> object:
    repo_root = Path(__file__).resolve().parents[2]
    module_path = repo_root / "src" / "update_modules_rst_file_cosmere.py"
    spec = importlib.util.spec_from_file_location("update_modules_rst_file_cosmere", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def test_update_modules_rst_file_cosmere(tmp_path):
    module = _load_update_module()
    repo_root = Path(__file__).resolve().parents[2]
    source_dir = repo_root / "src" / "rst_files"

    output_file = module.update_functions_rst_file(source_dir, tmp_path)

    assert output_file.exists()
    content = output_file.read_text()
    assert "Functions" in content
    assert "arcanumpy.arcanumpy" in content
