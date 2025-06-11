#!/usr/bin/env python3
"""
Generate Figure 1: Preprint Growth Over Time.
This script creates a contextual visualization of preprint repository growth.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import FuncFormatter
from pathlib import Path
import sys

# Add the figures directory to the path to enable imports
figures_dir = Path(__file__).parent.parent
sys.path.insert(0, str(figures_dir))

# Import after path setup for local modules
from utils.matplotlib_config import (  # noqa: E402
    save_figure, 
    COLORS, 
    FIGURE_SIZES
)

def generate_figure1(output_dir: Path) -> None:
    """Generate Figure 1: Preprint Growth Analysis."""
    
    # Load the preprint data
    project_root = Path(__file__).parent.parent.parent.parent
    data_dir = project_root / 'build' / 'data'
    
    try:
        # Load the mined preprint data
        growth_data = pd.read_csv(data_dir / 'preprint_growth_data.csv')
        repo_data = pd.read_csv(data_dir / 'repository_stats.csv')
        print(f"Loaded data: {len(growth_data)} years, {len(repo_data)} repositories")
    except FileNotFoundError:
        print("Warning: Preprint data not found, generating sample data")
        # Fallback to sample data
        years = list(range(2010, 2025))
        preprints = [5000, 7000, 10000, 15000, 25000, 40000, 60000, 85000, 
                    120000, 160000, 250000, 320000, 380000, 420000, 450000]
        growth_data = pd.DataFrame({'year': years, 'preprints': preprints})
        
        # Create sample repo data
        repo_data = pd.DataFrame({
            'repository': ['arXiv', 'bioRxiv', 'medRxiv', 'ChemRxiv'],
            'total_papers': [2100000, 180000, 50000, 15000],
            'category': ['General Science', 'Life Sciences', 'Life Sciences', 'Other Sciences']
        })
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZES['double_column'])
    
    # Plot 1: Annual preprint submissions
    years = growth_data['year'].values
    preprints = growth_data['preprints'].values
    
    # Convert to int arrays to avoid type issues
    years = np.array(years, dtype=int)
    preprints = np.array(preprints, dtype=int)
    
    # Identify COVID period for highlighting
    covid_mask = (years >= 2020) & (years <= 2021)
    pre_covid_mask = years < 2020
    post_covid_mask = years > 2021
    
    # Plot different periods with different colors
    if np.any(pre_covid_mask):
        ax1.plot(years[pre_covid_mask], preprints[pre_covid_mask], 
                 color=COLORS['primary'], linewidth=2.5, label='Pre-COVID (2010-2019)')
    
    if np.any(covid_mask):
        ax1.plot(years[covid_mask], preprints[covid_mask], 
                 color=COLORS['accent'], linewidth=3, label='COVID Era (2020-2021)', 
                 marker='o', markersize=4)
    
    if np.any(post_covid_mask):
        ax1.plot(years[post_covid_mask], preprints[post_covid_mask], 
                 color=COLORS['secondary'], linewidth=2.5, label='Post-COVID (2022+)')
    
    # Highlight COVID peak if data exists
    if 2020 in years:
        peak_idx = np.where(years == 2020)[0][0]
        ax1.annotate('COVID-19 Surge', 
                    xy=(2020, preprints[peak_idx]), 
                    xytext=(2018, preprints[peak_idx] + 100000),
                    arrowprops=dict(arrowstyle='->', color=COLORS['accent'], lw=1.5),
                    fontsize=8, ha='center')
    
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Annual Preprint Submissions')
    ax1.set_title('Growth of Preprint Repositories')
    ax1.legend(loc='upper left', fontsize=8)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(2010, 2024)
    
    # Format y-axis with thousands separator
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))
    
    # Plot 2: Repository comparison
    repo_names = repo_data['repository'].values
    repo_totals = repo_data['total_papers'].values
    categories = repo_data['category'].values
    
    # Create color map for categories
    unique_cats = list(set(categories))
    cat_colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent']][:len(unique_cats)]
    color_map = dict(zip(unique_cats, cat_colors))
    colors = [color_map[cat] for cat in categories]
    
    bars = ax2.barh(repo_names, repo_totals, color=colors, alpha=0.8)
    
    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, repo_totals)):
        ax2.text(value + max(repo_totals)*0.01, bar.get_y() + bar.get_height()/2, 
                f'{value/1000:.0f}K' if value >= 1000 else str(value),
                va='center', fontsize=7)
    
    ax2.set_xlabel('Total Papers (thousands)')
    ax2.set_title('Major Preprint Repositories')
    ax2.grid(True, alpha=0.3, axis='x')
    
    # Create legend for categories
    legend_elements = [patches.Rectangle((0,0),1,1, facecolor=color_map[cat], alpha=0.8) 
                      for cat in unique_cats]
    ax2.legend(legend_elements, unique_cats, loc='lower right', fontsize=8)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figure
    output_path = output_dir / 'Figure1'
    save_figure(fig, output_path, formats=('pdf', 'png'))
    plt.close()


def generate_subplot_example(output_dir: Path) -> None:
    """Generate a subplot example for supplementary materials."""
    
    # Create data
    x = np.linspace(0, 2*np.pi, 100)
    
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=FIGURE_SIZES['double_column'])
    
    # Plot 1: Sine wave
    ax1.plot(x, np.sin(x), color=COLORS['primary'])
    ax1.set_title('Sine Wave')
    ax1.set_xlabel('x')
    ax1.set_ylabel('sin(x)')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Cosine wave
    ax2.plot(x, np.cos(x), color=COLORS['secondary'])
    ax2.set_title('Cosine Wave')
    ax2.set_xlabel('x')
    ax2.set_ylabel('cos(x)')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Scatter plot
    np.random.seed(42)
    x_scatter = np.random.randn(50)
    y_scatter = 2 * x_scatter + np.random.randn(50)
    ax3.scatter(x_scatter, y_scatter, color=COLORS['accent'], alpha=0.6)
    ax3.set_title('Scatter Plot')
    ax3.set_xlabel('X values')
    ax3.set_ylabel('Y values')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Histogram
    data = np.random.normal(0, 1, 1000)
    ax4.hist(data, bins=30, color=COLORS['primary'], alpha=0.7)
    ax4.set_title('Normal Distribution')
    ax4.set_xlabel('Value')
    ax4.set_ylabel('Frequency')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    output_path = output_dir / 'Figure1_subplots'
    save_figure(fig, output_path, formats=('pdf', 'png'))
    plt.close()


def main():
    """Main function to generate all Figure 1 variants."""
    # Determine output directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    output_dir = project_root / 'build' / 'figures'
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating Figure 1...")
    try:
        generate_figure1(output_dir)
        generate_subplot_example(output_dir)
        print("Figure 1 generated successfully!")
    except Exception as e:
        print(f"Error generating Figure 1: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
