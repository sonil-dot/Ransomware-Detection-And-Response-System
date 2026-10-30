
import os
from pathlib import Path

import response


def test_quarantine_copies_file_and_preserves_original(tmp_path, monkeypatch):
    # Create a temporary test file
    original = tmp_path / "sample.txt"
    original.write_text("safe test content", encoding="utf-8")

    # Use a temporary quarantine folder
    quarantine_dir = tmp_path / "quarantine"
    monkeypatch.setattr(response, "os", os)

    # Redirect quarantine output to the temporary folder
    monkeypatch.chdir(tmp_path)

    result = response.quarantine_file(str(original))

    # Check that the operation succeeded
    assert result is True

    # Check that the original still exists and is unchanged
    assert original.exists()
    assert original.read_text(encoding="utf-8") == "safe test content"

    # Check that an evidence copy was created
    copied_files = list(quarantine_dir.iterdir())
    assert len(copied_files) == 1
    assert copied_files[0].read_text(encoding="utf-8") == "safe test content"


def test_quarantine_returns_false_for_missing_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    missing_file = tmp_path / "does_not_exist.txt"

    result = response.quarantine_file(str(missing_file))

    assert result is False
