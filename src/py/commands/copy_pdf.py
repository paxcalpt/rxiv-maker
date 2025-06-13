#!/usr/bin/env python3
"""
Standalone script to copy PDF with custom filename.

This script can be called from the Makefile or other build systems.
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import copy_pdf_to_base
from processors.yaml_processor import extract_yaml_metadata


def main():
    parser = argparse.ArgumentParser(description='Copy PDF to base directory with custom filename')
    parser.add_argument('--output-dir', '-o', default='output', help='Output directory containing ARTICLE.pdf')
    
    args = parser.parse_args()
    
    try:
        # Find and parse the article markdown (try new location first)
        article_md = Path.cwd() / "ARTICLE" / "00_ARTICLE.md"
        if not article_md.exists():
            # Fallback to old location for backward compatibility
            article_md = Path.cwd() / "00_ARTICLE.md"
            if not article_md.exists():
                raise FileNotFoundError("00_ARTICLE.md not found in ARTICLE/ or current directory")
        
        print(f"Reading metadata from: {article_md}")
        yaml_metadata = extract_yaml_metadata(article_md)
        
        # Copy PDF with custom filename
        result = copy_pdf_to_base(args.output_dir, yaml_metadata)
        
        if result:
            print("PDF copying completed successfully!")
        else:
            print("PDF copying failed!")
            return 1
        
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        print("Traceback:")
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())