#!/usr/bin/env python3
"""
Generate Figure 2: Statistical analysis with seaborn.
This script demonstrates seaborn usage for publication-quality statistical plots.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import os

# Add the scripts directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from figures.seaborn_config import (
    create_statistical_figure,
    create_correlation_heatmap,
    create_distribution_plot,
    create_regression_plot,
    configure_seaborn,
    CUSTOM_PALETTES
)
from figures.matplotlib_config import save_figure, FIGURE_SIZES

def generate_sample_data() -> pd.DataFrame:
    """Generate realistic preprint data for analysis."""
    # Load actual preprint data if available
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / 'build' / 'data'
    
    try:
        # Load the mined preprint data
        growth_data = pd.read_csv(data_dir / 'preprint_growth_data.csv')
        repo_data = pd.read_csv(data_dir / 'repository_stats.csv')
        
        # Create enhanced dataset
        years = growth_data['year'].values
        preprints = growth_data['preprints'].values
        
        # Calculate additional metrics
        growth_rates = [0] + [((preprints[i] - preprints[i-1]) / preprints[i-1]) * 100 
                             for i in range(1, len(preprints))]
        cumulative = np.cumsum(preprints.astype(float))
        log_preprints = np.log10(preprints.astype(float))
        
        # Add COVID period classification
        covid_period = ['Pre-COVID' if y < 2020 else 'COVID Era' if y <= 2021 else 'Post-COVID' 
                       for y in years]
        
        # Create volatility measure (rolling standard deviation of growth rates)
        volatility = []
        for i in range(len(growth_rates)):
            if i < 3:
                volatility.append(0)
            else:
                window = growth_rates[max(0, i-3):i+1]
                volatility.append(np.std(window))
        
        return pd.DataFrame({
            'Year': years,
            'Annual_Preprints': preprints,
            'Growth_Rate': growth_rates,
            'Cumulative': cumulative,
            'Log_Preprints': log_preprints,
            'COVID_Period': covid_period,
            'Volatility': volatility,
            'Year_Index': range(len(years))
        })
        
    except FileNotFoundError:
        print("Warning: Using fallback sample data")
        # Fallback to sample data
        np.random.seed(42)
        n_samples = 200
        
        # Generate correlated variables
        x1 = np.random.normal(0, 1, n_samples)
        x2 = 0.8 * x1 + 0.6 * np.random.normal(0, 1, n_samples)
        x3 = -0.5 * x1 + 0.7 * np.random.normal(0, 1, n_samples)
        
        # Generate categorical variable
        groups = np.random.choice(['Group A', 'Group B', 'Group C'], n_samples)
        
        # Generate target variable with some noise
        y = 2 * x1 + 1.5 * x2 - x3 + np.random.normal(0, 0.5, n_samples)
        
        # Add group effects
        group_effects = {'Group A': 0, 'Group B': 1.5, 'Group C': -1.0}
        y += [group_effects[g] for g in groups]
        
        return pd.DataFrame({
            'Variable_1': x1,
            'Variable_2': x2,
            'Variable_3': x3,
            'Target': y,
            'Group': groups,
            'Treatment': np.random.choice(['Control', 'Treatment'], n_samples),
            'Time_Point': np.random.choice(['T0', 'T1', 'T2'], n_samples)
        })

def generate_figure2_main(data: pd.DataFrame, output_dir: Path) -> None:
    """Generate main Figure 2: Correlation analysis."""
    
    # Check if we have preprint data or sample data
    if 'Year' in data.columns:
        # We have preprint data - select numerical columns for correlation
        numerical_cols = ['Year', 'Annual_Preprints', 'Growth_Rate', 'Log_Preprints', 'Volatility']
        available_cols = [col for col in numerical_cols if col in data.columns]
        correlation_data = data[available_cols]
    else:
        # We have sample data - use original columns
        numerical_cols = ['Variable_1', 'Variable_2', 'Variable_3', 'Target']
        correlation_data = data[numerical_cols]
    
    # Generate correlation heatmap
    output_path = output_dir / 'Figure2'
    create_correlation_heatmap(
        correlation_data, 
        output_path, 
        figsize=FIGURE_SIZES['square'],
        annot=True,
        fmt='.3f',
        cmap='RdBu_r',
        center=0
    )

def generate_figure2_distributions(data: pd.DataFrame, output_dir: Path) -> None:
    """Generate Figure 2B: Distribution analysis."""
    
    configure_seaborn(palette='deep')
    
    # Create figure with multiple distribution plots
    fig, axes = plt.subplots(2, 2, figsize=FIGURE_SIZES['double_column'])
    fig.suptitle('Variable Distributions Analysis', fontsize=12)
    
    import seaborn as sns
    
    if 'Year' in data.columns:
        # We have preprint data
        # Plot 1: Growth rate distribution by COVID period
        if 'COVID_Period' in data.columns:
            sns.boxplot(data=data[data['Growth_Rate'] > 0], x='COVID_Period', y='Growth_Rate', ax=axes[0,0])
            axes[0,0].set_title('Growth Rate by COVID Period')
            axes[0,0].tick_params(axis='x', rotation=45)
        else:
            axes[0,0].plot(data['Year'], data['Growth_Rate'])
            axes[0,0].set_title('Growth Rate Over Time')
        
        # Plot 2: Annual preprints distribution
        axes[0,1].hist(data['Annual_Preprints'], bins=10, alpha=0.7, edgecolor='black')
        axes[0,1].set_title('Distribution of Annual Preprints')
        axes[0,1].set_xlabel('Annual Preprints')
        
        # Plot 3: Log preprints vs year
        axes[1,0].scatter(data['Year'], data['Log_Preprints'], alpha=0.7)
        axes[1,0].set_title('Log Preprints vs Year')
        axes[1,0].set_xlabel('Year')
        axes[1,0].set_ylabel('Log(Preprints)')
        
        # Plot 4: Volatility over time
        if 'Volatility' in data.columns:
            axes[1,1].plot(data['Year'], data['Volatility'], marker='o')
            axes[1,1].set_title('Growth Rate Volatility')
            axes[1,1].set_xlabel('Year')
            axes[1,1].set_ylabel('Volatility')
        else:
            axes[1,1].bar(data['Year'][-5:], data['Annual_Preprints'][-5:])
            axes[1,1].set_title('Recent Preprint Growth')
    else:
        # We have sample data - use original logic
        variables = ['Variable_1', 'Variable_2', 'Variable_3', 'Target']
        
        for i, var in enumerate(variables):
            ax = axes[i//2, i%2]
            sns.violinplot(data=data, x='Group', y=var, ax=ax)
            ax.set_title(f'Distribution of {var}')
            ax.grid(True, alpha=0.3)
    
    for ax in axes.flat:
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    output_path = output_dir / 'Figure2_distributions'
    save_figure(fig, output_path, formats=('pdf',))
    plt.close()

def generate_figure2_regression(data: pd.DataFrame, output_dir: Path) -> None:
    """Generate Figure 2C: Regression analysis."""
    
    configure_seaborn(style='whitegrid', palette='deep')
    
    # Create regression plot
    fig, ax = plt.subplots(figsize=FIGURE_SIZES['single_column'])
    
    import seaborn as sns
    
    if 'Year' in data.columns:
        # We have preprint data - create regression of preprints vs year
        sns.scatterplot(data=data, x='Year', y='Annual_Preprints', 
                       hue='COVID_Period' if 'COVID_Period' in data.columns else None,
                       ax=ax, alpha=0.7, s=50)
        
        # Add regression line
        sns.regplot(data=data, x='Year', y='Annual_Preprints', ax=ax, 
                   scatter=False, color='black', line_kws={'linewidth': 2})
        
        ax.set_xlabel('Year')
        ax.set_ylabel('Annual Preprints')
        ax.set_title('Regression Analysis: Annual Preprints vs Year')
    else:
        # We have sample data - use original logic
        sns.scatterplot(data=data, x='Variable_1', y='Target', hue='Group', 
                       ax=ax, alpha=0.7, s=50)
        
        # Add regression line
        sns.regplot(data=data, x='Variable_1', y='Target', ax=ax, 
                   scatter=False, color='black', line_kws={'linewidth': 2})
        
        ax.set_xlabel('Variable 1')
        ax.set_ylabel('Target Variable')
        ax.set_title('Regression Analysis: Target vs Variable 1')
    
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save figure
    output_path = output_dir / 'Figure2_regression'
    save_figure(fig, output_path, formats=('pdf',))
    plt.close()

def generate_figure2_boxplots(data: pd.DataFrame, output_dir: Path) -> None:
    """Generate Figure 2D: Comparison analysis."""
    
    configure_seaborn(style='whitegrid', palette='colorblind')
    
    # Create comparison plot
    fig, ax = plt.subplots(figsize=FIGURE_SIZES['single_column'])
    
    import seaborn as sns
    
    if 'Year' in data.columns and 'COVID_Period' in data.columns:
        # We have preprint data - create period comparison
        period_data = data[data['Growth_Rate'] > 0]  # Exclude first year with 0 growth
        sns.boxplot(data=period_data, x='COVID_Period', y='Growth_Rate', ax=ax)
        
        ax.set_xlabel('Period')
        ax.set_ylabel('Growth Rate (%)')
        ax.set_title('Growth Rate Comparison by Period')
        ax.tick_params(axis='x', rotation=45)
    else:
        # We have sample data - use original logic  
        sns.boxplot(data=data, x='Treatment', y='Target', hue='Group', ax=ax)
        
        ax.set_xlabel('Treatment Condition')
        ax.set_ylabel('Target Variable')
        ax.set_title('Treatment Effect by Group')
    
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save figure
    output_path = output_dir / 'Figure2_treatment'
    save_figure(fig, output_path, formats=('pdf',))
    plt.close()

def generate_summary_statistics(data: pd.DataFrame, output_dir: Path) -> None:
    """Generate summary statistics table."""
    
    # Calculate summary statistics
    summary_stats = data.describe()
    
    if 'Year' in data.columns:
        # We have preprint data
        if 'COVID_Period' in data.columns:
            # Group statistics by COVID period
            period_stats = data.groupby('COVID_Period').agg({
                'Annual_Preprints': ['mean', 'std', 'min', 'max'],
                'Growth_Rate': ['mean', 'std', 'min', 'max']
            }).round(3)
            period_stats.to_csv(output_dir / 'period_statistics.csv')
        
        # Overall statistics
        overall_stats = data[['Year', 'Annual_Preprints', 'Growth_Rate']].describe()
        overall_stats.to_csv(output_dir / 'overall_statistics.csv')
    else:
        # We have sample data - use original logic
        group_stats = data.groupby('Group').agg({
            'Variable_1': ['mean', 'std'],
            'Variable_2': ['mean', 'std'],
            'Variable_3': ['mean', 'std'],
            'Target': ['mean', 'std']
        }).round(3)
        group_stats.to_csv(output_dir / 'group_statistics.csv')
    
    # Save to CSV for inclusion in LaTeX
    summary_stats.to_csv(output_dir / 'summary_statistics.csv')
    
    print("Summary statistics saved to CSV files")

def main():
    """Main function to generate all Figure 2 variants."""
    # Determine output directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    output_dir = project_root / 'build' / 'figures'
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating sample data...")
    data = generate_sample_data()
    
    print("Generating Figure 2...")
    try:
        generate_figure2_main(data, output_dir)
        generate_figure2_distributions(data, output_dir)
        generate_figure2_regression(data, output_dir)
        generate_figure2_boxplots(data, output_dir)
        generate_summary_statistics(data, output_dir)
        print("Figure 2 and related plots generated successfully!")
    except Exception as e:
        print(f"Error generating Figure 2: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
