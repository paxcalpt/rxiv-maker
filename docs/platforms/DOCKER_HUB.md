# RXiv-Maker on Docker Hub

RXiv-Maker provides official Multi-Architecture Docker images on Docker Hub for easy deployment across different platforms and architectures.

## 🐳 Official Images

**Repository:** [`henriqueslab/rxiv-maker`](https://hub.docker.com/r/henriqueslab/rxiv-maker)

### Available Tags

| Tag | Description | Use Case |
|-----|-------------|----------|
| `latest` | Latest production release | General usage, CI/CD |
| `production` | Production image alias | Explicit production deployments |
| `dev` | Development image with tools | Interactive development |
| `development` | Development image alias | Debugging and testing |

### Supported Platforms

| Platform | Architecture | Best For |
|----------|--------------|----------|
| `linux/amd64` | Intel/AMD 64-bit | Traditional servers, desktops |
| `linux/arm64` | ARM 64-bit | Apple Silicon Macs, AWS Graviton, Raspberry Pi 4+ |

## 🚀 Quick Start

### Basic PDF Generation

```bash
# Clone your manuscript repository
git clone https://github.com/your-org/your-manuscript.git
cd your-manuscript

# Generate PDF using Docker Hub image
docker run --rm -v $(pwd):/app henriqueslab/rxiv-maker:latest make pdf

# Output will be in ./output/MANUSCRIPT.pdf
```

### Platform-Specific Usage

#### Intel/AMD Systems (x86_64)
```bash
# Explicitly use amd64 image
docker run --platform linux/amd64 --rm -v $(pwd):/app henriqueslab/rxiv-maker:latest make pdf
```

#### Apple Silicon Macs (M1/M2/M3)
```bash
# Use native ARM64 image for better performance
docker run --platform linux/arm64 --rm -v $(pwd):/app henriqueslab/rxiv-maker:latest make pdf

# Or let Docker auto-detect (recommended)
docker run --rm -v $(pwd):/app henriqueslab/rxiv-maker:latest make pdf
```

#### AWS Graviton Instances
```bash
# Optimized for ARM-based AWS instances
docker run --platform linux/arm64 --rm -v $(pwd):/app henriqueslab/rxiv-maker:latest make pdf
```

## 🛠️ Development Mode

### Interactive Development Container

```bash
# Start development container
docker run -it --name rxiv-dev \
  -v $(pwd):/app \
  -p 8000:8000 \
  henriqueslab/rxiv-maker:dev bash

# Inside container, you can:
make pdf              # Generate PDF
make figures          # Generate figures only
python src/py/...     # Run Python scripts
```

### File Watching Mode

```bash
# Auto-rebuild on file changes (Linux/macOS)
docker run --rm -v $(pwd):/app henriqueslab/rxiv-maker:dev \
  bash -c "while inotifywait -e modify -r /app; do make pdf; done"
```

## 🔧 Advanced Usage

### Custom Build Commands

```bash
# Generate figures only
docker run --rm -v $(pwd):/app henriqueslab/rxiv-maker:latest make figures

# Force figure regeneration
docker run --rm -v $(pwd):/app henriqueslab/rxiv-maker:latest make figures-force

# Run tests
docker run --rm -v $(pwd):/app henriqueslab/rxiv-maker:dev make test

# Clean build artifacts
docker run --rm -v $(pwd):/app henriqueslab/rxiv-maker:latest make clean
```

### Docker Compose Setup

Create `docker-compose.yml` in your manuscript directory:

```yaml
version: '3.8'

services:
  rxiv-maker:
    image: henriqueslab/rxiv-maker:latest
    volumes:
      - .:/app
    command: make pdf
    
  rxiv-dev:
    image: henriqueslab/rxiv-maker:dev
    volumes:
      - .:/app
    stdin_open: true
    tty: true
    command: bash

  rxiv-watch:
    image: henriqueslab/rxiv-maker:dev
    volumes:
      - .:/app
    command: >
      bash -c "while inotifywait -e modify -r /app --exclude '/app/output'; do 
        echo 'Files changed, rebuilding...'
        make pdf
      done"
```

Usage:
```bash
# One-time PDF generation
docker compose run --rm rxiv-maker

# Interactive development
docker compose run --rm rxiv-dev

# Watch mode
docker compose up rxiv-watch
```

## 🌍 Multi-Platform Deployment

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rxiv-maker-worker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rxiv-maker
  template:
    metadata:
      labels:
        app: rxiv-maker
    spec:
      containers:
      - name: rxiv-maker
        image: henriqueslab/rxiv-maker:latest
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "4Gi" 
            cpu: "2"
        volumeMounts:
        - name: manuscript-data
          mountPath: /app
      volumes:
      - name: manuscript-data
        persistentVolumeClaim:
          claimName: manuscript-pvc
      nodeSelector:
        kubernetes.io/arch: amd64  # or arm64 for ARM nodes
```

### GitHub Actions CI/CD

```yaml
name: Build PDF
on: [push, pull_request]

jobs:
  build-pdf:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        platform: [amd64, arm64]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
      
    - name: Generate PDF
      run: |
        docker run --platform linux/${{ matrix.platform }} --rm \
          -v ${{ github.workspace }}:/app \
          henriqueslab/rxiv-maker:latest make pdf
    
    - name: Upload PDF
      uses: actions/upload-artifact@v4
      with:
        name: manuscript-${{ matrix.platform }}
        path: output/MANUSCRIPT.pdf
```

### GitLab CI Pipeline

```yaml
stages:
  - build

build-pdf:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  parallel:
    matrix:
      - PLATFORM: linux/amd64
      - PLATFORM: linux/arm64
  before_script:
    - docker info
  script:
    - docker run --platform $PLATFORM --rm 
        -v $PWD:/app henriqueslab/rxiv-maker:latest make pdf
  artifacts:
    paths:
      - output/MANUSCRIPT.pdf
    expire_in: 1 week
```

## 📊 Performance Benchmarks

### Build Times by Platform

| Platform | PDF Generation | Figure Generation | Full Build |
|----------|----------------|-------------------|------------|
| `linux/amd64` | ~30s | ~45s | ~2m |
| `linux/arm64` | ~25s | ~40s | ~1.5m |

*Note: ARM64 performance is often better due to more efficient instruction set*

### Resource Usage

| Task | Memory | CPU | Disk |
|------|--------|-----|------|
| PDF Generation | 512MB - 2GB | 1-2 cores | 100MB temp |
| Figure Generation | 256MB - 1GB | 1 core | 50MB temp |
| Development Mode | 1GB - 4GB | 2-4 cores | 200MB temp |

## 🔧 Troubleshooting

### Platform Detection Issues

```bash
# Check available platforms
docker buildx imagetools inspect henriqueslab/rxiv-maker:latest

# Force specific platform
docker run --platform linux/amd64 --rm henriqueslab/rxiv-maker:latest uname -m
```

### Performance Issues

```bash
# Apple Silicon: Ensure native ARM64 usage
docker run --platform linux/arm64 --rm henriqueslab/rxiv-maker:latest uname -m
# Should output: aarch64

# Intel systems: Use x86_64 optimized builds
docker run --platform linux/amd64 --rm henriqueslab/rxiv-maker:latest uname -m
# Should output: x86_64
```

### Memory Issues

```bash
# Increase Docker memory limits (Docker Desktop)
# Recommended: 4GB+ for complex documents

# Check memory usage
docker stats $(docker ps -q --filter ancestor=henriqueslab/rxiv-maker)
```

### Network Issues in CI/CD

```bash
# Use registry mirrors in restricted environments
docker run --rm \
  -e HTTP_PROXY=http://proxy.company.com:8080 \
  -e HTTPS_PROXY=http://proxy.company.com:8080 \
  -v $(pwd):/app henriqueslab/rxiv-maker:latest make pdf
```

## 🔗 Related Documentation

- [Local Development Setup](./LOCAL_DEVELOPMENT.md)
- [Azure Container Instances](./AZURE_CONTAINERS.md)
- [AWS Fargate Deployment](./AWS_FARGATE.md)
- [Docker Setup Guide](../DOCKER_SETUP.md)

## 📞 Support

- **Docker Hub Issues**: [Report on GitHub](https://github.com/HenriquesLab/rxiv-maker/issues)
- **Platform Support**: AMD64, ARM64 officially supported
- **Update Schedule**: Images updated with each release
- **Security**: Images scanned for vulnerabilities