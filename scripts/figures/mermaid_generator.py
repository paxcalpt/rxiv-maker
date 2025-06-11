"""
Mermaid diagram generation utilities for LaTeX documents.
This module provides tools to generate Mermaid diagrams as LaTeX-compatible images.
"""

import subprocess
import json
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import os

class MermaidGenerator:
    """Generator for Mermaid diagrams with LaTeX compatibility."""
    
    def __init__(self, cli_path: str = 'mmdc'):
        """
        Initialize the Mermaid generator.
        
        Args:
            cli_path: Path to mermaid-cli executable
        """
        self.cli_path = cli_path
        self._check_mermaid_cli()
    
    def _check_mermaid_cli(self) -> None:
        """Check if Mermaid CLI is available."""
        try:
            result = subprocess.run([self.cli_path, '--version'], 
                                  capture_output=True, text=True, check=True)
            print(f"Mermaid CLI version: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: Mermaid CLI not found. Please install with: npm install -g @mermaid-js/mermaid-cli")
    
    def generate_diagram(self, 
                        mermaid_code: str,
                        output_path: Path,
                        format: str = 'svg',
                        config: Optional[Dict[str, Any]] = None,
                        width: int = 800,
                        height: int = 600) -> bool:
        """
        Generate a Mermaid diagram from code.
        
        Args:
            mermaid_code: Mermaid diagram code
            output_path: Output file path
            format: Output format ('svg', 'png', 'pdf')
            config: Mermaid configuration
            width: Output width in pixels
            height: Output height in pixels
        
        Returns:
            True if successful, False otherwise
        """
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as mmd_file:
            mmd_file.write(mermaid_code)
            mmd_path = mmd_file.name
        
        try:
            # Prepare command
            cmd = [
                self.cli_path,
                '-i', mmd_path,
                '-o', str(output_path),
                '-w', str(width),
                '-H', str(height),
            ]
            
            # Add configuration if provided
            if config:
                config_path = mmd_path.replace('.mmd', '_config.json')
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
                cmd.extend(['-c', config_path])
            
            # Execute command
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Generated Mermaid diagram: {output_path}")
                return True
            else:
                print(f"Error generating Mermaid diagram: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Exception generating Mermaid diagram: {e}")
            return False
        finally:
            # Clean up temporary files
            os.unlink(mmd_path)
            config_path = mmd_path.replace('.mmd', '_config.json')
            if os.path.exists(config_path):
                os.unlink(config_path)
    
    def create_flowchart(self,
                        nodes: List[Dict[str, str]],
                        edges: List[Tuple[str, str, str]],
                        output_path: Path,
                        direction: str = 'TD') -> bool:
        """
        Create a flowchart diagram.
        
        Args:
            nodes: List of node dictionaries with 'id', 'label', 'shape'
            edges: List of (from_id, to_id, label) tuples
            output_path: Output file path
            direction: Flow direction ('TD', 'LR', 'BT', 'RL')
        
        Returns:
            True if successful
        """
        # Build Mermaid code
        code_lines = [f'flowchart {direction}']
        
        # Add nodes
        for node in nodes:
            node_id = node['id']
            label = node['label']
            shape = node.get('shape', 'rectangle')
            
            if shape == 'rectangle':
                code_lines.append(f'    {node_id}[{label}]')
            elif shape == 'circle':
                code_lines.append(f'    {node_id}(({label}))')
            elif shape == 'diamond':
                code_lines.append(f'    {node_id}{{{label}}}')
            elif shape == 'hexagon':
                code_lines.append(f'    {node_id}{{{{{label}}}}}')
        
        # Add edges
        for from_id, to_id, label in edges:
            if label:
                code_lines.append(f'    {from_id} -->|{label}| {to_id}')
            else:
                code_lines.append(f'    {from_id} --> {to_id}')
        
        mermaid_code = '\n'.join(code_lines)
        return self.generate_diagram(mermaid_code, output_path)
    
    def create_sequence_diagram(self,
                              participants: List[str],
                              messages: List[Tuple[str, str, str]],
                              output_path: Path) -> bool:
        """
        Create a sequence diagram.
        
        Args:
            participants: List of participant names
            messages: List of (from, to, message) tuples
            output_path: Output file path
        
        Returns:
            True if successful
        """
        code_lines = ['sequenceDiagram']
        
        # Add participants
        for participant in participants:
            code_lines.append(f'    participant {participant}')
        
        # Add messages
        for from_p, to_p, message in messages:
            code_lines.append(f'    {from_p}->>+{to_p}: {message}')
        
        mermaid_code = '\n'.join(code_lines)
        return self.generate_diagram(mermaid_code, output_path)
    
    def create_class_diagram(self,
                           classes: List[Dict[str, Any]],
                           relationships: List[Tuple[str, str, str]],
                           output_path: Path) -> bool:
        """
        Create a class diagram.
        
        Args:
            classes: List of class dictionaries with 'name', 'attributes', 'methods'
            relationships: List of (class1, class2, relationship_type) tuples
            output_path: Output file path
        
        Returns:
            True if successful
        """
        code_lines = ['classDiagram']
        
        # Add classes
        for cls in classes:
            name = cls['name']
            code_lines.append(f'    class {name} {{')
            
            # Add attributes
            for attr in cls.get('attributes', []):
                code_lines.append(f'        {attr}')
            
            # Add methods
            for method in cls.get('methods', []):
                code_lines.append(f'        {method}()')
            
            code_lines.append('    }')
        
        # Add relationships
        for cls1, cls2, rel_type in relationships:
            if rel_type == 'inheritance':
                code_lines.append(f'    {cls1} <|-- {cls2}')
            elif rel_type == 'composition':
                code_lines.append(f'    {cls1} *-- {cls2}')
            elif rel_type == 'aggregation':
                code_lines.append(f'    {cls1} o-- {cls2}')
            elif rel_type == 'association':
                code_lines.append(f'    {cls1} -- {cls2}')
        
        mermaid_code = '\n'.join(code_lines)
        return self.generate_diagram(mermaid_code, output_path)

