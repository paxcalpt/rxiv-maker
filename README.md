<div align="center">

<img src="src/logo/logo-rxiv-maker.svg" alt="RXiv-Maker Logo" width="200" height="200">

# 🔬 RXiv-Maker

<p align="center">
  <strong>Transform scientific writing from chaos to clarity.</strong><br>
  <em>An automated LaTeX article generation system that converts Markdown manuscripts into publication-ready PDFs with reproducible figures, professional typesetting, and zero LaTeX hassle.</em>
</p>

<p align="center">
  <a href="https://github.com/henriqueslab/rxiv-maker/actions/workflows/build-pdf.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/henriqueslab/rxiv-maker/build-pdf.yml?branch=main&label=PDF%20Build" alt="GitHub Actions PDF Build">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.9%2B-blue" alt="Python 3.9+">
  </a>
  <a href="https://hub.docker.com/r/henriqueslab/rxiv-maker">
    <img src="https://img.shields.io/docker/pulls/henriqueslab/rxiv-maker" alt="Docker Pulls">
  </a>
  <a href="https://github.com/henriqueslab/rxiv-maker/stargazers">
    <img src="https://img.shields.io/github/stars/henriqueslab/rxiv-maker?style=social" alt="GitHub stars">
  </a>
</p>

</div>

---

<div align="center">

## 🎯 **Why RXiv-Maker?**

<table>
<tr>
<td align="center" width="25%">
<img src="src/logo/logo-rxiv-maker.svg" width="80" height="80"><br>
<strong>📝 Easy Writing</strong><br>
<em>Write in Markdown</em><br>
No LaTeX knowledge required
</td>
<td align="center" width="25%">
🎯<br>
<strong>🎨 Beautiful Output</strong><br>
<em>Professional LaTeX</em><br>
Publication-ready formatting
</td>
<td align="center" width="25%">
📊<br>
<strong>📊 Smart Figures</strong><br>
<em>Code generates plots</em><br>
Always up-to-date visuals
</td>
<td align="center" width="25%">
🔄<br>
<strong>🔄 Reproducible</strong><br>
<em>Version controlled</em><br>
Science you can trust
</td>
</tr>
</table>

</div>

Scientific publishing shouldn't require a PhD in LaTeX. RXiv-Maker bridges the gap between **easy writing** (Markdown) and **beautiful output** (LaTeX), while adding superpowers:

- ✅ **Write in Markdown** → Get professional LaTeX output
- ✅ **Code generates figures** → Always up-to-date visuals  
- ✅ **One command builds everything** → From draft to publication
- ✅ **GitHub Actions automation** → Auto-generates PDFs on every commit
- ✅ **Version control friendly** → Git tracks everything
- ✅ **Reproducible science** → Code, data, and figures in sync

## 🚀 **Quick Start (2 minutes)**

<div align="center">

### Choose Your Installation Method 🎮

</div>

### 📋 **Installation Options**

RXiv-Maker can be installed in two ways, each with different advantages:

<table>
<tr>
<td width="50%" align="center">

#### 🍴 **Option A: Fork (Recommended)**
**Best for contributing and staying updated**

```bash
# 1. Click "Fork" on GitHub to create your copy
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/rxiv-maker.git
cd rxiv-maker

# 3. Add upstream for updates
git remote add upstream https://github.com/henriqueslab/rxiv-maker.git
```

**✅ Benefits:**
- Easy to contribute back improvements
- Get updates: `git pull upstream main`
- Your modifications stay separate
- GitHub tracks your contributions

</td>
<td width="50%" align="center">

#### 📥 **Option B: Direct Clone**
**Best for one-time usage**

```bash
# 1. Clone directly from main repository
git clone https://github.com/henriqueslab/rxiv-maker.git
cd rxiv-maker
```

**✅ Benefits:**
- Simple one-step setup
- No GitHub account needed
- Immediate access to latest version

</td>
</tr>
</table>

