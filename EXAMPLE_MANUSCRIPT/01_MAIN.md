# RXiv-Maker: An Automated Template Engine for Streamlined Scientific Publications
<!-- note that this title is not rendered in the PDF, rather the one in the YAML metadata is used -->


## Abstract
Modern scientific publishing has shifted towards rapid dissemination through preprint servers, placing increased demands on researchers for manuscript preparation and quality control. We present RXiv-Maker, a comprehensive GitHub-native system that simplifies scientific writing through markdown-based authoring with automated LaTeX conversion. The system enables researchers to write in familiar markdown syntax whilst producing publication-quality documents with professional typesetting. RXiv-Maker offers flexible compilation strategies ranging from GitHub Actions and Google Colab to local compilation with minimal installation requirements using Docker containerisation. The framework supports diverse visualisation approaches, including programmatic figure generation through Python libraries such as Matplotlib and Seaborn, alongside integrated Mermaid diagram rendering for conceptual illustrations. This self-documenting article demonstrates the system's capabilities, showcasing how markdown-centric authoring transforms scientific communication into an efficient, collaborative, and reproducible process. RXiv-Maker serves as a foundational tool for research groups seeking streamlined publishing workflows, enabling scientists to focus on research content whilst maintaining rigorous technical standards.

## Main

<!-- Introduction -->

Scientific publishing has undergone profound transformation over the past two decades, fundamentally altering how researchers communicate and disseminate findings [@Tennant2016_academic_publishing]. The emergence of preprint servers such as arXiv, bioRxiv, and medRxiv has enabled millions of manuscripts to bypass traditional peer-review bottlenecks, with exponential growth particularly evident during the COVID-19 pandemic [@Fraser2021_preprint_growth;@Abdill2019_biorxiv_growth]. This shift towards immediate publication reflects growing recognition that traditional publishing timelines are incompatible with the pace of modern scientific discovery.

