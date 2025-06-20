"""Markdown to LaTeX conversion module for RXiv-Forge.

This module handles the conversion of markdown content to LaTeX format,
including section extraction, citation processing, and text formatting.
"""

import re


def extract_content_sections(article_md):
    """Extract content sections from markdown file and convert to LaTeX."""
    # Check if article_md is a file path or content
    if article_md.startswith("#") or article_md.startswith("---") or "\n" in article_md:
        # It's content, not a file path
        content = article_md
    else:
        # It's a file path
        with open(article_md) as file:
            content = file.read()

    # Remove YAML front matter
    content = re.sub(r"^---\n.*?\n---\n", "", content, flags=re.DOTALL)

    # Dictionary to store extracted sections
    sections = {}

    # Split content by ## headers to find sections
    section_pattern = r"^## (.+?)$"
    section_matches = list(re.finditer(section_pattern, content, re.MULTILINE))

    # If no sections found, treat entire content as main
    if not section_matches:
        sections["main"] = convert_markdown_to_latex(content)
        return sections

    # Extract main content (everything before first ## header)
    first_section_start = section_matches[0].start()
    main_content = content[:first_section_start].strip()
    if main_content:
        sections["main"] = convert_markdown_to_latex(main_content)

    # Extract each section
    for i, match in enumerate(section_matches):
        section_title = match.group(1).strip()
        section_start = match.end()

        # Find end of section (next ## header or end of document)
        if i + 1 < len(section_matches):
            section_end = section_matches[i + 1].start()
        else:
            section_end = len(content)

        section_content = content[section_start:section_end].strip()
        section_content_latex = convert_markdown_to_latex(section_content)

        # Map section titles to our standard keys
        section_key = map_section_title_to_key(section_title)
        if section_key:
            sections[section_key] = section_content_latex

    return sections


def map_section_title_to_key(title):
    """Map section title to standardized key."""
    title_lower = title.lower()

    if "abstract" in title_lower:
        return "abstract"
    elif "introduction" in title_lower:
        return "main"
    elif "method" in title_lower:
        return "methods"
    elif "result" in title_lower and "discussion" in title_lower:
        return "results_and_discussion"
    elif "result" in title_lower:
        return "results"
    elif "discussion" in title_lower:
        return "discussion"
    elif "conclusion" in title_lower:
        return "conclusion"
    elif "data availability" in title_lower or "data access" in title_lower:
        return "data_availability"
    elif "code availability" in title_lower or "code access" in title_lower:
        return "code_availability"
    elif "author contribution" in title_lower or "contribution" in title_lower:
        return "author_contributions"
    elif "acknowledgement" in title_lower or "acknowledge" in title_lower:
        return "acknowledgements"
    elif (
        "funding" in title_lower
        or "financial support" in title_lower
        or "grant" in title_lower
    ):
        return "funding"
    else:
        # For other sections, return as lowercase with spaces replaced by underscores
        return title_lower.replace(" ", "_").replace("-", "_")


