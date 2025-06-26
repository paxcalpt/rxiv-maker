# Supplementary Information

## Supplementary Tables

| Markdown Element | LaTeX Output | Description |
|------------------|--------------|-------------|
| `**bold text**` | `\textbf{bold text}` | Bold formatting |
| `*italic text*` | `\textit{italic text}` | Italic formatting |
| `@citation` | `\cite{citation}` | Single citation |
| `[@cite1;@cite2]` | `\cite{cite1,cite2}` | Multiple citations |
| `@fig:label` | `\ref{fig:label}` | Figure reference |

{#stable:syntax} **Rxiv-Maker Syntax Examples.** Basic markdown-to-LaTeX conversion examples showing the essential syntax transformations.

| Deployment Method | Environment | Setup Required | Ease of Use |
|-------------------|-------------|----------------|-------------|
| GitHub Actions | Cloud CI/CD | None | Very High |
| Local Python | Local | Python + LaTeX | Medium |

{#stable:deployment-options} **Deployment Options.** Comparison of different ways to use Rxiv-Maker.

| Format | Description | Generation Method | Output |
|---------|-------------|-------------------|---------|
| `.png` | Raster images | Direct file or Python/Mermaid generation | PNG image |
| `.pdf` | Vector graphics | Direct file or Python/Mermaid generation | PDF image |  
| `.jpg/.jpeg` | Photo formats | Direct file | JPEG image |
| `.svg` | Scalable vector | Mermaid generation | SVG converted to PDF |
| `.py` | Python scripts | Automated execution | PNG/PDF outputs |
| `.mmd` | Mermaid diagrams | Mermaid.js processing | SVG/PNG/PDF outputs |
| `.eps` | PostScript graphics | Direct file | EPS image |

{#stable:figure-formats} **Supported Figure Formats.** Complete list of figure formats supported by Rxiv-Maker's automated processing pipeline.

| Tool | Primary Focus | Collaboration Model | Output Formats | Strengths | Limitations |
|------|---------------|-------------------|----------------|-----------|-------------|
| Rxiv-Maker | Reproducible PDFs | Git-based | PDF (LaTeX) | Version control, automation, reproducibility | PDF-only output |
| Quarto | Multi-format publishing | File-based | HTML, PDF, Word, etc. | Versatile output, R/Python integration | Complex setup |
| Overleaf | LaTeX collaboration | Real-time online | PDF (LaTeX) | Easy collaboration, no setup | Proprietary, limited automation |
| Typst | Modern typesetting | File-based | PDF, PNG | Fast compilation, clean syntax | Young ecosystem |
| MyST/Jupyter Book | Computational narratives | File-based | HTML, PDF | Interactive web content | Web-first design |

{#stable:tool-comparison} **Scientific Authoring Tool Comparison.** Feature comparison between Rxiv-Maker and other scientific writing platforms.

## Supplementary Notes

{#snote:examples} **Usage Examples and Best Practices.**

This supplementary note demonstrates the special syntax for creating structured supplementary content. The `{#snote:id}` syntax creates automatically numbered and labeled supplementary notes that can be cross-referenced from the main text.

Key best practices include:
- Use clear, descriptive labels for all figures and tables
- Include comprehensive captions that explain the content
- Cross-reference supplementary materials from the main text
- Organize supplementary content logically

{#snote:advanced-features} **Advanced Rxiv-Maker Features.**

The framework supports several advanced features beyond basic markdown conversion:

**Mathematical notation**: Both inline math $E = mc^2$ and display equations:
$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$

**Code syntax highlighting**: Python, R, and other languages are automatically highlighted when specified:

```python
import pandas as pd
data = pd.read_csv("input.csv")
print(data.head())
```

**Custom LaTeX commands**: Direct LaTeX code can be included when needed for specialized formatting requirements.

{#snote:figure-generation} **Figure Generation Technical Details.**

The Rxiv-Maker figure generation system operates through a multi-stage pipeline that automatically processes different figure types during compilation:

**Python Script Processing**: Python files (`.py`) in the `FIGURES/` directory are executed in isolated environments with common scientific libraries pre-installed (NumPy, Matplotlib, Seaborn, Pandas). Scripts must save outputs as both PNG (for preview) and PDF (for publication quality) formats. The system tracks file modification times to avoid unnecessary regeneration.

**Mermaid Diagram Processing**: Mermaid files (`.mmd`) are processed using Node.js and Mermaid CLI to generate SVG outputs, which are then converted to PDF for LaTeX inclusion. The system supports flowcharts, sequence diagrams, and other Mermaid syntax.

**Dependency Management**: Figure generation uses virtual environments to ensure reproducible builds across different systems. Dependencies are specified in `requirements.txt` and automatically installed during the build process.

**Build Optimization**: The pipeline implements intelligent caching - figures are only regenerated when source files change, significantly reducing compilation time for large documents with many programmatic figures.

## Supplementary Figures

![arXiv submission growth showing exponential increase from 2010-2023](FIGURES/SFigure_1/SFigure_1.png){#sfig:arxiv-growth width="0.8"}

{#sfig:arxiv-growth} **Exponential Growth in arXiv Submissions.** Annual submission counts to arXiv showing the dramatic increase in preprint sharing, particularly accelerating after 2015. This growth illustrates the increasing importance of efficient manuscript preparation tools like Rxiv-Maker. Data compiled from arXiv statistics reports.