# Default Mermaid configuration for LaTeX documents
DEFAULT_CONFIG = {
    "theme": "base",
    "themeVariables": {
        "primaryColor": "#ffffff",
        "primaryTextColor": "#000000",
        "primaryBorderColor": "#000000",
        "lineColor": "#000000",
        "secondaryColor": "#f5f5f5",
        "tertiaryColor": "#e0e0e0",
        "fontFamily": "Times, serif",
        "fontSize": "12px"
    },
    "flowchart": {
        "nodeSpacing": 50,
        "rankSpacing": 50,
        "curve": "basis"
    }
}

def create_mermaid_generator() -> MermaidGenerator:
    """Create a Mermaid generator with default settings."""
    return MermaidGenerator()

# Template functions for common diagram types
def create_process_flow(steps: List[str], output_path: Path) -> bool:
    """Create a simple process flow diagram."""
    generator = create_mermaid_generator()
    
    nodes = []
    edges = []
    
    for i, step in enumerate(steps):
        node_id = f"step{i+1}"
        nodes.append({
            'id': node_id,
            'label': step,
            'shape': 'rectangle'
        })
        
        if i > 0:
            edges.append((f"step{i}", node_id, ""))
    
    return generator.create_flowchart(nodes, edges, output_path)

def create_methodology_diagram(phases: List[Dict[str, Any]], output_path: Path) -> bool:
    """Create a methodology diagram with phases and sub-steps."""
    generator = create_mermaid_generator()
    
    nodes = []
    edges = []
    
    for i, phase in enumerate(phases):
        phase_id = f"phase{i+1}"
        nodes.append({
            'id': phase_id,
            'label': phase['name'],
            'shape': 'hexagon'
        })
        
        # Add sub-steps
        for j, substep in enumerate(phase.get('substeps', [])):
            substep_id = f"substep{i+1}_{j+1}"
            nodes.append({
                'id': substep_id,
                'label': substep,
                'shape': 'rectangle'
            })
            edges.append((phase_id, substep_id, ""))
        
        # Connect phases
        if i > 0:
            edges.append((f"phase{i}", phase_id, ""))
    
    return generator.create_flowchart(nodes, edges, output_path)