def convert_markdown_to_latex(content):
    """Convert basic markdown formatting to LaTeX."""
    # FIRST: Convert fenced code blocks BEFORE protecting backticks
    content = convert_code_blocks_to_latex(content)

    # THEN: Protect all remaining backtick content from bold/italic conversion
    # throughout the pipeline
    protected_backtick_content = {}
    protected_tables = {}

    def protect_backtick_content(match):
        original = match.group(0)
        placeholder = (
            f"XXPROTECTEDBACKTICKXX{len(protected_backtick_content)}"
            f"XXPROTECTEDBACKTICKXX"
        )
        protected_backtick_content[placeholder] = original
        return placeholder

    # Protect all backtick content globally (excluding fenced blocks which are
    # already processed)
    # Handle both single backticks and double backticks for inline code
    content = re.sub(
        r"``[^`]+``", protect_backtick_content, content
    )  # Double backticks first
    content = re.sub(
        r"`[^`]+`", protect_backtick_content, content
    )  # Then single backticks

    # Convert HTML comments to LaTeX comments
    content = convert_html_comments_to_latex(content)

    # Convert HTML tags to LaTeX equivalents
    content = convert_html_tags_to_latex(content)

    # Convert lists BEFORE other processing to avoid conflicts
    content = convert_lists_to_latex(content)

    # Convert tables BEFORE figures to avoid conflicts
    # Temporarily restore backtick content for table processing, then re-protect it
    temp_content = content

    # Only restore backticks that are actually in table rows to avoid
    # affecting verbatim blocks
    table_lines = temp_content.split("\n")
    for i, line in enumerate(table_lines):
        if "|" in line and line.strip().startswith("|") and line.strip().endswith("|"):
            # This is a table row - restore backticks in this line only
            for placeholder, original in protected_backtick_content.items():
                line = line.replace(placeholder, original)
            table_lines[i] = line

    temp_content = "\n".join(table_lines)

    # Process tables with selectively restored content
    table_processed_content = convert_tables_to_latex(
        temp_content, protected_backtick_content
    )

    # IMPORTANT: Protect entire LaTeX table blocks from further markdown processing
    # This prevents bold/italic/citation conversions from affecting table content
    def protect_latex_table(match):
        table_content = match.group(0)
        placeholder = f"XXPROTECTEDTABLEXX{len(protected_tables)}XXPROTECTEDTABLEXX"
        protected_tables[placeholder] = table_content
        return placeholder

    # Protect all LaTeX table environments from further processing
    table_processed_content = re.sub(
        r"\\begin\{table\*?\}.*?\\end\{table\*?\}",
        protect_latex_table,
        table_processed_content,
        flags=re.DOTALL,
    )

    # Re-protect any backtick content that wasn't converted to \texttt{} in tables
    for original, placeholder in [
        (v, k) for k, v in protected_backtick_content.items()
    ]:
        if original in table_processed_content:
            table_processed_content = table_processed_content.replace(
                original, placeholder
            )

    content = table_processed_content

    # Convert figures BEFORE headers to avoid conflicts
    content = convert_figures_to_latex(content)

    # Convert figure references BEFORE citations to avoid conflicts
    content = convert_figure_references_to_latex(content)

    # Convert headers
    content = re.sub(r"^# (.+)$", r"\\section{\1}", content, flags=re.MULTILINE)
    content = re.sub(r"^## (.+)$", r"\\subsection{\1}", content, flags=re.MULTILINE)
    content = re.sub(r"^### (.+)$", r"\\subsubsection{\1}", content, flags=re.MULTILINE)
    content = re.sub(r"^#### (.+)$", r"\\paragraph{\1}", content, flags=re.MULTILINE)

    # Convert citations - handle multiple citation formats
    # First handle bracketed multiple citations like [@citation1;@citation2]
    def process_multiple_citations(match):
        citations_text = match.group(1)
        # Split by semicolon and clean up each citation
        citations = []
        for cite in citations_text.split(";"):
            # Remove @ symbol and whitespace
            clean_cite = cite.strip().lstrip("@")
            if clean_cite:
                citations.append(clean_cite)
        return "\\cite{" + ",".join(citations) + "}"

    content = re.sub(r"\[(@[^]]+)\]", process_multiple_citations, content)

    # Handle single citations like @citation_key (but not figure references)
    # Allow alphanumeric, underscore, and hyphen in citation keys
    # Exclude figure references by not matching @fig: patterns
    content = re.sub(r"@(?!fig:)([a-zA-Z0-9_-]+)", r"\\cite{\1}", content)

    # Convert bold and italic (backtick content already protected earlier)
    content = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", content)
    content = re.sub(r"\*(.+?)\*", r"\\textit{\1}", content)

    # Convert markdown links to LaTeX URLs
    content = convert_links_to_latex(content)

    # Handle underscores carefully - LaTeX is very picky about this
    # We need to escape underscores in text mode but NOT double-escape them

    # First convert backticks to texttt with proper underscore handling
    def process_code_blocks(match):
        code_content = match.group(1)
        # In texttt, underscores need to be escaped as \_
        # Use placeholder to avoid double-escaping issues
        escaped_content = code_content.replace("_", "XUNDERSCOREX")
        return "\\texttt{" + escaped_content + "}"

    # Restore protected backtick content before processing code blocks
    for placeholder, original in protected_backtick_content.items():
        content = content.replace(placeholder, original)

    # Process both double and single backticks
    content = re.sub(
        r"``([^`]+)``", process_code_blocks, content
    )  # Double backticks first
    content = re.sub(
        r"`([^`]+)`", process_code_blocks, content
    )  # Then single backticks

    # Now handle remaining underscores in file paths within parentheses
    def escape_file_paths_in_parens(match):
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

    content = re.sub(r"\(([^)]+)\)", escape_file_paths_in_parens, content)

    # Handle remaining underscores in file names and paths
    # Match common filename patterns: WORD_WORD.ext, word_word.ext, etc.
    def escape_filenames(match):
        filename = match.group(0)
        # Escape underscores in anything that looks like a filename
        return filename.replace("_", "XUNDERSCOREX")

    # Match filenames with extensions
    content = re.sub(
        r"\b[\w]+_[\w._]*\.(md|yml|yaml|bib|tex|py|csv|pdf|png|svg|jpg)\b",
        escape_filenames,
        content,
    )

    # Also match numbered files like 00_CONFIG, 01_MAIN, etc.
    content = re.sub(r"\b\d+_[A-Z_]+\b", escape_filenames, content)

    # Final step: replace all placeholders with properly escaped underscores
    content = content.replace("XUNDERSCOREX", "\\_")

    # Restore protected tables at the very end (after all other conversions)
    for placeholder, table_content in protected_tables.items():
        content = content.replace(placeholder, table_content)

    return content


