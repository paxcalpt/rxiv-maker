# Article-Forge Docker Setup

This directory contains the optimized Docker configuration for running Article-Forge in a containerized environment with maximum efficiency and minimal resource usage.

## 🚀 Quick Start

```bash
# Build and generate PDF in one command
./manage.sh pdf

# Start development environment
./manage.sh dev

# Open interactive shell
./manage.sh shell
```

## 📁 Directory Structure

```
src/docker/
├── manage.sh                    # 🎯 Main management script (use this!)
├── Dockerfile.optimized         # 🏗️ Multi-stage optimized Dockerfile
├── docker-compose.optimized.yml # 🐳 Efficient compose configuration
├── build.env                    # ⚙️ Build configuration
├── .dockerignore               # 🚫 Optimized ignore patterns
├── README.md                   # 📚 This file
└── legacy/                     # 📦 Original files (for reference)
    ├── Dockerfile
    ├── Dockerfile.slim
    ├── docker-compose.yml
    ├── build.sh
    ├── dev.sh
    ├── run.sh
    └── ...
```

## 🛠️ Management Script Usage

The `manage.sh` script provides a unified interface for all Docker operations:

### Core Commands

| Command | Description | Example |
|---------|-------------|---------|
| `pdf` | Generate PDF document | `./manage.sh pdf` |
| `dev` | Start development environment | `./manage.sh dev` |
| `shell` | Open interactive shell | `./manage.sh shell` |
| `watch` | Auto-rebuild on file changes | `./manage.sh watch` |

### Build Commands

| Command | Description | Example |
|---------|-------------|---------|
| `build` | Build production image | `./manage.sh build` |
| `build development` | Build dev image | `./manage.sh build development` |
| `build --no-cache` | Force rebuild | `./manage.sh build --no-cache` |

### Management Commands

| Command | Description | Example |
|---------|-------------|---------|
| `status` | Show container/image status | `./manage.sh status` |
| `stop` | Stop all services | `./manage.sh stop` |
| `restart` | Restart services | `./manage.sh restart` |
| `clean` | Clean up resources | `./manage.sh clean` |
| `test` | Run tests | `./manage.sh test` |

## 🏗️ Architecture Overview

### Multi-Stage Build Process

The optimized Dockerfile uses a multi-stage build for maximum efficiency:

1. **Base System** - Core system dependencies
2. **Python Environment** - Python packages in virtual environment
3. **LaTeX Environment** - LaTeX packages and tools
4. **Node.js Environment** - Mermaid CLI and dependencies
5. **Production** - Minimal runtime image
6. **Development** - Extended image with dev tools

### Container Services

| Service | Purpose | Target | Resources |
|---------|---------|--------|-----------|
| `article-forge` | PDF generation | Production | 2GB RAM, 2 CPU |
| `dev` | Development | Development | 4GB RAM, 4 CPU |
| `watch` | Auto-rebuild | Development | Auto-restart |
| `test` | Testing | Development | On-demand |

## ⚡ Optimization Features

### Build Efficiency
- **Multi-stage builds** reduce final image size by ~60%
- **BuildKit support** enables advanced caching and parallelization
- **Layer optimization** minimizes rebuild times
- **Dependency caching** speeds up subsequent builds
- **Security hardening** with non-root user execution

### Runtime Efficiency
- **Resource limits** prevent system overload
- **Volume caching** for temporary files
- **Network isolation** with dedicated bridge network
- **Health checks** ensure container reliability
- **Graceful shutdown** handling

### Development Features
- **Hot reloading** with file watching
- **Persistent volumes** for development data
- **Interactive debugging** with full shell access
- **Test isolation** with dedicated test runner

## 🔧 Configuration

### Environment Variables

```bash
# Python settings
PYTHONPATH=/app/src/py
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1

# Development mode
DEVELOPMENT=1

# Resource optimization
PIP_NO_CACHE_DIR=1
NPM_CONFIG_UPDATE_NOTIFIER=false
```

### Volume Mounts

- **Source code**: `../../:/app` (read-only in production)
- **Output**: `../../output:/app/output` (read-write)
- **Cache**: `article-forge-cache:/tmp` (persistent cache)
- **Dev home**: `dev-home:/home/appuser` (development persistence)

## 🚀 Performance Tips

### For Faster Builds
```bash
# Use BuildKit for better caching
export DOCKER_BUILDKIT=1

# Build with inline cache
./manage.sh build --no-cache

# Clean up periodically
./manage.sh clean
```

### For Development
```bash
# Start development environment once
./manage.sh dev

# Use shell for multiple commands
./manage.sh shell

# Use watch mode for auto-rebuild
./manage.sh watch
```

## 🔍 Troubleshooting

### Common Issues

1. **Build fails with memory error**
   ```bash
   # Increase Docker memory limit in Docker Desktop
   # Or use slim build target
   ./manage.sh build development
   ```

2. **Permission denied errors**
   ```bash
   # Ensure manage.sh is executable
   chmod +x ./manage.sh
   
   # Check file ownership in output directory
   sudo chown -R $USER:$USER ../../output/
   ```

3. **Cache issues**
   ```bash
   # Clear Docker cache
   ./manage.sh clean
   
   # Rebuild without cache
   ./manage.sh build --no-cache
   ```

### Debug Mode

```bash
# Check container logs
docker logs article-forge-dev

# Inspect container
docker exec -it article-forge-dev bash

# Check resource usage
docker stats
```

## 📊 Resource Usage

### Image Sizes
- **Production**: ~1.2GB (optimized)
- **Development**: ~1.5GB (with dev tools)
- **Base system**: ~200MB (cached layers)

### Memory Usage
- **PDF generation**: 512MB - 2GB
- **Development**: 1GB - 4GB
- **Watch mode**: 256MB - 1GB

### Build Times
- **Cold build**: 5-8 minutes
- **Cached build**: 30-60 seconds
- **Layer updates**: 10-30 seconds

## 🔄 Migration from Legacy Scripts

The new `manage.sh` script replaces all individual scripts:

| Legacy Script | New Command |
|---------------|-------------|
| `build.sh` | `./manage.sh build` |
| `run.sh` | `./manage.sh pdf` |
| `dev.sh` | `./manage.sh dev` |
| `shell.sh` | `./manage.sh shell` |
| `test.sh` | `./manage.sh test` |

Legacy files are preserved in `legacy/` directory for reference.

## 🎯 Best Practices

### Development Workflow
1. Start development environment: `./manage.sh dev`
2. Open shell for interactive work: `./manage.sh shell`
3. Use watch mode for auto-rebuild: `./manage.sh watch`
4. Run tests before committing: `./manage.sh test`
5. Generate final PDF: `./manage.sh pdf`

### Production Deployment
1. Build optimized image: `./manage.sh build`
2. Generate PDF: `./manage.sh pdf`
3. Clean up resources: `./manage.sh clean`

### Maintenance
- Clean up weekly: `./manage.sh clean`
- Update base images monthly
- Monitor resource usage: `./manage.sh status`
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