#!/usr/bin/env python3
"""
Figure 2: ArXiv Preprints Over Time
Publication-ready plot showing the growth of arXiv submissions from 1991 to 2025.
Data source: https://arxiv.org/stats/monthly_submissions
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from pathlib import Path

# Set up publication-quality plotting parameters
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'axes.linewidth': 0.8,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'xtick.major.size': 4,
    'xtick.minor.size': 2,
    'ytick.major.size': 4,
    'ytick.minor.size': 2,
    'legend.frameon': False,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1
})

def load_and_process_data():
    """Load and process the arXiv submission data."""
    # Define the path to the data file
    data_path = Path(__file__).parent / "DATA" / "Figure_2" / "arxiv_monthly_submissions.csv"
    
    # Load the data
    df = pd.read_csv(data_path)
    
    # Convert month column to datetime
    df['date'] = pd.to_datetime(df['month'], format='%Y-%m')
    
    # Sort by date to ensure proper chronological order
    df = df.sort_values('date').reset_index(drop=True)
    
    return df

def create_figure():
    """Create the publication-ready figure."""
    # Load data
    df = load_and_process_data()
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the data
    ax.plot(df['date'], df['submissions'], 
            linewidth=1.5, 
            color='#2E86AB',  # Professional blue color
            alpha=0.8)
    
    # Fill area under the curve for visual appeal
    ax.fill_between(df['date'], df['submissions'], 
                    alpha=0.3, 
                    color='#2E86AB')
    
    # Customize axes
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Monthly Submissions', fontsize=12, fontweight='bold')
    ax.set_title('Growth of arXiv Preprint Submissions (1991-2025)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Format x-axis
    ax.xaxis.set_major_locator(mdates.YearLocator(5))  # Every 5 years
    ax.xaxis.set_minor_locator(mdates.YearLocator(1))  # Every year
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    # Format y-axis with thousands separator
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    
    # Set y-axis to start from 0
    ax.set_ylim(bottom=0)
    
    # Add grid for better readability
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)
    
    # Rotate x-axis labels for better readability
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Add some statistics as text annotations
    total_submissions = int(df['submissions'].sum())
    
    # Find peak values
    peak_row = df.loc[df['submissions'].idxmax()]
    peak_submissions = int(peak_row['submissions'])
    peak_date_str = str(peak_row['month'])
    peak_date = pd.to_datetime(peak_date_str)
    
    # Add annotation for peak - simplified to avoid type issues
    ax.text(0.7, 0.8, 
            f'Peak: {peak_submissions:,} submissions\n({peak_date.strftime("%b %Y")})',
            transform=ax.transAxes,
            ha='left', va='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))
    
    # Add total submissions text
    ax.text(0.02, 0.98, f'Total submissions: {total_submissions:,}',
            transform=ax.transAxes,
            ha='left', va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8),
            fontsize=9)
    
    # Tight layout
    plt.tight_layout()
    
    return fig, ax

def save_figure(fig, output_path=None):
    """Save the figure in multiple formats."""
    if output_path is None:
        output_path = Path(__file__).parent
    else:
        output_path = Path(output_path)
    
    # Save as PNG (high resolution)
    fig.savefig(output_path / 'Figure_2.png', 
                dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    # Save as PDF (vector format for publications)
    fig.savefig(output_path / 'Figure_2.pdf', 
                bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    # Print save locations relative to script directory
    script_dir = Path(__file__).parent
    print("Figure saved to:")
    print(f"  - {script_dir / 'Figure_2.png'}")
    print(f"  - {script_dir / 'Figure_2.pdf'}")

def main():
    """Main function to create and save the figure."""
    try:
        fig, ax = create_figure()
        save_figure(fig)
        plt.show()
        
    except FileNotFoundError as e:
        print(f"Error: Could not find data file. {e}")
        print("Please ensure arxiv_monthly_submissions.csv is in the DATA/Figure_2/ directory.")
    except Exception as e:
        print(f"Error creating figure: {e}")
        raise

if __name__ == "__main__":
    main()