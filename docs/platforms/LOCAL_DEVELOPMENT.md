# Local Development Setup

This guide covers setting up RXiv-Maker for local development across different platforms and architectures.

## 🖥️ Platform-Specific Setup

### macOS (Intel x86_64)

#### Prerequisites
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required tools
brew install python@3.11 node@20 git make
brew install --cask mactex-no-gui  # For LaTeX support
```

#### Docker Setup
```bash
# Install Docker Desktop
brew install --cask docker

# Start Docker Desktop and configure resources:
# - Memory: 4GB minimum, 8GB recommended
# - CPU: 2 cores minimum, 4 cores recommended
# - Disk: 64GB recommended
```

#### Local Build
```bash
# Clone repository
git clone https://github.com/HenriquesLab/rxiv-maker.git
cd rxiv-maker

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .

# Generate PDF
make pdf
```

### macOS (Apple Silicon M1/M2/M3)

#### Prerequisites
```bash
# Install Homebrew for ARM64
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required tools (native ARM64 versions)
brew install python@3.11 node@20 git make
brew install --cask mactex-no-gui
```

#### Docker Setup
```bash
# Install Docker Desktop with Apple Silicon support
brew install --cask docker

# Verify ARM64 Docker
docker version --format 'Architecture: {{.Server.Arch}}'
# Should output: Architecture: aarch64
```

#### Performance Optimization
```bash
# Use native ARM64 images
docker run --platform linux/arm64 --rm -v $(pwd):/app henriqueslab/rxiv-maker:latest make pdf

# Check if Rosetta 2 is installed (for x86_64 compatibility)
softwareupdate --install-rosetta
```

#### Local Build (Native ARM64)
```bash
# Clone repository
git clone https://github.com/HenriquesLab/rxiv-maker.git
cd rxiv-maker

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies with ARM64 optimizations
pip install -e .

# Verify native execution
python -c "import platform; print(f'Architecture: {platform.machine()}')"
# Should output: Architecture: arm64

# Generate PDF
make pdf
```

### Linux (Ubuntu/Debian x86_64)

#### Prerequisites
```bash
# Update package list
sudo apt update

# Install system dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip nodejs npm git make curl

# Install LaTeX (choose one)
sudo apt install -y texlive-full  # Complete installation (~4GB)
# OR
sudo apt install -y texlive-latex-recommended texlive-fonts-recommended  # Minimal (~500MB)
```

#### Docker Setup
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Buildx
mkdir -p ~/.docker/cli-plugins
curl -SL https://github.com/docker/buildx/releases/latest/download/buildx-v0.12.0.linux-amd64 -o ~/.docker/cli-plugins/docker-buildx
chmod a+x ~/.docker/cli-plugins/docker-buildx
```

#### Local Build
```bash
# Clone repository
git clone https://github.com/HenriquesLab/rxiv-maker.git
cd rxiv-maker

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .

# Generate PDF
make pdf
```

### Linux (ARM64 - Raspberry Pi, AWS Graviton)

#### Prerequisites (Raspberry Pi OS / Ubuntu ARM64)
```bash
# Update package list
sudo apt update

# Install system dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip nodejs npm git make curl

# Install LaTeX (ARM64 optimized)
sudo apt install -y texlive-latex-recommended texlive-fonts-recommended
```

#### Docker Setup
```bash
# Install Docker for ARM64
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Buildx for ARM64
mkdir -p ~/.docker/cli-plugins
curl -SL https://github.com/docker/buildx/releases/latest/download/buildx-v0.12.0.linux-arm64 -o ~/.docker/cli-plugins/docker-buildx
chmod a+x ~/.docker/cli-plugins/docker-buildx
```

#### Performance Tuning
```bash
# Increase swap for Raspberry Pi (if needed)
sudo dphys-swapfile swapoff
sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=1024/' /etc/dphys-swapfile
sudo dphys-swapfile setup
sudo dphys-swapfile swapon

# Set memory split for GPU (Raspberry Pi)
echo 'gpu_mem=16' | sudo tee -a /boot/config.txt
```

### Windows (x86_64)

#### Prerequisites
```powershell
# Install Chocolatey (as Administrator)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install required tools
choco install -y python311 nodejs git make

# Install MikTeX for LaTeX
choco install -y miktex
```

#### Docker Setup
```powershell
# Install Docker Desktop
choco install -y docker-desktop

# Configure WSL2 backend (recommended)
wsl --install
# Restart computer when prompted
```

#### Local Build (PowerShell)
```powershell
# Clone repository
git clone https://github.com/HenriquesLab/rxiv-maker.git
cd rxiv-maker

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -e .

# Generate PDF
make pdf
```

#### WSL2 Setup (Recommended)
```bash
# Install Ubuntu in WSL2
wsl --install -d Ubuntu-22.04

# Inside WSL2, follow Linux setup instructions
# Access Windows files at /mnt/c/Users/YourName/
```

