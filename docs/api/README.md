# API Documentation

This directory contains the automatically generated API documentation for the rxiv-forge Python modules.

## Modules Overview

### Commands (`src/py/commands/`)
- **[copy_pdf](copy_pdf.py.md)** - PDF file copying utilities
- **[generate_figures](generate_figures.py.md)** - Figure generation commands
- **[generate_preprint](generate_preprint.py.md)** - Preprint generation commands
- **[generate_docs](generate_docs.py.md)** - Documentation generation commands

### Converters (`src/py/converters/`)
*Note: Some converter modules failed to generate documentation due to import dependencies*
- **[types](types.py.md)** - Type definitions and constants used in converters

### Processors (`src/py/processors/`)
- **[author_processor](author_processor.py.md)** - Author information processing
- **[template_processor](template_processor.py.md)** - Template processing utilities
- **[yaml_processor](yaml_processor.py.md)** - YAML configuration processing

### Utilities
- **[utils](utils.py.md)** - General utility functions

### Other Modules
- **[types](types.py.md)** - Type definitions and constants
- **[_version](_version.py.md)** - Version information

## How to Update Documentation

Documentation is automatically generated using [lazydocs](https://github.com/ml-tooling/lazydocs). To regenerate:

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

*Generated automatically by [lazydocs](https://github.com/ml-tooling/lazydocs)*