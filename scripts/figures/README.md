# Figure Generation System

This directory contains the figure generation system for Article-Forge, providing automated creation of publication-quality figures using matplotlib, seaborn, and Mermaid diagrams.

## Overview

The figure generation system supports three main types of visualizations:

1. **Matplotlib**: Publication-quality scientific plots with LaTeX integration
2. **Seaborn**: Statistical visualizations and data analysis plots
3. **Mermaid**: Diagrams for methodology, workflows, and system architecture

## Quick Start

### Install Dependencies

```bash
# Install Python dependencies
make install-deps

# Install Mermaid CLI (for diagram generation)
npm install -g @mermaid-js/mermaid-cli
```

### Generate All Figures

```bash
# Generate all figures
make figures

# Or use the Python script directly
cd scripts/figures
python generate_all.py
```

### Generate Specific Figure Types

```bash
# Generate only matplotlib figures
python generate_all.py --types matplotlib

# Generate only seaborn figures
python generate_all.py --types seaborn

# Generate only Mermaid diagrams
python generate_all.py --types mermaid
```

## File Structure

```
scripts/figures/
├── __init__.py                 # Module initialization
├── config.yml                 # Configuration settings
├── matplotlib_config.py       # Matplotlib LaTeX configuration
├── seaborn_config.py          # Seaborn statistical plots configuration
├── mermaid_generator.py       # Mermaid diagram generation utilities
├── generate_figure1.py        # Matplotlib example figures
├── generate_figure2.py        # Seaborn statistical plots
├── generate_mermaid.py        # Mermaid diagram generation
├── generate_all.py            # Main orchestration script
├── mermaid_templates/         # Mermaid diagram templates
│   ├── methodology_template.mmd
│   ├── architecture_template.mmd
│   └── sequence_template.mmd
└── plot_templates/            # Future: matplotlib/seaborn templates
```

## Configuration

The system uses `config.yml` for centralized configuration:

- **Figure sizes**: Predefined sizes for single/double column layouts
- **Color schemes**: Consistent color palettes across all figures
- **LaTeX integration**: Font settings and mathematical typesetting
- **Output formats**: PDF (primary), PNG (backup), SVG (diagrams)

## LaTeX Integration

### Matplotlib with LaTeX

The system configures matplotlib for optimal LaTeX integration:

```python
from figures.matplotlib_config import create_publication_figure

# Create LaTeX-compatible figure
fig, ax = create_publication_figure(figsize=(6, 4))
# Your plotting code here
save_figure(fig, output_path, formats=('pdf',))
```

### Font Matching

All figures use Computer Modern fonts to match LaTeX documents:
- Font family: serif
- Font serif: Computer Modern
- Mathematical expressions: Rendered with LaTeX

### PGF Backend (Optional)

For maximum LaTeX integration, enable the PGF backend:

```python
configure_matplotlib(use_pgf=True)
```

## Figure Types

### 1. Scientific Plots (Matplotlib)

**Features:**
- Line plots, scatter plots, bar charts
- Mathematical notation support
- Custom color schemes
- Subplot layouts
- Error bars and confidence intervals

**Example:**
```python
from figures.matplotlib_config import create_publication_figure, COLORS

fig, ax = create_publication_figure()
ax.plot(x, y, color=COLORS['primary'], label='Data')
ax.set_xlabel('X Variable')
ax.set_ylabel('Y Variable')
```

### 2. Statistical Plots (Seaborn)

**Features:**
- Correlation heatmaps
- Distribution plots (histograms, KDE, violin plots)
- Regression analysis with confidence intervals
- Group comparisons (box plots, bar plots)
- Multi-panel statistical summaries

**Example:**
```python
from figures.seaborn_config import create_correlation_heatmap

# Generate correlation matrix visualization
create_correlation_heatmap(data, output_path, figsize=(8, 6))
```

### 3. Diagrams (Mermaid)

**Features:**
- Methodology flowcharts
- System architecture diagrams
- Sequence diagrams
- Process workflows
- Class diagrams

**Example:**
```python
from figures.mermaid_generator import create_process_flow

steps = ['Data Collection', 'Processing', 'Analysis', 'Results']
create_process_flow(steps, output_path)
```

## Usage Examples

### Custom Matplotlib Figure

