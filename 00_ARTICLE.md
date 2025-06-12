---
title: 
  - long: "Article-Forge: An Automated Template Engine for Streamlined Scientific Publications"
  - short: "Article-Forge"
  - lead_author: "Saraiva"

date: "2025-06-12"
version: "1.0.0"
status: "draft"
use_line_numbers: true

keywords:
  - "article template"
  - "scientific publishing"
  - "preprints"
  
authors:
  - name: "Bruno M. Saraiva"
    affiliations:
      - "ITQB NOVA"
    corresponding_author: true
    co_first_author: false
    email: "b.saraiva@itqb.unl.pt"
    orcid: 0000-0002-9151-5477
    x: "@Bruno_MSaraiva"
    linkedin: "bruno-saraiva"
  - name: "Guillaume Jaquemet"
    affiliations:
      - "Åbo"
      - "InFlames"
      - "Turku Bioscience"
    corresponding_author: true
    co_first_author: false
    email: "guillaume.jacquemet@abo.fi"
    orcid: 0000-0002-9286-920X
    twitter: "@guijacquemet"
    bluesky: "@guijacquemet.bsky.social"
  - name: "Ricardo Henriques"
    affiliations:
      - "ITQB NOVA"
      - "UCL"
    corresponding_author: true
    co_first_author: false
    email: "ricardo.henriques@itqb.unl.pt"
    orcid: 0000-0002-1234-5678
    bluesky: "@henriqueslab.bsky.social"
    x: "@HenriquesLab"
    linkedin: "ricardo-henriques"
affiliations:
  - shortname: "ITQB NOVA"
    full_name: "Instituto de Tecnologia Química e Biológica António Xavier, Universidade Nova de Lisboa"
    location: "Oeiras, Portugal"
  - shortname: "UCL"
    full_name: "UCL Laboratory for Molecular Cell Biology, University College London"
    location: "London, United Kingdom"
  - shortname: "Åbo"
    full_name: "Faculty of Science and Engineering, Cell Biology, Åbo Akademi University"
    location: "Turku, Finland"
  - shortname: "InFlames"
    full_name: "InFLAMES Research Flagship Center, University of Turku"
    location: "Turku, Finland"
  - shortname: "Turku Bioscience"
    full_name: "Turku Bioscience Centre, University of Turku and Åbo Akademi University"
    location: "Turku, Finland"

bibliography: 02_REFERENCES.bib
---

# Article-Forge: An Automated Template Engine for Streamlined Scientific Publications

## Abstract
Modern scientific publishing has shifted towards rapid dissemination through preprint servers, placing increased demands on researchers for manuscript preparation and quality control. We present Article-Forge, a comprehensive GitHub-native system that integrates modern software development practices into scientific article lifecycles. This system combines professional LaTeX typesetting with robust automation and reproducibility infrastructure. Article-Forge facilitates transparent version control through Git, ensures consistent environments via Docker containerisation, and automates compilation using GitHub Actions. A key innovation is the programmatic figure generation pipeline using Python libraries like Matplotlib and Seaborn to create publication-quality, version-controlled visualisations. This self-documenting article demonstrates the system's capabilities, showcasing how it transforms scientific authoring into an efficient, collaborative, and reproducible process. Article-Forge serves as a foundational tool for research groups adopting structured, automated approaches to preprint publication, enabling scientists to focus on their primary objective: the research itself.

## Main

