"""Utility modules for RXiv-Maker.

This package contains utility functions for various tasks including
email encoding/decoding and other helper functions.
"""

# Import functions from utils.py at the parent level
import sys
from pathlib import Path

from .email_encoder import (
    decode_email,
    encode_author_emails,
    encode_email,
    process_author_emails,
)

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils import copy_pdf_to_manuscript_folder, find_manuscript_md
except ImportError:
    # If utils.py is not accessible, define minimal versions
    import os
    import shutil

    def find_manuscript_md():
        current_dir = Path(__file__).parent.parent.parent.parent
        manuscript_path = os.getenv("MANUSCRIPT_PATH", "MANUSCRIPT")
        manuscript_md = current_dir / manuscript_path / "01_MAIN.md"
        if manuscript_md.exists():
            return manuscript_md
        raise FileNotFoundError(
            f"Main manuscript file 01_MAIN.md not found in "
            f"{current_dir}/{manuscript_path}/"
        )

    def copy_pdf_to_manuscript_folder(output_dir, yaml_metadata):
        output_pdf = Path(output_dir) / "MANUSCRIPT.pdf"
        if not output_pdf.exists():
            print(f"Warning: PDF not found at {output_pdf}")
            return None

        manuscript_path = os.getenv("MANUSCRIPT_PATH", "MANUSCRIPT")
        # Simple filename generation
        current_year = "2025"
        filename = f"{current_year}__manuscript_et_al__rxiv.pdf"
        manuscript_pdf_path = (
            Path(__file__).parent.parent.parent.parent / manuscript_path / filename
        )

        try:
            shutil.copy2(output_pdf, manuscript_pdf_path)
            print(f"✅ PDF copied to manuscript folder: {manuscript_pdf_path}")
            return manuscript_pdf_path
        except Exception as e:
            print(f"Error copying PDF: {e}")
            return None


__all__ = [
    "decode_email",
    "encode_author_emails",
    "encode_email",
    "process_author_emails",
    "find_manuscript_md",
    "copy_pdf_to_manuscript_folder",
]
