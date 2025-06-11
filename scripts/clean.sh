#!/bin/bash

# Clean script for LaTeX article
# This script removes all build artifacts and temporary files

set -e  # Exit on any error

echo "Cleaning LaTeX build artifacts..."

# Check if Docker is available for Docker-based cleaning
if command -v docker &> /dev/null; then
    echo "Docker found. Cleaning with Docker..."
    make docker-clean
else
    echo "Docker not found. Cleaning with local make..."
    make clean
fi

# Also clean any stray LaTeX auxiliary files in the source directory
echo "Cleaning auxiliary files in source directory..."
find src/ -name "*.aux" -delete 2>/dev/null || true
find src/ -name "*.log" -delete 2>/dev/null || true
find src/ -name "*.out" -delete 2>/dev/null || true
find src/ -name "*.bbl" -delete 2>/dev/null || true
find src/ -name "*.blg" -delete 2>/dev/null || true
find src/ -name "*.toc" -delete 2>/dev/null || true
find src/ -name "*.fls" -delete 2>/dev/null || true
find src/ -name "*.fdb_latexmk" -delete 2>/dev/null || true
find src/ -name "*.synctex.gz" -delete 2>/dev/null || true

echo "Cleaning completed successfully!"
