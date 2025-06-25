#!/usr/bin/env python3
"""Sample Plot: Demonstration of Python figure generation in RXiv-Maker.

Simple example showing how to create publication-ready plots that are
automatically integrated into the manuscript during compilation.
"""

import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Set backend based on command line arguments
if "--show" not in sys.argv:
    matplotlib.use("Agg")  # Use non-interactive backend for headless operation

# Set publication-quality parameters
plt.rcParams.update(
    {
        "font.size": 8,
        "font.family": "sans-serif",
        "axes.linewidth": 0.8,
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        "legend.frameon": False,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,
    }
)


def create_sample_plot():
    """Create a simple demonstration plot."""
    # Generate sample data
    x = np.linspace(0, 2 * np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)

    # Create figure
    fig, ax = plt.subplots(figsize=(4, 3))

    # Plot data
    ax.plot(x, y1, label="sin(x)", linewidth=1.5, color="#2563eb")
    ax.plot(x, y2, label="cos(x)", linewidth=1.5, color="#dc2626", linestyle="--")

    # Customize plot
    ax.set_xlabel("x", fontweight="bold")
    ax.set_ylabel("y", fontweight="bold")
    ax.set_title("Sample Mathematical Functions", fontweight="bold", pad=10)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-1.1, 1.1)

    # Set x-axis ticks to show π multiples
    ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
    ax.set_xticklabels(["0", "π/2", "π", "3π/2", "2π"])

    plt.tight_layout()
    return fig


def save_figure(fig, output_path=None):
    """Save the figure in multiple formats."""
    output_path = Path.cwd() if output_path is None else Path(output_path)

    # Save in multiple formats for compatibility
    formats = {
        "sample_plot.pdf": {"format": "pdf"},
        "sample_plot.png": {"format": "png", "dpi": 300},
        "sample_plot.svg": {"format": "svg"},
    }

    for filename, kwargs in formats.items():
        fig.savefig(
            output_path / filename,
            bbox_inches="tight",
            facecolor="white",
            edgecolor="none",
            **kwargs,
        )

    print("Figure saved as:")
    for filename in formats:
        print(f"  - {output_path / filename}")


def main():
    """Main function."""
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: python sample_plot.py [--show] [--help|-h]")
        print("  --show: Display plot (default is headless mode)")
        print("  --help|-h: Show this help message")
        return

    show_plot = "--show" in sys.argv

    try:
        fig = create_sample_plot()
        save_figure(fig)

        if show_plot:
            plt.show()
        else:
            plt.close(fig)

    except Exception as e:
        print(f"Error creating figure: {e}")
        raise


if __name__ == "__main__":
    main()
