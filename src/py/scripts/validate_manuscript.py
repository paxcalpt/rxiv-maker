#!/usr/bin/env python3
"""Manuscript Validation Script for RXiv-Maker.

This script validates that a manuscript directory contains all required files
and has the proper structure before attempting to build the PDF.

The validator checks for:
- Required files (config, main content, bibliography)
- Required directories (figures)
- Configuration file validity
- Basic content structure
- Figure reference consistency
"""

import argparse
import logging
import sys
from pathlib import Path

import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class ManuscriptValidator:
    """Validates manuscript structure and requirements for RXiv-Maker."""

    REQUIRED_FILES = {
        "00_CONFIG.yml": "Configuration file with manuscript metadata",
        "01_MAIN.md": "Main manuscript content in Markdown format",
        "03_REFERENCES.bib": "Bibliography file in BibTeX format",
    }

    OPTIONAL_FILES = {
        "02_SUPPLEMENTARY_INFO.md": "Supplementary information content",
    }

    REQUIRED_DIRS = {
        "FIGURES": "Directory for manuscript figures",
    }

    REQUIRED_CONFIG_FIELDS = {
        "title": "Manuscript title",
        "authors": "List of authors",
        "date": "Publication date",
        "keywords": "Keywords for the manuscript",
    }

    def __init__(self, manuscript_path: Path):
        """Initialize validator with manuscript directory path."""
        self.manuscript_path = Path(manuscript_path)
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def validate_directory_structure(self) -> bool:
        """Validate that the manuscript directory exists and is accessible."""
        if not self.manuscript_path.exists():
            self.errors.append(
                f"Manuscript directory not found: {self.manuscript_path}"
            )
            return False

        if not self.manuscript_path.is_dir():
            self.errors.append(f"Path is not a directory: {self.manuscript_path}")
            return False

        logger.info(f"✓ Manuscript directory found: {self.manuscript_path}")
        return True

    def validate_required_files(self) -> bool:
        """Check for required files in the manuscript directory."""
        all_files_present = True

        for filename, description in self.REQUIRED_FILES.items():
            file_path = self.manuscript_path / filename
            if not file_path.exists():
                self.errors.append(f"Required file missing: {filename} ({description})")
                all_files_present = False
            else:
                logger.info(f"✓ Found required file: {filename}")

        return all_files_present

    def validate_optional_files(self) -> None:
        """Check for optional files and warn if missing."""
        for filename, description in self.OPTIONAL_FILES.items():
            file_path = self.manuscript_path / filename
            if not file_path.exists():
                self.warnings.append(
                    f"Optional file missing: {filename} ({description})"
                )
            else:
                logger.info(f"✓ Found optional file: {filename}")

    def validate_required_directories(self) -> bool:
        """Check for required directories."""
        all_dirs_present = True

        for dirname, description in self.REQUIRED_DIRS.items():
            dir_path = self.manuscript_path / dirname
            if not dir_path.exists():
                self.errors.append(
                    f"Required directory missing: {dirname} ({description})"
                )
                all_dirs_present = False
            elif not dir_path.is_dir():
                self.errors.append(f"Path exists but is not a directory: {dirname}")
                all_dirs_present = False
            else:
                logger.info(f"✓ Found required directory: {dirname}")

        return all_dirs_present

    def validate_config_file(self) -> bool:
        """Validate the configuration YAML file."""
        config_path = self.manuscript_path / "00_CONFIG.yml"
        if not config_path.exists():
            # This error is already caught in validate_required_files
            return False

        try:
            with open(config_path, encoding="utf-8") as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML in config file: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Error reading config file: {e}")
            return False

        if not isinstance(config, dict):
            self.errors.append("Config file must contain a YAML dictionary")
            return False

        # Check required fields
        config_valid = True
        for field, description in self.REQUIRED_CONFIG_FIELDS.items():
            if field not in config:
                self.errors.append(
                    f"Missing required config field: {field} ({description})"
                )
                config_valid = False
            elif not config[field]:
                self.warnings.append(f"Config field is empty: {field} ({description})")

        if config_valid:
            logger.info("✓ Configuration file is valid")

        return config_valid

    def validate_bibliography(self) -> bool:
        """Basic validation of the bibliography file."""
        bib_path = self.manuscript_path / "03_REFERENCES.bib"
        if not bib_path.exists():
            # This error is already caught in validate_required_files
            return False

        try:
            with open(bib_path, encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            self.errors.append(f"Error reading bibliography file: {e}")
            return False

        # Basic check for BibTeX entries
        if not content.strip():
            self.warnings.append("Bibliography file is empty")
        elif "@" not in content:
            self.warnings.append(
                "Bibliography file appears to contain no BibTeX entries"
            )
        else:
            logger.info("✓ Bibliography file appears to contain BibTeX entries")

        return True

    def validate_main_content(self) -> bool:
        """Basic validation of the main manuscript file."""
        main_path = self.manuscript_path / "01_MAIN.md"
        if not main_path.exists():
            # This error is already caught in validate_required_files
            return False

        try:
            with open(main_path, encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            self.errors.append(f"Error reading main manuscript file: {e}")
            return False

        if not content.strip():
            self.errors.append("Main manuscript file is empty")
            return False

        # Check for common sections
        content_lower = content.lower()
        common_sections = [
            "abstract",
            "introduction",
            "methods",
            "results",
            "discussion",
        ]
        found_sections = [
            section for section in common_sections if section in content_lower
        ]

        if len(found_sections) < 2:
            self.warnings.append(
                f"Main manuscript appears to have few standard sections. "
                f"Found: {', '.join(found_sections) if found_sections else 'none'}"
            )

        logger.info("✓ Main manuscript file is readable and non-empty")
        return True

    def check_figure_references(self) -> None:
        """Check if referenced figures exist in the FIGURES directory."""
        main_path = self.manuscript_path / "01_MAIN.md"
        figures_dir = self.manuscript_path / "FIGURES"

        if not main_path.exists() or not figures_dir.exists():
            return

        try:
            with open(main_path, encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return

        # Simple regex to find figure references
        import re

        figure_refs = re.findall(r"!\[.*?\]\((FIGURES/[^)]+)\)", content)

        missing_figures = []
        for fig_ref in figure_refs:
            fig_path = self.manuscript_path / fig_ref
            if not fig_path.exists():
                missing_figures.append(fig_ref)

        if missing_figures:
            self.warnings.append(
                f"Referenced figures not found: {', '.join(missing_figures)}"
            )
        elif figure_refs:
            logger.info(f"✓ All {len(figure_refs)} referenced figures found")

    def validate(self) -> bool:
        """Run all validation checks."""
        logger.info(f"Validating manuscript: {self.manuscript_path}")

        # Check directory structure first
        if not self.validate_directory_structure():
            return False

        # Run all validation checks
        checks = [
            self.validate_required_files,
            self.validate_required_directories,
            self.validate_config_file,
            self.validate_bibliography,
            self.validate_main_content,
        ]

        validation_passed = all(check() for check in checks)

        # Run optional checks that don't affect overall validation
        self.validate_optional_files()
        self.check_figure_references()

        return validation_passed

    def print_summary(self) -> None:
        """Print validation summary."""
        print("\n" + "=" * 60)
        print("MANUSCRIPT VALIDATION SUMMARY")
        print("=" * 60)

        if not self.errors and not self.warnings:
            print("✅ Validation PASSED - No issues found!")
        elif not self.errors:
            print("⚠️  Validation PASSED with warnings")
        else:
            print("❌ Validation FAILED")

        if self.errors:
            print(f"\n🚨 ERRORS ({len(self.errors)}):")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")

        print("\n" + "=" * 60)


def main():
    """Main entry point for the manuscript validator."""
    parser = argparse.ArgumentParser(
        description="Validate RXiv-Maker manuscript structure and requirements",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s MANUSCRIPT
  %(prog)s EXAMPLE_MANUSCRIPT
  %(prog)s path/to/my/manuscript --verbose
        """,
    )

    parser.add_argument(
        "manuscript_path",
        help="Path to the manuscript directory to validate",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress informational messages",
    )

    args = parser.parse_args()

    # Configure logging level
    if args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate the manuscript
    validator = ManuscriptValidator(args.manuscript_path)
    validation_passed = validator.validate()
    validator.print_summary()

    # Exit with appropriate code
    sys.exit(0 if validation_passed else 1)


if __name__ == "__main__":
    main()