<!-- Introduction -->
The landscape of scientific publishing has undergone a profound transformation over the past two decades, fundamentally altering how researchers communicate, collaborate, and disseminate their findings. This evolution represents more than a simple digitisation of traditional publishing models; it constitutes a paradigmatic shift towards open, reproducible, and accelerated scientific discourse that challenges the very foundations of how knowledge is created and shared within the global research community.
The emergence of preprint servers has been central to this transformation, with platforms such as arXiv, bioRxiv, and medRxiv collectively hosting millions of manuscripts that bypass the traditional peer-review bottleneck. The exponential growth in preprint submissions, particularly evident during the COVID-19 pandemic, demonstrates researchers' increasing recognition that rapid dissemination of findings serves both individual career advancement and broader scientific progress [@Fraser2021_preprint_growth;@Abdill2019_biorxiv_growth]. This shift towards immediate publication reflects a growing understanding that the traditional publishing timeline, often spanning months or years, is fundamentally incompatible with the pace of modern scientific discovery and the urgent need for real-time knowledge sharing in addressing global challenges.
Concurrent with the preprint revolution, the integration of computational tools and automated workflows has become indispensable to contemporary research practice. Version control systems, particularly Git and GitHub, have evolved from software development tools into essential platforms for scientific collaboration, enabling transparent tracking of research progress, collaborative manuscript development, and reproducible computational analyses [@Ram2013_git_science;@Perez-Riverol2016_github_bioinformatics]. The adoption of containerisation technologies such as Docker has further enhanced reproducibility by providing standardised computational environments that eliminate the "works on my machine" problem that has long plagued scientific computing [@Boettiger2015_docker_reproducibility].
The traditional manuscript preparation process, however, has remained largely unchanged, relying on fragmented workflows that separate content creation, figure generation, and document compilation into discrete, often incompatible processes. Authors typically navigate between multiple software environments—word processors for text, specialised software for data analysis and visualisation, reference managers for citations, and various formatting tools for journal submission requirements. This fragmentation introduces numerous opportunities for error, version conflicts, and inefficiencies that ultimately impede rather than facilitate scientific communication.
Contemporary research increasingly demands sophisticated figure generation capabilities that integrate statistical analysis, publication-quality visualisation, and complex workflow documentation. The matplotlib and seaborn libraries have emerged as foundational tools for scientific visualisation in Python, offering extensive customisation options and LaTeX integration essential for professional publication standards [@Hunter2007_matplotlib;@Waskom2021_seaborn]. Similarly, diagram generation tools such as Mermaid have revolutionised the creation of methodology flowcharts and system architecture documentation, enabling researchers to communicate complex processes with unprecedented clarity and precision [@Mermaid2023_documentation].
The convergence of these technological developments creates both an opportunity and a necessity for integrated publishing workflows that leverage automation, version control, and reproducible computational environments. Modern research groups require systems that seamlessly integrate content creation, data analysis, figure generation, and document compilation within a unified, version-controlled framework. Such systems must accommodate collaborative authoring, automated quality assurance, and flexible output formatting whilst maintaining the rigorous standards expected in academic publishing.
Article-Forge addresses these requirements by implementing a comprehensive automated publishing system that integrates LaTeX document preparation with Python-based figure generation, containerised build environments, and continuous integration workflows. The system represents a practical implementation of best practices in reproducible research, combining the typographical excellence of LaTeX with the computational power of modern data science tools and the collaborative advantages of distributed version control systems.
The architecture of Article-Forge reflects a deep understanding of contemporary research workflows, providing automated figure generation through matplotlib and seaborn for statistical visualisation, integrated Mermaid diagram creation for methodology documentation, and robust build automation through Make and Docker. The system's integration with GitHub Actions enables continuous integration and automated deployment, ensuring that manuscript updates trigger automatic recompilation and quality assurance checks without manual intervention.
This integration of diverse technological components addresses a fundamental challenge in modern scientific publishing: the need to maintain rigorous quality standards whilst accelerating the publication process and enhancing collaborative capabilities. By automating routine tasks and providing standardised workflows, Article-Forge enables researchers to focus on scientific content whilst ensuring that technical implementation adheres to contemporary best practices in software development and computational reproducibility.
The following sections detail the technical implementation of this integrated publishing system, demonstrating how modern computational tools can be orchestrated to create a seamless workflow from initial content creation through final publication-ready output. This approach represents a significant advancement in scientific publishing infrastructure, providing a template for future developments in automated, reproducible, and collaborative academic communication.

<!-- Results -->

Blablabla

<!-- Discussion and conclusions section -->

Blablabla

## Methods
Blablabla

## Data availability

Blablabla

## Code availability

The Article-Forge computational framework is available at [https://github.com/henriqueslab/article-forge](https://github.com/henriqueslab/article-forge). All source code is under an MIT License.

## Author contributions

Both Bruno M. Saraiva, Guillaume Jaquemet and Ricardo Henriques conceived the project and designed the framework. All authors contributed to writing and reviewing the manuscript.

## Acknowledgements

Blablabla