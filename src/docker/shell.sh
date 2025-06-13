#!/bin/bash
# Article-Forge Docker Interactive Shell

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

echo -e "${BLUE}Article-Forge Interactive Shell${NC}"
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

echo -e "${YELLOW}Starting interactive shell...${NC}"
echo "You can now run make commands directly:"
echo -e "  ${BLUE}make pdf${NC}             - Generate PDF"
echo -e "  ${BLUE}make build${NC}           - Generate LaTeX only"
echo -e "  ${BLUE}make force-figures${NC}   - Regenerate figures"
echo -e "  ${BLUE}make clean${NC}           - Clean output directory"
echo -e "  ${BLUE}make help${NC}            - Show all available commands"
echo

# Run interactive shell
$COMPOSE_CMD -f src/docker/docker-compose.yml run --rm article-forge bash