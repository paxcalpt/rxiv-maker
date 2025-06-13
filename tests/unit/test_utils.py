"""Unit tests for the utils module."""

import pytest
from pathlib import Path
from src.py.utils import (
    create_output_dir,
    find_article_md,
    write_article_output,
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

    def test_find_article_md_standard_name(self, temp_dir, monkeypatch):
        """Test finding article markdown with standard name."""
        # Change to temp directory
        monkeypatch.chdir(temp_dir)
        
        # Create standard article file
        article_file = temp_dir / "00_ARTICLE.md"
        article_file.write_text("# Test Article")
        
        result = find_article_md()
        assert Path(result).name == "00_ARTICLE.md"

    def test_find_article_md_alternative_names(self, temp_dir, monkeypatch):
        """Test finding article markdown with alternative names."""
        # Change to temp directory
        monkeypatch.chdir(temp_dir)
        
        # Create alternative article files
        alt_names = ["article.md", "ARTICLE.md", "main.md"]
        
        for name in alt_names:
            # Clean up any existing files
            for f in temp_dir.glob("*.md"):
                f.unlink()
            
            article_file = temp_dir / name
            article_file.write_text("# Test Article")
            
            try:
                result = find_article_md()
                assert Path(result).name == name
                break
            except FileNotFoundError:
                continue

    def test_find_article_md_not_found(self, temp_dir, monkeypatch):
        """Test finding article markdown when none exists."""
        # Change to temp directory with no markdown files
        monkeypatch.chdir(temp_dir)
        
        with pytest.raises(FileNotFoundError):
            find_article_md()

    def test_write_article_output(self, temp_dir):
        """Test writing article output to file."""
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        
        latex_content = r"""
        \documentclass{article}
        \title{Test Article}
        \begin{document}
        \maketitle
        Test content
        \end{document}
        """
        
        result_file = write_article_output(str(output_dir), latex_content)
        
        assert Path(result_file).exists()
        assert Path(result_file).suffix == ".tex"
        
        # Check content was written
        written_content = Path(result_file).read_text()
        assert "Test Article" in written_content
        assert r"\documentclass{article}" in written_content

    def test_write_article_output_overwrite(self, temp_dir):
        """Test overwriting existing article output."""
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        
        # Write initial content
        initial_content = r"\documentclass{article}\title{Initial}"
        result_file = write_article_output(str(output_dir), initial_content)
        
        # Write new content
        new_content = r"\documentclass{article}\title{Updated}"
        result_file_2 = write_article_output(str(output_dir), new_content)
        
        # Should be same file
        assert result_file == result_file_2
        
        # Content should be updated
        written_content = Path(result_file).read_text()
        assert "Updated" in written_content
        assert "Initial" not in written_content