def convert_citations_to_latex(text):
    """Convert markdown citations to LaTeX format."""

    # Handle bracketed multiple citations like [@citation1;@citation2]
    def process_multiple_citations(match):
        citations_text = match.group(1)
        # Split by semicolon and clean up each citation
        citations = []
        for cite in citations_text.split(";"):
            # Remove @ symbol and whitespace
            clean_cite = cite.strip().lstrip("@")
            if clean_cite:
                citations.append(clean_cite)
        return "\\cite{" + ",".join(citations) + "}"

    text = re.sub(r"\[(@[^]]+)\]", process_multiple_citations, text)

    # Handle single citations like @citation_key
    # Allow alphanumeric, underscore, and hyphen in citation keys
    text = re.sub(r"@([a-zA-Z0-9_-]+)", r"\\cite{\1}", text)

    return text


def convert_text_formatting_to_latex(text):
    """Convert markdown text formatting to LaTeX."""
    # Convert bold and italic
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"\*(.+?)\*", r"\\textit{\1}", text)

    # Convert code
    text = re.sub(r"`(.+?)`", r"\\texttt{\1}", text)

    return text


def convert_headers_to_latex(text):
    """Convert markdown headers to LaTeX sections."""
    text = re.sub(r"^## (.+)$", r"\\section{\1}", text, flags=re.MULTILINE)
    text = re.sub(r"^### (.+)$", r"\\subsection{\1}", text, flags=re.MULTILINE)
    text = re.sub(r"^#### (.+)$", r"\\subsubsection{\1}", text, flags=re.MULTILINE)

    return text


def convert_html_comments_to_latex(text):
    """Convert HTML comments to LaTeX comments."""

    def replace_comment(match):
        comment_content = match.group(1)
        # Convert to LaTeX comment - each line needs to start with %
        lines = comment_content.split("\n")
        latex_comment_lines = []
        for line in lines:
            line = line.strip()
            if line:
                latex_comment_lines.append("% " + line)
            else:
                latex_comment_lines.append("%")
        return "\n".join(latex_comment_lines)

    return re.sub(r"<!--(.*?)-->", replace_comment, text, flags=re.DOTALL)


