#!/bin/bash
# Article-Forge Docker Run Script - Generate PDF

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

echo -e "${BLUE}Article-Forge PDF Generation${NC}"
echo

# Change to project root
cd "$PROJECT_ROOT"

# Determine compose command
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi

# Check if image exists, if not build it
if ! docker images | grep -q "article-forge"; then
    echo -e "${YELLOW}Docker image not found. Building...${NC}"
    ./src/docker/build.sh
fi

# Parse command line arguments
FORCE_FIGURES=false
COMMAND="make pdf"

while [[ $# -gt 0 ]]; do
    case $1 in
        --force-figures)
            FORCE_FIGURES=true
            shift
            ;;
        --figures-only)
            COMMAND="make force-figures"
            shift
            ;;
        --build-only)
            COMMAND="make build"
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --force-figures    Force regeneration of figures"
            echo "  --figures-only     Only generate figures"
            echo "  --build-only       Only generate LaTeX (no PDF)"
            echo "  --help            Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Set environment variable for figure generation
if [ "$FORCE_FIGURES" = true ]; then
    export FORCE_FIGURES=true
    COMMAND="make pdf FORCE_FIGURES=true"
fi

echo -e "${YELLOW}Running: $COMMAND${NC}"
echo

# Run the container
if $COMPOSE_CMD -f src/docker/docker-compose.yml run --rm build-pdf bash -c "$COMMAND"; then
    echo
    echo -e "${GREEN}✓ PDF generation completed successfully${NC}"
    
    # Check if PDF was created
    if [ -f "output/ARTICLE.pdf" ]; then
        echo -e "${GREEN}✓ PDF created: output/ARTICLE.pdf${NC}"
        
        # Get file size
        if command -v stat &> /dev/null; then
            SIZE=$(stat -c%s "output/ARTICLE.pdf" 2>/dev/null || stat -f%z "output/ARTICLE.pdf" 2>/dev/null)
            echo "  File size: $(echo $SIZE | awk '{ 
                if ($1 > 1048576) printf "%.1f MB", $1/1048576; 
                else if ($1 > 1024) printf "%.1f KB", $1/1024; 
                else printf "%d bytes", $1 
            }')"
        fi
    else
        echo -e "${YELLOW}⚠ PDF file not found in output directory${NC}"
    fi
else
    echo -e "${RED}✗ PDF generation failed${NC}"
    echo "Check the output above for error details."
    exit 1
fi