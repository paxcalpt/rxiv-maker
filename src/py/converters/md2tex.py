"""Markdown to LaTeX conversion module for RXiv-Forge.

This module handles the conversion of markdown content to LaTeX format,
including section extraction, citation processing, and text formatting.
"""

import re


def extract_content_sections(article_md):
    """Extract content sections from markdown file or content string and convert to LaTeX"""
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
    """Map section title to standardized key"""
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
    """Convert basic markdown formatting to LaTeX"""
    # Convert HTML comments to LaTeX comments
    content = convert_html_comments_to_latex(content)

    # Convert code blocks BEFORE other processing to protect their content
    content = convert_code_blocks_to_latex(content)

    # Convert lists BEFORE other processing to avoid conflicts
    content = convert_lists_to_latex(content)

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

    # Convert bold and italic
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

    content = re.sub(r"`([^`]+)`", process_code_blocks, content)

    # Now handle remaining underscores in file paths within parentheses
    def escape_file_paths_in_parens(match):
        paren_content = match.group(1)
        # Only escape if it looks like a file path (has extension or is all caps directory)
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

    return content


def convert_citations_to_latex(text):
    """Convert markdown citations to LaTeX format"""

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
    """Convert markdown text formatting to LaTeX"""
    # Convert bold and italic
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"\*(.+?)\*", r"\\textit{\1}", text)

    # Convert code
    text = re.sub(r"`(.+?)`", r"\\texttt{\1}", text)

    return text


def convert_headers_to_latex(text):
    """Convert markdown headers to LaTeX sections"""
    text = re.sub(r"^## (.+)$", r"\\section{\1}", text, flags=re.MULTILINE)
    text = re.sub(r"^### (.+)$", r"\\subsection{\1}", text, flags=re.MULTILINE)
    text = re.sub(r"^#### (.+)$", r"\\subsubsection{\1}", text, flags=re.MULTILINE)

    return text


def convert_html_comments_to_latex(text):
    """Convert HTML comments to LaTeX comments"""

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


def convert_links_to_latex(text):
    """Convert markdown links to LaTeX URLs"""

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
    """Escape special characters in URLs for LaTeX"""
    # Characters that need escaping in LaTeX URLs
    # Most URLs work fine in \url{} and \href{} without escaping
    # but we should handle common problematic characters
    url = url.replace("#", "\\#")  # Hash symbols need escaping
    url = url.replace("%", "\\%")  # Percent symbols need escaping

    # Note: underscores usually don't need escaping in \url{} but can be handled if needed
    # url = url.replace('_', '\\_')

    return url


def convert_figures_to_latex(text):
    """Convert markdown figures to LaTeX figure environments"""

    def parse_figure_attributes(attr_string):
        """Parse figure attributes like {#fig:1 tex_position="!ht" width="0.8"}"""
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

    # First handle figures with attributes
    text = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)\{([^}]+)\}", process_figure_with_attributes, text
    )

    # Then handle figures without attributes (remaining ones)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", process_figure_without_attributes, text)

    return text


def convert_figure_references_to_latex(text):
    """Convert figure references from @fig:id to \\ref{fig:id}"""
    # Convert @fig:id to \ref{fig:id}
    text = re.sub(r"@fig:([a-zA-Z0-9_-]+)", r"\\ref{fig:\1}", text)

    return text


def convert_lists_to_latex(text):
    """Convert markdown lists to LaTeX list environments"""
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
    """Convert markdown code blocks to LaTeX verbatim environments"""

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
