"""
YAML processing utilities for Article-Forge.

This module handles the extraction and parsing of YAML metadata from markdown files.
"""

import re
try:
    import yaml
except ImportError:
    yaml = None


def extract_yaml_metadata(md_file):
    """Extract yaml metadata from the markdown file"""
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