## 🛠️ Development Tools

### VS Code Setup

#### Extensions
```bash
# Install VS Code extensions
code --install-extension ms-python.python
code --install-extension ms-vscode.vscode-json
code --install-extension redhat.vscode-yaml
code --install-extension yzhang.markdown-all-in-one
code --install-extension James-Yu.latex-workshop
```

#### Settings (.vscode/settings.json)
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "latex-workshop.latex.autoBuild.run": "never",
    "latex-workshop.latex.build.clearLog.everyRecipeStep.enabled": false,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "output/**/*.aux": true,
        "output/**/*.log": true
    }
}
```

#### Launch Configuration (.vscode/launch.json)
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Generate PDF",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/py/commands/generate_preprint.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src/py"
            }
        },
        {
            "name": "Generate Figures",
            "type": "python", 
            "request": "launch",
            "program": "${workspaceFolder}/src/py/commands/generate_figures.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

### PyCharm Setup

#### Project Configuration
1. Open project in PyCharm
2. Configure Python interpreter: `File` → `Settings` → `Project` → `Python Interpreter`
3. Select virtual environment: `./venv/bin/python`
4. Configure run configurations for main scripts

### Vim/Neovim Setup

#### Configuration (.vimrc)
```vim
" Python development
autocmd FileType python setlocal expandtab shiftwidth=4 tabstop=4
autocmd FileType python setlocal textwidth=88

" Markdown
autocmd FileType markdown setlocal wrap linebreak
autocmd FileType markdown setlocal textwidth=80

" LaTeX
autocmd FileType tex setlocal wrap linebreak
autocmd FileType tex setlocal textwidth=80
```

## 🧪 Testing Setup

### Running Tests Locally

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=src/py --cov-report=html

# Run specific test file
pytest tests/unit/test_md2tex.py

# Run integration tests
pytest tests/integration/
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Docker-based Testing

```bash
# Test with Docker (all platforms)
./src/docker/build-multiarch.sh test

# Test specific platform
docker run --platform linux/amd64 --rm -v $(pwd):/app henriqueslab/rxiv-maker:dev pytest

# Test in clean environment
docker run --rm -v $(pwd):/app henriqueslab/rxiv-maker:dev bash -c "pip install -e . && pytest"
```

## 🚀 Performance Optimization

### Platform-Specific Optimizations

#### macOS Apple Silicon
```bash
# Use native ARM64 Python packages
pip install --upgrade pip setuptools wheel
pip install -e . --force-reinstall

# Enable ARM64 optimizations for NumPy/SciPy
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
```

#### Linux ARM64
```bash
# Use optimized BLAS libraries
sudo apt install -y libopenblas-dev liblapack-dev

# Set CPU affinity for better performance
taskset -c 0-3 make pdf  # Use cores 0-3
```

#### All Platforms
```bash
# Parallel processing
export MAKEFLAGS="-j$(nproc)"  # Linux
export MAKEFLAGS="-j$(sysctl -n hw.ncpu)"  # macOS

# Memory optimization
export PYTHONOPTIMIZE=1
export PYTHONDONTWRITEBYTECODE=1
```

## 📁 Project Structure for Development

```
rxiv-maker/
├── MANUSCRIPT/                 # Your manuscript content
│   ├── 00_CONFIG.yml          # Configuration
│   ├── 01_MAIN.md             # Main content
│   ├── 02_SUPPLEMENTARY_INFO.md
│   ├── 03_REFERENCES.bib
│   └── FIGURES/               # Figure source files
├── src/                       # RXiv-Maker source code
│   ├── py/                    # Python modules
│   ├── docker/                # Docker configuration
│   └── tex/                   # LaTeX templates
├── output/                    # Generated files
├── tests/                     # Test suite
├── docs/                      # Documentation
├── venv/                      # Virtual environment
├── Makefile                   # Build automation
└── pyproject.toml            # Project configuration
```

## 🔧 Troubleshooting

### Common Issues by Platform

#### macOS Issues
```bash
# Xcode command line tools
xcode-select --install

# Permission issues with Docker
sudo chown -R $(whoami) ~/.docker

# LaTeX font issues
sudo tlmgr update --self
sudo tlmgr install collection-fontsrecommended
```

#### Linux Issues
```bash
# Missing system dependencies
sudo apt install -y build-essential python3-dev

# Docker permission denied
sudo usermod -aG docker $USER
# Logout and login again

# LaTeX missing packages
sudo tlmgr install [package-name]
```

#### Windows Issues
```powershell
# PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Path issues
$env:PATH += ";C:\Program Files\Python311\Scripts"

# WSL2 integration
wsl --set-default-version 2
```

## 📖 Additional Resources

- [Docker Hub Instructions](./DOCKER_HUB.md)
- [Cloud Platform Guides](./cloud/)
- [CI/CD Setup](../ci-cd/)
- [Contributing Guide](../../CONTRIBUTING.md)