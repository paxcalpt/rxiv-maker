"""Template processing utilities for RXiv-Forge.

This module handles template content generation and replacement operations.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import os

from converters.md2tex import extract_content_sections
from processors.author_processor import (
    generate_authors_and_affiliations,
    generate_corresponding_authors,
    generate_extended_author_info,
)


def get_template_path():
    """Get the path to the template file"""
    return Path(__file__).parent.parent.parent / "tex" / "template.tex"


def find_supplementary_md():
    """Find supplementary information file in the manuscript directory"""
    current_dir = Path.cwd()
    manuscript_path = os.getenv("MANUSCRIPT_PATH", "MANUSCRIPT")

    # Look for supplementary file: 02_SUPPLEMENTARY_INFO.md
    supplementary_md = current_dir / manuscript_path / "02_SUPPLEMENTARY_INFO.md"
    if supplementary_md.exists():
        return supplementary_md

    return None


def generate_supplementary_tex(output_dir):
    """Generate Supplementary.tex file from supplementary markdown"""
    from converters.md2tex import convert_markdown_to_latex

    supplementary_md = find_supplementary_md()
    if not supplementary_md:
        # Create empty supplementary file
        supplementary_tex_path = Path(output_dir) / "Supplementary.tex"
        with open(supplementary_tex_path, "w") as f:
            f.write("% No supplementary information provided\n")
        return

    # Read and convert supplementary markdown to LaTeX
    with open(supplementary_md) as f:
        supplementary_content = f.read()

    # Convert markdown to LaTeX
    supplementary_latex = convert_markdown_to_latex(supplementary_content)

    # Set up supplementary figure and table environment and numbering
    supplementary_setup = """% Setup for supplementary figures
