# load tex template and generate article
import os
import re
import argparse
from pathlib import Path
try:
    import yaml
except ImportError:
    yaml = None

# Import markdown to LaTeX conversion functions
from md2tex import extract_content_sections

# template is on same level as this script
TEMPLATE_PATH = Path(__file__).parent.parent / "template.tex"

# create output directory if it doesn't exist
def create_output_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    else:
        print(f"Output directory already exists: {output_dir}")

# Look for 00_ARTICLE.md in the current directory
def find_article_md():
    current_dir = Path.cwd()
    article_md = current_dir / "00_ARTICLE.md"
    if article_md.exists():
        return article_md
    else:
        raise FileNotFoundError(f"00_ARTICLE.md not found in {current_dir}")
    
# Extract yaml metadata from the markdown file
def extract_yaml_metadata(md_file):
    with open(md_file, 'r') as file:
        content = file.read()
    
    # Use regex to find YAML metadata block
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        yaml_content = match.group(1)
        if yaml:
            try:
                return yaml.safe_load(yaml_content)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML: {e}")
                return {}
        else:
            # Fallback to simple parsing if yaml is not available
            return parse_yaml_simple(yaml_content)
    else:
        raise ValueError("YAML metadata not found in the markdown file.")

def parse_yaml_simple(yaml_content):
    """Simple YAML parser for basic key-value pairs"""
    metadata = {}
    lines = yaml_content.split('\n')
    current_key = None
    current_value = []
    
    for line in lines:
        line = line.strip()
        if ':' in line and not line.startswith('-'):
            if current_key:
                if isinstance(current_value, list) and len(current_value) == 1:
                    metadata[current_key] = current_value[0]
                else:
                    metadata[current_key] = current_value
            
            key, value = line.split(':', 1)
            current_key = key.strip()
            value = value.strip().strip('"\'')
            if value:
                current_value = value
            else:
                current_value = []
        elif line.startswith('-') and current_key:
            item = line[1:].strip().strip('"\'')
            if isinstance(current_value, list):
                current_value.append(item)
            else:
                current_value = [current_value, item] if current_value else [item]
    
    if current_key:
        if isinstance(current_value, list) and len(current_value) == 1:
            metadata[current_key] = current_value[0]
        else:
            metadata[current_key] = current_value
    
    return metadata
    
# Generate the article using the template
def generate_article(output_dir, yaml_metadata):
    with open(TEMPLATE_PATH, 'r') as template_file:
        template_content = template_file.read()

    # if use_line_numbers is True, add the line numbers to the template
    txt = ""
    if 'use_line_numbers' in yaml_metadata:
        use_line_numbers = str(yaml_metadata['use_line_numbers']).lower() == 'true'
        if use_line_numbers:
            txt = "% Add number to the lines\n\\usepackage{lineno}\n\\linenumbers\n"            
    template_content = template_content.replace("<PY-RPL:USE-LINE-NUMBERS>", txt)

    # add the lead author to the template
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

    # replace the long title in the template
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

    # replace the short title in the template
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
    article_md = find_article_md()
    content_sections = extract_content_sections(article_md)
    
    # Replace content placeholders with extracted sections
    template_content = template_content.replace("<PY-RPL:ABSTRACT>", content_sections.get('abstract', ''))
    template_content = template_content.replace("<PY-RPL:MAIN-CONTENT>", content_sections.get('main', ''))
    template_content = template_content.replace("<PY-RPL:METHODS>", content_sections.get('methods', ''))
    template_content = template_content.replace("<PY-RPL:DATA-AVAILABILITY>", content_sections.get('data_availability', ''))
    template_content = template_content.replace("<PY-RPL:CODE-AVAILABILITY>", content_sections.get('code_availability', ''))
    template_content = template_content.replace("<PY-RPL:AUTHOR-CONTRIBUTIONS>", content_sections.get('author_contributions', ''))
    template_content = template_content.replace("<PY-RPL:ACKNOWLEDGEMENTS>", content_sections.get('acknowledgements', ''))

    # Write the generated article to the output directory
    output_file = Path(output_dir) / "ARTICLE.tex"
    with open(output_file, 'w') as file:
        file.write(template_content)
    
    print(f"Generated article: {output_file}")
    return output_file

