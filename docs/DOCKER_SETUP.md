# 🐳 Docker Setup for RXiv-Forge

RXiv-Forge now includes a comprehensive Docker setup that makes it easy to use across different operating systems without installing LaTeX locally.

## Quick Start (Non-Programmers)

1. **Install Docker Desktop**: https://docker.com/get-started
2. **Run setup**: `make easy-setup`
3. **Generate PDF**: `make easy-build`

Your PDF will be in the `output/` directory!

## What's New

### 📁 Docker Files Location
All Docker-related files are now in `src/docker/`:
- `Dockerfile` - Debian-based container with LaTeX, Python, Mermaid
- `docker-compose.yml` - Multi-service configuration
- `setup.sh` - Beginner-friendly setup wizard
- `build.sh`, `run.sh`, `dev.sh`, `shell.sh` - Utility scripts
- `README.md` - Detailed Docker documentation

### 🚀 New Makefile Commands

**Easy Commands (for non-programmers):**
- `make easy-setup` - One-time Docker setup
- `make easy-build` - Generate PDF using Docker

**Docker Commands:**
- `make docker-setup` - Set up Docker environment
- `make docker-build` - Build PDF using Docker
- `make docker-force-figures` - Build PDF with figure regeneration
- `make docker-dev` - Development mode with auto-rebuild
- `make docker-shell` - Interactive Docker shell

### 🎯 Key Benefits

1. **No LaTeX Installation Required** - Everything runs in Docker
2. **Cross-Platform** - Works on Windows, macOS, Linux
3. **Consistent Environment** - Same results everywhere
4. **User-Friendly** - Color-coded output and clear instructions
5. **Multiple Usage Modes** - One-time build, development, interactive

### 🛠 Technical Details

- **Base Image**: `debian:bookworm-slim` (reliable LaTeX packages)
- **Includes**: LaTeX, Python 3, Node.js, Mermaid CLI, all required fonts
- **Volume Mounting**: Project directory mounted for live editing
- **Health Checks**: Built-in container health monitoring

### 📋 Testing

Run the comprehensive test suite:
```bash
./src/docker/test.sh
```

This validates all components without building the Docker image.

---

**Migration Note**: The old root-level `Dockerfile` is replaced by the new `src/docker/Dockerfile` with better organization and more features.