\\newcounter{sfigure}
\\renewcommand{\\figurename}{Sup. Fig.}
\\newenvironment{sfigure}[1][ht]{%
    \\renewcommand{\\thefigure}{\\arabic{sfigure}}%
    \\setcounter{figure}{0}%
    \\stepcounter{sfigure}%
    \\begin{figure}[#1]%
}{%
    \\end{figure}%
}

% Setup for supplementary tables
\\newcounter{stable}
\\renewcommand{\\tablename}{Sup. Table}
\\newenvironment{stable}[1][ht]{%
    \\renewcommand{\\thetable}{\\arabic{stable}}%
    \\setcounter{table}{0}%
    \\stepcounter{stable}%
    \\begin{table}[#1]%
}{%
    \\end{table}%
}

% Setup for supplementary two-column tables
\\newenvironment{stable*}[1][ht]{%
    \\renewcommand{\\thetable}{\\arabic{stable}}%
    \\setcounter{table}{0}%
    \\stepcounter{stable}%
    \\begin{table*}[#1]%
}{%
    \\end{table*}%
}

"""

    # Process the LaTeX to convert figure environments to sfigure environments
    # Replace \begin{figure} with \begin{sfigure} and \end{figure} with \end{sfigure}
    supplementary_latex = supplementary_latex.replace(
        "\\begin{figure}", "\\begin{sfigure}"
    )
    supplementary_latex = supplementary_latex.replace("\\end{figure}", "\\end{sfigure}")

    # Process the LaTeX to convert table environments to stable environments
    # Replace \begin{table} with \begin{stable} and \end{table} with \end{stable}
    supplementary_latex = supplementary_latex.replace(
        "\\begin{table}", "\\begin{stable}"
    )
    supplementary_latex = supplementary_latex.replace("\\end{table}", "\\end{stable}")

    # Also handle two-column tables
    supplementary_latex = supplementary_latex.replace(
        "\\begin{table*}", "\\begin{stable*}"
    )
    supplementary_latex = supplementary_latex.replace("\\end{table*}", "\\end{stable*}")

    # Combine setup and content
    final_latex = supplementary_setup + supplementary_latex

    # Write Supplementary.tex file
    supplementary_tex_path = Path(output_dir) / "Supplementary.tex"
    with open(supplementary_tex_path, "w") as f:
        f.write(final_latex)

    print(f"Generated supplementary information: {supplementary_tex_path}")


def generate_keywords(yaml_metadata):
    """Generate LaTeX keywords section from YAML metadata"""
    keywords = yaml_metadata.get("keywords", [])

    if not keywords:
        return "% No keywords found\n"

    # Join keywords with ' | ' separator
    keywords_str = " | ".join(keywords)

    result = "\\begin{keywords}\n"
    result += keywords_str
    result += "\n\\end{keywords}"

    return result


def generate_bibliography(yaml_metadata):
    """Generate LaTeX bibliography section from YAML metadata"""
    bibliography = yaml_metadata.get("bibliography", "02_REFERENCES")

    # Remove .bib extension if present
    if bibliography.endswith(".bib"):
        bibliography = bibliography[:-4]

    return f"\\bibliography{{{bibliography}}}"


def count_words_in_text(text):
    """Count words in text, excluding LaTeX commands"""
    import re

    # Remove LaTeX commands (backslash followed by word characters)
    text_no_latex = re.sub(r"\\[a-zA-Z]+\{[^}]*\}", "", text)
    text_no_latex = re.sub(r"\\[a-zA-Z]+", "", text_no_latex)
    # Remove remaining LaTeX markup
    text_no_latex = re.sub(r"[{}\\]", " ", text_no_latex)
    # Split by whitespace and count non-empty words
    words = [word.strip() for word in text_no_latex.split() if word.strip()]
    return len(words)


def analyze_section_word_counts(content_sections):
    """Analyze word counts for each section and provide warnings"""
    section_guidelines = {
        "abstract": {"ideal": 150, "max_warning": 250, "description": "Abstract"},
        "main": {"ideal": 1000, "max_warning": 3000, "description": "Main content"},
        "methods": {"ideal": 500, "max_warning": 1500, "description": "Methods"},
        "results": {"ideal": 800, "max_warning": 2000, "description": "Results"},
        "discussion": {"ideal": 600, "max_warning": 1500, "description": "Discussion"},
        "conclusion": {"ideal": 200, "max_warning": 500, "description": "Conclusion"},
        "funding": {"ideal": 50, "max_warning": 150, "description": "Funding"},
        "acknowledgements": {
            "ideal": 100,
            "max_warning": 300,
            "description": "Acknowledgements",
        },
    }

    print("\n📊 WORD COUNT ANALYSIS:")
    print("=" * 50)

    total_words = 0
    for section_key, content in content_sections.items():
        if content.strip():
            word_count = count_words_in_text(content)
            total_words += word_count

            # Get guidelines for this section
            guidelines = section_guidelines.get(section_key, {})
            section_name = guidelines.get(
                "description", section_key.replace("_", " ").title()
            )
            ideal = guidelines.get("ideal")
            max_warning = guidelines.get("max_warning")

            # Format output
            status = "✓"
            warning = ""

            if max_warning and word_count > max_warning:
                status = "⚠️"
                warning = f" (exceeds typical {max_warning} word limit)"
            elif ideal and word_count > ideal * 1.5:
                status = "⚠️"
                warning = f" (consider typical ~{ideal} words)"

            print(f"{status} {section_name:<15}: {word_count:>4} words{warning}")

    print("-" * 50)
    print(f"📝 Total article words: {total_words}")

    # Overall article length guidance
    if total_words > 8000:
        print(
            "⚠️  Article is quite long (>8000 words) - consider condensing for most journals"
        )
    elif total_words > 5000:
        print("ℹ️  Article length is substantial - check target journal word limits")
    elif total_words < 2000:
        print("ℹ️  Article is relatively short - ensure adequate detail for publication")

    print("=" * 50)


def process_template_replacements(template_content, yaml_metadata, article_md):
    """Process all template replacements with metadata and content"""
    # Process draft watermark based on status field
    is_draft = False
    if "status" in yaml_metadata:
        status = str(yaml_metadata["status"]).lower()
        is_draft = status == "draft"

    if is_draft:
        # Enable watermark option in document class
        template_content = template_content.replace(
            r"\documentclass[times, twoside]{HenriquesLab_style}",
            r"\documentclass[times, twoside, watermark]{HenriquesLab_style}",
        )

    # Process line numbers
    txt = ""
    if "use_line_numbers" in yaml_metadata:
        use_line_numbers = str(yaml_metadata["use_line_numbers"]).lower() == "true"
        if use_line_numbers:
            txt = "% Add number to the lines\n\\usepackage{lineno}\n\\linenumbers\n"
    template_content = template_content.replace("<PY-RPL:USE-LINE-NUMBERS>", txt)

    # Process date
    date_str = yaml_metadata.get("date", "")
    if date_str:
        # Redefine \today to use our custom date from metadata
        txt = f"\\renewcommand{{\\today}}{{{date_str}}}\n"
    else:
        # Use default \today if no date specified
        txt = ""
    template_content = template_content.replace("<PY-RPL:DATE>", txt)

    # Process lead author
    lead_author = "Unknown"
    if "title" in yaml_metadata:
        title_data = yaml_metadata["title"]
        if isinstance(title_data, list):
            for item in title_data:
                if isinstance(item, dict) and "lead_author" in item:
                    lead_author = item["lead_author"]
                    break
        elif isinstance(title_data, dict) and "lead_author" in title_data:
            lead_author = title_data["lead_author"]

    if (
        lead_author == "Unknown"
        and "authors" in yaml_metadata
        and yaml_metadata["authors"]
    ):
        # get the last name of the first author
        first_author = yaml_metadata["authors"][0]
        if isinstance(first_author, dict) and "name" in first_author:
            lead_author = first_author["name"].split()[-1]
        elif isinstance(first_author, str):
            lead_author = first_author.split()[-1]
    txt = f"\\leadauthor{{{lead_author}}}\n"
    template_content = template_content.replace("<PY-RPL:LEAD-AUTHOR>", txt)

    # Process long title
    long_title = "Untitled Article"
    if "title" in yaml_metadata:
        if (
            isinstance(yaml_metadata["title"], dict)
            and "long" in yaml_metadata["title"]
        ):
            long_title = yaml_metadata["title"]["long"]
        elif isinstance(yaml_metadata["title"], list):
            for item in yaml_metadata["title"]:
                if isinstance(item, dict) and "long" in item:
                    long_title = item["long"]
                    break
        elif isinstance(yaml_metadata["title"], str):
            long_title = yaml_metadata["title"]
    txt = f"\\title{{{long_title}}}\n"
    template_content = template_content.replace("<PY-RPL:LONG-TITLE-STR>", txt)

    # Process short title
    short_title = "Untitled"
    if "title" in yaml_metadata:
        if (
            isinstance(yaml_metadata["title"], dict)
            and "short" in yaml_metadata["title"]
        ):
            short_title = yaml_metadata["title"]["short"]
        elif isinstance(yaml_metadata["title"], list):
            for item in yaml_metadata["title"]:
                if isinstance(item, dict) and "short" in item:
                    short_title = item["short"]
                    break
        elif isinstance(yaml_metadata["title"], str):
            short_title = (
                yaml_metadata["title"][:50] + "..."
                if len(yaml_metadata["title"]) > 50
                else yaml_metadata["title"]
            )
    txt = f"\\shorttitle{{{short_title}}}\n"
    template_content = template_content.replace("<PY-RPL:SHORT-TITLE-STR>", txt)

    # Generate authors and affiliations dynamically
    authors_and_affiliations = generate_authors_and_affiliations(yaml_metadata)
    template_content = template_content.replace(
        "<PY-RPL:AUTHORS-AND-AFFILIATIONS>", authors_and_affiliations
    )

    # Generate corresponding authors section
    corresponding_authors = generate_corresponding_authors(yaml_metadata)
    template_content = template_content.replace(
        "<PY-RPL:CORRESPONDING-AUTHORS>", corresponding_authors
    )

    # Generate extended author information section
    extended_author_info = generate_extended_author_info(yaml_metadata)
    template_content = template_content.replace(
        "<PY-RPL:EXTENDED-AUTHOR-INFO>", extended_author_info
    )

    # Generate keywords section
    keywords_section = generate_keywords(yaml_metadata)
    template_content = template_content.replace("<PY-RPL:KEYWORDS>", keywords_section)

    # Generate bibliography section
    bibliography_section = generate_bibliography(yaml_metadata)
    template_content = template_content.replace(
        "<PY-RPL:BIBLIOGRAPHY>", bibliography_section
    )

    # Extract content sections from markdown
    content_sections = extract_content_sections(article_md)

    # Analyze word counts and provide warnings
    analyze_section_word_counts(content_sections)

    # Replace content placeholders with extracted sections
    template_content = template_content.replace(
        "<PY-RPL:ABSTRACT>", content_sections.get("abstract", "")
    )
    template_content = template_content.replace(
        "<PY-RPL:MAIN-CONTENT>", content_sections.get("main", "")
    )
    template_content = template_content.replace(
        "<PY-RPL:METHODS>", content_sections.get("methods", "")
    )
    template_content = template_content.replace(
        "<PY-RPL:DATA-AVAILABILITY>", content_sections.get("data_availability", "")
    )
    template_content = template_content.replace(
        "<PY-RPL:CODE-AVAILABILITY>", content_sections.get("code_availability", "")
    )
    template_content = template_content.replace(
        "<PY-RPL:FUNDING>", content_sections.get("funding", "")
    )
    template_content = template_content.replace(
        "<PY-RPL:AUTHOR-CONTRIBUTIONS>",
        content_sections.get("author_contributions", ""),
    )
    template_content = template_content.replace(
        "<PY-RPL:ACKNOWLEDGEMENTS>", content_sections.get("acknowledgements", "")
    )

    return template_content
