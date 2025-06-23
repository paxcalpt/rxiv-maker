## Supplementary Tables

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

{#stable:markdown-syntax} **RXiv-Maker Markdown Syntax Overview.** Comprehensive mapping of markdown elements to their LaTeX equivalents, demonstrating the automated translation system that enables researchers to write in familiar markdown syntax whilst producing professional LaTeX output.

| **Deployment Method** | **Environment** | **Dependencies** | **Collaboration** | **Ease of Use** | **Reproducibility** |
|-------------------|-------------|-------------|--------------|-------------|----------------|
| **Docker Local** | Local machine | Docker only | Git-based | High | Perfect |
| **GitHub Actions** | Cloud CI/CD | None (cloud) | Automatic | Very High | Perfect |
| **Google Colab** | Web browser | None (cloud) | Shared notebooks | Very High | High |
| **Local Python** | Local machine | Python + LaTeX | Git-based | Medium | Good |
| **Manual LaTeX** | Local machine | Full LaTeX suite | Git-based | Low | Variable |

{#stable:deployment-options} **RXiv-Maker Deployment Strategies.** Comparison of available compilation methods, highlighting the flexibility of the framework in accommodating different user preferences and technical environments whilst maintaining consistent output quality.

| **Directory** | **Purpose** | **Content Types** | **Version Control** | **Processing Stage** |
|------------|---------|---------------|----------------|-----------------|
| `MANUSCRIPT/` | Scientific content | Markdown, YAML, BibTeX | Full tracking | Source |
| `FIGURES/` | Visual content | Python scripts, Mermaid, data | Full tracking | Source + Generated |
| `src/` | Framework code | Python modules, templates | Full tracking | Processing |
| `output/` | Compilation workspace | LaTeX, PDF, auxiliaries | Excluded (.gitignore) | Output |
| `build/` | Docker environment | Container definitions | Full tracking | Infrastructure |

{#stable:file-structure} **Project Organisation Schema.** Systematic arrangement of project components that facilitates clear separation of concerns, enhances maintainability, and supports collaborative development workflows whilst ensuring computational reproducibility.

| **Format** | **Input Extension** | **Processing Method** | **Output Formats** | **Quality** | **Use Case** |
|---------|-----------------|------------------|----------------|---------|----------|
| **Mermaid Diagrams** | `.mmd` | Mermaid CLI | SVG, PNG, PDF | Vector/Raster | Flowcharts, architectures |
| **Python Figures** | `.py` | Script execution | PNG, PDF, SVG | Publication | Data visualisation |
| **Static Images** | `.png`, `.jpg`, `.svg` | Direct inclusion | Same format | Original | Photographs, logos |
| **LaTeX Graphics** | `.tex`, `.tikz` | LaTeX compilation | PDF | Vector | Mathematical diagrams |
| **Data Files** | `.csv`, `.json`, `.xlsx` | Python processing | Via scripts | Computed | Raw data integration |

{#stable:figure-formats} **Supported Figure Generation Methods.** Comprehensive overview of the framework's figure processing capabilities, demonstrating support for both static and dynamic content generation with emphasis on reproducible computational graphics.

<newpage>

| **Tool/Platform** | **Type** | **Markdown Support** | **LaTeX Quality** | **Version Control** | **Collaboration** | **Open Source** |
|-------------------|----------|---------------------|-------------------|--------------------|--------------------|-----------------|
| **RXiv-Maker** | Specialized Pipeline | Excellent | High | Git-native | Git-based | Yes |
| **Overleaf** [@Overleaf2024] | Web LaTeX Editor | Limited | Excellent | Basic | Real-time | Freemium |
| **Quarto** [@Quarto2024] | Multi-format Publisher | Native | High | Git-friendly | File-based | Yes |
| **Pandoc** [@MacFarlane2022] | Universal Converter | Excellent | Good | File-based | File-based | Yes |
| **MyST-Parser** [@Laursen2021_myst] | Sphinx Extension | Native | High | Git-friendly | File-based | Yes |
| **Jupyter Book** [@ExecutableBooks2020] | Computational Publishing | Native | High | Git-friendly | File-based | Yes |
| **Typst** [@Typst2024] | Modern Typesetter | Good | Excellent | Git-friendly | File-based | Yes |
| **Bookdown** [@Xie2016_bookdown] | R-based Publisher | R Markdown | High | Git-friendly | File-based | Yes |
| **Direct LaTeX** | Traditional Typesetter | None | Excellent | File-based | File-based | Yes |
| **arXiv Templates** | LaTeX Templates | None | Excellent | File-based | File-based | Yes |
| **bioRxiv Templates** | LaTeX Templates | None | Excellent | File-based | File-based | Yes |
| **Word + Zotero** [@Kratzer2019_zotero] | Traditional Workflow | None | Fair | Poor | Track changes | Zotero: Yes, Word: No |
| **Google Docs + Mendeley** | Cloud Workflow | None | Fair | Poor | Real-time | Docs: No, Mendeley: Freemium |

| **Tool/Platform** | **Reproducible Content** | **Learning Curve** | **Primary Use Case** | **Key Strengths** |
|-------------------|-------------------------|-------------------|---------------------|-------------------|
| **RXiv-Maker** | Programmatic figures | Medium | Preprint servers (arXiv, bioRxiv, medRxiv) | Containerized builds, automated workflows, template-based |
| **Overleaf** [@Overleaf2024] | Manual figures | Easy | General academic publishing | Real-time collaboration, rich templates, cloud-based |
| **Quarto** [@Quarto2024] | Computational documents | Medium | Multi-format scientific publishing | Polyglot support (R/Python/Julia), multiple outputs |
| **Pandoc** [@MacFarlane2022] | Limited | Steep | Format conversion, custom workflows | Universal format support, extensible |
| **MyST-Parser** [@Laursen2021_myst] | Jupyter integration | Medium | Technical documentation, books | Sphinx ecosystem, rich directives |
| **Jupyter Book** [@ExecutableBooks2020] | Native notebook support | Medium | Computational narratives, educational content | Interactive content, executable books |
| **Typst** [@Typst2024] | Script-based | Easy | Modern academic typesetting | Fast compilation, modern syntax, incremental updates |
| **Bookdown** [@Xie2016_bookdown] | R integration | Medium | Academic books, long-form documents | Cross-references, multiple formats, R ecosystem |
| **Direct LaTeX** | Manual integration | Steep | Traditional academic publishing | Ultimate control, established workflows |
| **arXiv Templates** | Manual | Medium | arXiv submissions | Preprint-optimized, submission-ready |
| **bioRxiv Templates** | Manual | Medium | bioRxiv submissions | Life sciences focus, journal compatibility |
| **Word + Zotero** [@Kratzer2019_zotero] | Manual figures | Easy | General academic writing | Familiar interface, reference management |
| **Google Docs + Mendeley** | Manual figures | Easy | Collaborative draft writing | Real-time collaboration, accessibility |

{#stable:tool-comparison} **Comprehensive Comparison of Manuscript Preparation Tools and Platforms.** This comparison provides an exhaustive overview of available tools for scientific manuscript preparation, positioning each within the broader ecosystem of academic publishing workflows. RXiv-Maker is designed as a specialized solution optimizing for preprint server submissions, complementing rather than replacing established tools like Overleaf for general LaTeX collaboration or Quarto for multi-format publishing. The comparison emphasizes that different tools excel in different contexts: Overleaf dominates collaborative LaTeX editing, Quarto excels at multi-format computational publishing, and RXiv-Maker streamlines the specific workflow of preparing reproducible preprints for arXiv, bioRxiv, and medRxiv submission.
<newpage>

## Supplementary Notes

{#snote:file-structure} **Architectural Philosophy and Project Organisation.**

The RXiv-Maker framework embodies a carefully considered architectural philosophy that prioritises clarity, maintainability, and computational reproducibility through systematic organisation of project components. The system's file structure reflects established software engineering principles whilst accommodating the specific requirements of scientific manuscript preparation. This organisational schema segregates content, configuration, and computational elements into distinct hierarchical domains, thereby facilitating both human comprehension and automated processing.

The primary manuscript content resides within the MANUSCRIPT directory, which houses the core intellectual contribution in easily accessible formats. This directory contains the YAML configuration file (00_CONFIG.yml) that centralises all metadata including authorship details, institutional affiliations, and document properties, thereby enabling programmatic manipulation of manuscript attributes without requiring modifications to the narrative content. The numbered markdown files (01_MAIN.md, 02_SUPPLEMENTARY_INFO.md) contain the substantive text, with the numerical prefixing ensuring logical processing order whilst maintaining intuitive organisation for collaborative authoring. The BibTeX references file (03_REFERENCES.bib) provides standardised bibliographic management, ensuring consistent citation formatting across the entire document. Figure sources and data are organised within dedicated subdirectories (FIGURES/, TABLES/) that maintain clear separation between content types whilst enabling automated discovery during the compilation process.

The src directory encompasses the computational infrastructure that transforms markdown source into publication-ready output. This separation ensures that the technical implementation remains distinct from the scientific content, facilitating maintenance and updates to the processing pipeline without affecting the manuscript itself. The modular structure within src reflects software engineering best practices, with specialised processors for different content types that can be independently developed and tested. The output directory serves as the compilation workspace where intermediate files and final products are generated, preventing contamination of source materials with temporary compilation artefacts whilst providing transparency into the conversion process.

{#snote:comparison} **Comparative Analysis with Alternative Scientific Authoring Platforms.**

Within the broader landscape of scientific authoring tools, RXiv-Maker occupies a distinctive position that reflects careful consideration of the trade-offs between functionality and simplicity. Platforms such as Overleaf [@Overleaf2024] have revolutionised collaborative LaTeX authoring by providing sophisticated web-based environments with real-time collaboration features, comprehensive template libraries, and integrated compilation services. These systems excel in scenarios requiring complex document structures, advanced typesetting control, and seamless multi-author workflows. The platform's strength lies in its ability to democratise LaTeX authoring by providing a familiar word-processor-like interface whilst maintaining the typographical excellence of LaTeX output.

Similarly, Quarto [@Quarto2024] represents a powerful framework for scientific and technical publishing that supports multiple programming languages, diverse output formats, and sophisticated computational document features. Its versatility enables researchers to create documents that seamlessly integrate narrative text with executable code, supporting formats ranging from HTML web pages to PDF documents and interactive presentations. Quarto's strength lies in its comprehensive approach to scientific communication, enabling complex multi-format publishing workflows across various scientific domains.

Pandoc [@MacFarlane2022], as a universal document converter, provides exceptional flexibility in transforming content between numerous formats. Its strength lies in its ability to serve as a foundation for custom publishing workflows, enabling researchers to develop bespoke solutions for specific requirements. However, this flexibility comes at the cost of increased complexity in configuration and setup.

RXiv-Maker deliberately positions itself as a complementary tool that prioritises simplicity and focused functionality over comprehensive feature coverage. Whilst acknowledging the considerable strengths of these established platforms, RXiv-Maker addresses a specific niche within the scientific publishing ecosystem: the efficient production of high-quality preprints for repositories such as arXiv, bioRxiv, and medRxiv. This focused approach enables optimisation for this particular use case, resulting in a streamlined workflow that minimises cognitive overhead for researchers primarily concerned with rapid dissemination of their findings. The framework's emphasis on markdown as the primary authoring language reflects a philosophical commitment to accessibility and sustainability, providing an intuitive syntax that most researchers can master quickly whilst maintaining typographical excellence. A comprehensive comparison of RXiv-Maker with alternative manuscript preparation tools across multiple dimensions is provided in {@stable:tool-comparison}, illustrating how different platforms excel in different contexts and use cases.

{#snote:figure-generation} **Programmatic Figure Generation and Computational Reproducibility.**

The technical architecture underlying RXiv-Maker's figure generation capabilities demonstrates how automated processing pipelines can maintain transparent connections between source data and final visualisations whilst ensuring computational reproducibility. The system supports two primary methodologies for figure creation: Mermaid diagram processing and Python-based data visualisation, each addressing distinct requirements within the scientific publishing workflow.

Mermaid diagram processing leverages the Mermaid CLI to convert text-based diagram specifications into publication-ready graphics. This approach enables version-controlled diagram creation where complex flowcharts, system architectures, and conceptual models can be specified using intuitive syntax and automatically rendered into multiple output formats. The system generates SVG, PNG, and PDF variants to accommodate different compilation requirements whilst maintaining vector quality where appropriate. This automation eliminates the manual effort traditionally required for diagram creation and updates, whilst ensuring that modifications to diagram specifications are immediately reflected in the final document.

Python figure generation represents a more sophisticated approach to computational reproducibility, where analytical scripts are executed during document compilation to generate figures directly from source data. This integration ensures that visualisations remain synchronised with the underlying datasets and analytical methods, eliminating the possibility of outdated or inconsistent graphics persisting in the manuscript. The system executes Python scripts within the compilation environment, automatically detecting generated image files and incorporating them into the document structure. This approach transforms figures from static illustrations into dynamic, reproducible computational artefacts that enhance the scientific rigour of the publication.

{#snote:markdown-conversion} **Markdown-to-LaTeX Conversion Architecture and Processing Pipeline.**

The markdown-to-LaTeX conversion architecture demonstrates how specialised processors can handle complex document transformations whilst maintaining code modularity and testability. The system employs dedicated processors for figures, tables, citations, and other content types, each implementing specific transformation rules that preserve semantic meaning whilst ensuring typographical excellence. This modular approach enables independent development and testing of conversion components, facilitating maintenance and enhancement of the framework's capabilities.

Figure processing supports multiple syntax variants to accommodate different authoring preferences, including the new format where images are followed by attribute blocks and captions, the attributed format with inline specifications, and simple format for basic inclusions. The core conversion function implements a multi-pass approach that protects literal content during transformation, processes each figure format through dedicated functions, and restores protected content after processing. This sophisticated content protection mechanism ensures that code examples and other literal content are preserved during transformation, proving essential for technical manuscripts.

Table processing handles GitHub Flavored Markdown tables with LaTeX-specific enhancements such as rotation capabilities and sophisticated cross-referencing systems. The conversion system supports both legacy and modern caption formats, enabling authors to specify table properties including width detection for double-column layouts, rotation angles for landscape orientation, and identifier extraction for cross-referencing. The table cell formatting function implements context-aware processing that preserves markdown syntax within examples whilst properly escaping special characters and converting emphasis markers to appropriate LaTeX commands.

Reference processing demonstrates how automated systems can enhance document quality whilst reducing authoring burden. The framework automatically converts markdown-style references into appropriate LaTeX cross-references, ensuring consistent formatting and enabling LaTeX's sophisticated reference management capabilities. This automation extends to bibliographic citations, where the system integrates seamlessly with BibTeX workflows to provide professional citation formatting without requiring authors to master LaTeX citation syntax.

{#snote:reproducibility} **Reproducibility Features and Version Control Integration.**

The RXiv-Maker framework incorporates reproducibility as a fundamental design principle rather than an afterthought, implementing features that ensure complete traceability from source data to final publication. The system's integration with Git version control provides comprehensive tracking of all components necessary for manuscript generation, including content files, configuration parameters, processing scripts, and even the framework code itself. This approach ensures that every aspect of the publication process can be reproduced, verified, and audited.

The containerised compilation environment, implemented through Docker, provides perfect isolation and reproducibility of the software environment. By encapsulating the exact versions of LaTeX, Python libraries, and system dependencies within a container image, the framework eliminates the common "works on my machine" problem that plagues many scientific computing workflows. This containerisation extends beyond mere convenience to serve as a critical component of scientific integrity, ensuring that the same input always produces identical output regardless of the host system configuration.

The framework's programmatic approach to figure generation creates an auditable chain from raw data to final visualisation. Python scripts that generate figures are version-controlled alongside the manuscript content, enabling complete reconstruction of all visual elements from source data. This approach contrasts sharply with traditional workflows where figures are created separately and inserted as static images, potentially leading to inconsistencies when data is updated or analysis methods are refined.

{#snote:customisation} **Template Customisation and Advanced Styling Options.**

The RXiv-Maker framework provides extensive customisation capabilities through its LaTeX template system, enabling researchers to adapt the visual presentation to meet specific publication requirements whilst maintaining the simplicity of the markdown authoring experience. The template architecture separates content from presentation through a sophisticated class file (rxiv_maker_style.cls) that encapsulates all formatting decisions, typography choices, and layout specifications.

The YAML configuration system enables fine-grained control over document properties including author information formatting, institutional affiliation handling, and abstract presentation. Advanced users can modify template parameters to adjust margins, typography, colour schemes, and sectioning styles without requiring direct LaTeX modifications. The framework supports customisation of citation styles through configurable BibTeX style files, enabling compliance with specific journal requirements or institutional guidelines.

For institutions requiring consistent branding or specific formatting requirements, the framework provides extension points that enable custom style development whilst maintaining compatibility with the core processing pipeline. This extensibility ensures that RXiv-Maker can adapt to diverse institutional requirements without compromising its fundamental commitment to simplicity and ease of use.
<newpage>

## Supplementary Figures 

![](FIGURES/SFigure_1.svg)
{#sfig:workflow} **RXiv-Maker Workflow Overview.** Simplified representation of the RXiv-Maker system architecture, illustrating how the standardised file naming convention (00_CONFIG.yml, 01_MAIN.md, 02_SUPPLEMENTARY_INFO.md, 03_REFERENCES.bib) integrates with the processing engine to generate publication-ready documents through a fully automated pipeline from markdown input to PDF output.

![](FIGURES/SFigure_2.svg)
{#sfig:architecture} **Detailed System Architecture and Processing Layers.** Comprehensive technical diagram showing the complete RXiv-Maker architecture, including input layer organisation, processing engine components (parsers, converters, generators), compilation infrastructure, output generation, and deployment methodology integration. This figure illustrates the modular design that enables independent development and testing of system components.

