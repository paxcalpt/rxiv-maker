"""Supplementary note processing for markdown to LaTeX conversion.

This module handles the conversion of supplementary note headers and creates
a reference system for citing supplementary notes from the main text.
"""

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from .types import LatexContent, MarkdownContent


def process_supplementary_notes(content: LatexContent) -> LatexContent:
    """Process supplementary note headers and create reference labels.

    Converts markdown {#snote:id} **Title** format to LaTeX format with automatic
    "Supplementary Note X:" numbering and reference labels. Processes all snote
    patterns throughout the document, giving priority to those after the
    "Supplementary Notes" section for numbering.

    Args:
        content: The LaTeX content to process

    Returns:
        Processed content with supplementary notes formatted
    """
    # Process {#snote:id} **Title** patterns throughout the entire document
    pattern = r"\{#snote:([^}]+)\}\s*\*\*([^*]+)\*\*"
    note_counter = 0
    first_note_processed = False

    def replace_note_header(match):
        nonlocal note_counter, first_note_processed
        snote_id = match.group(1).strip()
        title = match.group(2).strip()

        # This is a supplementary note, increment counter
        note_counter += 1

        # Use the provided snote_id as the reference label
        ref_label = f"snote:{snote_id}"

        # For the first note, add the renewcommand before the subsection
        prefix = ""
        if not first_note_processed:
            prefix = (
                "% Setup subsection numbering for supplementary notes\n"
                "\\renewcommand{\\thesubsection}{Supp. Note \\arabic{subsection}}\n"
                "\\setcounter{subsection}{0}\n\n"
            )
            first_note_processed = True

        # Create the LaTeX subsection with just the title and label
        # The "Supp. Note X:" prefix will be added automatically by LaTeX formatting
        result = f"{prefix}\\subsection{{{title}}}" f"\\label{{{ref_label}}}"
        return result

    # Replace all {#snote:id} **Title** patterns throughout the document
    processed_content = re.sub(
        pattern, replace_note_header, content, flags=re.MULTILINE
    )

    return processed_content


def process_supplementary_note_references(content: LatexContent) -> LatexContent:
    r"""Process supplementary note references in the content.

    Converts references like {@snote:title} to LaTeX \\ref{snote:title}.

    Args:
        content: The LaTeX content to process

    Returns:
        Processed content with supplementary note references converted
    """
    # Pattern to match supplementary note references
    # Matches: {@snote:label}
    pattern = r"\{@snote:([^}]+)\}"

    def replace_reference(match):
        label = match.group(1)
        return f"\\ref{{snote:{label}}}"

    # Replace supplementary note references
    content = re.sub(pattern, replace_reference, content)

    return content


def extract_supplementary_note_info(
    content: MarkdownContent,
) -> list[tuple[int, str, str]]:
    """Extract information about supplementary notes from markdown content.

    Args:
        content: The markdown content to analyze

    Returns:
        List of tuples containing (note_number, title, reference_label)
    """
    pattern = r"^### Supplementary Note (\d+):?\s*(.+)$"
    notes_info = []

    for match in re.finditer(pattern, content, re.MULTILINE):
        note_num = int(match.group(1))
        title = match.group(2).strip()

        # Create reference label
        label = re.sub(r"[^\w\s-]", "", title.lower())
        label = re.sub(r"[-\s]+", "_", label).strip("_")

        notes_info.append((note_num, title, label))

    return notes_info


def validate_supplementary_note_numbering(content: MarkdownContent) -> list[str]:
    """Validate that supplementary notes are numbered correctly.

    Args:
        content: The markdown content to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    notes_info = extract_supplementary_note_info(content)
    errors: list[str] = []

    if not notes_info:
        return errors

    # Check for sequential numbering starting from 1
    expected_num = 1
    for note_num, _title, _ in sorted(notes_info, key=lambda x: x[0]):
        if note_num != expected_num:
            errors.append(
                f"Supplementary Note {note_num} found, expected {expected_num}"
            )
        expected_num += 1

    # Check for duplicate numbers
    numbers = [num for num, _, _ in notes_info]
    duplicates = {num for num in numbers if numbers.count(num) > 1}
    if duplicates:
        errors.append(f"Duplicate supplementary note numbers: {sorted(duplicates)}")

    return errors
