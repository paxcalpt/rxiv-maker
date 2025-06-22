<!-- Supplementary Tables -->

| **Markdown Element** | **LaTeX Equivalent** | **Description** |
|------------------|------------------|-------------|
| `**bold text**` | `\textbf{bold text}` | Bold formatting for emphasis |
| `*italic text*` | `\textit{italic text}` | Italic formatting for emphasis |
| `# Header 1` | `\section{Header 1}` | Top-level section heading |
| `## Header 2` | `\subsection{Header 2}` | Second-level section heading |
| `### Header 3` | `\subsubsection{Header 3}` | Third-level section heading |
| `@citation` | `\cite{citation}` | Single citation reference |
| `[@cite1;@cite2]` | `\cite{cite1,cite2}` | Multiple citation references |
| `@fig:label` | `\ref{fig:label}` | Figure cross-reference |
| Image with attributes | `\begin{figure}...\end{figure}` | Figure with attributes (old format) |
| Image with caption | `\begin{figure}...\end{figure}` | Figure with separate caption (new format) |
| `- list item` | `\begin{itemize}\item...\end{itemize}` | Unordered list |
| `1. list item` | `\begin{enumerate}\item...\end{enumerate}` | Ordered list |
| `[link text](url)` | `\href{url}{link text}` | Hyperlink with custom text |
| `https://example.com` | `\url{https://example.com}` | Bare URL |
| `<!-- comment -->` | `% comment` | Comments (converted to LaTeX style) |
| Markdown table | `\begin{table}...\end{table}` | Table with automatic formatting |
| `<newpage>` | `\newpage` | Manual page break control |
| `<clearpage>` | `\clearpage` | Page break with float clearing |

