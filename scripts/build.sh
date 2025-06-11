#!/bin/bash

# Build script for LaTeX article with HenriquesLab style
# This script intelligently builds the document using either Docker or local LaTeX

set -e  # Exit on any error

echo "Building LaTeX article with HenriquesLab style..."

# Check if we're in the right directory
if [ ! -f "Makefile" ]; then
    echo "Error: Makefile not found. Please run this script from the repository root."
    exit 1
fi

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "Docker found. Building with Docker for consistency..."
    
    # Use Docker to build
    docker run --rm \
        -v "$(pwd):/workspace" \
        -w /workspace \
        texlive/texlive:latest \
        bash -c "
            echo 'Installing additional packages if needed...'
            tlmgr update --self || true
            tlmgr install xwatermark fontawesome || true
            echo 'Building with make...'
            make all
        "
        
elif command -v pdflatex &> /dev/null && command -v bibtex &> /dev/null; then
    echo "Local LaTeX installation found. Building locally..."
    make all
    
else
    echo "Error: Neither Docker nor local LaTeX installation found."
    echo "Please install either:"
    echo "  1. Docker (recommended)"
    echo "  2. A complete LaTeX distribution (TeX Live, MiKTeX, or MacTeX)"
    exit 1
fi

# Check if build was successful
if [ -f "build/output/main.pdf" ]; then
    echo "✅ Build successful! PDF created at: build/output/main.pdf"
    
    # Display PDF info if possible
    if command -v pdfinfo &> /dev/null; then
        echo ""
        echo "PDF Information:"
        pdfinfo build/output/main.pdf | head -5
    fi
    
    echo ""
    echo "To view the PDF:"
    echo "  macOS: open build/output/main.pdf"
    echo "  Linux: xdg-open build/output/main.pdf"
    echo "  Windows: start build/output/main.pdf"
    
else
    echo "❌ Build failed. Check the logs above for errors."
    exit 1
fi
