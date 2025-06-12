"""
Template processing utilities for Article-Forge.

This module handles template content generation and replacement operations.
"""

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from converters.md2tex import extract_content_sections
from processors.author_processor import (
    generate_authors_and_affiliations,
    generate_corresponding_authors,
    generate_extended_author_info
)


def get_template_path():
    """Get the path to the template file"""
    return Path(__file__).parent.parent.parent / "tex" / "template.tex"


def generate_keywords(yaml_metadata):
    """Generate LaTeX keywords section from YAML metadata"""
    keywords = yaml_metadata.get('keywords', [])
    
    if not keywords:
        return "% No keywords found\n"
    
    # Join keywords with ' | ' separator
    keywords_str = ' | '.join(keywords)
    
    result = "\\begin{keywords}\n"
    result += keywords_str
    result += "\n\\end{keywords}"
    
    return result


def generate_bibliography(yaml_metadata):
    """Generate LaTeX bibliography section from YAML metadata"""
    bibliography = yaml_metadata.get('bibliography', '02_REFERENCES')
    
    # Remove .bib extension if present
    if bibliography.endswith('.bib'):
        bibliography = bibliography[:-4]
    
    return f"\\bibliography{{{bibliography}}}"


def process_template_replacements(template_content, yaml_metadata, article_md):
    """Process all template replacements with metadata and content"""
    
    # Process line numbers
    txt = ""
    if 'use_line_numbers' in yaml_metadata:
        use_line_numbers = str(yaml_metadata['use_line_numbers']).lower() == 'true'
        if use_line_numbers:
            txt = "% Add number to the lines\n\\usepackage{lineno}\n\\linenumbers\n"            
    template_content = template_content.replace("<PY-RPL:USE-LINE-NUMBERS>", txt)

    # Process lead author
    lead_author = "Unknown"
    if 'title' in yaml_metadata:
        title_data = yaml_metadata['title']
        if isinstance(title_data, list):
            for item in title_data:
                if isinstance(item, dict) and 'lead_author' in item:
                    lead_author = item['lead_author']
                    break
        elif isinstance(title_data, dict) and 'lead_author' in title_data:
            lead_author = title_data['lead_author']
    
    if lead_author == "Unknown" and 'authors' in yaml_metadata and yaml_metadata['authors']:
        # get the last name of the first author
        first_author = yaml_metadata['authors'][0]
        if isinstance(first_author, dict) and 'name' in first_author:
            lead_author = first_author['name'].split()[-1]
        elif isinstance(first_author, str):
            lead_author = first_author.split()[-1]
    txt = f"\\leadauthor{{{lead_author}}}\n"
    template_content = template_content.replace("<PY-RPL:LEAD-AUTHOR>", txt)

    # Process long title
    long_title = "Untitled Article"
    if 'title' in yaml_metadata:
        if isinstance(yaml_metadata['title'], dict) and 'long' in yaml_metadata['title']:
            long_title = yaml_metadata['title']['long']
        elif isinstance(yaml_metadata['title'], list):
            for item in yaml_metadata['title']:
                if isinstance(item, dict) and 'long' in item:
                    long_title = item['long']
                    break
        elif isinstance(yaml_metadata['title'], str):
            long_title = yaml_metadata['title']
    txt = f"\\title{{{long_title}}}\n"
    template_content = template_content.replace("<PY-RPL:LONG-TITLE-STR>", txt)

    # Process short title
    short_title = "Untitled"
    if 'title' in yaml_metadata:
        if isinstance(yaml_metadata['title'], dict) and 'short' in yaml_metadata['title']:
            short_title = yaml_metadata['title']['short']
        elif isinstance(yaml_metadata['title'], list):
            for item in yaml_metadata['title']:
                if isinstance(item, dict) and 'short' in item:
                    short_title = item['short']
                    break
        elif isinstance(yaml_metadata['title'], str):
            short_title = yaml_metadata['title'][:50] + "..." if len(yaml_metadata['title']) > 50 else yaml_metadata['title']
    txt = f"\\shorttitle{{{short_title}}}\n"
    template_content = template_content.replace("<PY-RPL:SHORT-TITLE-STR>", txt)

    # Generate authors and affiliations dynamically
    authors_and_affiliations = generate_authors_and_affiliations(yaml_metadata)
    template_content = template_content.replace("<PY-RPL:AUTHORS-AND-AFFILIATIONS>", authors_and_affiliations)

    # Generate corresponding authors section
    corresponding_authors = generate_corresponding_authors(yaml_metadata)
    template_content = template_content.replace("<PY-RPL:CORRESPONDING-AUTHORS>", corresponding_authors)

    # Generate extended author information section
    extended_author_info = generate_extended_author_info(yaml_metadata)
    template_content = template_content.replace("<PY-RPL:EXTENDED-AUTHOR-INFO>", extended_author_info)

    # Generate keywords section
    keywords_section = generate_keywords(yaml_metadata)
    template_content = template_content.replace("<PY-RPL:KEYWORDS>", keywords_section)

    # Generate bibliography section
    bibliography_section = generate_bibliography(yaml_metadata)
    template_content = template_content.replace("<PY-RPL:BIBLIOGRAPHY>", bibliography_section)

    # Extract content sections from markdown
    content_sections = extract_content_sections(article_md)
    
    # Replace content placeholders with extracted sections
    template_content = template_content.replace("<PY-RPL:ABSTRACT>", content_sections.get('abstract', ''))
    template_content = template_content.replace("<PY-RPL:MAIN-CONTENT>", content_sections.get('main', ''))
    template_content = template_content.replace("<PY-RPL:METHODS>", content_sections.get('methods', ''))
    template_content = template_content.replace("<PY-RPL:DATA-AVAILABILITY>", content_sections.get('data_availability', ''))
    template_content = template_content.replace("<PY-RPL:CODE-AVAILABILITY>", content_sections.get('code_availability', ''))
    template_content = template_content.replace("<PY-RPL:AUTHOR-CONTRIBUTIONS>", content_sections.get('author_contributions', ''))
    template_content = template_content.replace("<PY-RPL:ACKNOWLEDGEMENTS>", content_sections.get('acknowledgements', ''))

    return template_content