### 🛠️ **Setup Methods**

<table>
<tr>
<td width="50%">

#### 🖥️ **Local Installation**

Perfect for power users who want full control

```bash
# After cloning (fork or direct):

# 1. Set up Docker environment (easiest approach)
make setup

# 2. Try the example first
MANUSCRIPT_PATH=EXAMPLE_MANUSCRIPT make pdf

# 3. Create your own manuscript
cp -r MANUSCRIPT MY_ARTICLE
# Edit MY_ARTICLE/00_CONFIG.yml and 01_MAIN.md
MANUSCRIPT_PATH=MY_ARTICLE make pdf
```

**Platform-specific guides:**
- 📖 [Local Development Setup](docs/platforms/LOCAL_DEVELOPMENT.md)

</td>
<td width="50%">

#### 🐳 **Docker (Zero Setup!)**

Perfect for beginners or anyone who wants to avoid installing LaTeX

```bash
# After cloning (fork or direct):

# 2. Try the example first
docker run --rm -v $(pwd):/app -w /app \
  -e MANUSCRIPT_PATH=EXAMPLE_MANUSCRIPT \
  henriqueslab/rxiv-maker:latest make pdf

# 3. Create your own manuscript
cp -r MANUSCRIPT MY_ARTICLE
# Edit MY_ARTICLE/00_CONFIG.yml and 01_MAIN.md
docker run --rm -v $(pwd):/app -w /app \
  -e MANUSCRIPT_PATH=MY_ARTICLE \
  henriqueslab/rxiv-maker:latest make pdf
```

**Multi-architecture support:**
- 📖 [Docker Hub Instructions](docs/platforms/DOCKER_HUB.md)
- 🌐 [Cloud Platform Deployment](docs/platforms/CLOUD_PLATFORMS.md)

#### ☁️ **Option 3: Google Colab**

Perfect for quick experiments

<div align="center">

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/henriqueslab/rxiv-maker/blob/main/rxiv_forge_colab.ipynb)

**Click the badge above to run RXiv-Maker in your browser!**

</div>


</td>
</tr>
</table>

---

<div align="center">

## 🎬 **Live Demo: See the Magic** ✨

</div>

<table>
<tr>
<td align="center" width="33%">
<h4>📝 Input: Markdown</h4>
<pre align="left">
```markdown
# Abstract
This paper introduces...

![Analysis](Figure_1.py){#fig:analysis}

See @fig:analysis for results.
```
</pre>
</td>
<td align="center" width="33%">
<h4>⚙️ Processing</h4>
<pre align="left">
```bash
$ make pdf
✓ Converting Markdown
✓ Generating figures
✓ Building LaTeX
✓ Creating PDF
```
</pre>
</td>
<td align="center" width="33%">
<h4>📄 Output: Professional PDF</h4>
📄<br><em>Beautiful<br>PDF Output</em>
</td>
</tr>
</table>

---

## 📋 **See It In Action**

RXiv-Maker generates **this very repository's sample article** that demonstrates all features:

<div align="center">

| 📥 **Input (Markdown/Code)** | 📤 **Output (PDF)** | ✨ **Magic** |
|:----------------------------:|:-------------------:|:------------:|
| `EXAMPLE_MANUSCRIPT/00_MANUSCRIPT.md` | Professional PDF | Auto-translation of Markdown to LaTeX |
| `EXAMPLE_MANUSCRIPT/FIGURES/Figure_1.mmd` | Mermaid diagrams | Coded figures auto-generated |
| `EXAMPLE_MANUSCRIPT/FIGURES/Figure_2.py` | Interactive plots | Python scripts → Beautiful visuals |
| `EXAMPLE_MANUSCRIPT/02_REFERENCES.bib` | Perfect citations | IEEE/Nature/Custom styles |

</div>

<div align="center">

**🤯 Live Example**: The generated PDF in this repo shows RXiv-Maker building a scientific article about itself!

