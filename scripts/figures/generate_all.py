"""
Main figure generation script that orchestrates all figure creation.
This script manages the generation of all figures for the article.
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Any
import argparse

def run_figure_script(script_path: Path) -> bool:
    """
    Run a figure generation script.
    
    Args:
        script_path: Path to the Python script
    
    Returns:
        True if successful, False otherwise
    """
    try:
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True, check=True)
        print(f"✓ {script_path.name} completed successfully")
        if result.stdout:
            print(f"  Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {script_path.name} failed")
        print(f"  Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"✗ {script_path.name} failed with exception: {e}")
        return False

def check_dependencies() -> Dict[str, bool]:
    """Check if required dependencies are available."""
    dependencies = {}
    
    # Check Python packages
    python_packages = ['matplotlib', 'seaborn', 'numpy', 'pandas']
    for package in python_packages:
        try:
            __import__(package)
            dependencies[package] = True
        except ImportError:
            dependencies[package] = False
    
    # Check Mermaid CLI
    try:
        subprocess.run(['mmdc', '--version'], capture_output=True, check=True)
        dependencies['mermaid-cli'] = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        dependencies['mermaid-cli'] = False
    
    return dependencies

def install_python_dependencies() -> bool:
    """Install Python dependencies using pip."""
    try:
        script_dir = Path(__file__).parent
        requirements_file = script_dir.parent.parent / 'requirements.txt'
        
        if requirements_file.exists():
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)], 
                         check=True)
            print("✓ Python dependencies installed successfully")
            return True
        else:
            print("✗ requirements.txt not found")
            return False
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install Python dependencies: {e}")
        return False

def generate_all_figures(figure_types: List[str] = None) -> bool:
    """
    Generate all figures for the article.
    
    Args:
        figure_types: List of figure types to generate (optional)
    
    Returns:
        True if all figures generated successfully
    """
    script_dir = Path(__file__).parent
    
    # Define available figure scripts
    figure_scripts = {
        'matplotlib': script_dir / 'generate_figure1.py',
        'seaborn': script_dir / 'generate_figure2.py',
        'mermaid': script_dir / 'generate_mermaid.py',
    }
    
    # Filter scripts if specific types requested
    if figure_types:
        figure_scripts = {k: v for k, v in figure_scripts.items() if k in figure_types}
    
    success_count = 0
    total_count = len(figure_scripts)
    
    print(f"Generating {total_count} figure type(s)...")
    print("-" * 50)
    
    for fig_type, script_path in figure_scripts.items():
        if script_path.exists():
            if run_figure_script(script_path):
                success_count += 1
        else:
            print(f"✗ Script not found: {script_path}")
    
    print("-" * 50)
    print(f"Results: {success_count}/{total_count} figure types generated successfully")
    
    return success_count == total_count

def create_figure_index(output_dir: Path) -> None:
    """Create an index of all generated figures."""
    
    figure_files = []
    
    # Find all figure files
    for pattern in ['*.pdf', '*.png', '*.svg']:
        figure_files.extend(output_dir.glob(pattern))
    
    # Create index file
    index_file = output_dir / 'figure_index.md'
    
    with open(index_file, 'w') as f:
        f.write("# Generated Figures Index\n\n")
        f.write(f"Generated on: {Path(__file__).stat().st_mtime}\n\n")
        
        if figure_files:
            f.write("## Available Figures\n\n")
            for fig_file in sorted(figure_files):
                f.write(f"- `{fig_file.name}`\n")
        else:
            f.write("No figures found.\n")
        
        f.write("\n## Figure Descriptions\n\n")
        f.write("- **Figure1**: Sample matplotlib visualization\n")
        f.write("- **Figure2**: Statistical analysis with seaborn\n")
        f.write("- **Mermaid diagrams**: Methodology and workflow visualizations\n")
    
    print(f"Figure index created: {index_file}")

def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(description='Generate figures for the article')
    parser.add_argument('--types', nargs='+', 
                       choices=['matplotlib', 'seaborn', 'mermaid'],
                       help='Specific figure types to generate')
    parser.add_argument('--check-deps', action='store_true',
                       help='Check dependencies and exit')
    parser.add_argument('--install-deps', action='store_true',
                       help='Install Python dependencies')
    parser.add_argument('--create-index', action='store_true',
                       help='Create figure index only')
    
    args = parser.parse_args()
    
    # Determine output directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    output_dir = project_root / 'build' / 'figures'
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check dependencies
    if args.check_deps:
        deps = check_dependencies()
        print("Dependency Status:")
        for dep, status in deps.items():
            status_str = "✓" if status else "✗"
            print(f"  {status_str} {dep}")
        return
    
    # Install dependencies
    if args.install_deps:
        if install_python_dependencies():
            print("Dependencies installed. You may also need to install Mermaid CLI:")
            print("  npm install -g @mermaid-js/mermaid-cli")
        return
    
    # Create index only
    if args.create_index:
        create_figure_index(output_dir)
        return
    
    # Check dependencies before generating
    deps = check_dependencies()
    missing_deps = [dep for dep, status in deps.items() if not status]
    
    if missing_deps:
        print("Warning: Missing dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nRun with --install-deps to install Python packages")
        print("For Mermaid CLI: npm install -g @mermaid-js/mermaid-cli")
        print()
    
    # Generate figures
    success = generate_all_figures(args.types)
    
    # Create figure index
    create_figure_index(output_dir)
    
    if success:
        print("\n🎉 All figures generated successfully!")
    else:
        print("\n⚠️  Some figures failed to generate. Check the output above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
