# load tex template and generate article
import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import from auxiliary modules
from processors.yaml_processor import extract_yaml_metadata
from processors.template_processor import get_template_path, process_template_replacements
from utils import create_output_dir, find_article_md, write_article_output


def generate_article(output_dir, yaml_metadata):
    """Generate the article using the template"""
    template_path = get_template_path()
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    # Find and process the article markdown
    article_md = find_article_md()
    
    # Process all template replacements
    template_content = process_template_replacements(template_content, yaml_metadata, str(article_md))

    # Write the generated article to the output directory
    return write_article_output(output_dir, template_content)


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
        
        yaml_metadata = extract_yaml_metadata(str(article_md))
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






    