[📥 **Download Sample PDF**](2025__saraiva_et_al__rxiv.pdf) | [📝 **View Source Markdown**](EXAMPLE_MANUSCRIPT/00_MANUSCRIPT.md)

</div>

---

## 🏗️ **Architecture Overview**

```mermaid
graph TD
    A[📝 Markdown Article] --> E[🔄 RXiv-Maker Engine]
    B[📊 Python Scripts] --> E
    C[📚 Bibliography] --> E
    D[⚙️ YAML Metadata] --> E
    
    E --> F[📄 LaTeX Document]
    E --> G[🖼️ Generated Figures]
    E --> H[📖 PDF Output]
    
    E -.-> I[🐳 Docker Build]
    E -.-> J[🤖 GitHub Actions]
    E -.-> K[☁️ Google Colab]
```

---

## 💡 **Core Features**

<div align="center">

### 🎯 **Feature Highlights**

</div>

<table>
<tr>
<td width="33%" align="center">

#### 🔄 **Automated Workflow**
⚡

- **One-command builds**: `make pdf` generates your document
- **Figure generation**: Python/Mermaid scripts are processed automatically
- **LaTeX integration**: Converts Markdown to LaTeX and compiles to PDF
- **Clear feedback**: See build progress and any errors

</td>
<td width="33%" align="center">

#### 📝 **Enhanced Markdown**
📝

Extended academic syntax with:
- Figure references: `@fig:plot`
- Smart citations: `[@cite1;@cite2]`
- Code execution: `![Plot](script.py)`
- Cross-references: Auto-numbered

</td>
<td width="33%" align="center">

#### 📊 **Programmatic Figures**
📊

- **Python scripts** → Publication plots
- **Mermaid diagrams** → Vector graphics
- **Multiple formats** → PDF + PNG output
- **Figure integration** → Automatically included in the document

</td>
</tr>
</table>

### 📝 **Enhanced Markdown Syntax**
```markdown
# Extended Academic Markdown

## Figures with references
![Figure caption](FIGURES/my_plot.py){#fig:plot width="0.8"}
See @fig:plot for details.

## Smart citations  
Multiple citations [@cite1;@cite2] or single @cite3

## Code and file references
Analysis script: `FIGURES/analysis.py`
Data file: `DATA/results.csv`
```

### 📊 **Programmatic Figure Generation**
```python
# FIGURES/Figure_2.py - Auto-executed during build
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('FIGURES/DATA/Figure_2/arxiv_monthly_submissions.csv')
plt.plot(data['year'], data['submissions'])
plt.savefig('output/Figures/Figure_2.pdf')  # LaTeX version
plt.savefig('output/Figures/Figure_2.png')  # Markdown preview
```

### 🎨 **Professional Templates**
- **Jacquemet and Henriques style**: Clean, modern scientific papers
- **Citation styles**: IEEE, Nature, APA, custom
- **Two-column layouts**: Journal-ready formatting
- **Figure positioning**: Automatic float placement

---

## 📂 **Project Structure**

<div align="center">

### 🏗️ **Clean & Organized File Layout**

</div>

<table>
<tr>
<td width="50%">

#### 📝 **Content Files** (What you edit)
```
📁 MANUSCRIPT/                # Your manuscript content
├── 📝 00_MANUSCRIPT.md       # Main manuscript (Markdown)
├── 📚 02_REFERENCES.bib      # Bibliography (BibTeX)
├── 📄 01_SUPPLEMENTARY_INFO.md # Optional supplements
└── 🖼️  FIGURES/               # Figure generation
    ├── Figure_1.png         # Static images
    ├── Figure_2.py          # Python scripts
    ├── diagram.mmd          # Mermaid diagrams
    └── DATA/                # Data files

📁 EXAMPLE_MANUSCRIPT/        # Example to learn from
├── 📝 00_MANUSCRIPT.md       # Complete example
├── 📚 02_REFERENCES.bib      # Sample references
└── 🖼️  FIGURES/               # Example figures

🔧 .env                       # Configuration file
```

