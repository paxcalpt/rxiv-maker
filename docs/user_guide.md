# Rxiv-Maker User Guide

This guide covers everything from getting started to advanced workflows, practical examples, and troubleshooting.

## Table of Contents
- [Getting Started](#getting-started)
- [Advanced Usage](#advanced-usage)
- [Examples & Cookbook](#examples--cookbook)
- [Troubleshooting & Debugging](#troubleshooting--debugging)
- [Where to Get Help](#where-to-get-help)

---

## Getting Started

For platform-specific setup, see [platforms/LOCAL_DEVELOPMENT.md](platforms/LOCAL_DEVELOPMENT.md).

- Install dependencies and LaTeX as described in the platform guide.
- Build your first PDF:
  ```bash
  make setup
  make pdf
  ```
- Use a different manuscript folder:
  ```bash
  MANUSCRIPT_PATH=MY_ARTICLE make pdf
  ```

---

## Advanced Usage

- **Custom Manuscript Paths:**
  ```bash
  MANUSCRIPT_PATH=MY_ARTICLE make pdf
  ```
- **Advanced Figure Generation:**
  - Place Python or Mermaid files in `MANUSCRIPT/FIGURES/`
  - Force regeneration:
    ```bash
    make pdf FORCE_FIGURES=true
    ```
- **Custom LaTeX Templates:**
  - Add `.sty`, `.cls`, or `.tex` files to `src/tex/style/`
  - Reference your custom style in `00_CONFIG.yml`
- **Continuous Integration (CI):**
  - GitHub Actions builds PDFs via manual trigger or git tags
  - See [GitHub Actions Guide](github-actions-guide.md) for step-by-step instructions
  - Customize workflows in `.github/workflows/`
- **Environment Variables:**
  - Use a `.env` file for persistent settings
- **Debugging and Verbose Output:**
  - Use `VERBOSE=true` for detailed logs:
    ```bash
    make pdf VERBOSE=true
    ```
- **Pre-commit Hooks and Linting:**
  - Install hooks: `pre-commit install`
  - Run all checks: `pre-commit run --all-files`

---

## Examples & Cookbook

- **Basic PDF Generation:**
  ```bash
  make pdf
  ```
- **Custom Manuscript Directory:**
  ```bash
  MANUSCRIPT_PATH=MY_PAPER make pdf
  ```
- **Adding Figures:**
  - Place `.py` or `.mmd` files in `MANUSCRIPT/FIGURES/`
  - Reference in Markdown:
    ```markdown
    ![My Plot](FIGURES/my_plot.py){#fig:plot}
    See @fig:plot for details.
    ```
- **Customizing Templates:**
  - Add `.sty` or `.cls` files to `src/tex/style/`
  - Reference in `00_CONFIG.yml`
- **Using Mermaid Diagrams:**
  - Place `.mmd` files in `FIGURES/`
  - Example:
    ```mermaid
    graph TD;
      A-->B;
      B-->C;
    ```
- **Citations and Bibliography:**
  - Add references to `03_REFERENCES.bib`
  - Use `[@cite1;@cite2]` in Markdown
- **CI/CD Automation:**
  - GitHub Actions builds PDFs on manual trigger or tags
  - See [GitHub Actions Guide](github-actions-guide.md) for complete instructions

---

## Troubleshooting & Debugging

- **LaTeX Not Found:**
  - Error: `LaTeX Error: File not found`
  - Solution: Install LaTeX (see [platforms/LOCAL_DEVELOPMENT.md](platforms/LOCAL_DEVELOPMENT.md))
  - Check: Is `pdflatex` in your PATH?
- **Python Import Errors:**
  - Error: `ModuleNotFoundError` or similar
  - Solution: Run `make setup` to install dependencies
  - Check: Is your virtual environment activated?
- **Figure Generation Fails:**
  - Error: Figures not generated or missing in PDF
  - Solution:
    - Check Python scripts in `FIGURES/` for errors
    - Use `make pdf FORCE_FIGURES=true`
    - Check for missing data files
- **Build Fails on GitHub Actions:**
  - Check: Is the manuscript directory path correct?
  - Check: Are all dependencies listed in `pyproject.toml`?
  - Check: Does the manuscript have required files (`00_CONFIG.yml`, `01_MAIN.md`)?
  - Solution: Review workflow logs in Actions tab → Click failed run → Click "build-pdf" job
  - See [GitHub Actions Guide](github-actions-guide.md) for detailed troubleshooting
- **Debugging Tips:**
  - Use `make pdf VERBOSE=true` for more output
  - Check `output/ARTICLE.log` for LaTeX errors
  - Use `pytest` for running tests

---

## Where to Get Help
- [GitHub Issues](https://github.com/henriqueslab/rxiv-maker/issues)
- [Discussions](https://github.com/henriqueslab/rxiv-maker/discussions)
- [Contributing Guide](../CONTRIBUTING.md)
