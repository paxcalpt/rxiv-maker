"""
Utility functions for Article-Forge.

This module contains general utility functions used across the Article-Forge system.
"""

import os
import shutil
from pathlib import Path


def create_output_dir(output_dir):
    """Create output directory if it doesn't exist"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    else:
        print(f"Output directory already exists: {output_dir}")


def find_article_md():
    """Look for 00_ARTICLE.md in the ARTICLE directory"""
    current_dir = Path.cwd()
    
    # First try the new ARTICLE directory structure
    article_md = current_dir / "ARTICLE" / "00_ARTICLE.md"
    if article_md.exists():
        return article_md
    
    # Fallback to old location for backward compatibility
    article_md = current_dir / "00_ARTICLE.md"
    if article_md.exists():
        return article_md
    
    raise FileNotFoundError(f"00_ARTICLE.md not found in {current_dir}/ARTICLE/ or {current_dir}")


def write_article_output(output_dir, template_content):
    """Write the generated article to the output directory"""
    output_file = Path(output_dir) / "ARTICLE.tex"
    with open(output_file, 'w') as file:
        file.write(template_content)
    
    print(f"Generated article: {output_file}")
    return output_file


def get_custom_pdf_filename(yaml_metadata):
    """Generate custom PDF filename from metadata"""
    # Extract date (year only)
    date = yaml_metadata.get('date', '2024')
    year = date[:4] if isinstance(date, str) and len(date) >= 4 else '2024'
    
    # Extract lead_author from title metadata
    title_info = yaml_metadata.get('title', {})
    if isinstance(title_info, list):
        # Find lead_author in the list
        lead_author = None
        for item in title_info:
            if isinstance(item, dict) and 'lead_author' in item:
                lead_author = item['lead_author']
                break
        if not lead_author:
            lead_author = 'unknown'
    elif isinstance(title_info, dict):
        lead_author = title_info.get('lead_author', 'unknown')
    else:
        lead_author = 'unknown'
    
    # Clean the lead author name (remove spaces, make lowercase)
    lead_author_clean = lead_author.lower().replace(' ', '_').replace('.', '')
    
    # Generate filename: year__lead_author_et_al__article_forge.pdf
    filename = f"{year}__{lead_author_clean}_et_al__article_forge.pdf"
    
    return filename


def copy_pdf_to_base(output_dir, yaml_metadata):
    """Copy generated PDF to base directory with custom filename"""
    output_pdf = Path(output_dir) / "ARTICLE.pdf"
    
    if not output_pdf.exists():
        print(f"Warning: PDF not found at {output_pdf}")
        return None
    
    # Generate custom filename
    custom_filename = get_custom_pdf_filename(yaml_metadata)
    base_pdf_path = Path.cwd() / custom_filename
    
    try:
        shutil.copy2(output_pdf, base_pdf_path)
        print(f"✅ PDF copied to: {base_pdf_path}")
        return base_pdf_path
    except Exception as e:
        print(f"Error copying PDF: {e}")
        return None
