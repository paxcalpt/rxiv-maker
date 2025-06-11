# Article Forge: Automated LaTeX Article Building

A modern, automated repository structure for LaTeX article development with GitHub Actions integration, Docker support, automated figure generation, and comprehensive build automation.

## Features

- 🚀 **Automated PDF Building**: GitHub Actions workflows for CI/CD
- 🐳 **Docker Integration**: Consistent builds across environments
- 📊 **Figure Generation**: Automated creation of publication-quality figures
- 📁 **Organized Structure**: Clean separation of source, build, and output files
- 🔄 **Live Reloading**: Watch mode for development
- 📦 **Release Automation**: Automatic PDF releases with Git tags
- 🧹 **Smart Cleanup**: Comprehensive build artifact management
- 🎨 **LaTeX Integration**: Seamless font matching and mathematical typesetting

## New: Figure Generation System

Article-Forge now includes a comprehensive figure generation system supporting:

- **Matplotlib**: Publication-quality scientific plots with LaTeX integration
- **Seaborn**: Statistical visualizations and data analysis plots  
- **Mermaid**: Diagrams for methodology, workflows, and system architecture

All figures are automatically generated with:
- LaTeX-compatible fonts (Computer Modern)
- Consistent color schemes and styling
- PDF output for crisp vector graphics
- Mathematical notation support

## Repository Structure

```
article-forge/
├── .github/workflows/     # GitHub Actions workflows
├── src/                   # Source files
│   ├── tex/              # LaTeX source files
│   ├── bibliography/     # Bibliography files
│   ├── figures/          # Images and figures
│   └── data/             # Raw data files
├── scripts/              # Build and utility scripts
│   └── figures/          # Figure generation system
│       ├── matplotlib_config.py    # Matplotlib LaTeX integration
│       ├── seaborn_config.py       # Statistical plot configuration
│       ├── mermaid_generator.py    # Diagram generation utilities
│       ├── generate_figure1.py     # Example matplotlib figures
│       ├── generate_figure2.py     # Example seaborn plots
│       ├── generate_mermaid.py     # Example diagrams
│       ├── generate_all.py         # Main generation script
│       └── mermaid_templates/      # Diagram templates
├── build/                # Build artifacts (auto-generated)
├── Makefile              # Advanced build configuration
├── Dockerfile            # Docker build environment
└── docker-compose.yml    # Docker development environment
```

## Quick Start

### Prerequisites

Choose one of the following options:

**Option 1: Local LaTeX Installation**
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Python 3.8+ with pip
- Make utility
- (Optional) Node.js and npm for Mermaid diagrams
- (Optional) fswatch (macOS) or inotify-tools (Linux) for watch mode

**Option 2: Docker (Recommended)**
- Docker
- Docker Compose (optional)

### Figure Generation Setup

**Install Python Dependencies:**
```bash
make install-deps
# or manually: pip install -r requirements.txt
```

**Install Mermaid CLI (for diagrams):**
```bash
npm install -g @mermaid-js/mermaid-cli
```

**Test Figure Generation:**
```bash
make check-deps          # Check dependencies
python scripts/figures/test_figures.py  # Run tests
```

### Building Your Article

**With Figure Generation (Recommended):**
```bash
make all          # Build PDF with automatic figure generation
make figures      # Generate figures only
make clean        # Clean build artifacts and generated figures
```

**Using Make (Traditional):**
```bash
make all          # Build the PDF
make clean        # Clean build artifacts
make help         # Show all available targets
```

**Using Scripts:**
```bash
./scripts/build.sh    # Build (auto-detects Docker/local)
./scripts/clean.sh    # Clean build artifacts
```

**Using Docker:**
```bash
make docker-build     # Build with Docker
docker-compose up     # Development environment
```

### Development Workflow

1. **Edit your content** in `src/tex/main.tex` and section files
2. **Add references** to `src/bibliography/references.bib`
3. **Include figures** in `src/figures/`
4. **Build and preview**:
   ```bash
   make all
   open build/output/main.pdf  # macOS
   ```

### Watch Mode for Live Development

```bash
make watch  # Requires inotify-tools
```

## File Organization

### LaTeX Source (`src/tex/`)
- `main.tex` - Main document file
- `sections/` - Individual section files
  - `abstract.tex` - Article abstract
  - `introduction.tex` - Introduction section
  - `supplementary.tex` - Supplementary material
- `style/` - Custom style files and document classes

### Bibliography (`src/bibliography/`)
- `references.bib` - BibTeX bibliography file

### Figures (`src/figures/`)
- Main figures (PNG, PDF, JPG)
- Generated figures from Python scripts
- `supplementary/` - Supplementary figures

