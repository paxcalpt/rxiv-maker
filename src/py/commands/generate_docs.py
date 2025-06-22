#!/usr/bin/env python3
"""Documentation generation script using lazydocs.

This script generates markdown documentation for the rxiv-forge Python modules
that can be viewed directly on GitHub without requiring GitHub Pages.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def generate_module_docs(docs_dir, module_path):
    """Generate documentation for a specific module using lazydocs."""
    try:
        # Generate documentation for the specific module
        cmd = [
            "lazydocs",
            str(module_path),
            "--output-path",
            str(docs_dir),
            "--no-watermark",
            "--remove-package-prefix",
        ]

        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating documentation for {module_path}: {e}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def main():
    """Generate API documentation using lazydocs."""
    # Get the project root directory (script is in src/py/commands/)
    project_root = Path(__file__).parent.parent.parent.parent
    src_dir = project_root / "src" / "py"
    docs_dir = project_root / "docs" / "api"

    # Ensure docs directory exists
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Clean existing generated docs (except README.md)
    for item in docs_dir.iterdir():
        if item.name != "README.md" and item.name != ".gitkeep":
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

    print("🚀 Generating API documentation with lazydocs...")

    # Change to project root for proper module discovery
    os.chdir(project_root)

    # Find all Python files to document
    python_files = []

    # Collect all Python modules excluding __pycache__ and test files
    for py_file in src_dir.rglob("*.py"):
        if "__pycache__" not in str(py_file) and not py_file.name.startswith("test_"):
            python_files.append(py_file)

    successful_files = []
    failed_files = []

    print(f"Found {len(python_files)} Python files to document:")
    for py_file in python_files:
        rel_path = py_file.relative_to(src_dir)
        print(f"  - {rel_path}")

    # Generate documentation for each file
    for py_file in python_files:
        rel_path = py_file.relative_to(src_dir)
        print(f"\n📦 Generating docs for {rel_path}...")

        if generate_module_docs(docs_dir, py_file):
            successful_files.append(rel_path)
            print(f"✅ {rel_path} documented successfully")
        else:
            failed_files.append(rel_path)
            print(f"❌ Failed to document {rel_path}")

    print(f"\n📁 Documentation saved to: {docs_dir}")

    # List generated files
    print("\n📄 Generated files:")
    md_files = list(docs_dir.rglob("*.md"))
    if md_files:
        for file in sorted(md_files):
            if file.name != "README.md":
                rel_path = file.relative_to(docs_dir)
                print(f"  - {rel_path}")
    else:
        print("  No markdown files generated")

    # Summary
    print("\n📊 Summary:")
    print(f"  ✅ Successful: {len(successful_files)} files")
    print(f"  ❌ Failed: {len(failed_files)} files")

    if successful_files:
        print("✅ Documentation generated successfully!")
        return True
    else:
        print("❌ No documentation could be generated")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
