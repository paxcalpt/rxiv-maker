"""Figure processing for markdown to LaTeX conversion.

This module handles conversion of markdown figures to LaTeX figure environments,
including figure attributes, captions, and references.
"""

import re
from typing import Optional

from .types import (
    FigureAttributes,
    FigureCaption,
    FigureId,
    FigurePath,
    FigurePosition,
    FigureWidth,
    LatexContent,
    MarkdownContent,
)


def convert_figures_to_latex(
    text: MarkdownContent, is_supplementary: bool = False
) -> LatexContent:
    r"""Convert markdown figures to LaTeX figure environments.

    Args:
        text: The text containing markdown figures
        is_supplementary: If True, enables supplementary content processing

    Returns:
        Text with figures converted to LaTeX format
    """
    # First protect code blocks from figure processing
    protected_blocks: list[str] = []

    def protect_code_blocks(match: re.Match[str]) -> str:
        return f"__CODE_BLOCK_{len(protected_blocks)}__"

    # Protect inline code (backticks)
    def protect_inline_code(match: re.Match[str]) -> str:
        protected_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(protected_blocks)-1}__"

    text = re.sub(r"`[^`]+`", protect_inline_code, text)

    # Protect fenced code blocks
    def protect_fenced_code(match: re.Match[str]) -> str:
        protected_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(protected_blocks)-1}__"

    text = re.sub(r"```.*?```", protect_fenced_code, text, flags=re.DOTALL)

    # Process different figure formats
    text = _process_new_figure_format(text)
    text = _process_figure_with_attributes(text)
    text = _process_figure_without_attributes(text)

    # Restore protected code blocks
    for i, block in enumerate(protected_blocks):
        text = text.replace(f"__CODE_BLOCK_{i}__", block)

    return text


def convert_figure_references_to_latex(text: MarkdownContent) -> LatexContent:
    r"""Convert figure references from @fig:id and @sfig:id to LaTeX.

    Converts @fig:id to \\ref{fig:id} and @sfig:id to \\ref{sfig:id}.

    Args:
        text: Text containing figure references

    Returns:
        Text with figure references converted to LaTeX format
    """
    # Convert @fig:id to \ref{fig:id}
    text = re.sub(r"@fig:([a-zA-Z0-9_-]+)", r"\\ref{fig:\1}", text)

    # Convert @sfig:id to \ref{sfig:id} (supplementary figures)
    text = re.sub(r"@sfig:([a-zA-Z0-9_-]+)", r"\\ref{sfig:\1}", text)

    return text


def parse_figure_attributes(attr_string: str) -> FigureAttributes:
    r"""Parse figure attributes like {#fig:1 tex_position="!ht" width="0.8"}.

    Args:
        attr_string: String containing figure attributes

    Returns:
        Dictionary of parsed attributes
    """
    attributes: FigureAttributes = {}

    # Extract ID (starts with #)
    id_match = re.search(r"#([a-zA-Z0-9_:-]+)", attr_string)
    if id_match:
        attributes["id"] = id_match.group(1)

    # Extract other attributes (key="value" or key=value)
    attr_matches = re.findall(r'(\w+)=(["\'])([^"\']*)\2', attr_string)
    for match in attr_matches:
        key, _, value = match
        attributes[key] = value

    return attributes