## Figure Generation System

Article-Forge includes a sophisticated figure generation system that creates publication-quality figures with LaTeX integration.

### Quick Figure Generation

```bash
# Generate all figures
make figures

# Generate specific types
cd scripts/figures
python generate_all.py --types matplotlib seaborn
python generate_all.py --types mermaid
```

### Supported Figure Types

**1. Scientific Plots (Matplotlib)**
- Line plots, scatter plots, bar charts with LaTeX fonts
- Mathematical notation and equations
- Custom color schemes for consistency
- Example: `scripts/figures/generate_figure1.py`

**2. Statistical Analysis (Seaborn)**
- Correlation heatmaps and distribution plots
- Regression analysis with confidence intervals
- Group comparisons and multi-panel layouts
- Example: `scripts/figures/generate_figure2.py`

**3. Diagrams (Mermaid)**
- Methodology flowcharts and process diagrams
- System architecture and sequence diagrams
- Automatically converted to LaTeX-compatible formats
- Example: `scripts/figures/generate_mermaid.py`

### Creating Custom Figures

**Matplotlib Example:**
```python
from figures.matplotlib_config import create_publication_figure, save_figure

fig, ax = create_publication_figure(figsize=(6, 4))
ax.plot(x, y, label='Data')
ax.set_xlabel('X Variable')
ax.set_ylabel('Y Variable')
save_figure(fig, Path('Figure1'), formats=('pdf',))
```

**Seaborn Example:**
```python
from figures.seaborn_config import create_correlation_heatmap

create_correlation_heatmap(data, output_path, figsize=(8, 6))
```

**Mermaid Example:**
```python
from figures.mermaid_generator import create_process_flow

steps = ['Data Collection', 'Processing', 'Analysis']
create_process_flow(steps, output_path)
```

### LaTeX Integration

All generated figures use:
- Computer Modern fonts to match LaTeX documents
- Consistent sizing for single/double column layouts
- PDF output for crisp vector graphics
- Mathematical notation support

Include in LaTeX:
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/Figure1.pdf}
    \caption{Generated figure with LaTeX integration.}
    \label{fig:figure1}
\end{figure}
```

For detailed documentation, see [`scripts/figures/README.md`](scripts/figures/README.md).

### Build Output (`build/`)
- `output/` - Final PDF files
- `aux/` - LaTeX auxiliary files
- `logs/` - Build logs

## GitHub Actions Integration

This repository includes automated workflows:

### Build Workflow (`.github/workflows/build-pdf.yml`)
- Triggers on push to `main`/`develop` branches and pull requests
- Builds PDF using both native LaTeX and Docker
- Uploads PDF artifacts for download

### Release Workflow (`.github/workflows/release.yml`)
- Triggers on version tags (`v*`)
- Automatically creates GitHub releases with compiled PDFs
- Includes build metadata in release notes

### Creating a Release

```bash
git tag v1.0.0
git push origin v1.0.0
```

The release workflow will automatically build and attach the PDF to the GitHub release.

## Docker Usage

### Building with Docker

```bash
# Build once
make docker-build

# Development environment with live reload
docker-compose up
```

### Custom Docker Commands

```bash
# Run specific commands in container
docker run --rm -v "$(pwd):/workspace" -w /workspace texlive/texlive:latest make all

# Interactive shell in container
docker run --rm -it -v "$(pwd):/workspace" -w /workspace texlive/texlive:latest bash
```

## Advanced Usage

### Custom Style Files

Place your custom LaTeX class files (`.cls`) and bibliography styles (`.bst`) in `src/tex/style/`:

```latex
% In main.tex
\documentclass{style/your-custom-style}
\bibliographystyle{style/your-bib-style}
```

### Multiple Documents

To build multiple documents, modify the `PROJECT` variable in the Makefile:

```makefile
PROJECT = article-name
```

### Adding New Sections

1. Create a new `.tex` file in `src/tex/sections/`
2. Include it in `main.tex`:
   ```latex
   \input{sections/your-new-section}
   ```

## Troubleshooting

### Common Issues

**Build Fails with Missing Packages:**
- Use Docker for consistent package availability
- Or install missing packages in your local LaTeX distribution

**Permission Errors:**
```bash
chmod +x scripts/*.sh
```

**Docker Issues:**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild containers
docker-compose build --no-cache
```

### Getting Help

Run `make help` to see all available build targets and their descriptions.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the build locally
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on modern LaTeX best practices
- Inspired by academic publishing workflows
- Docker integration for reproducible builds
- GitHub Actions for automated CI/CD