</td>
<td width="50%">

#### ⚙️ **System Files** (Auto-managed)
```
📁 src/                       # RXiv-Maker engine
├── py/                      # Python processors
├── tex/                     # LaTeX templates
└── docker/                  # Docker setup

📁 output/                    # Generated files
├── ARTICLE.tex              # Generated LaTeX
├── ARTICLE.pdf              # Final PDF ✨
└── Figures/                 # Processed figures

🛠️ Makefile                   # Build automation
🐳 docker.sh                  # Docker wrapper
```

</td>
</tr>
</table>

<div align="center">

**🎯 Simple Rule**: Edit files in `MANUSCRIPT/`, get magic in `output/`!

</div>

---

## 📖 **Getting Started Guide**

### 🎯 **For New Users**

1. **Fork the repository** to your GitHub account
2. **Clone your fork** locally
3. **Build the example** to see how it works:
   ```bash
   # Set environment to use example
   MANUSCRIPT_PATH=EXAMPLE_MANUSCRIPT make pdf
   # Or with Docker
   docker run --rm -v $(pwd):/app -e MANUSCRIPT_PATH=EXAMPLE_MANUSCRIPT henriqueslab/rxiv-maker make pdf
   ```
4. **Create your manuscript**:
   ```bash
   cp -r MANUSCRIPT MY_PAPER  # Copy template
   # Edit MY_PAPER/00_MANUSCRIPT.md with your content
   MANUSCRIPT_PATH=MY_PAPER make pdf
   ```

### ⚙️ **Configuration**

RXiv-Maker uses a `.env` file for configuration:

```bash
# .env file (automatically created)
MANUSCRIPT_PATH=MANUSCRIPT           # Default manuscript folder
EXAMPLE_MANUSCRIPT_PATH=EXAMPLE_MANUSCRIPT  # Example folder
```

You can override the manuscript path:
- **Environment variable**: `MANUSCRIPT_PATH=MY_PAPER make pdf`
- **Docker**: `docker run -e MANUSCRIPT_PATH=MY_PAPER ...`
- **Edit .env file**: Change `MANUSCRIPT_PATH=MY_PAPER`

### 🔄 **Development Workflow**

1. **Edit your manuscript**: `MANUSCRIPT/00_MANUSCRIPT.md`
2. **Add figures**: Place `.py`, `.mmd`, or image files in `MANUSCRIPT/FIGURES/`
3. **Build and preview**: `make pdf` (or `make dev` for quick preview)
4. **Iterate**: Edit → Build → Preview → Repeat

## 📚 **Documentation**

<div align="center">

### 🎯 **Comprehensive Documentation**

</div>

RXiv-Maker provides extensive documentation including platform guides and API reference:

### 📖 **API Documentation**

For developers working with the rxiv-forge codebase, detailed API documentation is available:

- **[API Reference](docs/api/README.md)** - Complete Python API documentation
- **[Module Documentation](docs/api/)** - Detailed documentation for all modules

The API documentation is automatically generated from the codebase and includes:
- Function signatures and docstrings
- Class definitions and methods
- Module overviews and usage examples
- Cross-references between related components

To generate or update the API documentation, see the documentation generation script in the repository.

### 🎯 **Platform Support**

RXiv-Maker provides detailed documentation for different platforms and deployment scenarios:

<table>
<tr>
<td align="center" width="33%">

### 🖥️ **Local Development**
<img src="https://img.shields.io/badge/Platform-macOS%20|%20Linux%20|%20Windows-blue" alt="Platforms">

**Complete setup guides for:**
- 🍎 macOS (Intel & Apple Silicon)
- 🐧 Linux (x86_64 & ARM64)
- 🪟 Windows (Native & WSL2)

[📖 **Local Development Guide**](docs/platforms/LOCAL_DEVELOPMENT.md)

