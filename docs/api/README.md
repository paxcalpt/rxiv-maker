# API Documentation

This directory contains the automatically generated API documentation for the rxiv-forge Python modules.

## Quick Navigation

- [Main Package](rxiv_maker.md) - Main package overview
- [Commands](commands/) - Command-line interface modules
- [Converters](converters/) - Markdown to LaTeX conversion modules
- [Processors](processors/) - Document processing modules

## Modules Overview

### Commands (`src/py/commands/`)
- **[copy_pdf](commands/copy_pdf.md)** - PDF file copying utilities
- **[generate_figures](commands/generate_figures.md)** - Figure generation commands
- **[generate_preprint](commands/generate_preprint.md)** - Preprint generation commands

### Converters (`src/py/converters/`)
- **[citation_processor](converters/citation_processor.md)** - Citation processing utilities
- **[code_processor](converters/code_processor.md)** - Code block processing
- **[figure_processor](converters/figure_processor.md)** - Figure processing and conversion
- **[html_processor](converters/html_processor.md)** - HTML processing utilities
- **[list_processor](converters/list_processor.md)** - List formatting utilities
- **[md2tex](converters/md2tex.md)** - Main Markdown to LaTeX converter
- **[section_processor](converters/section_processor.md)** - Section processing utilities
- **[supplementary_note_processor](converters/supplementary_note_processor.md)** - Supplementary material processing
- **[table_processor](converters/table_processor.md)** - Table processing utilities
- **[text_formatters](converters/text_formatters.md)** - Text formatting utilities
- **[url_processor](converters/url_processor.md)** - URL processing utilities

### Processors (`src/py/processors/`)
- **[author_processor](processors/author_processor.md)** - Author information processing
- **[template_processor](processors/template_processor.md)** - Template processing utilities
- **[yaml_processor](processors/yaml_processor.md)** - YAML configuration processing

### Utilities
- **[utils](utils.md)** - General utility functions

## How to Update Documentation

Documentation is automatically generated using [pdoc](https://pdoc.dev/). To regenerate:

```bash
# Generate documentation
make docs

# Preview documentation locally
make docs-serve
```

The documentation is generated in markdown format and can be viewed directly on GitHub without requiring GitHub Pages.

## Documentation Coverage

This documentation covers all public modules, classes, and functions in the rxiv-forge codebase. Each module page includes:

- Module overview and purpose
- Class definitions with methods
- Function signatures and docstrings
- Usage examples where available
- Cross-references to related modules

---

*Generated automatically by [pdoc](https://pdoc.dev/)*