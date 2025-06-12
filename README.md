# Article-Forge

**Automated LaTeX Article Generation and Building System**

Article-Forge is a modern, automated publishing pipeline that transforms Markdown manuscripts into publication-ready LaTeX documents and PDFs. It integrates version control, reproducible figure generation, and professional typesetting into a streamlined workflow.

## 🚀 Quick Start

```bash
# Check project status
make status

# Build complete PDF
make pdf

# Preview the result
make preview
```

## 📋 Prerequisites

- **Python 3.7+** - For processing scripts
- **LaTeX** - For PDF compilation
- **macOS/Linux** - Primary support (Windows via Docker)

### Auto-install Dependencies

```bash
# Install everything
make install

# Or install individually
make install-python    # Python dependencies
make install-latex     # LaTeX distribution (macOS)
```

## 🛠️ Main Commands

| Command | Description |
|---------|-------------|
| `make pdf` | **Build complete PDF** (recommended) |
| `make build` | Generate LaTeX only (faster for development) |
| `make preview` | Open generated PDF |
| `make figures` | Generate figures from Python/Mermaid sources |
| `make status` | Show project status and missing dependencies |

## 🔄 Development Workflow

```bash
# Quick development cycle
make dev                # figures + build + preview

# Auto-rebuild on changes (requires fswatch)
make watch

# Check everything is ready
make status
```

## 📁 Project Structure

```
article-forge/
├── 00_ARTICLE.md           # Main manuscript (Markdown)
├── 02_REFERENCES.bib       # Bibliography (BibTeX)
├── FIGURES/                # Figures directory
│   ├── Figure_1.mmd       # Mermaid diagrams
│   ├── Figure_2.py        # Python plots
│   └── DATA/              # Data files
├── src/
│   ├── py/                # Processing scripts
│   └── tex/               # LaTeX templates & styles
└── output/                # Generated files
    └── ARTICLE.pdf        # Final PDF
```

## ✨ Key Features

### 📊 **Automated Figure Generation**
- **Python scripts** - Generate plots with matplotlib, seaborn
- **Mermaid diagrams** - Create flowcharts, diagrams
- **Version controlled** - Figures regenerate from source data
- **Format options** - PNG, PDF output

### 📝 **Markdown to LaTeX Conversion**
- **Enhanced syntax** - Figure references (`@fig:id`), citations (`@author2023`)
- **Metadata support** - YAML frontmatter for authors, affiliations
- **Cross-references** - Automatic figure numbering and referencing
- **Text formatting** - Bold, italic, inline code conversion

### 🔧 **Professional Typesetting**
- **LaTeX templates** - Publication-ready layouts
- **Bibliography** - Automated citation processing
- **Style consistency** - Professional formatting

### 🐳 **Docker Support**
```bash
# Build without local LaTeX installation
make docker-build
```

## 📖 Common Workflows

### Writing a New Article
1. Edit `00_ARTICLE.md` in Markdown
2. Add references to `02_REFERENCES.bib`
3. Create figures in `FIGURES/` (`.py` or `.mmd` files)
4. Build: `make pdf`

### Adding Figures
1. Create `FIGURES/my_figure.py` with matplotlib code
2. Reference in markdown: `![Caption](FIGURES/my_figure.png){#fig:id}`
3. Cite in text: `@fig:id`
4. Regenerate: `make figures`

### Development Cycle
```bash
make dev      # Quick build + preview
make watch    # Auto-rebuild on changes
```

### Continuous Integration
```yaml
# .github/workflows/build.yml
- name: Build Article
  run: make docker-build
```

## 🔧 Configuration

### Makefile Variables
```makefile
OUTPUT_DIR := output          # Output directory
FIGURES_DIR := FIGURES        # Figures source directory
ARTICLE_MD := 00_ARTICLE.md   # Main markdown file
```

### Python Dependencies
Managed via `pyproject.toml` or `requirements.txt`

### LaTeX Styles
Custom styles in `src/tex/style/`

## 🐛 Troubleshooting

### Common Issues

**LaTeX not found**
```bash
make install-latex
# or manually install MacTeX
```

**Figure generation fails**
```bash
make check     # Validate source files
make figures   # Regenerate figures only
```

**PDF compilation errors**
```bash
make build     # LaTeX only (faster debugging)
# Check output/ARTICLE.log for errors
```

**Dependencies missing**
```bash
make status    # Check what's missing
make install   # Install everything
```

### Debug Mode
```bash
# Verbose output
make pdf V=1

# Check individual steps
make build     # LaTeX generation only
make figures   # Figure generation only
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Test with `make check`
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LaTeX Community** - Professional typesetting
- **Python Scientific Stack** - matplotlib, pandas, seaborn
- **Mermaid** - Diagram generation
- **Academic Community** - Reproducible research practices

---

**Quick Reference:**
- 📊 `make pdf` - Build everything
- 🚀 `make dev` - Development workflow  
- 📋 `make status` - Check dependencies
- 🔧 `make help` - Full command list