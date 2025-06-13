"""Unit tests for the md2tex module."""

import pytest
from src.py.converters.md2tex import (
    convert_markdown_to_latex,
    convert_figures_to_latex,
    convert_figure_references_to_latex,
    convert_citations_to_latex,
    extract_content_sections,
    map_section_title_to_key,
    convert_html_comments_to_latex,
    escape_url_for_latex,
)


class TestMarkdownToLatexConversion:
    """Test basic markdown to LaTeX conversion."""

    def test_convert_bold_text(self):
        """Test conversion of bold text."""
        markdown = "This is **bold** text."
        expected = r"This is \textbf{bold} text."
        result = convert_markdown_to_latex(markdown)
        assert expected in result

    def test_convert_italic_text(self):
        """Test conversion of italic text."""
        markdown = "This is *italic* text."
        expected = r"This is \textit{italic} text."
        result = convert_markdown_to_latex(markdown)
        assert expected in result

    def test_convert_headers(self):
        """Test conversion of markdown headers."""
        markdown = "## Section\n### Subsection\n#### Subsubsection"
        result = convert_markdown_to_latex(markdown)
        assert r"\section{Section}" in result
        assert r"\subsection{Subsection}" in result
        assert r"\subsubsection{Subsubsection}" in result

    def test_convert_code_blocks(self):
        """Test conversion of inline code."""
        markdown = "Use `code_here` for testing."
        result = convert_markdown_to_latex(markdown)
        assert r"\texttt{code\_here}" in result


class TestCitationConversion:
    """Test citation conversion functionality."""

    def test_single_citation(self):
        """Test conversion of single citations."""
        text = "According to @smith2023, this is true."
        expected = r"According to \cite{smith2023}, this is true."
        result = convert_citations_to_latex(text)
        assert result == expected

    def test_multiple_citations_bracketed(self):
        """Test conversion of multiple bracketed citations."""
        text = "This is supported [@smith2023;@jones2022]."
        expected = r"This is supported \cite{smith2023,jones2022}."
        result = convert_citations_to_latex(text)
        assert result == expected

    def test_citation_with_underscores(self):
        """Test citations with underscores in keys."""
        text = "See @author_name_2023 for details."
        expected = r"See \cite{author_name_2023} for details."
        result = convert_citations_to_latex(text)
        assert result == expected


class TestFigureConversion:
    """Test figure conversion functionality."""

    def test_figure_with_attributes(self):
        """Test conversion of figures with attributes."""
        markdown = '![Test Caption](FIGURES/test.png){#fig:test width="0.8" tex_position="!ht"}'
        result = convert_figures_to_latex(markdown)
        
        assert r"\begin{figure}[!ht]" in result
        assert r"\includegraphics[width=0.8\linewidth]{Figures/test.png}" in result
        assert r"\caption{Test Caption}" in result
        assert r"\label{fig:test}" in result
        assert r"\end{figure}" in result

    def test_figure_without_attributes(self):
        """Test conversion of figures without attributes."""
        markdown = "![Simple Caption](FIGURES/simple.png)"
        result = convert_figures_to_latex(markdown)
        
        assert r"\begin{figure}[ht]" in result
        assert r"\includegraphics[width=\linewidth]{Figures/simple.png}" in result
        assert r"\caption{Simple Caption}" in result
        assert r"\end{figure}" in result

    def test_figure_reference_conversion(self):
        """Test conversion of figure references."""
        text = "As shown in @fig:test, the results are clear."
        expected = r"As shown in \ref{fig:test}, the results are clear."
        result = convert_figure_references_to_latex(text)
        assert result == expected


class TestSectionExtraction:
    """Test section extraction from markdown."""

    def test_map_section_titles(self):
        """Test mapping of section titles to keys."""
        assert map_section_title_to_key("Abstract") == "abstract"
        assert map_section_title_to_key("Methods") == "methods"
        assert map_section_title_to_key("Results and Discussion") == "results_and_discussion"
        assert map_section_title_to_key("Acknowledgements") == "acknowledgements"

    def test_extract_sections_with_yaml(self, temp_dir, sample_markdown):
        """Test extraction of sections from markdown with YAML frontmatter."""
        markdown_file = temp_dir / "test.md"
        markdown_file.write_text(sample_markdown)
        
        sections = extract_content_sections(str(markdown_file))
        
        assert "main" in sections
        assert "methods" in sections
        assert "results" in sections
        # Check that YAML frontmatter is removed
        assert "---" not in sections["main"]


class TestHTMLCommentConversion:
    """Test HTML comment conversion."""

    def test_html_comment_to_latex(self):
        """Test conversion of HTML comments to LaTeX comments."""
        html = "<!-- This is a comment\nwith multiple lines -->"
        result = convert_html_comments_to_latex(html)
        expected = "% This is a comment\n% with multiple lines"
        assert result == expected


class TestURLEscaping:
    """Test URL escaping for LaTeX."""

    def test_escape_hash_in_url(self):
        """Test escaping of hash symbols in URLs."""
        url = "https://example.com/page#section"
        expected = "https://example.com/page\\#section"
        result = escape_url_for_latex(url)
        assert result == expected

    def test_escape_percent_in_url(self):
        """Test escaping of percent symbols in URLs."""
        url = "https://example.com/page%20with%20spaces"
        expected = "https://example.com/page\\%20with\\%20spaces"
        result = escape_url_for_latex(url)
        assert result == expected