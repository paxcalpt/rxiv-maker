"""
Seaborn configuration for LaTeX-compatible statistical visualizations.
This module extends matplotlib_config for publication-quality statistical plots.
"""

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

from .matplotlib_config import configure_matplotlib, save_figure, COLORS

# Seaborn-specific LaTeX configuration
SEABORN_CONFIG = {
    'axes.spines.left': True,
    'axes.spines.bottom': True,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'xtick.bottom': True,
    'xtick.top': False,
    'ytick.left': True,
    'ytick.right': False,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'axes.axisbelow': True,
}

def configure_seaborn(style: str = 'whitegrid', 
                     palette: str = 'deep',
                     use_pgf: bool = False,
                     custom_config: Optional[Dict[str, Any]] = None) -> None:
    """
    Configure seaborn with LaTeX-compatible settings.
    
    Args:
        style: Seaborn style preset
        palette: Color palette name or custom palette
        use_pgf: Use PGF backend for LaTeX integration
        custom_config: Additional configuration parameters
    """
    # First configure matplotlib
    configure_matplotlib(use_pgf=use_pgf)
    
    # Apply seaborn settings
    if palette in CUSTOM_PALETTES:
        sns.set_theme(style=style, palette=CUSTOM_PALETTES[palette])
    else:
        sns.set_theme(style=style, palette=palette)
    
    # Update with seaborn-specific config
    config = SEABORN_CONFIG.copy()
    if custom_config:
        config.update(custom_config)
    
    plt.rcParams.update(config)

def create_statistical_figure(data: Optional[pd.DataFrame] = None,
                            figsize: Tuple[float, float] = (8, 6),
                            style: str = 'whitegrid',
                            palette: str = 'deep') -> Tuple[plt.Figure, plt.Axes]:
    """
    Create a figure optimized for statistical visualizations.
    
    Args:
        data: Optional DataFrame for context
        figsize: Figure size in inches
        style: Seaborn style
        palette: Color palette
    
    Returns:
        Figure and axes objects
    """
    configure_seaborn(style=style, palette=palette)
    
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax

def create_correlation_heatmap(data: pd.DataFrame,
                             output_path: Path,
                             figsize: Tuple[float, float] = (8, 6),
                             **kwargs) -> None:
    """
    Create a publication-ready correlation heatmap.
    
    Args:
        data: DataFrame with numerical columns
        output_path: Output file path
        figsize: Figure size
        **kwargs: Additional arguments for heatmap
    """
    configure_seaborn()
    
    # Calculate correlation matrix
    corr_matrix = data.corr()
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Default heatmap settings
    heatmap_kwargs = {
        'annot': True,
        'cmap': 'RdBu_r',
        'center': 0,
        'square': True,
        'fmt': '.2f',
        'cbar_kws': {'shrink': 0.8},
    }
    heatmap_kwargs.update(kwargs)
    
    # Create heatmap
    sns.heatmap(corr_matrix, ax=ax, **heatmap_kwargs)
    
    plt.title('Correlation Matrix')
    plt.tight_layout()
    
    save_figure(fig, output_path)
    plt.close()

def create_distribution_plot(data: pd.DataFrame,
                           column: str,
                           output_path: Path,
                           kind: str = 'hist',
                           figsize: Tuple[float, float] = (6, 4),
                           **kwargs) -> None:
    """
    Create distribution plots with LaTeX formatting.
    
    Args:
        data: DataFrame containing the data
        column: Column name to plot
        output_path: Output file path
        kind: Type of plot ('hist', 'kde', 'box', 'violin')
        figsize: Figure size
        **kwargs: Additional plot arguments
    """
    configure_seaborn()
    
    fig, ax = plt.subplots(figsize=figsize)
    
    if kind == 'hist':
        sns.histplot(data=data, x=column, ax=ax, **kwargs)
    elif kind == 'kde':
        sns.kdeplot(data=data, x=column, ax=ax, **kwargs)
    elif kind == 'box':
        sns.boxplot(data=data, y=column, ax=ax, **kwargs)
    elif kind == 'violin':
        sns.violinplot(data=data, y=column, ax=ax, **kwargs)
    else:
        raise ValueError(f"Unsupported plot kind: {kind}")
    
    plt.title(f'Distribution of {column}')
    plt.tight_layout()
    
    save_figure(fig, output_path)
    plt.close()

def create_regression_plot(data: pd.DataFrame,
                         x: str,
                         y: str,
                         output_path: Path,
                         hue: Optional[str] = None,
                         figsize: Tuple[float, float] = (6, 4),
                         **kwargs) -> None:
    """
    Create regression plots with confidence intervals.
    
    Args:
        data: DataFrame containing the data
        x: X-axis variable
        y: Y-axis variable
        output_path: Output file path
        hue: Grouping variable
        figsize: Figure size
        **kwargs: Additional plot arguments
    """
    configure_seaborn()
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Default regression plot settings
    regplot_kwargs = {
        'scatter_kws': {'alpha': 0.6},
        'line_kws': {'linewidth': 1.5},
    }
    regplot_kwargs.update(kwargs)
    
    if hue is not None:
        sns.scatterplot(data=data, x=x, y=y, hue=hue, ax=ax, alpha=0.6)
        # Add regression lines for each group
        for group in data[hue].unique():
            group_data = data[data[hue] == group]
            sns.regplot(data=group_data, x=x, y=y, ax=ax, 
                       scatter=False, **regplot_kwargs['line_kws'])
    else:
        sns.regplot(data=data, x=x, y=y, ax=ax, **regplot_kwargs)
    
    plt.title(f'{y} vs {x}')
    plt.tight_layout()
    
    save_figure(fig, output_path)
    plt.close()

# Predefined color palettes for consistency
CUSTOM_PALETTES = {
    'publication': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
    'grayscale': ['#000000', '#404040', '#808080', '#b0b0b0', '#d0d0d0'],
    'scientific': ['#0173b2', '#de8f05', '#029e73', '#cc78bc', '#ca9161'],
    'colorblind': ['#0072B2', '#E69F00', '#009E73', '#F0E442', '#CC79A7'],
}
