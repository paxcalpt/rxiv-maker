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

    Converts markdown headers like "### Title" to LaTeX format with automatic
    "Supplementary Note X:" numbering and reference labels. Only processes
    ### headers that appear after the "Supplementary Notes" section.

    Args:
        content: The LaTeX content to process

    Returns:
        Processed content with supplementary notes formatted
    """
    # Split content at the "Supplementary Notes" section
    supp_notes_pattern = r"\\subsection\{Supplementary Notes\}"
    parts = re.split(supp_notes_pattern, content, maxsplit=1)

    if len(parts) != 2:
        # No "Supplementary Notes" section found, return content unchanged
        return content

    before_notes = parts[0]
    notes_section = parts[1]

    # Process ### headers only in the notes section
    pattern = r"^### (.+)$"
    note_counter = 0

    # List of headers that should NOT be treated as supplementary notes
    excluded_headers = [
        "file structure and organisation",
        "file structure and organization",
    ]

    def replace_note_header(match):
        nonlocal note_counter
        title = match.group(1).strip()

        # Skip headers that are not meant to be supplementary notes
        if title.lower() in excluded_headers:
            return f"\\subsubsection{{{title}}}"

        # This is a supplementary note, increment counter
        note_counter += 1

        # Create a reference label from the title
        # Convert title to lowercase, replace spaces/punctuation with underscores
        label = re.sub(r"[^\w\s-]", "", title.lower())
        label = re.sub(r"[-\s]+", "_", label).strip("_")
        ref_label = f"snote:{label}"

        # Create the LaTeX subsection with "Supplementary Note X:" prefix and label
        return (
            f"\\subsection{{Supplementary Note {note_counter}: {title}}}"
            f"\\label{{{ref_label}}}"
        )

    # Replace ### headers with supplementary note format only in notes section
    processed_notes_section = re.sub(
        pattern, replace_note_header, notes_section, flags=re.MULTILINE
    )

    # Reconstruct the content
    return before_notes + r"\subsection{Supplementary Notes}" + processed_notes_section


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
