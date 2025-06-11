# Style Directory

This directory contains custom LaTeX style files and document classes.

## Supported Files

- `.cls` files - Custom document classes
- `.bst` files - Bibliography styles  
- `.sty` files - Style packages
- Font files and other style assets

## HenriquesLab Style

This template is designed to work with the HenriquesLab style files:
- `HenriquesLab_style.cls` - Document class
- `HenriquesLab_style.bst` - Bibliography style

## Usage

To use custom styles in your document:

```latex
% For document classes
\documentclass{style/your-custom-class}

% For bibliography styles
\bibliographystyle{style/your-bib-style}

% For style packages
\usepackage{style/your-package}
```

## Installation

1. Place your style files in this directory
2. Update the `main.tex` file to reference them
3. Ensure all dependencies are available

## Notes

- The template falls back to standard article class if custom styles are not found
- Test your styles locally before committing
- Include license information for third-party styles
