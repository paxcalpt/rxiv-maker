"""Table processing for markdown to LaTeX conversion.

This module handles conversion of markdown tables to LaTeX table environments,
including table formatting, rotation, and special syntax handling.
"""

import re
from typing import Optional

from .types import (
    LatexContent,
    MarkdownContent,
    ProtectedContent,
    TableData,
    TableHeaders,
)


def convert_tables_to_latex(
    text: MarkdownContent,
    protected_backtick_content: Optional[ProtectedContent] = None,
    is_supplementary: bool = False,
) -> LatexContent:
    r"""Convert markdown tables to LaTeX table environments.

    Args:
        text: The text containing markdown tables
        protected_backtick_content: Dict of protected backtick content
        is_supplementary: If True, adds \newpage after tables

    Returns:
        Text with tables converted to LaTeX format
    """
    if protected_backtick_content is None:
        protected_backtick_content = {}

    lines = text.split("\n")
    result_lines: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check for table caption before the table
        table_caption = None
        table_width = "single"  # default to single column

        # Look for a caption line before the table
        # (format: "Table 1: Caption text" or "Table* 1: Caption text")
        if i > 0 and re.match(
            r"^Table\*?\s+\d+[:.]\s*", lines[i - 1].strip(), re.IGNORECASE
        ):
            caption_line = lines[i - 1].strip()
            # Check if it's a two-column table (Table* format)
            if caption_line.lower().startswith("table*"):
                table_width = "double"
            # Extract caption text after "Table X:" or "Table* X:"
            caption_match = re.match(
                r"^Table\*?\s+\d+[:.]\s*(.*)$", caption_line, re.IGNORECASE
            )
            if caption_match:
                table_caption = caption_match.group(1).strip()

        # Check if current line starts a table (contains pipe symbols)
        if _is_table_start(line, lines, i):
            # Found a table! Extract it
            header_line = line.strip()

            # Parse header
            headers = [cell.strip() for cell in header_line.split("|")[1:-1]]
            num_cols = len(headers)

            # Skip header and separator
            i += 2

            # Collect data rows
            data_rows: TableData = []
            while i < len(lines) and lines[i].strip():
                current_line = lines[i].strip()
                if _is_table_row(current_line):
                    cells = [cell.strip() for cell in current_line.split("|")[1:-1]]
                    # Pad cells if needed
                    while len(cells) < num_cols:
                        cells.append("")
                    data_rows.append(cells[:num_cols])  # Truncate if too many
                    i += 1
                else:
                    break

            # Remove the caption line from result_lines if it was added
            if (
                table_caption
                and result_lines
                and result_lines[-1].strip().lower().startswith("table")
            ):
                result_lines.pop()

            # Check for new format table caption after the table
            new_format_caption, table_id, rotation_angle = _parse_table_caption(
                lines, i
            )
            if new_format_caption:
                i += 2  # Skip blank line and caption line

            # Generate LaTeX table with the processed caption
            latex_table = generate_latex_table(
                headers,
                data_rows,
                new_format_caption or table_caption,
                table_width,
                table_id,
                protected_backtick_content,
                rotation_angle,
                is_supplementary,
            )
            result_lines.extend(latex_table.split("\n"))

            # Add newpage after supplementary tables
            if is_supplementary:
                result_lines.append("\\newpage")

            # Continue with next line (i is already incremented)
            continue

        # Not a table, add line as-is
        result_lines.append(line)
        i += 1

    return "\n".join(result_lines)


