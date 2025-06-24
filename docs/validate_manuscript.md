# Manuscript Validation Tool

The `validate_manuscript.py` script helps ensure that your manuscript directory contains all required files and has the proper structure before attempting to build the PDF.

## Usage

```bash
# Validate a manuscript directory
python src/py/scripts/validate_manuscript.py MANUSCRIPT

# Validate with verbose output
python src/py/scripts/validate_manuscript.py MANUSCRIPT --verbose

# Suppress informational messages
python src/py/scripts/validate_manuscript.py MANUSCRIPT --quiet
```

## What it checks

### Required Files
- `00_CONFIG.yml` - Configuration file with manuscript metadata
- `01_MAIN.md` - Main manuscript content in Markdown format  
- `03_REFERENCES.bib` - Bibliography file in BibTeX format

### Optional Files
- `02_SUPPLEMENTARY_INFO.md` - Supplementary information content

### Required Directories
- `FIGURES/` - Directory for manuscript figures

### Configuration Validation
The script validates the YAML configuration file and checks for required fields:
- `title` - Manuscript title
- `authors` - List of authors
- `date` - Publication date
- `keywords` - Keywords for the manuscript

### Content Validation
- Checks that the main manuscript file is readable and non-empty
- Validates that the bibliography file contains BibTeX entries
- Verifies figure references against files in the FIGURES directory

## Exit Codes

- `0` - Validation passed (may have warnings)
- `1` - Validation failed (has errors)

## Example Output

```
INFO: Validating manuscript: EXAMPLE_MANUSCRIPT
INFO: ✓ Manuscript directory found: EXAMPLE_MANUSCRIPT
INFO: ✓ Found required file: 00_CONFIG.yml
INFO: ✓ Found required file: 01_MAIN.md
INFO: ✓ Found required file: 03_REFERENCES.bib
INFO: ✓ Found required directory: FIGURES
INFO: ✓ Configuration file is valid
INFO: ✓ Bibliography file appears to contain BibTeX entries
INFO: ✓ Main manuscript file is readable and non-empty
INFO: ✓ Found optional file: 02_SUPPLEMENTARY_INFO.md

============================================================
MANUSCRIPT VALIDATION SUMMARY
============================================================
⚠️  Validation PASSED with warnings

⚠️  WARNINGS (1):
  1. Referenced figures not found: FIGURES/Figure_1.svg, FIGURES/Figure_2.svg
```

This tool is particularly useful for:
- Pre-build validation in CI/CD pipelines
- Local development workflow validation
- Troubleshooting manuscript build issues
- Ensuring manuscript completeness before submission
