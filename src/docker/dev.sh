#!/bin/bash
# Article-Forge Docker Development Script

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

echo -e "${BLUE}Article-Forge Development Mode${NC}"
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

echo -e "${YELLOW}Starting development mode...${NC}"
echo "This will watch for file changes and automatically rebuild."
echo -e "${BLUE}Press Ctrl+C to stop.${NC}"
echo

# Run development container with file watching
$COMPOSE_CMD -f src/docker/docker-compose.yml up dev