def generate_latex_table(
    headers: TableHeaders,
    data_rows: TableData,
    caption: Optional[str] = None,
    width: str = "single",
    table_id: Optional[str] = None,
    protected_backtick_content: Optional[ProtectedContent] = None,
    rotation_angle: Optional[int] = None,
    is_supplementary: bool = False,
) -> LatexContent:
    """Generate LaTeX table from headers and data rows.

    Uses sidewaystable for rotation.

    Args:
        headers: List of table header strings
        data_rows: List of table rows (each row is a list of cell strings)
        caption: Optional table caption
        width: Table width ("single" or "double")
        table_id: Optional table ID for labeling
        protected_backtick_content: Protected backtick content dictionary
        rotation_angle: Optional rotation angle for table
        is_supplementary: Whether this is a supplementary table

    Returns:
        Complete LaTeX table environment as string
    """
    if protected_backtick_content is None:
        protected_backtick_content = {}

    num_cols = len(headers)

    # Create column specification (all left-aligned with borders)
    col_spec = "|" + "l|" * num_cols

    # Check if this is a Markdown Syntax Overview table to preserve literal
    # syntax in all columns
    # Remove markdown formatting from header for comparison
    first_header_clean = headers[0].lower().strip() if headers else ""
    first_header_clean = re.sub(
        r"\*\*(.*?)\*\*", r"\1", first_header_clean
    )  # Remove **bold**
    first_header_clean = re.sub(
        r"\*(.*?)\*", r"\1", first_header_clean
    )  # Remove *italic*
    is_markdown_syntax_table = first_header_clean == "markdown element"

    # Format headers
    formatted_headers: list[str] = []
    for header in headers:
        # If this is the markdown syntax overview table, treat all cells as literal
        formatted_headers.append(
            _format_table_cell(
                header,
                is_markdown_syntax_table,
                is_header=True,
                protected_backtick_content=protected_backtick_content,
            )
        )

    # Format data rows
    formatted_data_rows: list[list[str]] = []
    for row in data_rows:
        formatted_row: list[str] = []
        for cell in row:
            # If this is the markdown syntax overview table, treat all cells as literal
            formatted_row.append(
                _format_table_cell(
                    cell,
                    is_markdown_syntax_table,
                    is_header=False,
                    protected_backtick_content=protected_backtick_content,
                )
            )
        formatted_data_rows.append(formatted_row)

    # Determine table environment
    table_env, position = _determine_table_environment(
        width, rotation_angle, is_supplementary
    )

    # Build LaTeX table environment
    latex_lines = [
        f"\\begin{{{table_env}}}{position}",
        "\\centering",
    ]

    # Add rotation if specified and not already using sidewaystable
    use_rotatebox = rotation_angle and not table_env.startswith("sideways")
    if use_rotatebox:
        latex_lines.append(f"\\rotatebox{{{rotation_angle}}}{{%")

    # Add tabular
    latex_lines.append(f"\\begin{{tabular}}{{{col_spec}}}")
    latex_lines.append("\\hline")

    # Add header row
    header_row = " & ".join(formatted_headers) + " \\\\"
    latex_lines.append(header_row)
    latex_lines.append("\\hline")

    # Add data rows
    for row in formatted_data_rows:
        data_row = " & ".join(row) + " \\\\"
        latex_lines.append(data_row)
        latex_lines.append("\\hline")

    # Close tabular
    latex_lines.append("\\end{tabular}")

    # Close rotatebox if used
    if use_rotatebox:
        latex_lines.append("}%")

    # Add caption
    if caption:
        latex_lines.append("\\raggedright")
        latex_lines.append(f"\\caption{{{caption}}}")
        label = table_id if table_id else "tab:comparison"
        latex_lines.append(f"\\label{{{label}}}")

    # Close environment
    latex_lines.append(f"\\end{{{table_env}}}")

    return "\n".join(latex_lines)


def _format_table_cell(
    cell: str,
    is_markdown_example_column: bool = False,
    is_header: bool = False,
    protected_backtick_content: Optional[ProtectedContent] = None,
) -> str:
    """Format a table cell for LaTeX output.

    Args:
        cell: Cell content to format
        is_markdown_example_column: Whether this is a markdown syntax example column
        is_header: Whether this is a header cell
        protected_backtick_content: Protected backtick content dictionary

    Returns:
        Formatted cell content for LaTeX
    """
    if protected_backtick_content is None:
        protected_backtick_content = {}

    # First restore any protected backtick content
    for placeholder, original in protected_backtick_content.items():
        cell = cell.replace(placeholder, original)

    # If this is the "Markdown Element" column but it's a header, process normally
    if is_markdown_example_column and is_header:
        # For headers in markdown syntax table, process markdown normally
        # Convert **bold** to \textbf{bold}
        cell = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", cell)
        # Convert *italic* to \textit{italic}
        cell = re.sub(r"\*([^*]+)\*", r"\\textit{\1}", cell)
        return cell

    # If this is the "Markdown Element" column, preserve literal syntax
    if is_markdown_example_column:
        return _format_markdown_syntax_cell(cell)

    # Regular cell formatting
    return _format_regular_table_cell(cell)


