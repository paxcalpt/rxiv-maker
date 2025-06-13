#!/bin/bash
# Article-Forge Docker Build Script

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

echo -e "${BLUE}Article-Forge Docker Build Script${NC}"
echo "Project root: $PROJECT_ROOT"
echo

# Change to project root
cd "$PROJECT_ROOT"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed or not in PATH${NC}"
    echo "Please install Docker from https://docker.com/get-started"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not available${NC}"
    echo "Please install Docker Compose"
    exit 1
fi

# Determine compose command
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi

echo -e "${YELLOW}Building Article-Forge Docker image...${NC}"

# Build the Docker image
if $COMPOSE_CMD -f src/docker/docker-compose.yml build article-forge; then
    echo -e "${GREEN}✓ Docker image built successfully${NC}"
else
    echo -e "${RED}✗ Failed to build Docker image${NC}"
    exit 1
fi

echo
echo -e "${GREEN}Build complete!${NC}"
echo
echo "Available commands:"
echo -e "  ${BLUE}./src/docker/run.sh${NC}        - Generate PDF"
echo -e "  ${BLUE}./src/docker/dev.sh${NC}        - Start development mode"
echo -e "  ${BLUE}./src/docker/shell.sh${NC}      - Open interactive shell"
echo