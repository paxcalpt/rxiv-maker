## Supplementary Figures

![**RXiv-Forge Workflow Details.** This figure provides a comprehensive overview of the RXiv-Forge system architecture, showing how the simplified file naming convention (00_CONFIG.yml, 01_MAIN.md, 02_SUPPLEMENTARY_INFO.md, 03_REFERENCES.bib) integrates with the processing engine to generate publication-ready documents. The system demonstrates the complete automation pipeline from markdown input to PDF output.](FIGURES/SFigure_1.svg){#sfig:1}

## Supplementary Notes

### File Structure and Organization

The RXiv-Forge system employs a streamlined file naming convention that enhances clarity and reduces redundancy. The new structure eliminates the word "MANUSCRIPT" from filenames, making the organization more intuitive:

- **00_CONFIG.yml**: Contains all metadata, author information, and configuration settings
- **01_MAIN.md**: Houses the primary manuscript content in markdown format  
- **02_SUPPLEMENTARY_INFO.md**: Provides additional supporting information and figures
- **03_REFERENCES.bib**: Manages bibliographic references in standard BibTeX format

### Technical Implementation Details

The system processes these files through a sophisticated conversion pipeline that:

1. **Parses configuration**: Extracts metadata from the YAML configuration file
2. **Converts content**: Transforms markdown syntax into LaTeX formatting
3. **Generates figures**: Executes Python scripts and Mermaid diagrams automatically
4. **Assembles document**: Combines all components into a cohesive LaTeX document
5. **Compiles output**: Produces publication-ready PDF with proper formatting and citations

This approach ensures **reproducibility**, **version control compatibility**, and **automated processing** while maintaining the flexibility needed for academic publishing.