</td>
<td align="center" width="33%">

### 🐳 **Docker Hub**
<img src="https://img.shields.io/badge/Architecture-amd64%20|%20arm64-green" alt="Architectures">

**Multi-architecture images:**
- Intel/AMD x86_64
- ARM64 (Apple Silicon, AWS Graviton)
- Production & development variants

[📖 **Docker Hub Instructions**](docs/platforms/DOCKER_HUB.md)

</td>
<td align="center" width="33%">

### ☁️ **Cloud Platforms**
<img src="https://img.shields.io/badge/Cloud-AWS%20|%20Azure%20|%20GCP-orange" alt="Cloud Providers">

**Deployment guides for:**
- AWS Fargate, Lambda
- Azure Container Instances
- Google Cloud Run, GKE
- Cost optimization tips

[📖 **Cloud Deployment Guide**](docs/platforms/CLOUD_PLATFORMS.md)

</td>
</tr>
</table>

### 🚀 **Quick Setup**

For immediate usage, we recommend the Docker approach:

```bash
# 1. Get RXiv-Maker (fork recommended for contributions)
git clone https://github.com/YOUR_USERNAME/rxiv-maker.git  # If forked
# OR
git clone https://github.com/henriqueslab/rxiv-maker.git    # Direct clone

cd rxiv-maker

# 2. One-command Docker setup
docker run --rm -v $(pwd):/app -w /app \
  -e MANUSCRIPT_PATH=EXAMPLE_MANUSCRIPT \
  henriqueslab/rxiv-maker:latest make pdf

# 3. View the generated PDF in output/MANUSCRIPT.pdf
```

### 📋 **Prerequisites Summary**

| Method | Requirements | Setup Time |
|--------|-------------|------------|
| **Docker** | Docker Desktop | 2 minutes |
| **Local** | Python 3.8+, LaTeX, Make | 10-30 minutes |
| **Cloud** | Cloud account, Docker | 5-15 minutes |

**Docker Benefits:**
- ✅ **Multi-architecture support** (Intel, ARM64, Apple Silicon)
- ✅ **No local dependencies** required
- ✅ **Consistent results** across platforms
- ✅ **Production-ready** deployment options

---

## 🎯 **Usage Examples**

### Basic Workflow
```bash
# Generate PDF using Docker (no LaTeX needed)
make pdf

# Generate PDF locally (requires LaTeX)
make local

# Set up Docker environment (first time)
make setup

# Clean output directory
make clean

# Show all available commands
make help
```

### Advanced Workflows

#### 📊 **Working with different manuscript directories**
```bash
# Use a different manuscript folder
MANUSCRIPT_PATH=MY_MANUSCRIPT make pdf
# Or with Docker explicitly
docker run --rm -v $(pwd):/app -w /app \
  -e MANUSCRIPT_PATH=MY_MANUSCRIPT \
  henriqueslab/rxiv-maker:latest make pdf
```

#### 🖼️ **Force figure regeneration**
```bash
# Force regeneration of all figures
make pdf FORCE_FIGURES=true
```

---

## ✨ **Advanced Features**

### 🔧 **Customization**

#### YAML Frontmatter Example
```yaml
---
title: "My Amazing Research Paper"
date: 2024-12-13
authors:
  - name: "Dr. Jane Smith"
    affiliation: "University of Science"
    email: "jane.smith@uni.edu"
    orcid: "0000-0000-0000-0000"
keywords: ["machine learning", "biology", "automation"]
bibliography: 02_REFERENCES.bib
---
```

#### Custom LaTeX Styling
```bash
# Add custom style files to src/tex/style/
cp my_custom.sty src/tex/style/
make pdf
```

### 🚀 **Integration Options**

#### GitHub Actions (CI/CD)

**🎉 Fully Automated PDF Generation & Release**