def _format_markdown_syntax_cell(cell: str) -> str:
    """Format a cell in markdown syntax overview table to preserve literal syntax."""

    # Only convert backticks to \texttt{} but preserve other markdown syntax
    def process_code_only(match: re.Match[str]) -> str:
        code_content = match.group(1)
        # Escape special characters for LaTeX, including brackets and @
        code_content = _escape_latex_special_chars(code_content)
        return f"\\texttt{{{code_content}}}"

    # Convert backticks to \texttt{} but preserve ** * @ [] etc.
    cell = re.sub(r"`([^`]+)`", process_code_only, cell)

    # For non-backtick content, wrap entire cell in \texttt{} to preserve
    # literal display
    if not re.search(r"\\texttt\{", cell):  # Only if not already wrapped
        # Escape special characters that would break LaTeX, including
        # brackets and @
        cell = _escape_latex_special_chars(cell)
        return f"\\texttt{{{cell}}}"

    return cell


def _format_regular_table_cell(cell: str) -> str:
    """Format a regular table cell with markdown processing."""

    # First, process code blocks to protect them from markdown formatting
    def process_code_in_table(match: re.Match[str]) -> str:
        code_content = match.group(1)
        # Replace problematic characters that break tables
        # Order matters - do backslashes first, then other characters
        code_content = _escape_latex_special_chars(code_content)
        # For multiline code in tables, replace newlines with spaces
        code_content = code_content.replace("\n", " ")
        # Remove multiple spaces
        code_content = re.sub(r"\s+", " ", code_content).strip()
        return f"\\texttt{{{code_content}}}"

    # Process code blocks - use simple approach that handles all cases
    # First handle the specific case of `` `code` `` (double backticks with
    # inner backticks)
    cell = re.sub(r"``\s*`([^`]+)`\s*``", lambda m: f"\\texttt{{{m.group(1)}}}", cell)
    # Then handle regular double backticks
    cell = re.sub(r"``([^`]+)``", process_code_in_table, cell)
    # Finally handle single backticks
    cell = re.sub(r"`([^`]+)`", process_code_in_table, cell)

    # Apply formatting outside texttt blocks
    cell = _apply_formatting_outside_texttt(cell)

    # Escape remaining special characters outside texttt blocks
    cell = _escape_outside_texttt(cell)

    return cell


def _escape_latex_special_chars(text: str) -> str:
    """Escape LaTeX special characters in text."""
    text = text.replace("\\", "\\textbackslash{}")
    text = text.replace("{", "\\{")
    text = text.replace("}", "\\}")
    text = text.replace("&", "\\&")
    text = text.replace("%", "\\%")
    text = text.replace("$", "\\$")
    text = text.replace("#", "\\#")
    text = text.replace("^", "\\textasciicircum{}")
    text = text.replace("~", "\\textasciitilde{}")
    text = text.replace("_", "\\_")
    text = text.replace("[", "\\lbrack{}")
    text = text.replace("]", "\\rbrack{}")
    text = text.replace("@", "\\@")
    return text