![](FIGURES/Figure_1.svg)
{#fig:diagram tex_position="t"} **The RXiv-Maker Diagram.** The system integrates Markdown content, YAML metadata, Python scripts, and bibliography files through a processing engine. This engine leverages Docker, GitHub Actions, and LaTeX to produce a publication-ready scientific article, demonstrating a fully automated and reproducible pipeline.

Concurrent with this transformation, computational tools and automated workflows have become essential to contemporary research practice. Version control systems, particularly Git and GitHub, have evolved into platforms for scientific collaboration, enabling transparent manuscript development and reproducible analyses [@Ram2013_git_science;@Perez-Riverol2016_github_bioinformatics]. Containerisation technologies such as Docker have enhanced reproducibility by providing standardised computational environments [@Boettiger2015_docker_reproducibility;@Hidalgo-Cenalmor2024_DL4MicEverywhere].
Traditional manuscript preparation remains largely unchanged, relying on fragmented workflows that separate content creation, figure generation, and document compilation. This fragmentation introduces opportunities for error and version conflicts. Contemporary research demands sophisticated figure generation capabilities integrating statistical analysis and publication-quality visualisation. Whilst Python libraries such as Matplotlib and Seaborn provide foundational tools for scientific visualisation [@Hunter2007_matplotlib;@Waskom2021_seaborn], modern workflows also benefit from declarative diagram creation through Mermaid, enabling researchers to generate flowcharts and conceptual illustrations using text-based syntax.

RXiv-Maker addresses these requirements through a markdown-centric authoring system that automatically translates familiar markdown syntax into professional LaTeX documents. Built upon the established Jacquemet and Henriques bioRxiv template [@RxivMaker2015_template], the system extends capabilities through automated processing pipelines, integrated figure generation, and flexible deployment strategies. The architecture, detailed in Fig. @fig:diagram and comprehensively illustrated in Sup. Fig. @sfig:workflow, provides automated figure generation for statistical visualisation, integrated Mermaid diagram creation, and robust build automation through containerised environments.

<!-- Results -->

![](FIGURES/Figure_2.svg)
{#fig:2 tex_position="t" width=100%} **The growth of preprint submissions on the arXiv server from 1991 to 2025.** The data, sourced from arXiv's public statistics, is plotted using a Python script integrated into our RXiv-Maker pipeline. This demonstrates the system's capacity for reproducible, data-driven figure generation directly within the publication workflow.

RXiv-Maker provides extensive capabilities for programmatic and reproducible figure generation directly from underlying data and source code, though researchers may choose traditional static figure inclusion based on their workflow preferences. When employed, this approach ensures that visualisations become dynamic artefacts, intrinsically linked to the research process and subject to the same rigorous version control as the manuscript text itself. <!--TODO: rewrite the next sentence to explain first how figure 1 is generated as a mermaid plot, and then talk about fig:2 --> To demonstrate this capability, we have configured RXiv-Maker to generate a visualisation depicting the growth of preprint submissions to the arXiv server from its inception to the present day (@fig:2).

This figure is rendered automatically during the article's compilation by executing a version-controlled Python script (`Figure_2.py`) found in `FIGURES/`. The script uses the Matplotlib and Pandas libraries to process a dataset of arxiv monthly submission statistics, whose snapshot copy is maintained within the repository. This methodology exemplifies a core aspect of transparent and reproducible science: the unbreakable link between data, analysis, and the resulting visualisation. Any modification to the dataset or the visualisation code will be automatically reflected in the manuscript upon recompilation, thus ensuring complete transparency, eliminating the possibility of data-figure mismatch, and allowing for full verifiability by peers. This self-generating figure serves as a direct validation of the RXiv-Maker system's capacity to streamline and safeguard the integrity of scientific reporting.
<br>

**Core Functionality Overview**

RXiv-Maker provides comprehensive manuscript authoring capabilities through its integrated toolchain. The system supports multiple input formats including standard markdown syntax, YAML-based metadata configuration, and BibTeX bibliography management. Figure generation encompasses both programmatic approaches through Python scripts and declarative diagram creation using Mermaid syntax, enabling researchers to maintain complete reproducibility whilst accommodating diverse visualisation requirements.

The compilation pipeline offers multiple deployment strategies to accommodate different research environments and computational preferences. Users can leverage GitHub Actions for automated cloud-based compilation, utilise Google Colab for interactive development and testing, or deploy locally using Docker containers with minimal system requirements. This flexibility ensures that RXiv-Maker remains accessible across different computational environments and institutional constraints.
<br>

**Comparative Analysis**

Table* 1: presents a detailed comparison of RXiv-Maker against established manuscript preparation systems, highlighting key differentiators in workflow integration, reproducibility features, and deployment flexibility.

| Feature | RXiv-Maker | Overleaf | Traditional LaTeX | R Markdown |
|---------|------------|----------|-------------------|------------|
| **Input Format** | Markdown + YAML | LaTeX | LaTeX | R Markdown |
| **Learning Curve** | Low | Medium | High | Medium |
| **Version Control** | Native Git | Limited | Git Compatible | Git Compatible |
| **Reproducible Figures** | Python + Mermaid | Manual | Manual | R Integration |
| **Collaboration** | GitHub-native | Web-based | File-based | Git-based |
| **Deployment Options** | GitHub Actions, Colab, Local Docker | Web-only | Local compilation | Local compilation |
| **Template System** | Automated conversion | Manual setup | Manual setup | Manual setup |
| **Citation Management** | BibTeX integration | BibTeX integration | BibTeX integration | BibTeX integration |
| **Containerisation** | Docker-native | N/A | Optional | Optional |
| **Continuous Integration** | GitHub Actions | N/A | Manual setup | Manual setup |

<!-- Discussion and conclusions section -->

RXiv-Maker responds directly to evolving demands of modern scientific communication. The programmatic generation of Figure 2 within this document validates our framework, demonstrating how figures become reproducible and verifiable components of the scientific record rather than static images. This approach mitigates common errors whilst the integration of Git, Docker, and GitHub Actions establishes a research environment where transparency and collaboration are structurally embedded. RXiv-Maker provides a foundational tool for research groups adopting structured, automated publishing approaches, enabling scientists to focus on research content whilst ensuring efficient and robust dissemination processes.

## Methods

The RXiv-Maker framework orchestrates a series of computational tools to achieve a fully automated publication pipeline. The process begins with manuscript content authored in Markdown (01_MAIN.md) and metadata defined in a separate YAML configuration file (00_CONFIG.yml). Bibliographic information is managed in a standard BibTeX file (03_REFERENCES.bib). The core of the system is a set of Python scripts located in src/py/ which parse the Markdown and YAML to dynamically generate a main LaTeX file (MANUSCRIPT.tex) from a template (src/tex/template.tex).

Figure generation is a key automated step. Mermaid diagrams (.mmd) and Python scripts (.py) placed in the FIGURES/ directory are executed to produce visual content. For instance, Figure 2 was generated by executing `FIGURES/Figure_2.py`, which processes data from `FIGURES/DATA/Figure_2/` `arxiv_monthly_submissions.csv`. The entire build process is managed by a Makefile and can be encapsulated within a Docker container defined by the Dockerfile, ensuring a consistent and reproducible compilation environment. Continuous integration and deployment are handled by GitHub Actions, which automates the compilation of the PDF upon every commit, making the latest version of the manuscript perpetually available.

## Data availability
Arxiv monthly submission data used in this article is available at [https://arxiv.org/stats/monthly_submissions](https://arxiv.org/stats/monthly_submissions). The source code and data for the figures in this article are available at [https://github.com/henriques/rxiv-maker](https://github.com/henriques/rxiv-maker).

## Code availability
The RXiv-Maker computational framework is available at [https://github.com/henriques/rxiv-maker](https://github.com/henriques/rxiv-maker). All source code is under an MIT License.

## Author contributions
Both Bruno M. Saraiva, Guillaume Jacquemet and Ricardo Henriques conceived the project and designed the framework. All authors contributed to writing and reviewing the manuscript.

## Acknowledgements
B.S. and R.H. acknowledge support from the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (grant agreement No. 101001332) (to R.H.) and funding from the European Union through the Horizon Europe program (AI4LIFE project with grant agreement 101057970-AI4LIFE and RT-SuperES project with grant agreement 101099654-RTSuperES to R.H.). Funded by the European Union. However, the views and opinions expressed are those of the authors only and do not necessarily reflect those of the European Union. Neither the European Union nor the granting authority can be held responsible for them. This work was also supported by a European Molecular Biology Organization (EMBO) installation grant (EMBO-2020-IG-4734 to R.H.), a Chan Zuckerberg Initiative Visual Proteomics Grant (vpi-0000000044 with https://doi.org/10.37921/743590vtudfp to R.H.) and a Chan Zuckerberg Initiative Essential Open Source Software for Science (EOSS6-0000000260). This study was supported by the Academy of Finland (no. 338537 to G.J.), the Sigrid Juselius Foundation (to G.J.), the Cancer Society of Finland (Syöpäjärjestöt, to G.J.) and the Solutions for Health strategic funding to Åbo Akademi University (to G.J.). This research was supported by InFLAMES Flagship Program of the Academy of Finland (decision no. 337531).
