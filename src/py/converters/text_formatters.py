"""Text formatting processors for markdown to LaTeX conversion.

This module handles basic text formatting including bold, italic, code,
headers, and special character escaping.
"""

import re
from typing import List

from .types import LatexContent, MarkdownContent


def convert_text_formatting_to_latex(text: MarkdownContent) -> LatexContent:
    """Convert markdown text formatting to LaTeX.

    Args:
        text: Markdown text with formatting

    Returns:
        LaTeX formatted text
    """
    # Convert bold and italic
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"\*(.+?)\*", r"\\textit{\1}", text)

    # Convert code
    text = re.sub(r"`(.+?)`", r"\\texttt{\1}", text)

    return text


def convert_headers_to_latex(text: MarkdownContent) -> LatexContent:
    """Convert markdown headers to LaTeX sections.

    Args:
        text: Markdown text with headers

    Returns:
        LaTeX text with section commands
    """
    text = re.sub(r"^## (.+)$", r"\\section{\1}", text, flags=re.MULTILINE)
    text = re.sub(r"^### (.+)$", r"\\subsection{\1}", text, flags=re.MULTILINE)
    text = re.sub(r"^#### (.+)$", r"\\subsubsection{\1}", text, flags=re.MULTILINE)

    return text


def process_code_spans(text: MarkdownContent) -> LatexContent:
    """Process inline code spans with proper escaping.

    Args:
        text: Text containing inline code spans

    Returns:
        Text with code spans converted to LaTeX
    """

    def process_code_blocks(match: re.Match[str]) -> str:
        code_content = match.group(1)
        # In texttt, underscores need to be escaped as \_
        # Use placeholder to avoid double-escaping issues
        escaped_content = code_content.replace("_", "XUNDERSCOREX")
        return "\\texttt{" + escaped_content + "}"

    # Process both double and single backticks
    text = re.sub(r"``([^`]+)``", process_code_blocks, text)  # Double backticks first
    text = re.sub(r"`([^`]+)`", process_code_blocks, text)  # Then single backticks

    return text


def apply_bold_italic_formatting(text: MarkdownContent) -> LatexContent:
    """Apply bold and italic formatting while protecting LaTeX commands.

    Args:
        text: Text to format

    Returns:
        Formatted text with LaTeX commands protected
    """

    def safe_bold_replace(match: re.Match[str]) -> str:
        bold_content = match.group(1)
        return f"\\textbf{{{bold_content}}}"

    def safe_italic_replace(match: re.Match[str]) -> str:
        italic_content = match.group(1)
        return f"\\textit{{{italic_content}}}"

    # Replace bold/italic but skip if inside LaTeX commands
    # Split by LaTeX commands and only process text parts
    parts = re.split(r"(\\[a-zA-Z]+\{[^}]*\})", text)
    processed_parts: List[str] = []

    for i, part in enumerate(parts):
        if i % 2 == 0:  # This is regular text, not a LaTeX command
            # Apply bold/italic formatting
            part = re.sub(r"\*\*(.+?)\*\*", safe_bold_replace, part)
            part = re.sub(r"\*(.+?)\*", safe_italic_replace, part)
        # If i % 2 == 1, it's a LaTeX command - leave it unchanged
        processed_parts.append(part)

    return "".join(processed_parts)


def protect_bold_outside_texttt(text: MarkdownContent) -> LatexContent:
    """Apply bold formatting only outside texttt blocks.

    Args:
        text: Text to process

    Returns:
        Text with bold formatting applied outside code blocks
    """
    # Split by \texttt{} blocks and process only non-texttt parts
    parts = re.split(r"(\\texttt\{[^}]*\})", text)
    result: List[str] = []

    for _i, part in enumerate(parts):
        if part.startswith("\\texttt{"):
            # This is a texttt block, don't process it
            result.append(part)
        else:
            # This is regular text, apply bold formatting
            part = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", part)
            result.append(part)
    return "".join(result)


def protect_italic_outside_texttt(text: MarkdownContent) -> LatexContent:
    """Apply italic formatting only outside texttt blocks.

    Args:
        text: Text to process

    Returns:
        Text with italic formatting applied outside code blocks
    """
    # Split by \texttt{} blocks and process only non-texttt parts
    parts = re.split(r"(\\texttt\{[^}]*\})", text)
    result: List[str] = []

    for _i, part in enumerate(parts):
        if part.startswith("\\texttt{"):
            # This is a texttt block, don't process it
            result.append(part)
        else:
            # This is regular text, apply italic formatting
            part = re.sub(
                r"(?<!\*)\*([^*\s][^*]*[^*\s]|\w)\*(?!\*)",
                r"\\textit{\1}",
                part,
            )
            result.append(part)
    return "".join(result)


def escape_special_characters(text: MarkdownContent) -> LatexContent:
    """Escape special LaTeX characters in text.

    Args:
        text: Text to escape

    Returns:
        Text with LaTeX special characters escaped
    """
    # Handle underscores carefully - LaTeX is very picky about this
    # We need to escape underscores in text mode but NOT double-escape them

    # Handle remaining underscores in file paths within parentheses
    def escape_file_paths_in_parens(match: re.Match[str]) -> str:
        paren_content = match.group(1)
        # Only escape if it looks like a file path (has extension or
        # is all caps directory)
        if ("." in paren_content and "_" in paren_content) or (
            paren_content.endswith(".md")
            or paren_content.endswith(".bib")
            or paren_content.endswith(".tex")
            or paren_content.endswith(".py")
            or paren_content.endswith(".csv")
        ):
            return f"({paren_content.replace('_', 'XUNDERSCOREX')})"
        return match.group(0)

    text = re.sub(r"\(([^)]+)\)", escape_file_paths_in_parens, text)

    # Handle remaining underscores in file names and paths
    # Match common filename patterns: WORD_WORD.ext, word_word.ext, etc.
    def escape_filenames(match: re.Match[str]) -> str:
        filename = match.group(0)
        # Escape underscores in anything that looks like a filename
        return filename.replace("_", "XUNDERSCOREX")

    # Match filenames with extensions
    text = re.sub(
        r"\b[\w]+_[\w._]*\.(md|yml|yaml|bib|tex|py|csv|pdf|png|svg|jpg)\b",
        escape_filenames,
        text,
    )

    # Also match numbered files like 00_CONFIG, 01_MAIN, etc.
    text = re.sub(r"\b\d+_[A-Z_]+\b", escape_filenames, text)

    # Final step: replace all placeholders with properly escaped underscores
    text = text.replace("XUNDERSCOREX", "\\_")

    return text
