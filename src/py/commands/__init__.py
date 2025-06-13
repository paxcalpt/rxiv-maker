"""
Command-line interface modules for RXiv-Forge.

This package contains the main executable scripts for article and figure generation.
"""

from .generate_article import generate_article, main as article_main
from .generate_figures import FigureGenerator, main as figures_main

__all__ = ['generate_article', 'article_main', 'FigureGenerator', 'figures_main']