def _apply_formatting_outside_texttt(text: str) -> str:
    """Apply markdown formatting outside texttt blocks."""

    # Handle bold first (double asterisks) - but only outside \texttt{}
    def replace_bold_outside_texttt(text: str) -> str:
        parts = re.split(r"(\\texttt\{[^}]*\})", text)
        result: list[str] = []
        for _i, part in enumerate(parts):
            if part.startswith("\\texttt{"):
                result.append(part)
            else:
                part = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", part)
                result.append(part)
        return "".join(result)

    # Handle italic (single asterisks) - but only outside \texttt{}
    def replace_italic_outside_texttt(text: str) -> str:
        parts = re.split(r"(\\texttt\{[^}]*\})", text)
        result: list[str] = []
        for _i, part in enumerate(parts):
            if part.startswith("\\texttt{"):
                result.append(part)
            else:
                part = re.sub(
                    r"(?<!\*)\*([^*\s][^*]*[^*\s]|\w)\*(?!\*)",
                    r"\\textit{\1}",
                    part,
                )
                result.append(part)
        return "".join(result)

    text = replace_bold_outside_texttt(text)
    text = replace_italic_outside_texttt(text)
    return text


def _escape_outside_texttt(text: str) -> str:
    """Escape special characters outside texttt blocks."""
    parts = re.split(r"(\\texttt\{[^}]*\})", text)
    result: list[str] = []
    for _i, part in enumerate(parts):
        if part.startswith("\\texttt{"):
            result.append(part)
        else:
            part = part.replace("&", "\\&")
            part = part.replace("%", "\\%")
            part = part.replace("$", "\\$")
            part = part.replace("#", "\\#")
            part = part.replace("^", "\\textasciicircum{}")
            part = part.replace("~", "\\textasciitilde{}")
            part = part.replace("_", "\\_")
            result.append(part)
    return "".join(result)


def _is_table_start(line: str, lines: list[str], i: int) -> bool:
    """Check if a line starts a markdown table."""
    return (
        "|" in line
        and line.strip().startswith("|")
        and line.strip().endswith("|")
        and i + 1 < len(lines)
        and "|" in lines[i + 1]
        and "-" in lines[i + 1]
    )


def _is_table_row(line: str) -> bool:
    """Check if a line is a valid table row."""
    return "|" in line and line.startswith("|") and line.endswith("|")


def _parse_table_caption(
    lines: list[str], i: int
) -> tuple[Optional[str], Optional[str], Optional[int]]:
    """Parse table caption in new format after table."""
    new_format_caption = None
    table_id = None
    rotation_angle = None

    if (
        i < len(lines)
        and lines[i].strip() == ""
        and i + 1 < len(lines)
        and re.match(r"^\{#[a-zA-Z0-9_:-]+.*\}\s*\*\*.*\*\*", lines[i + 1].strip())
    ):
        # Found new format caption, parse it
        caption_line = lines[i + 1].strip()

        # Parse caption with optional attributes like rotate=90
        caption_match = re.match(
            r"^\{#([a-zA-Z0-9_:-]+)([^}]*)\}\s*(.+)$", caption_line
        )
        if caption_match:
            table_id = caption_match.group(1)
            attributes_str = caption_match.group(2).strip()
            caption_text = caption_match.group(3)

            # Extract rotation attribute if present
            if attributes_str:
                rotation_match = re.search(r"rotate=(\d+)", attributes_str)
                if rotation_match:
                    rotation_angle = int(rotation_match.group(1))

            # Process caption text to handle markdown formatting
            new_format_caption = re.sub(
                r"\*\*([^*]+)\*\*", r"\\textbf{\1}", caption_text
            )
            new_format_caption = re.sub(
                r"\*([^*]+)\*", r"\\textit{\1}", new_format_caption
            )

    return new_format_caption, table_id, rotation_angle


def _determine_table_environment(
    width: str, rotation_angle: Optional[int], is_supplementary: bool
) -> tuple[str, str]:
    """Determine the appropriate table environment and position."""
    if rotation_angle and is_supplementary:
        # Use sideways table for rotated supplementary tables
        table_env = "sidewaystable*" if width == "double" else "sidewaystable"
        position = "[ht]"
    elif is_supplementary:
        table_env = "stable*" if width == "double" else "stable"
        position = "[ht]"
    else:
        table_env = "table*" if width == "double" else "table"
        position = width == "double" and "[!ht]" or "[ht]"

    return table_env, position
