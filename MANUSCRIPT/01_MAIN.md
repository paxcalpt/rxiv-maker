# Rxiv-Maker: A Template Engine for Scientific Publications
<!-- note that this title is not rendered in the PDF, rather the one in the YAML metadata is used -->

## Abstract

This document demonstrates the essential features of Rxiv-Maker, a markdown-based template engine for scientific publications. The system automatically converts markdown content into publication-ready LaTeX documents, supporting citations [@example2023], cross-references to Fig. @fig:workflow, programmatic figure generation, and comprehensive document formatting. This minimal example showcases the core functionality needed for scientific manuscript preparation.

## Main

**Introduction.** Rxiv-Maker transforms scientific writing by enabling authors to focus on content while the system handles formatting and compilation [@modern_publishing2024]. The framework supports multiple deployment strategies and integrates seamlessly with version control systems.

Key features demonstrated in this template include:
- Automatic markdown-to-LaTeX conversion
- Programmatic figure generation (see Fig. @fig:workflow)
- Citation processing with BibTeX integration
- Cross-referencing system for figures and sections
- Supplementary material support (detailed in @snote:examples)

**Methods.** The Rxiv-Maker system processes markdown files through a multi-stage pipeline:

1. **Content parsing**: Markdown files are parsed for special syntax
2. **Figure generation**: Python scripts and Mermaid diagrams are executed
3. **LaTeX conversion**: Content is converted to LaTeX with proper formatting
4. **Document compilation**: Final PDF is generated using LaTeX

Code blocks are preserved during processing:

```python
# Example Python code
import matplotlib.pyplot as plt
import numpy as np

# Generate sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create plot
plt.plot(x, y)
plt.savefig('output.png')
```

![](FIGURES/workflow.svg)
{#fig:workflow tex_position="t"} **Rxiv-Maker Workflow Diagram.** This Mermaid-generated diagram shows the conversion process from markdown input to PDF output, demonstrating automated figure generation capabilities.

**Results.** The system successfully converts markdown syntax into professional LaTeX output. Table @stable:features summarizes the key capabilities:

| Feature | Input | Output |
|:-------|:------|:-------|
| Format | `**bold**` | `\textbf{}` |
| Citations | `[@example2023]` | `\cite{example2023}` |
| Figures | `![](image.png)` | `\includegraphics{}` |

{#stable:features} **Core Rxiv-Maker Features.** Essential functionality for scientific document preparation.

![](FIGURES/sample_plot.png)
{#fig:data width="0.8"} **Sample Data Visualization.** This figure demonstrates Python-generated plots with automatic integration into the document.

**Discussion.** Rxiv-Maker addresses the common challenges in scientific writing by providing:
- **Simplicity**: Authors write in familiar markdown syntax
- **Reproducibility**: Figures are generated programmatically from source data
- **Automation**: Complex LaTeX formatting is handled automatically
- **Flexibility**: Multiple deployment options support different workflows

The template system is designed to be minimal yet comprehensive, showcasing all essential features without overwhelming complexity.

## Data availability

Example data used in this template is included in the `FIGURES/DATA/` directory.

## Code availability

Rxiv-Maker source code is available at the project repository.

## Author contributions

All authors contributed to the design and testing of the Rxiv-Maker system.

## Acknowledgements

We thank the scientific community for feedback on manuscript preparation workflows.