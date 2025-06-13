#!/bin/bash
# Article-Forge Easy Setup Script for Non-Programmers

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

clear
echo -e "${BOLD}${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${BLUE}║                    Article-Forge Setup                      ║${NC}"
echo -e "${BOLD}${BLUE}║              Easy PDF Generation from Markdown              ║${NC}"
echo -e "${BOLD}${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo
echo -e "${YELLOW}This script will set up Article-Forge to generate PDFs from your Markdown files.${NC}"
echo

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Change to project root
cd "$PROJECT_ROOT"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Check Docker installation
echo -e "${BLUE}Checking requirements...${NC}"

if ! command_exists docker; then
    echo -e "${RED}✗ Docker is not installed${NC}"
    echo
    echo "Docker is required to run Article-Forge easily."
    echo "Please install Docker Desktop from: https://docker.com/get-started"
    echo
    
    OS=$(detect_os)
    case $OS in
        "macos")
            echo "For macOS: Download Docker Desktop for Mac"
            ;;
        "linux")
            echo "For Linux: Follow the installation guide for your distribution"
            ;;
        "windows")
            echo "For Windows: Download Docker Desktop for Windows"
            ;;
    esac
    
    echo
    echo "After installing Docker, run this script again."
    exit 1
else
    echo -e "${GREEN}✓ Docker is installed${NC}"
fi

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}✗ Docker is not running${NC}"
    echo
    echo "Please start Docker Desktop and try again."
    exit 1
else
    echo -e "${GREEN}✓ Docker is running${NC}"
fi

# Check Docker Compose
if ! command_exists docker-compose && ! docker compose version >/dev/null 2>&1; then
    echo -e "${RED}✗ Docker Compose is not available${NC}"
    echo
    echo "Docker Compose is usually included with Docker Desktop."
    echo "Please update your Docker installation."
    exit 1
else
    echo -e "${GREEN}✓ Docker Compose is available${NC}"
fi

echo
echo -e "${YELLOW}Building Article-Forge Docker image...${NC}"
echo "This may take a few minutes on first run."
echo

# Build the Docker image
./src/docker/build.sh

echo
echo -e "${BOLD}${GREEN}🎉 Setup Complete!${NC}"
echo
echo -e "${BOLD}How to use Article-Forge:${NC}"
echo
echo -e "${BLUE}1. Edit your article:${NC}"
echo "   - Edit '00_ARTICLE.md' with your content"
echo "   - Add references to '02_REFERENCES.bib'"
echo "   - Add figures to 'FIGURES/' directory"
echo
echo -e "${BLUE}2. Generate PDF:${NC}"
echo -e "   ${YELLOW}./src/docker/run.sh${NC}"
echo
echo -e "${BLUE}3. Other useful commands:${NC}"
echo -e "   ${YELLOW}./src/docker/run.sh --force-figures${NC}  - Regenerate figures"
echo -e "   ${YELLOW}./src/docker/dev.sh${NC}                  - Auto-rebuild on changes"
echo -e "   ${YELLOW}./src/docker/shell.sh${NC}                - Interactive shell"
echo
echo -e "${GREEN}Your PDF will be created in the 'output/' directory.${NC}"
echo
echo -e "${BOLD}Need help?${NC} Check the README or open an issue on GitHub."