{#stable:markdown-syntax rotate=90} **RXiv-Maker Markdown Syntax Overview.** Comprehensive overview of RXiv-Maker's markdown to LaTeX conversion capabilities, demonstrating the automated translation system that enables researchers to write in familiar markdown syntax while producing professional LaTeX output. 
<newpage>

<!-- Supplementary Notes -->

{#snote:file-structure} **File Structure and Organisation.**

<!--TODO: write this section -->
Blablabla

{#snote:figure-generation} **Figure Generation System.**

The figure generation system is implemented in `src/py/commands/generate_figures.py` and provides automated processing of figure source files from the `FIGURES/` directory. The system supports two primary figure types:

**Mermaid Diagrams (.mmd files)**: 
- Processed using the Mermaid CLI (`mmdc`) through the `generate_mermaid_figure()` method
- Automatically generates multiple output formats (SVG, PNG, and optionally PDF/EPS)
- Uses format-specific options:
  - PNG files at 1200×800 resolution
  - SVG files maintain vector format
  - PDF files use transparent backgrounds
- Provides comprehensive error handling and status reporting

**Python-Generated Figures (.py files)**:
- Python scripts are executed in the output directory context through the `generate_python_figure()` method
- System features:
  - Executes Python scripts using `subprocess.run()` with the current Python interpreter
  - Changes the working directory to the output folder before execution
  - Automatically detects generated figure files by scanning for common image formats (PNG, PDF, SVG, EPS)
  - Matches output files to source scripts using filename patterns

The figure generation process includes automatic detection of available dependencies (matplotlib, seaborn, numpy, pandas) and provides fallback behavior when libraries are unavailable.

{#snote:markdown-conversion} **Markdown-to-LaTeX Conversion Architecture.**

The conversion system consists of specialized processors for different content types, implemented across multiple modules:

**Figure Processing** (`src/py/converters/figure_processor.py`): 

The figure conversion system processes three markdown figure syntaxes:
1. New format: `![](path)` followed by `{attributes} **Caption**` on the next line
2. Attributed format: `![caption](path){attributes}`
3. Simple format: `![caption](path)`

The core conversion function `convert_figures_to_latex()` implements a multi-pass approach:
1. **Code protection**: Inline code (backticks) and fenced code blocks are temporarily replaced with placeholders to prevent interference with figure syntax parsing
2. **Format processing**: Each figure format is processed by dedicated functions
3. **Code restoration**: Protected code blocks are restored after figure processing

The `create_latex_figure_environment()` function generates complete LaTeX figure environments with:
- Path conversion (`FIGURES/` → `Figures/` and `.svg` → `.png` for LaTeX compatibility)
- Caption processing (markdown formatting converted to LaTeX equivalents)
- Attribute handling (position, width, and ID attributes are parsed and applied)
- Label generation (figure IDs are automatically converted to LaTeX `\label{}` commands)

The system provides user control over page breaks through `<newpage>` and `<clearpage>` markdown syntax, which are converted to LaTeX `\newpage` and `\clearpage` commands respectively. The `<newpage>` command creates a simple page break, while `<clearpage>` forces a page break and flushes all pending floats (figures/tables). This allows precise control over document layout without automatic page breaks for figures and tables.

**Table Processing** (`src/py/converters/table_processor.py`): 

Table conversion handles GitHub Flavored Markdown tables with additional LaTeX-specific features. The system supports two caption formats:
1. Legacy format: `Table X: Caption` (preceding the table)
2. New format: `**Table X: Caption** {\#table:id}` (following the table)

Caption parsing includes:
- Width detection (`Table*` indicates double-column tables)
- ID extraction (attribute blocks are parsed for table labels)  
- Rotation support (rotation angles can be specified in attribute blocks)

The `_format_table_cell()` function implements context-aware cell formatting with:
- Markdown syntax preservation (special handling for tables containing markdown syntax examples)
- LaTeX escaping (special characters are properly escaped)
- Code formatting (backtick-enclosed content is converted to `\texttt{}` commands)
- Emphasis conversion (`**bold**` and `*italic*` are converted to LaTeX equivalents)

**Reference Processing**: 

Both figures and tables support automatic reference conversion:
- Figure references: `@fig:id` → `\ref{fig:id}`
- Supplementary figure references: `@sfig:id` → `\ref{sfig:id}`  
- Table references: Similar pattern for `@table:id` and `@stable:id`

This reference system is implemented using regex-based substitution.

**Integration Pipeline**:

The figure and table processors are integrated into the main markdown-to-LaTeX conversion pipeline (`src/py/converters/md2tex.py`) through the `convert_markdown_to_latex()` function, which orchestrates:
- Content protection
- Header conversion  
- Figure processing
- Table processing
- Reference resolution
- Content restoration

This architecture ensures robust conversion while maintaining the semantic structure and formatting requirements of academic publications, demonstrating:
- Separation of concerns
- Extensibility
- Robustness through comprehensive error handling
- Testability through modular design

{#snote:comparison} **Comparison with similar systems.**

<!--TODO: this section should compare RXiv-Maker with other systems like Overleaf, Quarto, etc. It should very positively highlight the positive aspects of alternative strategies. Explain that compared to the other approeaches, RXiv-Maker aims for simplicity at the cost of generalization, it aims to do only one this and that one thing very well - the production of high-quality scientific preprints for arXiv, bioRxiv, medRxiv and similar venues... -->


{#snote:auto-translation} **Auto-Translation System Examples.**

The RXiv-Maker auto-translation system processes structured input files to generate professional LaTeX output. The following examples demonstrate the system's capabilities across different file types.

#### YAML Configuration Example (00_CONFIG.yml)

```yaml
title: "RXiv-Maker: An Automated Template Engine for Streamlined Scientific Publications"
short_title: "RXiv-Maker"
authors:
  - name: "Bruno M. Saraiva"
    affiliation: [1, 2]
    email: "bruno.saraiva@example.com"
    orcid: "0000-0000-0000-0000"
  - name: "Guillaume Jaquemet"
    affiliation: [3]
    email: "guillaume.jaquemet@example.com"
    orcid: "0000-0000-0000-0000"
  - name: "Ricardo Henriques"
    affiliation: [1, 2]
    email: "ricardo.henriques@example.com"
    orcid: "0000-0000-0000-0000"
    corresponding: true

affiliations:
  1: "Instituto Gulbenkian de Ciência, Oeiras, Portugal"
  2: "University College London, London, United Kingdom"
  3: "Åbo Akademi University, Turku, Finland"

abstract: "Modern scientific publishing requires..."
keywords: ["scientific publishing", "reproducibility", "automation"]
```

#### Markdown Content Structure (01_MAIN.md)

```markdown
## Abstract
Modern scientific publishing has shifted towards rapid dissemination...

## Main
Scientific publishing has undergone profound transformation...

![Figure caption with cross-reference](FIGURES/Figure_1.svg){#fig:1}

Statistical analysis demonstrates significant improvements [@reference2023].

## Methods
The RXiv-Maker framework orchestrates computational tools...
```

#### BibTeX Reference Format (03_REFERENCES.bib)

```bibtex
@article{Tennant2016_academic_publishing,
  title={The academic, economic and societal impacts of Open Access},
  author={Tennant, Jonathan P and Waldner, Fran{\c{c}}ois and Jacques, Damien C},
  journal={PLoS Biology},
  volume={14},
  number={7},
  pages={e1002510},
  year={2016},
  publisher={Public Library of Science}
}

@article{Fraser2021_preprint_growth,
  title={The relationship between bioRxiv preprints and citations},
  author={Fraser, Nicholas and Momeni, Fakhri and Mayr, Philipp and Peters, Isabella},
  journal={Quantitative Science Studies},
  volume={2},
  number={2},
  pages={618--638},
  year={2021}
}
```

{#snote:technical-implementation} **Technical Implementation Pipeline.**

The system processes these files through a sophisticated conversion pipeline:

1. **Configuration Parsing**: Extracts metadata from YAML configuration file, including author information, affiliations, and document settings
2. **Content Conversion**: Transforms markdown syntax into LaTeX formatting, preserving cross-references, citations, and figure placements
3. **Figure Generation**: Executes Python scripts and processes Mermaid diagrams automatically during compilation
4. **Document Assembly**: Combines all components into a cohesive LaTeX document using the template system
5. **Citation Processing**: Integrates BibTeX references with proper formatting and cross-referencing
6. **Output Compilation**: Produces publication-ready PDF with professional typesetting and formatting

This approach ensures reproducibility, version control compatibility, and automated processing whilst maintaining the flexibility needed for academic publishing. The system automatically handles complex LaTeX formatting requirements, enabling researchers to focus on content creation rather than technical implementation details.


<!-- Supplementary Figures -->

![](FIGURES/SFigure_1.svg)
{#sfig:workflow} **RXiv-Maker Workflow Details.** This figure provides a comprehensive overview of the RXiv-Maker system architecture, showing how the simplified file naming convention (00_CONFIG.yml, 01_MAIN.md, 02_SUPPLEMENTARY_INFO.md, 03_REFERENCES.bib) integrates with the processing engine to generate publication-ready documents. The system demonstrates the complete automation pipeline from markdown input to PDF output.
<newpage>