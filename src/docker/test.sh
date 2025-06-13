#!/bin/bash
# Quick test script for Article-Forge Docker setup (without building)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Article-Forge Docker Setup Test${NC}"
echo "================================"
echo

# Test 1: Check if all files exist
echo -e "${YELLOW}Test 1: Checking required files...${NC}"
FILES=(
    "src/docker/Dockerfile"
    "src/docker/docker-compose.yml"
    "src/docker/setup.sh"
    "src/docker/build.sh"
    "src/docker/run.sh"
    "src/docker/dev.sh"
    "src/docker/shell.sh"
    "src/docker/README.md"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file exists"
    else
        echo -e "${RED}✗${NC} $file missing"
        exit 1
    fi
done

# Test 2: Check script permissions
echo
echo -e "${YELLOW}Test 2: Checking script permissions...${NC}"
SCRIPTS=(
    "src/docker/setup.sh"
    "src/docker/build.sh"
    "src/docker/run.sh"
    "src/docker/dev.sh"
    "src/docker/shell.sh"
)

for script in "${SCRIPTS[@]}"; do
    if [ -x "$script" ]; then
        echo -e "${GREEN}✓${NC} $script is executable"
    else
        echo -e "${RED}✗${NC} $script not executable"
        exit 1
    fi
done

# Test 3: Check script help functionality
echo
echo -e "${YELLOW}Test 3: Testing script help functionality...${NC}"

# Test run.sh help by checking if it contains help text
if grep -q "Usage:" src/docker/run.sh; then
    echo -e "${GREEN}✓${NC} run.sh contains help text"
else
    echo -e "${RED}✗${NC} run.sh missing help text"
    exit 1
fi

# Test 4: Check Dockerfile syntax
echo
echo -e "${YELLOW}Test 4: Checking Dockerfile syntax...${NC}"
if grep -q "FROM debian:bookworm-slim" src/docker/Dockerfile; then
    echo -e "${GREEN}✓${NC} Dockerfile uses correct base image"
else
    echo -e "${RED}✗${NC} Dockerfile base image incorrect"
    exit 1
fi

if grep -q "RUN apt-get update" src/docker/Dockerfile; then
    echo -e "${GREEN}✓${NC} Dockerfile has package installation"
else
    echo -e "${RED}✗${NC} Dockerfile missing package installation"
    exit 1
fi

# Test 5: Check docker-compose.yml syntax
echo
echo -e "${YELLOW}Test 5: Checking docker-compose.yml syntax...${NC}"
if grep -q "services:" src/docker/docker-compose.yml; then
    echo -e "${GREEN}✓${NC} docker-compose.yml has services section"
else
    echo -e "${RED}✗${NC} docker-compose.yml missing services"
    exit 1
fi

if grep -q "article-forge:" src/docker/docker-compose.yml; then
    echo -e "${GREEN}✓${NC} docker-compose.yml has article-forge service"
else
    echo -e "${RED}✗${NC} docker-compose.yml missing article-forge service"
    exit 1
fi

# Test 6: Check Makefile integration
echo
echo -e "${YELLOW}Test 6: Testing Makefile integration...${NC}"
if make help | grep -q "docker-setup"; then
    echo -e "${GREEN}✓${NC} Makefile has docker-setup command"
else
    echo -e "${RED}✗${NC} Makefile missing docker-setup"
    exit 1
fi

if make help | grep -q "easy-setup"; then
    echo -e "${GREEN}✓${NC} Makefile has easy-setup alias"
else
    echo -e "${RED}✗${NC} Makefile missing easy-setup alias"
    exit 1
fi

# Test 7: Check Docker availability
echo
echo -e "${YELLOW}Test 7: Checking Docker availability...${NC}"
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker is installed"
    
    if docker info &> /dev/null; then
        echo -e "${GREEN}✓${NC} Docker is running"
    else
        echo -e "${YELLOW}⚠${NC} Docker not running (but installed)"
    fi
else
    echo -e "${YELLOW}⚠${NC} Docker not installed (expected for testing)"
fi

echo
echo -e "${GREEN}🎉 All tests passed!${NC}"
echo
echo "The Docker setup appears to be correctly configured."
echo "To actually test PDF generation, run: ./src/docker/setup.sh"