#!/usr/bin/env python3
"""
Generate Mermaid diagrams for the article.
This script creates various Mermaid diagrams for methodology and workflow visualization.
"""

import sys
import os
from pathlib import Path

# Add the scripts directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from figures.mermaid_generator import (
    MermaidGenerator,
    create_process_flow,
    create_methodology_diagram,
    DEFAULT_CONFIG
)

def generate_methodology_diagram(output_dir: Path) -> None:
    """Generate methodology flowchart."""
    
    phases = [
        {
            'name': 'Data Collection',
            'substeps': ['Survey Design', 'Sampling', 'Data Acquisition']
        },
        {
            'name': 'Data Processing',
            'substeps': ['Cleaning', 'Validation', 'Transformation']
        },
        {
            'name': 'Analysis',
            'substeps': ['Statistical Analysis', 'Model Training', 'Validation']
        },
        {
            'name': 'Results',
            'substeps': ['Visualization', 'Interpretation', 'Documentation']
        }
    ]
    
    output_path = output_dir / 'methodology_diagram.svg'
    success = create_methodology_diagram(phases, output_path)
    
    if success:
        print(f"Generated methodology diagram: {output_path}")
    else:
        print("Failed to generate methodology diagram")

def generate_system_architecture(output_dir: Path) -> None:
    """Generate system architecture diagram."""
    
    generator = MermaidGenerator()
    
    nodes = [
        {'id': 'user', 'label': 'User Interface', 'shape': 'rectangle'},
        {'id': 'api', 'label': 'API Gateway', 'shape': 'hexagon'},
        {'id': 'auth', 'label': 'Authentication', 'shape': 'diamond'},
        {'id': 'processor', 'label': 'Data Processor', 'shape': 'rectangle'},
        {'id': 'ml', 'label': 'ML Engine', 'shape': 'rectangle'},
        {'id': 'db', 'label': 'Database', 'shape': 'circle'},
        {'id': 'cache', 'label': 'Cache', 'shape': 'circle'}
    ]
    
    edges = [
        ('user', 'api', 'HTTP'),
        ('api', 'auth', 'validate'),
        ('auth', 'processor', 'authorized'),
        ('processor', 'ml', 'analyze'),
        ('processor', 'db', 'store/retrieve'),
        ('ml', 'cache', 'cache results'),
        ('processor', 'user', 'response')
    ]
    
    output_path = output_dir / 'system_architecture.svg'
    success = generator.create_flowchart(nodes, edges, output_path, direction='TD')
    
    if success:
        print(f"Generated system architecture: {output_path}")
    else:
        print("Failed to generate system architecture")

def generate_workflow_diagram(output_dir: Path) -> None:
    """Generate workflow process diagram."""
    
    steps = [
        'Start Process',
        'Initialize Parameters',
        'Load Data',
        'Validate Input',
        'Process Data',
        'Generate Results',
        'Save Output',
        'End Process'
    ]
    
    output_path = output_dir / 'workflow_diagram.svg'
    success = create_process_flow(steps, output_path)
    
    if success:
        print(f"Generated workflow diagram: {output_path}")
    else:
        print("Failed to generate workflow diagram")

def generate_sequence_diagram(output_dir: Path) -> None:
    """Generate sequence diagram for system interactions."""
    
    generator = MermaidGenerator()
    
    participants = ['Client', 'Server', 'Database', 'External_API']
    
    messages = [
        ('Client', 'Server', 'Request data'),
        ('Server', 'Database', 'Query data'),
        ('Database', 'Server', 'Return results'),
        ('Server', 'External_API', 'Validate data'),
        ('External_API', 'Server', 'Validation response'),
        ('Server', 'Client', 'Processed data')
    ]
    
    output_path = output_dir / 'sequence_diagram.svg'
    success = generator.create_sequence_diagram(participants, messages, output_path)
    
    if success:
        print(f"Generated sequence diagram: {output_path}")
    else:
        print("Failed to generate sequence diagram")

def main():
    """Main function to generate all Mermaid diagrams."""
    # Determine output directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    output_dir = project_root / 'build' / 'figures'
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating Mermaid diagrams...")
    try:
        generate_methodology_diagram(output_dir)
        generate_system_architecture(output_dir)
        generate_workflow_diagram(output_dir)
        generate_sequence_diagram(output_dir)
        print("All Mermaid diagrams generated successfully!")
    except Exception as e:
        print(f"Error generating Mermaid diagrams: {e}")
        print("Note: Make sure Mermaid CLI is installed: npm install -g @mermaid-js/mermaid-cli")
        sys.exit(1)

if __name__ == '__main__':
    main()