```python
#!/usr/bin/env python3
import numpy as np
from pathlib import Path
from figures.matplotlib_config import create_publication_figure, save_figure

def generate_custom_figure(output_dir: Path):
    # Create data
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.exp(-x/3)
    
    # Create figure
    fig, ax = create_publication_figure(figsize=(6, 4))
    ax.plot(x, y, linewidth=2, label='Exponential decay')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Save figure
    save_figure(fig, output_dir / 'custom_figure', formats=('pdf', 'png'))

if __name__ == '__main__':
    generate_custom_figure(Path('../../src/figures'))
```

### Custom Seaborn Analysis

```python
#!/usr/bin/env python3
import pandas as pd
from pathlib import Path
from figures.seaborn_config import configure_seaborn, create_regression_plot

def generate_analysis(data: pd.DataFrame, output_dir: Path):
    # Configure seaborn
    configure_seaborn(style='whitegrid', palette='publication')
    
    # Create regression analysis
    create_regression_plot(
        data=data,
        x='predictor',
        y='response',
        hue='group',
        output_path=output_dir / 'regression_analysis'
    )
```

### Custom Mermaid Diagram

```python
#!/usr/bin/env python3
from pathlib import Path
from figures.mermaid_generator import MermaidGenerator

def generate_custom_diagram(output_dir: Path):
    generator = MermaidGenerator()
    
    # Define flowchart
    nodes = [
        {'id': 'start', 'label': 'Start', 'shape': 'circle'},
        {'id': 'process', 'label': 'Process Data', 'shape': 'rectangle'},
        {'id': 'decision', 'label': 'Valid?', 'shape': 'diamond'},
        {'id': 'end', 'label': 'End', 'shape': 'circle'}
    ]
    
    edges = [
        ('start', 'process', ''),
        ('process', 'decision', ''),
        ('decision', 'end', 'Yes'),
        ('decision', 'process', 'No')
    ]
    
    generator.create_flowchart(nodes, edges, output_dir / 'workflow.svg')
```

## Integration with LaTeX

Include generated figures in your LaTeX document:

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/Figure1.pdf}
    \caption{Sample data visualization showing exponential decay.}
    \label{fig:figure1}
\end{figure}
```

For Mermaid diagrams (SVG format):

```latex
\begin{figure}[htbp]
    \centering
    \includesvg[width=0.9\textwidth]{figures/methodology_diagram.svg}
    \caption{Research methodology flowchart.}
    \label{fig:methodology}
\end{figure}
```

## Troubleshooting

### Common Issues

1. **LaTeX not found**: Install a LaTeX distribution (TeX Live, MiKTeX)
2. **Mermaid CLI not found**: Install with `npm install -g @mermaid-js/mermaid-cli`
3. **Font warnings**: Ensure Computer Modern fonts are available
4. **Import errors**: Install dependencies with `make install-deps`

### Dependency Check

```bash
# Check all dependencies
python generate_all.py --check-deps

# Example output:
# ✓ matplotlib
# ✓ seaborn
# ✓ numpy
# ✓ pandas
# ✗ mermaid-cli
```

### Debug Mode

For debugging figure generation issues:

```python
# Enable matplotlib debug mode
import matplotlib
matplotlib.verbose.set_level('debug')
```

## Best Practices

1. **Consistent Styling**: Use predefined color schemes and figure sizes
2. **LaTeX Compatibility**: Always test figures in the LaTeX document
3. **Version Control**: Track source scripts, not generated figures
4. **Automation**: Integrate figure generation into the build process
5. **Documentation**: Comment figure generation scripts thoroughly

## Contributing

When adding new figure types:

1. Create a new generation script in `scripts/figures/`
2. Add configuration to `config.yml`
3. Update `generate_all.py` to include the new script
4. Add documentation and examples
5. Test LaTeX integration

## Dependencies

### Python Packages
- matplotlib>=3.7.0 (plotting and LaTeX integration)
- seaborn>=0.12.0 (statistical visualizations)
- numpy>=1.24.0 (numerical computations)
- pandas>=2.0.0 (data manipulation)
- scipy>=1.10.0 (scientific computing)
- Pillow>=9.0.0 (image processing)
- pypdf>=3.0.0 (PDF utilities)

### External Tools
- **Mermaid CLI**: `npm install -g @mermaid-js/mermaid-cli`
- **LaTeX**: TeX Live, MiKTeX, or similar distribution
- **Git**: For version control integration
