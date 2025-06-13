# Article-Forge Docker Container
# Debian-slim based image with LaTeX, Python, and Mermaid support

FROM debian:bookworm-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Core build tools
    make \
    bash \
    curl \
    wget \
    git \
    # Python and pip
    python3 \
    python3-pip \
    python3-venv \
    # LaTeX dependencies
    texlive \
    texlive-latex-extra \
    texlive-latex-recommended \
    texlive-bibtex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-science \
    biber \
    # Node.js for Mermaid
    nodejs \
    npm \
    # File watching tools
    inotify-tools \
    # Additional utilities
    ca-certificates \
    # Clean up
    && rm -rf /var/lib/apt/lists/*

# Install Mermaid CLI globally
RUN npm install -g @mermaid-js/mermaid-cli

# Create app directory
WORKDIR /app

# Copy Python dependencies first for better layer caching
COPY pyproject.toml ./

# Install Python dependencies (using --break-system-packages for Docker)
RUN pip3 install --no-cache-dir --break-system-packages \
    matplotlib>=3.7.0 \
    seaborn>=0.12.0 \
    numpy>=1.24.0 \
    pandas>=2.0.0 \
    scipy>=1.10.0 \
    Pillow>=9.0.0 \
    pypdf>=3.0.0 \
    PyYAML>=6.0.0

# Copy the entire project
COPY . .

# Create output directory
RUN mkdir -p output

# Set environment variables
ENV PYTHONPATH=/app/src/py
ENV PATH="/app/src/docker:$PATH"

# Default command
CMD ["make", "pdf"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 --version && pdflatex --version || exit 1