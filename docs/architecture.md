# RXiv-Maker Architecture Overview

This document provides a high-level overview of the architecture and design of RXiv-Maker.

## Table of Contents
- [System Overview](#system-overview)
- [Key Components](#key-components)
- [Data Flow](#data-flow)
- [Build Process](#build-process)
- [Extensibility](#extensibility)
- [Directory Structure](#directory-structure)

## System Overview
RXiv-Maker is an automated scientific article generation system that converts Markdown manuscripts into publication-ready PDFs, with reproducible figures and professional typesetting.

## Key Components
- **Markdown Processor**: Converts Markdown to LaTeX
- **Figure Processor**: Executes Python/Mermaid scripts to generate figures
- **LaTeX Engine**: Compiles LaTeX to PDF
- **Configuration Loader**: Reads YAML config for manuscript metadata
- **Bibliography Manager**: Handles citations and references
- **CLI/Makefile**: Orchestrates the build process

## Data Flow
1. **User edits manuscript** in Markdown and YAML config
2. **Figures generated** from Python/Mermaid scripts
3. **Markdown converted** to LaTeX
4. **LaTeX compiled** to PDF
5. **Output** is placed in the `output/` directory

## Build Process
- `make pdf` runs the full pipeline:
  - Installs dependencies (if needed)
  - Generates figures
  - Converts Markdown to LaTeX
  - Compiles LaTeX to PDF
  - Copies all assets to output

## Extensibility
- Add new processors in `src/py/processors/`
- Add new commands in `src/py/commands/`
- Customize templates in `src/tex/style/`
- Extend API docs in `docs/api/`

## Directory Structure
```
rxiv-maker/
├── MANUSCRIPT/                 # Manuscript content
├── src/                        # Source code
│   ├── py/                     # Python modules
│   └── tex/                    # LaTeX templates
├── output/                     # Generated files
├── docs/                       # Documentation
├── Makefile                    # Build automation
└── pyproject.toml              # Project config
```

For more details, see the [Developer Guide](api/README.md).
