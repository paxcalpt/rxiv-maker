#!/bin/bash
# Quick Build Script for RXiv-Forge Docker Container
# Minimal script for fast container builds and testing

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
IMAGE_NAME="rxiv-forge"

# Functions
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✓${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
    exit 1
}

# Quick build function
quick_build() {
    log "Starting quick Docker build..."
    
    cd "$PROJECT_ROOT"
    
    # Enable BuildKit for faster builds
    export DOCKER_BUILDKIT=1
    
    # Build the production image
    log "Building production image..."
    if docker build -f src/docker/Dockerfile -t "${IMAGE_NAME}:latest" --target production .; then
        success "Production image built successfully"
    else
        error "Failed to build production image"
    fi
    
    # Build the development image
    log "Building development image..."
    if docker build -f src/docker/Dockerfile -t "${IMAGE_NAME}:dev" --target development .; then
        success "Development image built successfully"
    else
        error "Failed to build development image"
    fi
    
    success "All images built successfully!"
}

# Quick test function
quick_test() {
    log "Running quick test..."
    
    cd "$PROJECT_ROOT"
    
    # Check if image exists
    if ! docker images "${IMAGE_NAME}:latest" | grep -q "${IMAGE_NAME}"; then
        log "Image not found. Building..."
        quick_build
    fi
    
    # Test the container
    log "Testing container functionality..."
    if docker run --rm -v "${PROJECT_ROOT}:/app" "${IMAGE_NAME}:latest" python3 --version; then
        success "Container test passed"
    else
        error "Container test failed"
    fi
    
    if docker run --rm -v "${PROJECT_ROOT}:/app" "${IMAGE_NAME}:latest" pdflatex --version >/dev/null 2>&1; then
        success "LaTeX environment test passed"
    else
        error "LaTeX environment test failed"
    fi
    
    success "All tests passed!"
}

# Quick PDF generation
quick_pdf() {
    log "Generating PDF with Docker..."
    
    cd "$PROJECT_ROOT"
    
    # Check if image exists
    if ! docker images "${IMAGE_NAME}:latest" | grep -q "${IMAGE_NAME}"; then
        log "Image not found. Building..."
        quick_build
    fi
    
    # Generate PDF
    log "Running PDF generation..."
    if docker run --rm -v "${PROJECT_ROOT}:/app" "${IMAGE_NAME}:latest" make pdf; then
        success "PDF generated successfully!"
        log "Output available in: ${PROJECT_ROOT}/output/"
    else
        error "PDF generation failed"
    fi
}

# Show usage
show_usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  build    - Quick build of Docker images"
    echo "  test     - Quick test of built containers"
    echo "  pdf      - Generate PDF using Docker"
    echo "  all      - Build, test, and generate PDF"
    echo "  help     - Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 build    # Quick build"
    echo "  $0 test     # Test containers"
    echo "  $0 pdf      # Generate PDF"
    echo "  $0 all      # Do everything"
}

# Main logic
case "${1:-help}" in
    build)
        quick_build
        ;;
    test)
        quick_test
        ;;
    pdf)
        quick_pdf
        ;;
    all)
        quick_build
        quick_test
        quick_pdf
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        echo "Unknown command: $1"
        echo ""
        show_usage
        exit 1
        ;;
esac