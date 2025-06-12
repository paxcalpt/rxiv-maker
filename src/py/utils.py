"""
Utility functions for Article-Forge.

This module contains general utility functions used across the Article-Forge system.
"""

import os
from pathlib import Path


def create_output_dir(output_dir):
    """Create output directory if it doesn't exist"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    else:
        print(f"Output directory already exists: {output_dir}")


def find_article_md():
    """Look for 00_ARTICLE.md in the current directory"""
    current_dir = Path.cwd()
    article_md = current_dir / "00_ARTICLE.md"
    if article_md.exists():
        return article_md
    else:
        raise FileNotFoundError(f"00_ARTICLE.md not found in {current_dir}")


def write_article_output(output_dir, template_content):
    """Write the generated article to the output directory"""
    output_file = Path(output_dir) / "ARTICLE.tex"
    with open(output_file, 'w') as file:
        file.write(template_content)
    
    print(f"Generated article: {output_file}")
    return output_file