def generate_authors_and_affiliations(yaml_metadata):
    """Generate LaTeX author and affiliation blocks from YAML metadata"""
    authors_latex = []
    affiliations_latex = []
    
    # Extract authors and affiliations from metadata
    authors = yaml_metadata.get('authors', [])
    affiliations = yaml_metadata.get('affiliations', [])
    
    if not authors:
        # Fallback to default if no authors specified
        return """% Use letters for affiliations, numbers to show equal authorship (if applicable) and to indicate the corresponding author
\\author[1]{Author Name}
\\affil[1]{Institution}"""
    
    # Create affiliations mapping from shortname to number and full details
    affil_map = {}
    used_affiliations = []  # Keep order of first appearance
    
    # First pass: collect all unique affiliations used by authors in order of appearance
    for author in authors:
        if isinstance(author, dict):
            author_affiliations = author.get('affiliations', [])
            for affil_short in author_affiliations:
                if affil_short not in used_affiliations:
                    used_affiliations.append(affil_short)
    
    # Create mapping and LaTeX for used affiliations in order of appearance
    for i, affil_short in enumerate(used_affiliations, 1):
        affil_map[affil_short] = i
        
        # Find full affiliation details
        full_affil = affil_short  # fallback to shortname
        for affil_detail in affiliations:
            if isinstance(affil_detail, dict) and affil_detail.get('shortname') == affil_short:
                full_name = affil_detail.get('full_name', affil_short)
                location = affil_detail.get('location', '')
                if location:
                    full_affil = f"{full_name}, {location}"
                else:
                    full_affil = full_name
                break
        
        affiliations_latex.append(f"\\affil[{i}]{{{full_affil}}}")
    
    # Create authors with proper affiliation mapping
    corresponding_authors = []
    equal_contributors = []
    
    for author in authors:
        if isinstance(author, dict):
            name = author.get('name', 'Unknown Author')
            author_affiliations = author.get('affiliations', [])
            is_corresponding = author.get('corresponding_author', False)
            is_equal = author.get('co_first_author', False)
            
            # Map author affiliations to numbers and sort them
            affil_numbers = []
            for affil in author_affiliations:
                if affil in affil_map:
                    affil_numbers.append(affil_map[affil])
            
            # Sort affiliation numbers for each author
            affil_numbers.sort()
            
            # Format affiliations for author
            if affil_numbers:
                affil_str = ','.join(map(str, affil_numbers))
            else:
                affil_str = '1'  # Default to first affiliation
            
            # Add special markers
            special_markers = []
            if is_equal:
                special_markers.append('*')
                equal_contributors.append(name)
            if is_corresponding:
                special_markers.append('\\Letter')
                corresponding_authors.append(name)
            
            if special_markers:
                affil_str += ',' + ','.join(special_markers)
            
            authors_latex.append(f"\\author[{affil_str}]{{{name}}}")
        elif isinstance(author, str):
            authors_latex.append(f"\\author[1]{{{author}}}")
    
    # Add special affiliations for equal contributors
    if equal_contributors:
        affiliations_latex.append("\\affil[*]{Equally contributed authors}")
    
    # Combine all parts
    result = "% Authors and affiliations generated from metadata\n"
    result += '\n'.join(authors_latex)
    result += '\n'
    result += '\n'.join(affiliations_latex)
    
    return result

def generate_corresponding_authors(yaml_metadata):
    """Generate LaTeX corresponding authors section from YAML metadata"""
    authors = yaml_metadata.get('authors', [])
    
    if not authors:
        return "% No corresponding authors found\n"
    
    corresponding_authors = []
    
    for author in authors:
        if isinstance(author, dict):
            # Check if this author is marked as corresponding author
            is_corresponding = author.get('corresponding_author', False)
            
            if is_corresponding:
                name = author.get('name', 'Unknown Author')
                email = author.get('email', '')
                
                # Generate abbreviated name (first letter of first and middle names, then last name)
                name_parts = name.split()
                if len(name_parts) >= 2:
                    # Get first letters of all names except the last one
                    initials = [part[0].upper() for part in name_parts[:-1]]
                    last_name = name_parts[-1]
                    abbreviated_name = '. '.join(initials) + '. ' + last_name
                else:
                    abbreviated_name = name
                
                # Format contact information
                contact_info = []
                if email:
                    # Convert @ to \at for LaTeX
                    email_tex = email.replace('@', '\\at ')
                    contact_info.append(email_tex)
                # Note: Bluesky handles excluded from corresponding authors section
                
                if contact_info:
                    contact_str = ', '.join(contact_info)
                    corresponding_authors.append(f"({abbreviated_name}) {contact_str}")
                else:
                    # If no contact info, just include the abbreviated name
                    corresponding_authors.append(f"({abbreviated_name})")
    
    if corresponding_authors:
        result = "\\begin{corrauthor}\n"
        result += ', \n'.join(corresponding_authors)
        result += "\n\\end{corrauthor}"
        return result
    else:
        return "% No corresponding authors found\n"

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

