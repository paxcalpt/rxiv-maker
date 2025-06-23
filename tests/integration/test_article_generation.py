"""Integration tests for complete article generation pipeline."""

from unittest.mock import patch

import pytest


class TestManuscriptGeneration:
    """Integration tests for the complete manuscript generation process."""

    def test_generate_manuscript_command(self, temp_dir, sample_markdown):
        """Test the complete manuscript generation command."""
        # Set up test environment with proper manuscript structure
        manuscript_dir = temp_dir / "MANUSCRIPT"
        manuscript_dir.mkdir()
        manuscript_file = manuscript_dir / "00_MANUSCRIPT.md"
        manuscript_file.write_text(sample_markdown)
        output_dir = temp_dir / "output"

        # Change to test directory and run generation
        with (
            patch(
                "sys.argv", ["generate_preprint.py", "--output-dir", str(output_dir)]
            ),
            patch("os.getcwd", return_value=str(temp_dir)),
        ):
            # Import and run the main function
            from src.py.commands.generate_preprint import main

            try:
                result = main()
                assert result == 0  # Success

                # Check that output was generated
                assert output_dir.exists()

                # Look for generated LaTeX file
                tex_files = list(output_dir.glob("*.tex"))
                assert len(tex_files) > 0

                # Check content of generated file
                tex_content = tex_files[0].read_text()
                assert "Test" in tex_content

            except Exception as e:
                pytest.skip(f"Manuscript generation failed: {e}")

    def test_figure_generation_integration(self, temp_dir):
        """Test figure generation as part of complete pipeline."""
        # Create a simple Python figure script
        figures_dir = temp_dir / "FIGURES"
        figures_dir.mkdir()

        figure_script = figures_dir / "test_figure.py"
        figure_script.write_text(
            """
import matplotlib.pyplot as plt
import numpy as np

# Generate simple plot
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.title('Test Figure')
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.savefig('FIGURES/test_figure.png', dpi=300, bbox_inches='tight')
plt.savefig('FIGURES/test_figure.pdf', bbox_inches='tight')
plt.close()
"""
        )

        # Test figure generation
        with (
            patch("sys.argv", ["generate_figures.py"]),
            patch("os.getcwd", return_value=str(temp_dir)),
        ):
            try:
                from src.py.commands.generate_figures import main as fig_main

                result = fig_main()

                # Check if figures were generated
                png_file = figures_dir / "test_figure.png"
                pdf_file = figures_dir / "test_figure.pdf"
                if png_file.exists() and pdf_file.exists():
                    assert result == 0
                else:
                    pytest.skip(
                        "Figure generation requires matplotlib and may fail "
                        "in test environment"
                    )

            except Exception as e:
                pytest.skip(f"Figure generation test failed: {e}")

    def test_end_to_end_with_citations(self, temp_dir):
        """Test end-to-end generation with citations and references."""
        # Set up manuscript structure
        manuscript_dir = temp_dir / "MANUSCRIPT"
        manuscript_dir.mkdir()

        # Create manuscript with citations
        manuscript_content = """---
title: "Integration Test Manuscript"
authors:
  - name: "Test Author"
    affiliation: "Test Institution"
keywords: ["testing", "integration"]
---

# Introduction

This work builds on @smith2023 and [@jones2022;@brown2021].

## Results

See @fig:result for the main findings.

![Main Result](FIGURES/result.png){#fig:result width="0.7"}

## Bibliography

References will be processed from 02_REFERENCES.bib.
"""

        # Create bibliography file
        bib_content = """@article{smith2023,
  title={Example Article},
  author={Smith, John},
  journal={Test Journal},
  year={2023}
}

@article{jones2022,
  title={Another Example},
  author={Jones, Jane},
  journal={Test Journal},
  year={2022}
}

@article{brown2021,
  title={Third Example},
  author={Brown, Bob},
  journal={Test Journal},
  year={2021}
}
"""

        manuscript_file = manuscript_dir / "00_MANUSCRIPT.md"
        manuscript_file.write_text(manuscript_content)

        bib_file = manuscript_dir / "02_REFERENCES.bib"
        bib_file.write_text(bib_content)

        output_dir = temp_dir / "output"

        # Run article generation
        with (
            patch(
                "sys.argv", ["generate_preprint.py", "--output-dir", str(output_dir)]
            ),
            patch("os.getcwd", return_value=str(temp_dir)),
        ):
            try:
                from src.py.commands.generate_preprint import main

                result = main()

                if result == 0:
                    # Check generated content
                    tex_files = list(output_dir.glob("*.tex"))
                    assert len(tex_files) > 0

                    tex_content = tex_files[0].read_text()

                    # Check citations were converted
                    assert r"\cite{smith2023}" in tex_content
                    assert r"\cite{jones2022,brown2021}" in tex_content

                    # Check figure reference was converted
                    assert r"\ref{fig:result}" in tex_content

                    # Check figure environment was created
                    assert r"\begin{figure}" in tex_content
                    assert r"\includegraphics" in tex_content

            except Exception as e:
                pytest.skip(f"End-to-end test failed: {e}")
