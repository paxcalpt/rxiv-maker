"""
Matplotlib configuration for LaTeX-compatible figure generation.
This module provides standardized settings for creating publication-quality figures.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, Dict, Any

# LaTeX-compatible configuration
LATEX_CONFIG = {
    'text.usetex': True,
    'font.family': 'serif',
    'font.serif': 'Computer Modern',
    'text.latex.preamble': r'\usepackage{amsmath}\usepackage{amssymb}\usepackage{siunitx}',
    'savefig.format': 'pdf',
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
    'figure.figsize': (6, 4),
    'axes.labelsize': 10,
    'font.size': 10,
    'legend.fontsize': 8,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'axes.linewidth': 0.8,
    'grid.linewidth': 0.6,
}

# PGF backend configuration for maximum LaTeX integration
PGF_CONFIG = {
    'pgf.texsystem': 'pdflatex',
    'pgf.preamble': r'\usepackage{amsmath}\usepackage{amssymb}\usepackage{siunitx}',
    'font.family': 'serif',
    'font.serif': 'Computer Modern',
    'axes.labelsize': 10,
    'font.size': 10,
    'legend.fontsize': 8,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
}

def configure_matplotlib(use_pgf: bool = False, custom_config: Optional[Dict[str, Any]] = None) -> None:
    """
    Configure matplotlib for LaTeX-compatible output.
    
    Args:
        use_pgf: If True, use PGF backend for maximum LaTeX integration
        custom_config: Additional configuration parameters to override defaults
    """
    if use_pgf:
        mpl.use('pgf')
        config = PGF_CONFIG.copy()
    else:
        config = LATEX_CONFIG.copy()
    
    if custom_config:
        config.update(custom_config)
    
    plt.rcParams.update(config)

def get_figure_size(width_pt: float, fraction: float = 1.0, ratio: Optional[float] = None) -> Tuple[float, float]:
    """
    Calculate figure size in inches from LaTeX textwidth.
    
    Args:
        width_pt: Width in points (from LaTeX \the\textwidth)
        fraction: Fraction of textwidth to use
        ratio: Height/width ratio (default: golden ratio)
    
    Returns:
        Figure width and height in inches
    """
    if ratio is None:
        ratio = (5**0.5 - 1) / 2  # Golden ratio
    
    # Convert from pt to inches
    inches_per_pt = 1.0 / 72.27
    
    fig_width = width_pt * inches_per_pt * fraction
    fig_height = fig_width * ratio
    
    return fig_width, fig_height

def create_publication_figure(figsize: Tuple[float, float] = (6, 4), 
                            dpi: int = 300, 
                            use_pgf: bool = False) -> Tuple[mpl.figure.Figure, mpl.axes.Axes]:
    """
    Create a figure with publication-ready settings.
    
    Args:
        figsize: Figure size in inches
        dpi: Resolution for raster elements
        use_pgf: Use PGF backend
    
    Returns:
        Figure and axes objects
    """
    configure_matplotlib(use_pgf=use_pgf)
    
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    return fig, ax

def save_figure(fig: mpl.figure.Figure, 
                output_path: Path, 
                formats: Tuple[str, ...] = ('pdf',),
                **kwargs) -> None:
    """
    Save figure in specified formats with optimized settings.
    
    Args:
        fig: Figure to save
        output_path: Output path (without extension)
        formats: File formats to save
        **kwargs: Additional arguments for savefig
    """
    save_kwargs = {
        'bbox_inches': 'tight',
        'pad_inches': 0.1,
        'dpi': 300,
    }
    save_kwargs.update(kwargs)
    
    for fmt in formats:
        filepath = output_path.with_suffix(f'.{fmt}')
        fig.savefig(filepath, format=fmt, **save_kwargs)
        print(f"Saved figure: {filepath}")

# Color schemes for consistent styling
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'accent': '#2ca02c',
    'error': '#d62728',
    'warning': '#ff8c00',
    'info': '#17a2b8',
    'success': '#28a745',
    'muted': '#6c757d',
}

# Standard figure dimensions for common use cases
FIGURE_SIZES = {
    'single_column': (3.5, 2.6),
    'double_column': (7.0, 5.25),
    'square': (4, 4),
    'wide': (8, 3),
    'tall': (4, 6),
}