def convert_html_tags_to_latex(text):
    """Convert common HTML tags to LaTeX equivalents."""
    # Convert line breaks
    text = re.sub(r"<br\s*/?>", r"\\\\", text, flags=re.IGNORECASE)

    # Convert bold tags
    text = re.sub(
        r"<b>(.*?)</b>", r"\\textbf{\1}", text, flags=re.IGNORECASE | re.DOTALL
    )
    text = re.sub(
        r"<strong>(.*?)</strong>",
        r"\\textbf{\1}",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # Convert italic tags
    text = re.sub(
        r"<i>(.*?)</i>", r"\\textit{\1}", text, flags=re.IGNORECASE | re.DOTALL
    )
    text = re.sub(
        r"<em>(.*?)</em>", r"\\textit{\1}", text, flags=re.IGNORECASE | re.DOTALL
    )

    # Convert code tags
    text = re.sub(
        r"<code>(.*?)</code>", r"\\texttt{\1}", text, flags=re.IGNORECASE | re.DOTALL
    )

    return text


def convert_links_to_latex(text):
    """Convert markdown links to LaTeX URLs."""

    # Handle markdown links [text](url)
    def process_link(match):
        link_text = match.group(1)
        url = match.group(2)

        # Escape special LaTeX characters in URL
        url_escaped = escape_url_for_latex(url)

        # If link text is the same as URL, use \url{}
        if link_text.strip() == url.strip():
            return f"\\url{{{url_escaped}}}"
        else:
            # Use \href{url}{text} for links with different text
            return f"\\href{{{url_escaped}}}{{{link_text}}}"

    # Convert [text](url) format
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", process_link, text)

    # Handle bare URLs (convert standalone URLs to \url{})
    # Use a simpler approach: find URLs that are not already in LaTeX commands
    def process_bare_url(match):
        url = match.group(0)
        url_escaped = escape_url_for_latex(url)
        return f"\\url{{{url_escaped}}}"

    # First pass: protect existing LaTeX commands by temporarily replacing them
    latex_url_pattern = r"\\url\{[^}]+\}"
    latex_href_pattern = r"\\href\{[^}]+\}\{[^}]+\}"

    # Store existing LaTeX commands to avoid double-processing
    protected_commands = []

    def protect_latex_command(match):
        protected_commands.append(match.group(0))
        return f"__PROTECTED_LATEX_CMD_{len(protected_commands)-1}__"

    # Protect existing LaTeX URL commands
    text = re.sub(latex_url_pattern, protect_latex_command, text)
    text = re.sub(latex_href_pattern, protect_latex_command, text)

    # Now convert bare URLs
    text = re.sub(r"https?://[^\s\}>\]]+", process_bare_url, text)

    # Restore protected LaTeX commands
    for i, cmd in enumerate(protected_commands):
        text = text.replace(f"__PROTECTED_LATEX_CMD_{i}__", cmd)

    return text


def escape_url_for_latex(url):
    """Escape special characters in URLs for LaTeX."""
    # Characters that need escaping in LaTeX URLs
    # Most URLs work fine in \url{} and \href{} without escaping
    # but we should handle common problematic characters
    url = url.replace("#", "\\#")  # Hash symbols need escaping
    url = url.replace("%", "\\%")  # Percent symbols need escaping

    # Note: underscores usually don't need escaping in \url{} but can be
    # handled if needed
    # url = url.replace('_', '\\_')

    return url


def convert_figures_to_latex(text):
    """Convert markdown figures to LaTeX figure environments."""

    # First protect code blocks from figure processing
    def protect_code_blocks(match):
        return f"__CODE_BLOCK_{len(protected_blocks)}__"

    protected_blocks = []

    # Protect inline code (backticks)
    def protect_inline_code(match):
        protected_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(protected_blocks)-1}__"

    text = re.sub(r"`[^`]+`", protect_inline_code, text)

    # Protect fenced code blocks
    def protect_fenced_code(match):
        protected_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(protected_blocks)-1}__"

    text = re.sub(r"```.*?```", protect_fenced_code, text, flags=re.DOTALL)

    def parse_figure_attributes(attr_string):
        r"""Parse figure attributes like {#fig:1 tex_position="!ht" width="0.8"}."""
        attributes = {}

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

    # Pattern to match new format: ![](path)\n{attributes} **Caption text**
    def process_new_figure_format(match):
        path = match.group(1)
        attr_string = match.group(2)
        caption = match.group(3)

        # Parse attributes
        attributes = parse_figure_attributes(attr_string)

        # Convert path from FIGURES/ to Figures/ for LaTeX
        latex_path = path.replace("FIGURES/", "Figures/")

        # Convert SVG to PNG for LaTeX compatibility
        if latex_path.endswith(".svg"):
            latex_path = latex_path.replace(".svg", ".png")

        # Get positioning (default to 'ht' if not specified)
        position = attributes.get("tex_position", "ht")

        # Get width (default to '\linewidth' if not specified)
        width = attributes.get("width", "\\linewidth")
        if not width.startswith("\\"):
            width = (
                f"{width}\\linewidth"  # Assume fraction of linewidth if no backslash
            )

        # Create LaTeX figure environment
        latex_figure = f"""\\begin{{figure}}[{position}]
\\centering
\\includegraphics[width={width}]{{{latex_path}}}
\\caption{{{caption}}}"""

        # Add label if ID is present
        if "id" in attributes:
            latex_figure += f"\n\\label{{{attributes['id']}}}"

        latex_figure += "\n\\end{figure}"

        return latex_figure

    # Pattern to match new format with full caption text
    def process_new_figure_format_full(match, parse_attrs_func):
        path = match.group(1)
        attr_string = match.group(2)
        caption_text = match.group(3).strip()

        # Parse attributes
        attributes = parse_attrs_func(attr_string)

        # Convert path from FIGURES/ to Figures/ for LaTeX
        latex_path = path.replace("FIGURES/", "Figures/")

        # Convert SVG to PNG for LaTeX compatibility
        if latex_path.endswith(".svg"):
            latex_path = latex_path.replace(".svg", ".png")

        # Get positioning (default to 'ht' if not specified)
        position = attributes.get("tex_position", "ht")

        # Get width (default to '\linewidth' if not specified)
        width = attributes.get("width", "\\linewidth")
        if not width.startswith("\\"):
            width = (
                f"{width}\\linewidth"  # Assume fraction of linewidth if no backslash
            )

        # Process caption text to remove markdown formatting
        caption = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", caption_text)
        caption = re.sub(r"\*([^*]+)\*", r"\\textit{\1}", caption)

        # Create LaTeX figure environment
        latex_figure = f"""\\begin{{figure}}[{position}]
\\centering
\\includegraphics[width={width}]{{{latex_path}}}
\\caption{{{caption}}}"""

        # Add label if ID is present
        if "id" in attributes:
            latex_figure += f"\n\\label{{{attributes['id']}}}"

        latex_figure += "\n\\end{figure}"

        return latex_figure

    # Pattern to match: ![caption](path){attributes}
    def process_figure_with_attributes(match):
        caption = match.group(1)
        path = match.group(2)
        attr_string = match.group(3)

        # Parse attributes
        attributes = parse_figure_attributes(attr_string)

        # Convert path from FIGURES/ to Figures/ for LaTeX
        latex_path = path.replace("FIGURES/", "Figures/")

        # Convert SVG to PNG for LaTeX compatibility
        if latex_path.endswith(".svg"):
            latex_path = latex_path.replace(".svg", ".png")

        # Get positioning (default to 'ht' if not specified)
        position = attributes.get("tex_position", "ht")

        # Get width (default to '\linewidth' if not specified)
        width = attributes.get("width", "\\linewidth")
        if not width.startswith("\\"):
            width = (
                f"{width}\\linewidth"  # Assume fraction of linewidth if no backslash
            )

        # Create LaTeX figure environment
        latex_figure = f"""\\begin{{figure}}[{position}]
\\centering
\\includegraphics[width={width}]{{{latex_path}}}
\\caption{{{caption}}}"""

        # Add label if ID is present
        if "id" in attributes:
            latex_figure += f"\n\\label{{{attributes['id']}}}"

        latex_figure += "\n\\end{figure}"

        return latex_figure

    # Pattern to match: ![caption](path) without attributes
    def process_figure_without_attributes(match):
        caption = match.group(1)
        path = match.group(2)

        # Convert path from FIGURES/ to Figures/ for LaTeX
        latex_path = path.replace("FIGURES/", "Figures/")

        # Convert SVG to PNG for LaTeX compatibility
        if latex_path.endswith(".svg"):
            latex_path = latex_path.replace(".svg", ".png")

        # Create LaTeX figure environment without label
        latex_figure = f"""\\begin{{figure}}[ht]
\\centering
\\includegraphics[width=\\linewidth]{{{latex_path}}}
\\caption{{{caption}}}
\\end{{figure}}"""

        return latex_figure

    # First handle new format: ![](path)\n{attributes} **Caption text**
    text = re.sub(
        r"!\[\]\(([^)]+)\)\s*\n\{([^}]+)\}\s*(.+?)(?=\n\n|\n$|$)",
        lambda m: process_new_figure_format_full(m, parse_figure_attributes),
        text,
        flags=re.MULTILINE | re.DOTALL,
    )

    # Then handle figures with attributes (old format)
    text = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)\{([^}]+)\}", process_figure_with_attributes, text
    )

    # Finally handle figures without attributes (remaining ones)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", process_figure_without_attributes, text)

    # Restore protected code blocks
    for i, block in enumerate(protected_blocks):
        text = text.replace(f"__CODE_BLOCK_{i}__", block)

    return text


