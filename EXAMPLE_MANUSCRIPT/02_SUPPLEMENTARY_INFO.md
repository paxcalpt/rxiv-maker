## Supplementary Tables

| **Format** | **Input Extension** | **Processing Method** | **Output Formats** | **Quality** | **Use Case** |
|---------|-----------------|------------------|----------------|---------|----------|
| **Mermaid Diagrams** | `.mmd` | Mermaid CLI | SVG, PNG, PDF | Vector/Raster | Flowcharts, architectures |
| **Python Figures** | `.py` | Script execution | PNG, PDF, SVG | Publication | Data visualisation |
| **Static Images** | `.png`, `.jpg`, `.svg` | Direct inclusion | Same format | Original | Photographs, logos |
| **LaTeX Graphics** | `.tex`, `.tikz` | LaTeX compilation | PDF | Vector | Mathematical diagrams |
| **Data Files** | `.csv`, `.json`, `.xlsx` | Python processing | Via scripts | Computed | Raw data integration |

{#stable:figure-formats} **Supported Figure Generation Methods.** Comprehensive overview of the framework's figure processing capabilities, demonstrating support for both static and dynamic content generation with emphasis on reproducible computational graphics.

| **Tool** | **Type** | **Markdown** | **Primary Use Case** | **Key Strengths** | **Open Source** |
|----------|----------|--------------|-------------------|-------------------|-----------------|
| **RXiv-Maker** | Pipeline | Excellent | Preprint servers | GitHub Actions integration, automated workflows | Yes |
| **Overleaf** [@Overleaf2024] | Web Editor | Limited | Academic publishing | Real-time collaboration, rich templates | Freemium |
| **Quarto** [@Quarto2024] | Publisher | Native | Multi-format publishing | Polyglot support, multiple outputs | Yes |
| **Pandoc** [@MacFarlane2022] | Converter | Excellent | Format conversion | Universal format support, extensible | Yes |
| **MyST-Parser** [@Laursen2021_myst] | Extension | Native | Technical documentation | Sphinx ecosystem, rich directives | Yes |
| **Jupyter Book** [@ExecutableBooks2020] | Publisher | Native | Educational content | Interactive content, executable books | Yes |
| **Typst** [@Typst2024] | Typesetter | Good | Modern typesetting | Fast compilation, modern syntax | Yes |
| **Bookdown** [@Xie2016_bookdown] | Publisher | R Markdown | Academic books | Cross-references, multiple formats | Yes |
| **Direct LaTeX** | Typesetter | Limited | Traditional publishing | Ultimate control, established workflows | Yes |

{#stable:tool-comparison} **Comprehensive Comparison of Manuscript Preparation Tools.** This comparison provides an exhaustive overview of available tools for scientific manuscript preparation, positioning each within the broader ecosystem of academic publishing workflows. RXiv-Maker is designed as a specialized solution optimizing for preprint server submissions, complementing rather than replacing established tools like Overleaf for general LaTeX collaboration or Quarto for multi-format publishing. The comparison highlights that different tools excel in distinct contexts: Overleaf dominates collaborative LaTeX editing, Quarto excels at multi-format computational publishing, and RXiv-Maker streamlines the specific workflow of preparing reproducible preprints for submission to arXiv, bioRxiv, and medRxiv.

| **Deployment Method** | **Environment** | **Dependencies** | **Collaboration** | **Ease of Use** | **Reproducibility** |
|-------------------|-------------|-------------|--------------|-------------|----------------|
| **GitHub Actions** | Cloud CI/CD | None (cloud) | Automatic | Very High | Perfect |
| **Google Colab** | Web browser | None (cloud) | Shared notebooks | Very High | High |
| **Local Python** | Local machine | Python + LaTeX | Git-based | Medium | Good |
| **Manual LaTeX** | Local machine | Full LaTeX suite | Git-based | Low | Variable |

{#stable:deployment-options} **RXiv-Maker Deployment Strategies.** Comparison of available compilation methods, highlighting the flexibility of the framework in accommodating different user preferences and technical environments whilst maintaining consistent output quality.

| **Markdown Element** | **LaTeX Equivalent** | **Description** |
|------------------|------------------|-------------|
| `**bold text**` | `\textbf{bold text}` | Bold formatting for emphasis |
| `*italic text*` | `\textit{italic text}` | Italic formatting for emphasis |
| `~subscript~` | `\textsubscript{subscript}` | Subscript formatting (H~2~O, CO~2~) |
| `^superscript^` | `\textsuperscript{superscript}` | Superscript formatting (E=mc^2^, x^n^) |
| `# Header 1` | `\section{Header 1}` | Top-level section heading |
| `## Header 2` | `\subsection{Header 2}` | Second-level section heading |
| `### Header 3` | `\subsubsection{Header 3}` | Third-level section heading |
| `@citation` | `\cite{citation}` | Single citation reference |
| `[@cite1;@cite2]` | `\cite{cite1,cite2}` | Multiple citation references |
| `@fig:label` | `\ref{fig:label}` | Figure cross-reference |
| `@sfig:label` | `\ref{sfig:label}` | Supplementary figure cross-reference |
| `@table:label` | `\ref{table:label}` | Table cross-reference |
| `@stable:label` | `\ref{stable:label}` | Supplementary table cross-reference |
| `@eq:label` | `\eqref{eq:label}` | Equation cross-reference |
| `@snote:label` | `\sidenote{label}` | Supplement note cross-reference |
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


<newpage>

## Supplementary Notes

{#snote:figure-generation} **Programmatic Figure Generation and Computational Reproducibility.**

The technical architecture underlying RXiv-Maker's figure generation capabilities demonstrates how automated processing pipelines can maintain transparent connections between source data and final visualisations whilst ensuring computational reproducibility. The system supports two primary methodologies for figure creation: Mermaid diagram processing and Python-based data visualisation, each addressing distinct requirements within the scientific publishing workflow.

Mermaid diagram processing leverages the Mermaid CLI to convert text-based diagram specifications into publication-ready graphics. This approach enables version-controlled diagram creation where complex flowcharts, system architectures, and conceptual models can be specified using intuitive syntax and automatically rendered into multiple output formats. The system generates SVG, PNG, and PDF variants to accommodate different compilation requirements whilst maintaining vector quality where appropriate. This automation eliminates the manual effort traditionally required for diagram creation and updates, whilst ensuring that modifications to diagram specifications are immediately reflected in the final document.

Python figure generation represents a more sophisticated approach to computational reproducibility, where analytical scripts are executed during document compilation to generate figures directly from source data. This integration ensures that visualisations remain synchronised with the underlying datasets and analytical methods, eliminating the possibility of outdated or inconsistent graphics persisting in the manuscript. The system executes Python scripts within the compilation environment, automatically detecting generated image files and incorporating them into the document structure. This approach transforms figures from static illustrations into dynamic, reproducible computational artefacts that enhance the scientific rigour of the publication.

{#snote:comparison} **Comparative Analysis with Alternative Scientific Authoring Platforms.**

Within the broader landscape of scientific authoring tools, RXiv-Maker occupies a distinctive position that reflects careful consideration of the trade-offs between functionality and simplicity. Platforms such as Overleaf [@Overleaf2024] have revolutionised collaborative LaTeX authoring by providing sophisticated web-based environments with real-time collaboration features, comprehensive template libraries, and integrated compilation services. These systems excel in scenarios requiring complex document structures, advanced typesetting control, and seamless multi-author workflows. The platform's strength lies in its ability to democratize LaTeX authoring by providing a familiar, word-processor-like interface while maintaining the typographical excellence of LaTeX output.

Similarly, Quarto [@Quarto2024] represents a robust framework for scientific and technical publishing that supports multiple programming languages, diverse output formats, and sophisticated computational document features. Its versatility enables researchers to create documents that seamlessly integrate narrative text with executable code, supporting formats ranging from HTML web pages to PDF documents and interactive presentations. Quarto's strength lies in its comprehensive approach to scientific communication, enabling complex multi-format publishing workflows across various scientific domains.

Pandoc [@MacFarlane2022], a universal document converter, offers exceptional flexibility in transforming content between various formats. Its strength lies in its ability to serve as a foundation for custom publishing workflows, enabling researchers to develop bespoke solutions for specific requirements. However, this flexibility comes at the cost of increased complexity in configuration and setup.

{#snote:reproducibility} **Reproducibility Features and Version Control Integration.**

The RXiv-Maker framework incorporates reproducibility as a fundamental design principle rather than an afterthought, implementing features that ensure complete traceability from source data to final publication. The system's integration with Git version control provides comprehensive tracking of all components necessary for manuscript generation, including content files, configuration parameters, processing scripts, and even the framework code itself. This approach ensures that every aspect of the publication process can be reproduced, verified, and audited.

The automated GitHub Actions compilation environment provides perfect isolation and reproducibility of the software environment. By encapsulating the exact versions of LaTeX, Python libraries, and system dependencies within a controlled cloud environment, the framework eliminates the standard "works on my machine" problem that plagues many scientific computing workflows. This automated approach extends beyond mere convenience to serve as a critical component of scientific integrity, ensuring that the same input always produces identical output regardless of the host system configuration.

The framework's programmatic approach to figure generation creates an auditable chain from raw data to final visualisation. Python scripts that generate figures are version-controlled alongside the manuscript content, allowing for the complete reconstruction of all visual elements from the source data. This approach contrasts sharply with traditional workflows, where figures are created separately and inserted as static images, which can lead to inconsistencies when data is updated or analysis methods are refined.

{#snote:customisation} **Template Customisation and Advanced Styling Options.**

The RXiv-Maker framework provides extensive customization capabilities through its LaTeX template system, enabling researchers to adapt the visual presentation to meet specific publication requirements while maintaining the simplicity of the Markdown authoring experience. The template architecture separates content from presentation through a sophisticated class file (rxiv_maker_style.cls) that encapsulates all formatting decisions, typography choices, and layout specifications.

The YAML configuration system provides fine-grained control over document properties, including author information formatting, handling of institutional affiliations, and presentation of abstracts. Advanced users can modify template parameters to adjust margins, typography, colour schemes, and sectioning styles without requiring direct LaTeX modifications. The framework supports customisation of citation styles through configurable BibTeX style files, enabling compliance with specific journal requirements or institutional guidelines.

For institutions requiring consistent branding or specific formatting requirements, the framework provides extension points that enable custom style development whilst maintaining compatibility with the core processing pipeline. This extensibility ensures that RXiv-Maker can adapt to diverse institutional requirements without compromising its fundamental commitment to simplicity and ease of use.

{#snote:mathematical-formulas} **Mathematical Formula Support and LaTeX Integration.**

The RXiv-Maker framework seamlessly integrates mathematical notation by automatically translating markdown-style mathematical expressions into publication-ready LaTeX mathematics. This capability enables researchers to author complex mathematical content using familiar syntax whilst benefiting from LaTeX's superior mathematical typesetting capabilities.

Inline mathematical expressions are supported through dollar sign delimiters (`$...$`), enabling simple formulas such as $E = mc^2$ or $\alpha = \frac{\beta}{\gamma}$ to be embedded within narrative text. The conversion system automatically preserves these expressions during the markdown-to-LaTeX transformation, ensuring that mathematical notation maintains proper formatting and spacing according to established typographical conventions.

Display equations utilise double dollar sign delimiters (`$$...$$`) for prominent mathematical expressions that require centered presentation. Complex equations such as the Schrödinger equation:

$$i\hbar\frac{\partial}{\partial t}\Psi(\mathbf{r},t) = \hat{H}\Psi(\mathbf{r},t)$$

or the Navier-Stokes equations:

$$\rho\left(\frac{\partial \mathbf{v}}{\partial t} + \mathbf{v} \cdot \nabla \mathbf{v}\right) = -\nabla p + \mu \nabla^2 \mathbf{v} + \mathbf{f}$$

demonstrate the framework's capability to handle sophisticated mathematical typography, including Greek letters, partial derivatives, vector notation, and complex fraction structures.

The system also supports LaTeX's advanced mathematical environments by directly including LaTeX code blocks. This hybrid approach enables authors to utilise simple markdown syntax for straightforward expressions whilst retaining access to LaTeX's full mathematical typesetting capabilities for complex multi-line derivations:

```latex
\begin{align}
\nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} \\
\nabla \times \mathbf{B} &= \mu_0 \mathbf{J} + \mu_0 \epsilon_0 \frac{\partial \mathbf{E}}{\partial t} \\
\nabla \cdot \mathbf{E} &= \frac{\rho}{\epsilon_0} \\
\nabla \cdot \mathbf{B} &= 0
\end{align}
```

Mathematical expressions within figure captions, table entries, and cross-references are automatically processed, ensuring consistent mathematical typography throughout the document. The framework's content protection system ensures that mathematical expressions are preserved during the multi-stage conversion pipeline, preventing unwanted modifications to delicate mathematical syntax.

Statistical notation commonly required in scientific manuscripts is fully supported, including confidence intervals $\mu \pm \sigma$, probability distributions $P(X \leq x)$, and statistical tests with significance levels $p < 0.05$. Complex expressions involving summations $\sum_{i=1}^{n} x_i$, integrals $\int_{-\infty}^{\infty} f(x) dx$, and matrix operations $\mathbf{A}^{-1}\mathbf{b} = \mathbf{x}$ are rendered with appropriate spacing and sizing.

{#snote:numbered-equations} **Enhanced Mathematical Notation and Equation Systems.**

The RXiv-Maker framework supports both traditional LaTeX math environments and an enhanced markdown-like syntax for numbered equations, enabling intuitive mathematical authoring while maintaining LaTeX's typographical excellence. This dual approach accommodates different user preferences and workflow requirements.

**Enhanced Markdown-Like Syntax:** The framework introduces simplified syntax for numbered equations using attributed display math blocks. The new approach uses `$$...$$ {#eq:id}` syntax to create numbered equations automatically, while traditional LaTeX environments remain fully supported.

**Simple Numbered Equations:** Basic equations can be written as:

```
$$F = ma$$ {#eq:newton-simple}
```

This creates a numbered equation as shown by referencing `@eq:newton-simple`.

**Multi-line Aligned Equations:** For systems of equations:

```
$$x = a + b \\
y = c + d$$ {#eq:simple-system .align}
```

The system can be referenced with `@eq:simple-system` to demonstrate aligned equations.

**Unnumbered Display Math:** For emphasis without numbering:

```
$$E = mc^2$$ {#eq:einstein .unnumbered}
```

**Syntax Overview:** The enhanced math syntax provides:

- Numbered equations: Use `$$...$$ {#eq:id}` pattern
- Multiple environments: Align, equation, unnumbered styles  
- Automatic cross-referencing: `@eq:identifier` becomes `\eqref{eq:identifier}`
- Backward compatibility: Traditional LaTeX environments remain unchanged

**Traditional LaTeX Support:** Complex equations can still use traditional environments:

\begin{equation}
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
\label{eq:gaussian-integral}
\end{equation}

References to traditional equations, such as @eq:gaussian-integral, work seamlessly.

**Backward Compatibility:** Traditional LaTeX environments remain fully supported for complex cases requiring specialized formatting:

\begin{equation}
\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}
\label{eq:maxwell-traditional}
\end{equation}

**Key Features:** The enhanced equation system provides:

- **Simplified syntax**: Use `$$...$$ {#eq:id}` pattern for numbered equations
- **Multiple environments**: Support for align, equation, and unnumbered styles  
- **Automatic numbering**: Consistent equation numbering throughout document
- **Cross-referencing**: Pattern `@eq:identifier` converts to LaTeX `\eqref{eq:identifier}`
- **Backward compatibility**: Existing LaTeX environments work unchanged

This dual approach ensures that equation numbers remain consistent during manuscript development, while providing multiple pathways for mathematical expressions suited to different user preferences and complexity requirements.

{#snote:file-structure} **Architectural Philosophy and Project Organisation.**

The RXiv-Maker framework embodies a carefully considered architectural philosophy that prioritizes clarity, maintainability, and computational reproducibility through the systematic organization of project components. The system's file structure reflects established software engineering principles whilst accommodating the specific requirements of scientific manuscript preparation. This organisational schema segregates content, configuration, and computational elements into distinct hierarchical domains, thereby facilitating both human comprehension and automated processing.

The primary manuscript content resides within the MANUSCRIPT directory, which houses the core intellectual contribution in easily accessible formats. This directory contains the YAML configuration file (00_CONFIG.yml) that centralises all metadata, including authorship details, institutional affiliations, and document properties, thereby enabling programmatic manipulation of manuscript attributes without requiring modifications to the narrative content. The numbered markdown files (01_MAIN.md, 02_SUPPLEMENTARY_INFO.md) contain the substantive text, with the numerical prefix ensuring a logical processing order while maintaining an intuitive organization for collaborative authoring. The BibTeX references file (03_REFERENCES.bib) provides standardised bibliographic management, ensuring consistent citation formatting across the entire document. Figure sources and data are organized within dedicated subdirectories (FIGURES/, TABLES/) that maintain a clear separation between content types, while enabling automated discovery during the compilation process.

The src directory encompasses the computational infrastructure that transforms markdown source into publication-ready output. This separation ensures that the technical implementation remains distinct from the scientific content, facilitating maintenance and updates to the processing pipeline without affecting the manuscript itself. The modular structure within src reflects software engineering best practices, with specialised processors for different content types that can be independently developed and tested. The output directory serves as the compilation workspace, where intermediate files and final products are generated. This prevents contamination of source materials with temporary compilation artifacts while providing transparency into the conversion process.

{#snote:markdown-conversion} **Markdown-to-LaTeX Conversion Architecture and Processing Pipeline.**

The markdown-to-LaTeX conversion architecture demonstrates how specialised processors can handle complex document transformations whilst maintaining code modularity and testability. The system employs dedicated processors for figures, tables, citations, and other content types, each implementing specific transformation rules that preserve semantic meaning whilst ensuring typographical excellence. This modular approach enables independent development and testing of conversion components, facilitating maintenance and enhancement of the framework's capabilities.

Figure processing supports multiple syntax variants to accommodate different authoring preferences, including the new format where images are followed by attribute blocks and captions, the attributed format with inline specifications, and a simple format for basic inclusions. The core conversion function implements a multi-pass approach that protects literal content during transformation, processes each figure format through dedicated functions, and restores protected content after processing. This sophisticated content protection mechanism ensures that code examples and other literal content are preserved during transformation, proving essential for technical manuscripts.

Table processing handles GitHub Flavored Markdown tables with LaTeX-specific enhancements, including rotation capabilities and sophisticated cross-referencing systems. The conversion system supports both legacy and modern caption formats, enabling authors to specify table properties including width detection for double-column layouts, rotation angles for landscape orientation, and identifier extraction for cross-referencing. The table cell formatting function implements context-aware processing that preserves Markdown syntax within examples, while properly escaping special characters and converting emphasis markers to the appropriate LaTeX commands.

Reference processing demonstrates how automated systems can enhance document quality whilst reducing authoring burden. The framework automatically converts markdown-style references into appropriate LaTeX cross-references, ensuring consistent formatting and enabling LaTeX's sophisticated reference management capabilities. This automation extends to bibliographic citations, where the system integrates seamlessly with BibTeX workflows to provide professional citation formatting without requiring authors to master LaTeX citation syntax.

{#snote:private-workflow} **Private Repository Workflows and Secure Collaborative Authoring.**

The RXiv-Maker framework fully supports private repository workflows, addressing the specific requirements of sensitive research projects, proprietary collaborations, and manuscripts under embargo restrictions. Private repositories enable secure collaborative authoring whilst maintaining the framework's core reproducibility guarantees and automated processing capabilities. The GitHub Actions integration functions seamlessly within private repositories, ensuring that confidential research content remains protected throughout the compilation process whilst benefiting from the same level of automation available in public repositories.

Private repository workflows offer particular advantages for industry-academic collaborations where intellectual property considerations necessitate restricted access during manuscript development. The framework's automated build processes execute within GitHub's secure infrastructure without exposing manuscript content to external services or systems. This isolation ensures that proprietary datasets, unpublished methodologies, and confidential research findings remain protected whilst enabling the sophisticated processing capabilities that characterize the RXiv-Maker system.

The collaborative features within private repositories maintain full compatibility with the framework's version control integration. Multiple authors can contribute simultaneously through branch-based workflows, with automated conflict resolution and merge capabilities ensuring smooth collaboration despite access restrictions. The pull request workflow enables structured peer review processes within research teams, allowing for systematic evaluation of contributions before integration into the main manuscript. This approach maintains scientific rigour whilst accommodating the security requirements of sensitive research projects.

For organisations requiring additional security measures, the framework supports GitHub Enterprise environments and self-hosted runners, enabling complete control over the computational infrastructure used for manuscript processing. These deployment options ensure compliance with institutional security policies whilst preserving the automated capabilities that make RXiv-Maker effective for scientific publishing workflows.

{#snote:limitations} **Platform Constraints and Computational Limitations.**

The RXiv-Maker framework operates within well-defined computational constraints that reflect both GitHub Actions infrastructure limitations and deliberate design choices optimised for scientific manuscript preparation. Understanding these constraints enables authors to structure their workflows effectively whilst maximizing the framework's capabilities.

GitHub Actions provides generous computational resources for open-source projects, with each workflow run allocated up to 6 hours of execution time and 2 CPU cores with 7GB of RAM. For private repositories, these resources are subject to account-specific usage limits, typically providing 2000 minutes monthly for free accounts and additional time through paid plans. These constraints are sufficient for typical manuscript processing, including complex figure generation and LaTeX compilation with extensive bibliographies and cross-references.

The framework's processing pipeline is optimised to operate efficiently within these constraints through intelligent caching mechanisms and selective regeneration of content. Figure generation scripts are cached based on modification timestamps, ensuring that unchanged analyses are not unnecessarily re-executed. LaTeX compilation utilizes incremental building strategies that minimize processing time for manuscript updates. These optimizations enable the system to handle substantial manuscripts, including those with dozens of figures and extensive bibliographic databases, within standard computational allocations.

Large datasets present specific considerations within the framework's constraints. The GitHub repository size limit of 1GB necessitates careful management of data files used for figure generation. The framework supports external data sources through programmatic downloading within figure generation scripts, enabling access to large datasets without repository storage requirements. For manuscripts requiring substantial computational resources, the framework provides extension points for custom runners and external processing systems whilst maintaining reproducibility guarantees.

The PDF compilation process itself operates within LaTeX's established constraints, including memory limitations for complex documents with extensive cross-referencing or large embedded graphics. The framework provides optimization strategies for managing these constraints, including figure compression options and modular compilation approaches for particularly complex manuscripts.

{#snote:usability} **Accessibility for Non-Technical Researchers and Learning Pathways.**

The RXiv-Maker framework, whilst leveraging developer-centric tools and methodologies, is designed with careful consideration for researchers without extensive technical backgrounds. The system's reliance on Markdown syntax, Git version control, and command-line interfaces reflects a strategic investment in transferable skills that extend beyond manuscript preparation into broader research computing practices.

Markdown represents an exceptionally accessible markup language that has gained widespread adoption across diverse research communities. Unlike LaTeX, which requires mastery of complex syntax and specialized commands, Markdown enables authors to focus on content whilst automatically handling formatting concerns. The learning curve for basic Markdown syntax is minimal, typically requiring less than an hour for competency in the core elements necessary for scientific writing. Advanced features, such as cross-referencing and citation management, build naturally upon this foundation without requiring comprehensive system knowledge.

The framework provides extensive documentation and educational resources designed specifically for researchers transitioning from traditional word processing workflows. Interactive tutorials guide users through the essential concepts of version control, demonstrating how Git's branching and merging capabilities enhance collaborative writing. These educational materials emphasize practical applications rather than technical implementation details, ensuring that researchers can leverage the system's capabilities without becoming software developers.

GitHub's web interface provides an accessible entry point for researchers hesitant about command-line tools. The platform's editing capabilities enable direct manuscript modification through a familiar web browser interface, whilst still benefiting from version control and automated processing. This approach allows gradual adoption of more advanced features as researchers become comfortable with the fundamental concepts.

The framework's educational value extends beyond manuscript preparation to encompass broader research computing skills increasingly essential in modern scientific practice. Proficiency with Git version control, Markdown authoring, and automated workflows provides researchers with transferable capabilities applicable to data analysis, software development, and collaborative research projects. These skills align with growing expectations for computational literacy in scientific careers.

{#snote:privacy} **Privacy Considerations and Data Protection in Collaborative Research.**

The RXiv-Maker framework addresses privacy considerations through a comprehensive approach that balances collaborative functionality with robust data protection measures. The system's architecture ensures that sensitive research content, including unpublished findings, proprietary methodologies, and confidential datasets, remains appropriately protected throughout the manuscript development process.

GitHub's security infrastructure provides enterprise-grade protection for repository content, including encryption at rest and in transit, two-factor authentication requirements, and sophisticated access control mechanisms. Private repositories ensure that manuscript content remains accessible only to designated collaborators, with granular permission systems enabling fine-tuned control over editing and viewing privileges. These measures meet the security requirements of most academic and industrial research environments.

The automated processing workflows execute within isolated GitHub Actions environments that are ephemeral and secure. Each compilation run provisions a fresh computational environment that is completely isolated from other users and projects. Compilation artifacts, including intermediate files and logs, are automatically purged after workflow completion unless explicitly configured for retention. This approach ensures that sensitive content cannot persist in shared infrastructure beyond the immediate processing requirements.

For research involving human subjects data, personal health information, or other regulated content, the framework supports integration with institutional data governance frameworks. The processing pipeline can be configured to exclude sensitive datasets from automated workflows whilst maintaining reproducibility for non-sensitive components. This hybrid approach enables researchers to benefit from automated manuscript preparation whilst maintaining compliance with ethical and regulatory requirements.

Advanced privacy features include support for encrypted repository content, integration with institutional single sign-on systems, and compatibility with air-gapped network environments through self-hosted runners. These capabilities ensure that the framework can accommodate diverse institutional security policies whilst preserving its core collaborative and reproducibility benefits.

{#snote:training} **Educational Benefits and Professional Development Opportunities.**

The RXiv-Maker framework provides substantial educational benefits that extend beyond manuscript preparation to encompass essential professional development in modern research computing. The skills acquired through framework adoption align closely with industry standards and best practices increasingly valued across academic, industrial, and governmental research environments.

Version control proficiency using Git represents a fundamental competency in contemporary collaborative work. The framework provides practical experience with branching strategies, merge conflict resolution, and distributed collaboration workflows that directly transfer to software development, data analysis projects, and large-scale research collaborations. These skills are increasingly recognized as essential for research positions requiring computational components or collaborative data analysis.

Markdown authoring capabilities extend beyond academic writing to encompass technical documentation, research notebooks, and web content creation. Proficiency with Markdown syntax enables researchers to create professional documentation for software projects, maintain laboratory protocols in version-controlled systems, and contribute to collaborative research platforms. This markup language has become standard across numerous research computing environments and documentation systems.

The framework's automated workflow concepts introduce researchers to continuous integration and deployment practices that form the foundation of modern software development. Understanding these concepts enhances researchers' ability to participate in interdisciplinary projects involving software components, contributes to more robust computational research practices, and provides insights into quality assurance methodologies applicable across diverse research domains.

GitHub platform familiarity gained through framework adoption enables participation in the open science ecosystem, including contribution to research software projects, collaboration on data analysis workflows, and engagement with the broader scientific computing community. These connections facilitate professional networking opportunities and provide pathways for career development in research computing and data science roles.

The educational progression from basic Markdown authoring to advanced workflow automation provides a structured pathway for researchers to develop computational skills at their own pace. This gradual skill acquisition approach ensures that researchers can immediately benefit from the framework whilst building capabilities for more sophisticated applications as their expertise develops.

{#snote:subscript-superscript} **Advanced Typography for Chemical Formulas and Mathematical Notation.**

The RXiv-Maker framework provides comprehensive support for subscript and superscript notation essential for chemical formulas, mathematical expressions, and scientific nomenclature. The system seamlessly integrates LaTeX's superior typesetting capabilities with accessible Markdown-based authoring through multiple syntax approaches that accommodate different complexity levels and authoring preferences.

For basic chemical formulas, the framework supports direct LaTeX notation within mathematical expressions. Standard chemical compounds can be expressed using LaTeX's math mode syntax: $H_2O$ for water, $CO_2$ for carbon dioxide, and $CaCl_2$ for calcium chloride. More complex chemical expressions benefit from specialized LaTeX packages that are automatically included in the processing pipeline, such as $\ce{H2SO4}$ using the mhchem package for enhanced chemical typesetting.

Buffer systems and complex biochemical formulas require sophisticated subscript and superscript handling that maintains readability whilst ensuring scientific accuracy. The framework automatically processes expressions such as $HEPES_{buffer}$ for 4-(2-hydroxyethyl)-1-piperazineethanesulfonic acid buffers, or $Tris-HCl_{pH 8.0}$ for tris(hydroxymethyl)aminomethane hydrochloride solutions. Ion concentrations can be expressed with proper charge notation: $Ca^{2+}$, $Cl^{-}$, or $PO_4^{3-}$.

Mathematical expressions requiring multiple levels of subscripting and superscripting are handled through LaTeX's nested notation capabilities. Complex expressions such as $x_{i,j}^{(k)}$ for matrix elements or $\sum_{i=1}^{n} x_i^2$ for statistical calculations maintain proper spacing and alignment. The framework preserves these expressions during the conversion pipeline through sophisticated content protection mechanisms that prevent interference from other processing stages.

Isotope notation commonly required in chemistry and physics utilizes specialized positioning for mass and atomic numbers. The framework supports expressions such as $^{14}C$, $^{32}P$, and $^{235}U$ through LaTeX's prescript package, automatically loaded during compilation. Decay reactions can be expressed with proper alignment: $^{14}C \rightarrow ^{14}N + e^- + \bar{\nu}_e$.

The system also supports HTML-style subscript and superscript notation for simple cases where mathematical mode is unnecessary. Basic expressions can use `<sub>` and `<sup>` tags: H<sub>2</sub>O or E=mc<sup>2</sup>, which are automatically converted to appropriate LaTeX commands during processing.

{#snote:special-characters} **Robust Handling of Special Characters and Escape Sequences.**

The RXiv-Maker framework implements a sophisticated character handling system that automatically manages the complexities of special character processing across the Markdown-to-LaTeX conversion pipeline. This system ensures that researchers can author content naturally without requiring detailed knowledge of LaTeX's character escaping requirements, whilst maintaining typographical accuracy in the final output.

LaTeX treats several characters as special control sequences that require careful escaping to render literally. The framework automatically handles the most problematic characters: hash symbols for headings and hashtags, ampersands commonly found in chemical names and URLs, percent signs used in concentrations and statistical reporting, dollar signs for currency and funding amounts, underscores in filenames and identifiers, carets in mathematical notation, and tildes in URLs and file paths.

The conversion system employs intelligent context-aware processing that distinguishes between characters serving syntactic functions and those intended for literal rendering. Hash symbols in Markdown headings are correctly processed as sectioning commands, whilst hash symbols within paragraph text are automatically escaped as `\#` in the LaTeX output. This contextual processing extends to all special characters, ensuring that mathematical expressions, code blocks, and regular text are handled appropriately.

Email addresses and URLs present particular challenges due to their heavy reliance on characters with special meaning in LaTeX. The framework automatically detects these patterns and applies appropriate escaping and formatting. Email addresses like `author@institution.edu` are processed using LaTeX's `\url{}` command, which handles special characters correctly whilst enabling proper line breaking. Complex URLs with query parameters are similarly protected during processing whilst maintaining proper character escaping.

Chemical nomenclature often includes characters that require special handling, such as Greek letters (`α`, `β`, `γ`), prime symbols (`'`), and various diacritical marks. The framework maintains a comprehensive mapping of Unicode characters to their LaTeX equivalents, ensuring that scientific text authored with standard keyboard input methods renders correctly in the final document. This includes support for degree symbols (`°`), plus-minus indicators (`±`), and multiplication symbols (`×`).

Programming code and computational expressions embedded within scientific manuscripts present additional considerations. The framework's code block protection system ensures that programming syntax, including special characters used in conditional statements, regular expressions, and data structure definitions, remains unmodified during the conversion process. This protection extends to inline code segments, where backtick-delimited expressions are preserved exactly as authored.

{#snote:figure-legends} **Advanced Figure Caption Management and Multi-Page Layout Control.**

The RXiv-Maker framework provides sophisticated control over figure caption formatting and page layout behaviour, addressing the complex requirements of scientific publishing where detailed figure descriptions often require substantial space and careful positioning relative to the associated graphics. The system's caption management capabilities ensure professional presentation whilst maintaining flexibility for diverse content requirements.

Figure caption length presents unique challenges in scientific publishing where comprehensive descriptions are essential for reproducibility and clarity. The framework supports extensive captions through LaTeX's advanced caption package, which automatically handles text wrapping, proper spacing, and alignment with figure content. Long captions are intelligently formatted with appropriate line spacing and indentation that maintains readability whilst preserving the visual relationship between caption and figure.

Multi-page caption handling utilizes LaTeX's sophisticated float management system to ensure optimal presentation across page boundaries. When captions extend beyond the available space on a figure's initial page, the system can automatically continue the caption on subsequent pages with appropriate formatting cues. The `\ContinuedFloat` environment enables figure captions to span multiple pages whilst maintaining proper numbering and cross-referencing functionality.

The framework provides explicit control over caption behaviour through specialized attributes and LaTeX commands. Authors can specify caption positioning using the `tex_position` attribute to control whether figures appear at the top (t), bottom (b), or inline (h) with their associated content. For complex layouts requiring precise control, the system supports the `\captionsetup{}` command to modify spacing, font selection, and alignment properties on a per-figure basis.

Figure caption formatting can be customized to meet specific journal requirements or institutional guidelines. The framework supports various caption styles, including hanging indentation for numbered lists within captions, custom label formatting for specialized figure types, and integration with cross-referencing systems that maintain consistent formatting throughout the document. These customization capabilities ensure compatibility with diverse publication standards whilst maintaining the framework's ease of use.

Advanced layout scenarios, such as figures with multiple panels requiring individual sub-captions, are supported through the subcaption package integration. This capability enables complex figure presentations where each panel requires detailed description whilst maintaining overall figure cohesion. The framework automatically manages the hierarchical numbering and cross-referencing required for such presentations.

{#snote:full-page-figures} **Full-Page Figure Integration and Column Layout Management.**

The RXiv-Maker framework provides comprehensive support for full-page figure presentation within multi-column document layouts, addressing the common requirement for large graphics that require maximum visual impact whilst maintaining document consistency. The system's approach to full-page figures ensures optimal presentation whilst preserving automated processing capabilities and cross-referencing functionality.

Full-page figure implementation utilizes LaTeX's specialized float environments that temporarily suspend column formatting to provide complete page utilization for large graphics. The `figure*` environment automatically spans both columns in two-column layouts, providing maximum width for detailed diagrams, complex data visualizations, or high-resolution photographic content. This approach maintains proper figure numbering and caption formatting whilst enabling optimal graphic presentation.

The framework supports various full-page presentation modes to accommodate different content requirements. The `\begin{figure*}[p]` directive creates dedicated figure pages that contain only the graphic and caption, providing uninterrupted visual presentation for particularly important content. Alternative positioning options enable full-width figures to appear at the top or bottom of pages whilst maintaining surrounding text flow, ensuring optimal integration with manuscript narrative.

Complex multi-panel figures benefit from the framework's support for custom layout specifications that maintain readability whilst maximizing visual impact. The system can automatically scale graphics to utilize available space whilst preserving aspect ratios and ensuring that detailed content remains legible. Custom spacing and positioning commands enable fine-tuned control over multi-element presentations within full-page contexts.

The automated processing pipeline ensures that full-page figures integrate seamlessly with the overall document structure. Cross-referencing functionality operates identically for full-page figures, enabling consistent citation throughout the manuscript text. The figure numbering system maintains proper sequence regardless of positioning choices, ensuring that document organization remains logical and accessible.

File format considerations for full-page figures include support for high-resolution graphics that maintain quality when scaled to full-page dimensions. The framework automatically handles PDF, PNG, and SVG formats with appropriate optimization for print and digital distribution. Vector graphics formats are preferred for diagrams and plots to ensure scalability, whilst high-resolution raster formats support photographic content and complex visualizations that require pixel-perfect representation.

<newpage>

## Supplementary Figures 

![](FIGURES/SFigure_2.svg)
{#sfig:arxiv-growth width="100%"} **The growth of preprint submissions on the arXiv server from 1991 to 2025.** The data, sourced from arXiv's public statistics, is plotted using a Python script integrated into our RXiv-Maker pipeline. This demonstrates the system's capacity for reproducible, data-driven figure generation directly within the publication workflow.

![](FIGURES/SFigure_1.svg)
{#sfig:architecture width="80%"} **Detailed System Architecture and Processing Layers.** Comprehensive technical diagram showing the complete RXiv-Maker architecture, including input layer organisation, processing engine components (parsers, converters, generators), compilation infrastructure, output generation, and deployment methodology integration. This figure illustrates the modular design that enables independent development and testing of system components.