RXiv-Maker includes a robust GitHub Actions workflow that automatically:
- ✅ **Installs LaTeX and Python dependencies** natively (no Docker needed)
- ✅ **Generates PDF on every push** to main branch  
- ✅ **Creates GitHub releases** with downloadable PDFs
- ✅ **Supports manual triggers** with custom manuscript paths
- ✅ **Caches dependencies** for faster builds
- ✅ **Handles figure generation** automatically

```yaml
# .github/workflows/build-pdf.yml - Simplified view
name: Build and Release PDF
on:
  push:
    branches: [ main ]
  workflow_dispatch:
    inputs:
      manuscript_path:
        description: 'Path to manuscript directory'
        required: false
        default: 'MANUSCRIPT'
        type: string

jobs:
  prepare:
    runs-on: ubuntu-latest
    outputs:
      manuscript_path: ${{ steps.set-path.outputs.manuscript_path }}
    steps:
      - uses: actions/checkout@v4
      - name: Set manuscript path
        id: set-path
        run: |
          # Auto-detects manuscript path from .env or uses default
          MANUSCRIPT_PATH="${{ github.event.inputs.manuscript_path || 'EXAMPLE_MANUSCRIPT' }}"
          echo "manuscript_path=$MANUSCRIPT_PATH" >> $GITHUB_OUTPUT

  build-pdf:
    needs: prepare
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # Install LaTeX and Python dependencies directly (much faster than Docker)
      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            texlive-latex-base texlive-latex-recommended texlive-latex-extra \
            texlive-fonts-recommended texlive-fonts-extra texlive-science \
            texlive-bibtex-extra texlive-pictures biber \
            python3 python3-pip make
          pip install pyyaml matplotlib pandas seaborn pypdf python-dotenv
      
      # Generate PDF natively (no Docker required)
      - name: Generate PDF
        run: |
          export MANUSCRIPT_PATH=${{ needs.prepare.outputs.manuscript_path }}
          make _build_pdf
      
      # Create release with PDF
      - name: Create or update release
        uses: softprops/action-gh-release@v1
        with:
          tag_name: latest-pdf
          name: "Latest PDF Build"
          files: release/*.pdf
```

**Key Improvements:**
- 🚀 **5x faster** than Docker approach (no image building)
- 💾 **Uses dependency caching** for even faster subsequent builds
- 🔧 **Native execution** eliminates architecture compatibility issues
- 📦 **Automatic releases** with timestamped PDFs
- 🎯 **Manual workflow dispatch** for testing different manuscripts

#### Pre-commit Hooks
```bash
# Setup automatic formatting
pip install pre-commit
pre-commit install
```

### 🐳 **Docker Workflow**

RXiv-Maker provides Docker support for running without local LaTeX installation:

```bash
# Generate PDF with Docker
docker run --rm -v $(pwd):/app -w /app \
  -e MANUSCRIPT_PATH=EXAMPLE_MANUSCRIPT \
  henriqueslab/rxiv-maker:latest make pdf

# Or use the convenience wrapper in the Makefile
make pdf
```

**Docker Benefits:**
- ✅ **Consistent environment** across different platforms
- ✅ **No LaTeX installation needed** on your local machine
- ✅ **Multi-architecture support** (x86_64 and ARM64)
- ✅ **Reproducible builds** across different systems

Docker configuration is available in the `src/docker` directory.

---

## 🐛 **Troubleshooting**

### Common Issues

#### ❌ **"LaTeX Error: File not found"**
```bash
# Solution: Use Docker to avoid LaTeX installation issues
make pdf
```

#### ❌ **"Python import error"** 
```bash
# Solution: Install Python dependencies
pip install -r requirements.txt
```

#### ❌ **"Figure generation failed"**
```bash
# Solution: Check Python scripts and data files
# Check: FIGURES/ directory structure and data files
```

### Debug Mode
```bash
# Verbose output for debugging
make pdf VERBOSE=true

# Check intermediate files
ls -la output/
cat output/ARTICLE.log  # LaTeX compilation log
```

