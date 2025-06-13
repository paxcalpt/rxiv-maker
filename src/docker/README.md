# Article-Forge Docker Setup

This directory contains Docker configurations for running Article-Forge without installing LaTeX locally.

## Quick Start (Non-Programmers)

1. **Install Docker Desktop** from https://docker.com/get-started
2. **Run setup**: `./src/docker/setup.sh` (or `make easy-setup`)
3. **Generate PDF**: `./src/docker/run.sh` (or `make easy-build`)

That's it! Your PDF will be in the `output/` directory.

## Files Overview

- `Dockerfile` - Alpine-based container with LaTeX, Python, and Mermaid
- `docker-compose.yml` - Multi-service configuration
- `setup.sh` - One-time setup script for beginners
- `build.sh` - Build the Docker image
- `run.sh` - Generate PDF (with options)
- `dev.sh` - Development mode with auto-rebuild
- `shell.sh` - Interactive shell for manual commands

## Usage Examples

### Basic PDF Generation
```bash
./src/docker/run.sh
```

### Force Figure Regeneration
```bash
./src/docker/run.sh --force-figures
```

### Development Mode (Auto-rebuild)
```bash
./src/docker/dev.sh
```

### Interactive Shell
```bash
./src/docker/shell.sh
# Then run: make pdf, make build, etc.
```

## Benefits of Docker Approach

- **No LaTeX installation required** - Everything runs in container
- **Cross-platform** - Works on Windows, macOS, Linux
- **Consistent environment** - Same results everywhere
- **Easy setup** - One command to get started
- **Isolated dependencies** - Doesn't affect your system

## Troubleshooting

### Docker Not Found
Install Docker Desktop from https://docker.com/get-started

### Permission Denied
Make scripts executable: `chmod +x src/docker/*.sh`

### Build Fails
Try: `docker system prune` then re-run setup

### Container Won't Start
Check Docker Desktop is running and has sufficient resources allocated.