def convert_figure_references_to_latex(text):
    r"""Convert figure references from @fig:id and @sfig:id to LaTeX.
    
    Converts @fig:id to \\ref{fig:id} and @sfig:id to \\ref{sfig:id}.
    """
    # Convert @fig:id to \ref{fig:id}
    text = re.sub(r"@fig:([a-zA-Z0-9_-]+)", r"\\ref{fig:\1}", text)

    # Convert @sfig:id to \ref{sfig:id} (supplementary figures)
    text = re.sub(r"@sfig:([a-zA-Z0-9_-]+)", r"\\ref{sfig:\1}", text)

    return text


def convert_lists_to_latex(text):
    """Convert markdown lists to LaTeX list environments."""
    lines = text.split("\n")
    result_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check for unordered list (- or * at start of line)
        if re.match(r"^\s*[-*]\s+", line):
            # Start of unordered list
            list_lines = []
            indent_level = len(line) - len(line.lstrip())

            # Collect all consecutive list items at the same indent level
            while i < len(lines):
                current_line = lines[i]
                if re.match(rf"^\s{{0,{indent_level + 2}}}[-*]\s+", current_line):
                    # Extract the list item content (remove the bullet)
                    item_content = re.sub(r"^\s*[-*]\s+", "", current_line)
                    list_lines.append(f"  \\item {item_content}")
                    i += 1
                elif current_line.strip() == "":
                    # Empty line, might continue list
                    i += 1
                    if i < len(lines) and re.match(
                        rf"^\s{{0,{indent_level + 2}}}[-*]\s+", lines[i]
                    ):
                        continue
                    else:
                        break
                else:
                    # Not a list item, end of list
                    break

            # Add the complete itemize environment
            result_lines.append("\\begin{itemize}")
            result_lines.extend(list_lines)
            result_lines.append("\\end{itemize}")

        # Check for ordered list (number followed by . or ))
        elif re.match(r"^\s*\d+[.)]\s+", line):
            # Start of ordered list
            list_lines = []
            indent_level = len(line) - len(line.lstrip())

            # Collect all consecutive list items at the same indent level
            while i < len(lines):
                current_line = lines[i]
                if re.match(rf"^\s{{0,{indent_level + 2}}}\d+[.)]\s+", current_line):
                    # Extract the list item content (remove the number)
                    item_content = re.sub(r"^\s*\d+[.)]\s+", "", current_line)
                    list_lines.append(f"  \\item {item_content}")
                    i += 1
                elif current_line.strip() == "":
                    # Empty line, might continue list
                    i += 1
                    if i < len(lines) and re.match(
                        rf"^\s{{0,{indent_level + 2}}}\d+[.)]\s+", lines[i]
                    ):
                        continue
                    else:
                        break
                else:
                    # Not a list item, end of list
                    break

            # Add the complete enumerate environment
            result_lines.append("\\begin{enumerate}")
            result_lines.extend(list_lines)
            result_lines.append("\\end{enumerate}")

        else:
            # Regular line, not a list
            result_lines.append(line)
            i += 1

    return "\n".join(result_lines)