def create_latex_figure_environment(
    path: FigurePath,
    caption: FigureCaption,
    attributes: Optional[FigureAttributes] = None,
    is_supplementary: bool = False,
) -> LatexContent:
    """Create a complete LaTeX figure environment.

    Args:
        path: Path to the figure file
        caption: Figure caption text
        attributes: Optional figure attributes (position, width, id)
        is_supplementary: Whether this is a supplementary figure

    Returns:
        Complete LaTeX figure environment
    """
    if attributes is None:
        attributes = {}

    # Convert path from FIGURES/ to Figures/ for LaTeX and handle new
    # subdirectory structure
    latex_path = path.replace("FIGURES/", "Figures/")

    # Handle new subdirectory structure: Figure_1.svg -> Figure_1/Figure_1.png
    if (
        "/" not in latex_path.split("Figures/")[-1]
    ):  # Only if not already in subdirectory
        # Extract figure name from path like "Figures/Figure_1.svg"
        import os

        figure_name = os.path.splitext(os.path.basename(latex_path))[0]
        figure_ext = os.path.splitext(latex_path)[1]

        # Convert to subdirectory format: Figures/Figure_1/Figure_1.ext
        latex_path = f"Figures/{figure_name}/{figure_name}{figure_ext}"

    # Convert SVG to PNG for LaTeX compatibility
    if latex_path.endswith(".svg"):
        latex_path = latex_path.replace(".svg", ".png")

    # Get positioning (default to 'ht' if not specified)
    position: FigurePosition = attributes.get("tex_position", "ht")

    # Get width (default to '\linewidth' if not specified)
    width: FigureWidth = attributes.get("width", "\\linewidth")
    if not width.startswith("\\"):
        width = f"{width}\\linewidth"  # Assume fraction of linewidth if no backslash

    # Process caption text to remove markdown formatting
    processed_caption = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", caption)
    processed_caption = re.sub(r"\*([^*]+)\*", r"\\textit{\1}", processed_caption)

    # Create LaTeX figure environment
    latex_figure = f"""\\begin{{figure}}[{position}]
\\centering
\\includegraphics[width={width}]{{{latex_path}}}
\\caption{{{processed_caption}}}"""

    # Add label if ID is present
    if "id" in attributes:
        latex_figure += f"\n\\label{{{attributes['id']}}}"

    latex_figure += "\n\\end{figure}"

    return latex_figure


def _process_new_figure_format(text: MarkdownContent) -> LatexContent:
    r"""Process new figure format: ![](path)\n{attributes} **Caption text**."""

    def process_new_figure_format_full(match: re.Match[str]) -> str:
        path = match.group(1)
        attr_string = match.group(2)
        caption_text = match.group(3).strip()

        # Parse attributes
        attributes = parse_figure_attributes(attr_string)
        return create_latex_figure_environment(path, caption_text, attributes)

    # Handle new format: ![](path)\n{attributes} **Caption text**
    return re.sub(
        r"!\[\]\(([^)]+)\)\s*\n\{([^}]+)\}\s*(.+?)(?=\n\n|\n$|$)",
        process_new_figure_format_full,
        text,
        flags=re.MULTILINE | re.DOTALL,
    )


def _process_figure_with_attributes(text: MarkdownContent) -> LatexContent:
    """Process figures with attributes: ![caption](path){attributes}."""

    def process_figure_with_attributes(match: re.Match[str]) -> str:
        caption = match.group(1)
        path = match.group(2)
        attr_string = match.group(3)

        # Parse attributes
        attributes = parse_figure_attributes(attr_string)
        return create_latex_figure_environment(path, caption, attributes)

    # Handle figures with attributes (old format)
    return re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)\{([^}]+)\}", process_figure_with_attributes, text
    )


def _process_figure_without_attributes(text: MarkdownContent) -> LatexContent:
    """Process figures without attributes: ![caption](path)."""

    def process_figure_without_attributes(match: re.Match[str]) -> str:
        caption = match.group(1)
        path = match.group(2)
        return create_latex_figure_environment(path, caption)

    # Handle figures without attributes (remaining ones)
    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", process_figure_without_attributes, text)


def validate_figure_path(path: FigurePath) -> bool:
    """Validate that a figure path is properly formatted.

    Args:
        path: Figure file path

    Returns:
        True if path is valid, False otherwise
    """
    # Check for valid image extensions
    valid_extensions = [".png", ".jpg", ".jpeg", ".pdf", ".svg", ".eps"]
    return any(path.lower().endswith(ext) for ext in valid_extensions)


def extract_figure_ids_from_text(text: MarkdownContent) -> list[FigureId]:
    """Extract all figure IDs from markdown text.

    Args:
        text: Text to extract figure IDs from

    Returns:
        List of unique figure IDs found in the text
    """
    figure_ids: list[FigureId] = []

    # Find figure attribute blocks
    attr_matches = re.findall(r"\{#([a-zA-Z0-9_:-]+)[^}]*\}", text)
    for match in attr_matches:
        if (
            match.startswith("fig:") or match.startswith("sfig:")
        ) and match not in figure_ids:
            figure_ids.append(match)

    return figure_ids