def generate_extended_author_info(yaml_metadata):
    """Generate LaTeX extended author information section from YAML metadata"""
    authors = yaml_metadata.get('authors', [])
    
    if not authors:
        return "% No authors found for extended author information\n"
    
    def escape_latex_special_chars(text):
        """Escape special LaTeX characters in text"""
        # Replace common special characters that need escaping in LaTeX
        text = text.replace('_', '\\_')
        text = text.replace('&', '\\&')
        text = text.replace('%', '\\%')
        text = text.replace('#', '\\#')
        text = text.replace('{', '\\{')
        text = text.replace('}', '\\}')
        return text
    
    result = "\\vspace*{-\\baselineskip}\n"
    result += "\\begin{itemize}\n"
    result += "\\setlength\\itemsep{-0.5em}\n\n"
    
    author_items = []
    
    for author in authors:
        if isinstance(author, dict):
            name = author.get('name', 'Unknown Author')
            orcid = author.get('orcid', '')
            
            # Social media handles
            twitter = author.get('twitter', '')
            x = author.get('x', '')  
            bluesky = author.get('bluesky', '')
            linkedin = author.get('linkedin', '')
            
            # Build the author line starting with name and colon
            author_line = f"\\item {name}:"
            
            # Add ORCID if available
            if orcid:
                # Remove any https://orcid.org/ prefix if present
                orcid_clean = orcid.replace('https://orcid.org/', '').replace('http://orcid.org/', '')
                author_line += f"\n\\orcidicon{{{orcid_clean}}};"
            
            # Add social media icons in order: Twitter/X, Bluesky, LinkedIn
            social_icons = []
            
            # Prefer X over Twitter if both are present
            if x:
                # Clean X handle (remove @ if present)
                x_clean = x.replace('@', '').replace('https://x.com/', '').replace('http://x.com/', '')
                x_clean = escape_latex_special_chars(x_clean)
                social_icons.append(f"\\xicon{{{x_clean}}}")
            elif twitter:
                # Clean Twitter handle (remove @ if present)
                twitter_clean = twitter.replace('@', '').replace('https://twitter.com/', '').replace('http://twitter.com/', '')
                twitter_clean = escape_latex_special_chars(twitter_clean)
                social_icons.append(f"\\twittericon{{{twitter_clean}}}")
            
            if bluesky:
                # Clean Bluesky handle (remove @ if present)
                bluesky_clean = bluesky.replace('@', '').replace('https://bsky.app/profile/', '').replace('http://bsky.app/profile/', '')
                bluesky_clean = escape_latex_special_chars(bluesky_clean)
                social_icons.append(f"\\blueskyicon{{{bluesky_clean}}}")
                
            if linkedin:
                # Clean LinkedIn handle
                linkedin_clean = linkedin.replace('https://linkedin.com/in/', '').replace('http://linkedin.com/in/', '')
                linkedin_clean = escape_latex_special_chars(linkedin_clean)
                social_icons.append(f"\\linkedinicon{{{linkedin_clean}}}")
            
            # Add social media icons with semicolon separators
            if social_icons:
                author_line += "\n" + ";\n".join(social_icons)
            
            author_items.append(author_line)
    
    result += "\n\n".join(author_items)
    result += "\n\n\\end{itemize}\n"
    result += "\\vspace*{-.5\\baselineskip}"
    
    return result

def generate_bibliography(yaml_metadata):
    """Generate LaTeX bibliography section from YAML metadata"""
    bibliography = yaml_metadata.get('bibliography', '01_REFERENCES')
    
    # Remove .bib extension if present
    if bibliography.endswith('.bib'):
        bibliography = bibliography[:-4]
    
    return f"\\bibliography{{{bibliography}}}"

def main():
    parser = argparse.ArgumentParser(description='Generate LaTeX article from markdown template')
    parser.add_argument('--output-dir', '-o', default='output', help='Output directory (default: output)')
    
    args = parser.parse_args()
    
    try:
        # Create output directory
        create_output_dir(args.output_dir)
        
        # Find and parse the article markdown
        article_md = find_article_md()
        print(f"Found article: {article_md}")
        
        yaml_metadata = extract_yaml_metadata(article_md)
        print(f"Extracted metadata: {list(yaml_metadata.keys()) if yaml_metadata else 'None'}")
        
        # Generate the article
        generate_article(args.output_dir, yaml_metadata)
        
        print("Article generation completed successfully!")
        
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        print("Traceback:")
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())






    