def convert_code_blocks_to_latex(text):
    """Convert markdown code blocks to LaTeX verbatim environments."""

    # Handle fenced code blocks first (``` ... ```)
    def process_fenced_code_block(match):
        code_content = match.group(1)

        # Use verbatim environment for code blocks
        # This preserves whitespace and special characters
        return f"\\begin{{verbatim}}\n{code_content}\n\\end{{verbatim}}"

    # Convert fenced code blocks first to protect them from further processing
    text = re.sub(
        r"^```(?:\w+)?\n(.*?)\n```$",
        process_fenced_code_block,
        text,
        flags=re.MULTILINE | re.DOTALL,
    )

    # Handle indented code blocks (4+ spaces at start of line)
    # But skip lines that are already inside verbatim environments
    lines = text.split("\n")
    result_lines = []
    i = 0
    in_verbatim = False

    while i < len(lines):
        line = lines[i]

        # Track verbatim environment state
        if "\\begin{verbatim}" in line:
            in_verbatim = True
            result_lines.append(line)
            i += 1
            continue
        elif "\\end{verbatim}" in line:
            in_verbatim = False
            result_lines.append(line)
            i += 1
            continue
        elif in_verbatim:
            # We're inside a verbatim block, don't process as indented code
            result_lines.append(line)
            i += 1
            continue

        # Check if line is indented with 4+ spaces (code block) and not in verbatim
        if re.match(r"^    ", line) and line.strip() and not in_verbatim:
            # Start of indented code block
            code_lines = []

            # Collect all consecutive indented lines
            while i < len(lines):
                current_line = lines[i]
                if re.match(r"^    ", current_line) or current_line.strip() == "":
                    # Remove 4 spaces of indentation
                    if current_line.startswith("    "):
                        code_lines.append(current_line[4:])
                    else:
                        code_lines.append(current_line)
                    i += 1
                else:
                    break

            # Remove trailing empty lines
            while code_lines and code_lines[-1].strip() == "":
                code_lines.pop()

            if code_lines:
                result_lines.append("\\begin{verbatim}")
                result_lines.extend(code_lines)
                result_lines.append("\\end{verbatim}")
        else:
            result_lines.append(line)
            i += 1

    return "\n".join(result_lines)


