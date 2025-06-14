"""
Command-line interface modules for RXiv-Forge.

This package contains the main executable scripts for article and figure generation.
"""

from .generate_preprint import generate_preprint, main as preprint_main
from .generate_figures import FigureGenerator, main as figures_main

__all__ = ['generate_preprint', 'preprint_main', 'FigureGenerator', 'figures_main']
