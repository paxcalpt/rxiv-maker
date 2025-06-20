"""Unit tests for the utils module."""

from pathlib import Path

import pytest

from src.py.utils import (
    create_output_dir,
    find_manuscript_md,
    write_manuscript_output,
)


class TestUtils:
    """Test utility functions."""

    def test_create_output_dir(self, temp_dir):
        """Test creating output directory."""
        output_path = temp_dir / "output"
        create_output_dir(str(output_path))

        assert output_path.exists()
        assert output_path.is_dir()

    def test_create_output_dir_existing(self, temp_dir):
        """Test creating output directory when it already exists."""
        output_path = temp_dir / "existing_output"
        output_path.mkdir()

        # Should not raise error
        create_output_dir(str(output_path))
        assert output_path.exists()

    def test_find_manuscript_md_standard_name(self, temp_dir, monkeypatch):
        """Test finding manuscript markdown with standard name."""
        # Change to temp directory
        monkeypatch.chdir(temp_dir)

        # Clean up environment variable to ensure clean test
        import os

        if "MANUSCRIPT_PATH" in os.environ:
            monkeypatch.delenv("MANUSCRIPT_PATH")

        # Create manuscript directory and file
        manuscript_dir = temp_dir / "MANUSCRIPT"
        manuscript_dir.mkdir()
        manuscript_file = manuscript_dir / "01_MAIN.md"
        manuscript_file.write_text("# Test Manuscript")

        result = find_manuscript_md()
        assert Path(result).name == "01_MAIN.md"

    def test_find_manuscript_md_custom_path(self, temp_dir, monkeypatch):
        """Test finding manuscript markdown with custom path."""
        # Change to temp directory
        monkeypatch.chdir(temp_dir)

        # Set custom manuscript path
        import os

        os.environ["MANUSCRIPT_PATH"] = "MY_PAPER"

        # Create custom manuscript directory and file
        manuscript_dir = temp_dir / "MY_PAPER"
        manuscript_dir.mkdir()
        manuscript_file = manuscript_dir / "01_MAIN.md"
        manuscript_file.write_text("# Test Manuscript")

        result = find_manuscript_md()
        assert Path(result).name == "01_MAIN.md"
        assert "MY_PAPER" in str(result)

        # Clean up
        if "MANUSCRIPT_PATH" in os.environ:
            del os.environ["MANUSCRIPT_PATH"]

    def test_find_manuscript_md_not_found(self, temp_dir, monkeypatch):
        """Test finding manuscript markdown when none exists."""
        # Change to temp directory with no manuscript files
        monkeypatch.chdir(temp_dir)

        with pytest.raises(FileNotFoundError):
            find_manuscript_md()

    def test_write_manuscript_output(self, temp_dir):
        """Test writing manuscript output to file."""
        output_dir = temp_dir / "output"
        output_dir.mkdir()

        latex_content = r"""
        \documentclass{article}
        \title{Test Manuscript}
        \begin{document}
        \maketitle
        Test content
        \end{document}
        """

        result_file = write_manuscript_output(str(output_dir), latex_content)

        assert Path(result_file).exists()
        assert Path(result_file).suffix == ".tex"
        assert Path(result_file).name == "MANUSCRIPT.tex"

        # Check content was written
        written_content = Path(result_file).read_text()
        assert "Test Manuscript" in written_content
        assert r"\documentclass{article}" in written_content

    def test_write_manuscript_output_overwrite(self, temp_dir):
        """Test overwriting existing manuscript output."""
        output_dir = temp_dir / "output"
        output_dir.mkdir()

        # Write initial content
        initial_content = r"\documentclass{article}\title{Initial}"
        result_file = write_manuscript_output(str(output_dir), initial_content)

        # Write new content
        new_content = r"\documentclass{article}\title{Updated}"
        result_file_2 = write_manuscript_output(str(output_dir), new_content)

        # Should be same file
        assert result_file == result_file_2

        # Content should be updated
        written_content = Path(result_file).read_text()
        assert "Updated" in written_content
        assert "Initial" not in written_content
