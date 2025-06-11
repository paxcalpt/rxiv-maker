# Article Forge: Automated LaTeX Article Building

A modern, automated repository structure for LaTeX article development with GitHub Actions integration, Docker support, and comprehensive build automation.

## Features

- 🚀 **Automated PDF Building**: GitHub Actions workflows for CI/CD
- 🐳 **Docker Integration**: Consistent builds across environments
- 📁 **Organized Structure**: Clean separation of source, build, and output files
- 🔄 **Live Reloading**: Watch mode for development
- 📦 **Release Automation**: Automatic PDF releases with Git tags
- 🧹 **Smart Cleanup**: Comprehensive build artifact management

## Repository Structure

```
article-forge/
├── .github/workflows/     # GitHub Actions workflows
├── src/                   # Source files
│   ├── tex/              # LaTeX source files
│   ├── bibliography/     # Bibliography files
│   ├── figures/          # Images and figures
│   └── data/             # Raw data files
├── build/                # Build artifacts (auto-generated)
├── scripts/              # Build and utility scripts
├── Makefile              # Advanced build configuration
├── Dockerfile            # Docker build environment
└── docker-compose.yml    # Docker development environment
```

## Quick Start

### Prerequisites

Choose one of the following options:

**Option 1: Local LaTeX Installation**
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Make utility
- (Optional) inotify-tools for watch mode

**Option 2: Docker (Recommended)**
- Docker
- Docker Compose (optional)

### Building Your Article

**Using Make (Recommended):**
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
- `supplementary/` - Supplementary figures

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
