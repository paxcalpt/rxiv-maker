#!/bin/bash
# Article-Forge Docker Wrapper Script
# Provides easy access to Docker management from project root

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKER_SCRIPT="${SCRIPT_DIR}/src/docker/manage.sh"

# Check if Docker management script exists
if [[ ! -f "$DOCKER_SCRIPT" ]]; then
    echo "Error: Docker management script not found at $DOCKER_SCRIPT"
    exit 1
fi

# Make sure it's executable
chmod +x "$DOCKER_SCRIPT"

# Forward all arguments to the Docker management script
exec "$DOCKER_SCRIPT" "$@"