def convert_tables_to_latex(text, protected_backtick_content=None):
    """Convert markdown tables to LaTeX table environments."""
    lines = text.split("\n")
    result_lines = []
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
        if (
            "|" in line
            and line.strip().startswith("|")
            and line.strip().endswith("|")
            and i + 1 < len(lines)
            and "|" in lines[i + 1]
            and "-" in lines[i + 1]
        ):
            # Found a table! Extract it
            header_line = line.strip()

            # Parse header
            headers = [cell.strip() for cell in header_line.split("|")[1:-1]]
            num_cols = len(headers)

            # Skip header and separator
            i += 2

            # Collect data rows
            data_rows = []
            while i < len(lines) and lines[i].strip():
                current_line = lines[i].strip()
                if (
                    "|" in current_line
                    and current_line.startswith("|")
                    and current_line.endswith("|")
                ):
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
            new_format_caption = None
            table_id = None

            if (
                i < len(lines)
                and lines[i].strip() == ""
                and i + 1 < len(lines)
                and re.match(
                    r"^\{#[a-zA-Z0-9_:-]+\}\s*\*\*.*\*\*", lines[i + 1].strip()
                )
            ):
                # Found new format caption, parse it
                caption_line = lines[i + 1].strip()
                caption_match = re.match(
                    r"^\{#([a-zA-Z0-9_:-]+)\}\s*(.+)$", caption_line
                )
                if caption_match:
                    table_id = caption_match.group(1)
                    caption_text = caption_match.group(2)

                    # Process caption text to handle markdown formatting
                    new_format_caption = re.sub(
                        r"\*\*([^*]+)\*\*", r"\\textbf{\1}", caption_text
                    )
                    new_format_caption = re.sub(
                        r"\*([^*]+)\*", r"\\textit{\1}", new_format_caption
                    )

                    # Skip blank line and caption line
                    i += 2

            # Generate LaTeX table with the processed caption
            latex_table = generate_latex_table(
                headers,
                data_rows,
                new_format_caption or table_caption,
                table_width,
                table_id,
                protected_backtick_content,
            )
            result_lines.extend(latex_table.split("\n"))

            # Continue with next line (i is already incremented)
            continue

        # Not a table, add line as-is
        result_lines.append(line)
        i += 1

    return "\n".join(result_lines)


