"""
Figure generation module for Article-Forge.

This module provides utilities for generating publication-quality figures
using matplotlib, seaborn, and Mermaid diagrams for LaTeX documents.
"""

from .matplotlib_config import (
    configure_matplotlib,
    create_publication_figure,
    save_figure,
    get_figure_size,
    COLORS,
    FIGURE_SIZES
)

from .seaborn_config import (
    configure_seaborn,
    create_statistical_figure,
    create_correlation_heatmap,
    create_distribution_plot,
    create_regression_plot,
    CUSTOM_PALETTES
)

from .mermaid_generator import (
    MermaidGenerator,
    create_mermaid_generator,
    create_process_flow,
    create_methodology_diagram,
    DEFAULT_CONFIG
)

__version__ = "1.0.0"
__author__ = "Article-Forge"

__all__ = [
    # Matplotlib utilities
    'configure_matplotlib',
    'create_publication_figure',
    'save_figure',
    'get_figure_size',
    'COLORS',
    'FIGURE_SIZES',
    
    # Seaborn utilities
    'configure_seaborn',
    'create_statistical_figure',
    'create_correlation_heatmap',
    'create_distribution_plot',
    'create_regression_plot',
    'CUSTOM_PALETTES',
    
    # Mermaid utilities
    'MermaidGenerator',
    'create_mermaid_generator',
    'create_process_flow',
    'create_methodology_diagram',
    'DEFAULT_CONFIG',
]
