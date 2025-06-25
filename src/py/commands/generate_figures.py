#!/usr/bin/env python3
"""Figure Generation Script for Rxiv-Maker.

This script automatically processes figure files in the FIGURES directory and generates
publication-ready output files. It supports:
- .mmd files: Mermaid diagrams (generates SVG/PNG/PDF)
- .py files: Python scripts for matplotlib/seaborn figures

Usage:
    python generate_figures.py [--output-dir OUTPUT_DIR] [--format FORMAT]
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import tomllib


class FigureGenerator:
    """Main class for generating figures from various source formats."""

    def __init__(
        self, figures_dir="FIGURES", output_dir="FIGURES", output_format="png"
    ):
        """Initialize the figure generator.

        Args:
            figures_dir: Directory containing source figure files
            output_dir: Directory for generated output files
            output_format: Default output format for figures
        """
        self.figures_dir = Path(figures_dir)
        self.output_dir = Path(output_dir)
        self.output_format = output_format.lower()
        self.supported_formats = ["png", "svg", "pdf", "eps"]

        if self.output_format not in self.supported_formats:
            raise ValueError(
                f"Unsupported format: {self.output_format}. "
                f"Supported: {self.supported_formats}"
            )

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_all_figures(self):
        """Generate all figures found in the figures directory."""
        if not self.figures_dir.exists():
            print(
                f"Warning: Figures directory '{self.figures_dir}' does not exist"
            )
            return

        print(f"Scanning for figures in: {self.figures_dir}")
        print(f"Output directory: {self.output_dir}")
        print(f"Output format: {self.output_format}")
        print("-" * 50)

        # Find all figure files
        mermaid_files = list(self.figures_dir.glob("*.mmd"))
        python_files = list(self.figures_dir.glob("*.py"))

        if not mermaid_files and not python_files:
            print("No figure files found (.mmd or .py)")
            return

        # Process Mermaid files
        if mermaid_files:
            print(f"Found {len(mermaid_files)} Mermaid file(s):")
            for mmd_file in mermaid_files:
                print(f"  - {mmd_file.name}")
                self.generate_mermaid_figure(mmd_file)

        # Process Python files
        if python_files:
            print(f"\nFound {len(python_files)} Python file(s):")
            for py_file in python_files:
                print(f"  - {py_file.name}")
                self.generate_python_figure(py_file)

        print("\nFigure generation completed!")

    def generate_mermaid_figure(self, mmd_file):
        """Generate figure from Mermaid diagram file."""
        temp_config_path = None
        try:
            # Check if mmdc (Mermaid CLI) is available
            if not self._check_mermaid_cli():
                print(
                    f"  ⚠️  Skipping {mmd_file.name}: Mermaid CLI not available"
                )
                print(
                    "     Install with: npm install -g @mermaid-js/mermaid-cli"
                )
                return

            # Create subdirectory for this figure
            figure_dir = self.output_dir / mmd_file.stem
            figure_dir.mkdir(parents=True, exist_ok=True)

            # Always generate SVG, PNG, and PDF for Mermaid diagrams
            formats_to_generate = ["svg", "png", "pdf"]

            # Add the requested format if it's not already included
            if self.output_format not in formats_to_generate:
                formats_to_generate.append(self.output_format)

            generated_files = []

            for format_type in formats_to_generate:
                output_file = figure_dir / f"{mmd_file.stem}.{format_type}"

                # Generate the figure using Mermaid CLI
                cmd = ["mmdc", "-i", str(mmd_file), "-o", str(output_file)]

                # Add format-specific options
                if format_type == "pdf":
                    # Create temporary config file from pyproject.toml
                    temp_config_path = self._create_temp_mermaid_config()
                    cmd.extend(
                        [
                            "--backgroundColor",
                            "transparent",
                            "--configFile",
                            temp_config_path,
                        ]
                    )
                elif format_type == "png":
                    cmd.extend(["--width", "1200", "--height", "800"])
                # No extra options needed for svg

                print(
                    f"  🎨 Generating {figure_dir.name}/{output_file.name}..."
                )
                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    success_msg = f"Successfully generated {figure_dir.name}/"
                    success_msg += f"{output_file.name}"
                    print(f"  ✅ {success_msg}")
                    generated_files.append(
                        f"{figure_dir.name}/{output_file.name}"
                    )
                else:
                    print(
                        f"  ❌ Error generating {format_type} for {mmd_file.name}:"
                    )
                    print(f"     {result.stderr}")

            if generated_files:
                print(
                    f"     Total files generated: {', '.join(generated_files)}"
                )

        except Exception as e:
            print(f"  ❌ Error processing {mmd_file.name}: {e}")
        finally:
            # Clean up temporary config file
            if temp_config_path and Path(temp_config_path).exists():
                Path(temp_config_path).unlink()

    def generate_python_figure(self, py_file):
        """Generate figure from Python script."""
        try:
            # Create subdirectory for this figure
            figure_dir = self.output_dir / py_file.stem
            figure_dir.mkdir(parents=True, exist_ok=True)

            print(f"  🐍 Executing {py_file.name}...")

            # Execute the Python script in the figure-specific subdirectory
            result = subprocess.run(
                [sys.executable, str(py_file.absolute())],
                capture_output=True,
                text=True,
                cwd=str(figure_dir.absolute()),
            )

            if result.stdout:
                # Print any output from the script (like success messages)
                for line in result.stdout.strip().split("\n"):
                    if line.strip():
                        print(f"     {line}")

            if result.returncode != 0:
                print(f"  ❌ Error executing {py_file.name}:")
                if result.stderr:
                    print(f"     {result.stderr}")
                return

            # Check for generated files by scanning the figure subdirectory
            current_files = set()
            for ext in ["png", "pdf", "svg", "eps"]:
                current_files.update(figure_dir.glob(f"*.{ext}"))

            # Look for files that might have been created by this script
            base_name = py_file.stem
            potential_files = []
            for file_path in current_files:
                # Check if filename contains the base name or is a common figure pattern
                if (
                    base_name.lower() in file_path.stem.lower()
                    or file_path.stem.lower().startswith("figure")
                    or file_path.stem.lower().startswith("fig")
                ):
                    potential_files.append(file_path)

            if potential_files:
                print("  ✅ Generated figures:")
                for gen_file in sorted(potential_files):
                    print(f"     - {figure_dir.name}/{gen_file.name}")
            else:
                print(f"  ⚠️  No output files detected for {py_file.name}")

        except Exception as e:
            print(f"  ❌ Error executing {py_file.name}: {e}")

    def _check_mermaid_cli(self):
        """Check if Mermaid CLI (mmdc) is available."""
        try:
            subprocess.run(
                ["mmdc", "--version"], capture_output=True, check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _import_matplotlib(self):
        """Safely import matplotlib."""
        try:
            import matplotlib

            # Use non-interactive backend for headless operation
            matplotlib.use("Agg")
            return matplotlib
        except ImportError:
            print("  ⚠️  matplotlib not available for Python figures")
            return None

    def _import_seaborn(self):
        """Safely import seaborn."""
        try:
            import seaborn as sns

            return sns
        except ImportError:
            print("  ⚠️  seaborn not available")
            return None

    def _import_numpy(self):
        """Safely import numpy."""
        try:
            import numpy as np

            return np
        except ImportError:
            print("  ⚠️  numpy not available")
            return None

    def _import_pandas(self):
        """Safely import pandas."""
        try:
            import pandas as pd

            return pd
        except ImportError:
            print("  ⚠️  pandas not available")
            return None

    def _load_mermaid_config_from_pyproject(self):
        """Load Mermaid configuration from pyproject.toml."""
        try:
            # Find pyproject.toml in the project root
            project_root = Path(__file__).parent.parent.parent.parent
            pyproject_path = project_root / "pyproject.toml"

            if not pyproject_path.exists():
                return None

            with open(pyproject_path, "rb") as f:
                config = tomllib.load(f)

            # Extract mermaid configuration
            mermaid_config = config.get("tool", {}).get("mermaid", {})

            if not mermaid_config:
                return None

            # Convert to mermaid-cli format
            cli_config = {
                "theme": mermaid_config.get("theme", "base"),
                "themeVariables": mermaid_config.get("themeVariables", {}),
                "layout": "elk",
                "flowchart": {"useMaxWidth": True, "htmlLabels": True},
                "sequence": {"useMaxWidth": True, "wrap": True},
                "gantt": {"useMaxWidth": True},
            }

            return cli_config

        except Exception as e:
            print(
                f"  ⚠️  Could not load mermaid config from pyproject.toml: {e}"
            )
            return None

    def _create_temp_mermaid_config(self):
        """Create a temporary mermaid config file from pyproject.toml settings."""
        config = self._load_mermaid_config_from_pyproject()

        if config is None:
            # Fallback to default config
            config = {
                "theme": "base",
                "themeVariables": {
                    "fontFamily": "Arial, Helvetica, sans-serif",
                    "fontSize": "16px",
                    "primaryColor": "#ffffff",
                    "primaryTextColor": "#333333",
                    "primaryBorderColor": "#cccccc",
                    "lineColor": "#666666",
                    "background": "#ffffff",
                },
                "layout": "elk",
                "flowchart": {"useMaxWidth": True, "htmlLabels": True},
                "sequence": {"useMaxWidth": True, "wrap": True},
                "gantt": {"useMaxWidth": True},
            }

        # Create temporary config file using context manager
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as temp_file:
            json.dump(config, temp_file, indent=2)
            return temp_file.name


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description="Generate figures from .mmd and .py files in FIGURES directory"
    )
    parser.add_argument(
        "--figures-dir",
        "-d",
        default="FIGURES",
        help="Directory containing figure source files (default: FIGURES)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="FIGURES",
        help="Output directory for generated figures (default: FIGURES)",
    )
    parser.add_argument(
        "--format",
        "-f",
        default="png",
        choices=["png", "svg", "pdf", "eps"],
        help="Output format for figures (default: png)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    try:
        generator = FigureGenerator(
            figures_dir=args.figures_dir,
            output_dir=args.output_dir,
            output_format=args.format,
        )
        generator.generate_all_figures()

    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