def generate_latex_table(
    headers,
    data_rows,
    caption=None,
    width="single",
    table_id=None,
    protected_backtick_content=None,
):
    """Generate LaTeX table from headers and data rows.

    Args:
        headers: List of header strings
        data_rows: List of data row lists
        caption: Optional table caption text
        width: "single" for single column, "double" for two-column table
        table_id: Optional table ID for labeling
        protected_backtick_content: Dict of protected backtick content placeholders
    """
    num_cols = len(headers)

    # Create column specification (all left-aligned with borders)
    col_spec = "|" + "l|" * num_cols

    # Convert markdown formatting in cells to LaTeX
    def format_cell(cell, is_markdown_example_column=False):
        # First restore any protected backtick content
        if protected_backtick_content:
            for placeholder, original in protected_backtick_content.items():
                cell = cell.replace(placeholder, original)

        # If this is the "Markdown Element" column, preserve literal syntax
        if is_markdown_example_column:
            # Only convert backticks to \texttt{} but preserve other markdown syntax
            def process_code_only(match):
                code_content = match.group(1)
                # Escape special characters for LaTeX
                code_content = code_content.replace("\\", "\\textbackslash{}")
                code_content = code_content.replace("{", "\\{")
                code_content = code_content.replace("}", "\\}")
                code_content = code_content.replace("&", "\\&")
                code_content = code_content.replace("%", "\\%")
                code_content = code_content.replace("$", "\\$")
                code_content = code_content.replace("#", "\\#")
                code_content = code_content.replace("^", "\\textasciicircum{}")
                code_content = code_content.replace("~", "\\textasciitilde{}")
                code_content = code_content.replace("_", "\\_")
                return f"\\texttt{{{code_content}}}"

            # Convert backticks to \texttt{} but preserve ** * @ [] etc.
            cell = re.sub(r"`([^`]+)`", process_code_only, cell)

            # For non-backtick content, wrap entire cell in \texttt{} to preserve
            # literal display
            # This ensures markdown syntax like **bold**, @citation, # Header etc.
            # display literally
            if not re.search(r"\\texttt\{", cell):  # Only if not already wrapped
                # Escape special characters that would break LaTeX
                cell = cell.replace("\\", "\\textbackslash{}")
                cell = cell.replace("{", "\\{")
                cell = cell.replace("}", "\\}")
                cell = cell.replace("&", "\\&")
                cell = cell.replace("%", "\\%")
                cell = cell.replace("$", "\\$")
                cell = cell.replace("#", "\\#")
                cell = cell.replace("^", "\\textasciicircum{}")
                cell = cell.replace("~", "\\textasciitilde{}")
                cell = cell.replace("_", "\\_")
                return f"\\texttt{{{cell}}}"

            return cell

        # Handle code blocks specially - they need different treatment in tables
        def process_code_in_table(match):
            code_content = match.group(1)
            # Replace problematic characters that break tables
            # Order matters - do backslashes first, then other characters
            code_content = code_content.replace("\\", "\\textbackslash{}")
            code_content = code_content.replace("{", "\\{")
            code_content = code_content.replace("}", "\\}")
            code_content = code_content.replace("&", "\\&")
            code_content = code_content.replace("%", "\\%")
            code_content = code_content.replace("$", "\\$")
            code_content = code_content.replace("#", "\\#")
            code_content = code_content.replace("^", "\\textasciicircum{}")
            code_content = code_content.replace("~", "\\textasciitilde{}")
            code_content = code_content.replace("_", "\\_")
            # For multiline code in tables, replace newlines with spaces
            code_content = code_content.replace("\n", " ")
            # Remove multiple spaces
            code_content = re.sub(r"\s+", " ", code_content).strip()
            return f"\\texttt{{{code_content}}}"

        # Process code blocks - use simple approach that handles all cases
        # First handle the specific case of `` `code` `` (double backticks with
        # inner backticks)
        cell = re.sub(
            r"``\s*`([^`]+)`\s*``", lambda m: f"\\texttt{{{m.group(1)}}}", cell
        )
        # Then handle regular double backticks
        cell = re.sub(r"``([^`]+)``", process_code_in_table, cell)
        # Finally handle single backticks
        cell = re.sub(r"`([^`]+)`", process_code_in_table, cell)

        # Then escape remaining special characters outside of \texttt{}
        def escape_outside_texttt(text):
            # Simple approach: split by \texttt{} blocks and escape only outside parts
            parts = re.split(r"(\\texttt\{[^}]*\})", text)
            result = []
            for _i, part in enumerate(parts):
                if part.startswith("\\texttt{"):
                    # This is a texttt block, don't escape
                    result.append(part)
                else:
                    # This is regular text, escape it
                    part = part.replace("&", "\\&")
                    part = part.replace("%", "\\%")
                    part = part.replace("$", "\\$")
                    part = part.replace("#", "\\#")
                    part = part.replace("^", "\\textasciicircum{}")
                    part = part.replace("~", "\\textasciitilde{}")
                    part = part.replace("_", "\\_")
                    result.append(part)
            return "".join(result)

        cell = escape_outside_texttt(cell)
        return cell

    # Check if first column is "Markdown Element" to preserve literal syntax
    is_markdown_syntax_table = (
        len(headers) > 0 and headers[0].lower().strip() == "markdown element"
    )

    # Format headers
    formatted_headers = []
    for i, header in enumerate(headers):
        is_markdown_col = is_markdown_syntax_table and i == 0
        formatted_headers.append(format_cell(header, is_markdown_col))

    # Format data rows
    formatted_data_rows = []
    for row in data_rows:
        formatted_row = []
        for i, cell in enumerate(row):
            is_markdown_col = is_markdown_syntax_table and i == 0
            formatted_row.append(format_cell(cell, is_markdown_col))
        formatted_data_rows.append(formatted_row)

    # Choose table environment based on width
    if width == "double":
        table_env = "table*"
        position = "[!ht]"  # Use !ht for two-column tables
    else:
        table_env = "table"
        position = "[ht]"

    # Build LaTeX table
    latex_lines = [
        f"\\begin{{{table_env}}}{position}",
        "\\centering",
        f"\\begin{{tabular}}{{{col_spec}}}",
        "\\hline",
    ]

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

    # Add caption at the bottom, left-aligned like figures
    if caption:
        # Use \raggedright to make caption left-aligned
        latex_lines.append("\\raggedright")
        latex_lines.append(f"\\caption{{{caption}}}")
        # Use provided table_id or generate label from caption
        label = table_id if table_id else "tab:comparison"
        latex_lines.append(f"\\label{{{label}}}")

    # Close table environment
    latex_lines.append(f"\\end{{{table_env}}}")

    return "\n".join(latex_lines)