### Getting Help
```bash
# Show available make commands
make help
```

---

## 🤝 **Contributing**

We love contributions! Here's how to help:

### Quick Contributions
- 🐛 **Report bugs**: [Open an issue](https://github.com/henriqueslab/rxiv-maker/issues)
- 💡 **Suggest features**: [Start a discussion](https://github.com/henriqueslab/rxiv-maker/discussions)
- 📖 **Improve docs**: Edit this README or add examples

### Development Setup
```bash
# Fork and clone your fork
git clone https://github.com/YOUR_USERNAME/rxiv-maker.git
cd rxiv-maker

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Areas We Need Help With
- 🎨 **New LaTeX templates** (journal-specific styles)
- 🔌 **Integration plugins** (Overleaf, Notion, etc.)
- 🌍 **Internationalization** (support for non-English papers)
- 📱 **Web interface** (browser-based editor)

---

## 📄 **License**

MIT License - see [LICENSE](LICENSE) for details.

**TL;DR**: Use it, modify it, share it, make money with it. Just don't blame us if it breaks! 😉

---

## 🙏 **Acknowledgments**

- **Jacquemet and Henriques Labs** for the beautiful LaTeX style templates
- **matplotlib/seaborn** communities for amazing Python plotting
- **LaTeX Project** for the typesetting engine that makes everything beautiful
- **Mermaid** for diagram generation that doesn't make you cry

---

## 🔗 **Related Projects**

- **[Pandoc](https://pandoc.org/)**: Universal document converter
- **[Jupyter Book](https://jupyterbook.org/)**: Build books with Jupyter notebooks  
- **[MyST](https://myst-parser.readthedocs.io/)**: Markedly Structured Text
- **[Quarto](https://quarto.org/)**: Scientific publishing system
- **[Overleaf](https://www.overleaf.com/)**: Collaborative LaTeX editor

---

<div align="center">

---

## 🌟 **Join the RXiv-Maker Community!** 🌟

<img src="src/logo/logo-rxiv-maker.svg" alt="RXiv-Maker Logo" width="100" height="100">

### 💫 **Star us on GitHub if RXiv-Maker helps your research!** 💫

<p>
  <a href="https://github.com/henriqueslab/rxiv-maker">
    <img src="https://img.shields.io/github/stars/henriqueslab/rxiv-maker?style=for-the-badge&logo=github&logoColor=white&labelColor=black&color=yellow" alt="GitHub Stars">
  </a>
  <a href="https://github.com/henriqueslab/rxiv-maker/fork">
    <img src="https://img.shields.io/github/forks/henriqueslab/rxiv-maker?style=for-the-badge&logo=github&logoColor=white&labelColor=black&color=blue" alt="GitHub Forks">
  </a>
</p>

<table>
<tr>
<td align="center" width="33%">
<a href="https://github.com/henriqueslab/rxiv-maker">
⭐<br>
<strong>⭐ Give us a star</strong><br>
<em>Show your support!</em>
</a>
</td>
<td align="center" width="33%">
<a href="https://github.com/henriqueslab/rxiv-maker/issues">
🐛<br>
<strong>🐛 Report issues</strong><br>
<em>Help us improve!</em>
</a>
</td>
<td align="center" width="33%">
<a href="https://github.com/henriqueslab/rxiv-maker/discussions">
💬<br>
<strong>💬 Join discussions</strong><br>
<em>Share your ideas!</em>
</a>
</td>
</tr>
</table>


---

<h3>💝 Made with ❤️ by scientists, for scientists</h3>

<em>"Because science is hard enough without fighting with LaTeX."</em>

<p>
  <strong>🔬 Transforming scientific publishing, one paper at a time.</strong>
</p>

---

**© 2025 Jacquemet and Henriques Labs | RXiv-Forge**  
Licensed under MIT License | Built with passion for open science
