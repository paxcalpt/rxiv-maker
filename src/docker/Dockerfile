# Article-Forge Docker Container - Optimized Multi-stage Build
# This Dockerfile provides an efficient build process with multiple optimization layers

# =====================================
# Stage 1: Base System Dependencies
# =====================================
FROM debian:bookworm-slim AS base-system

# Install system dependencies in a single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Core build tools
    make \
    bash \
    curl \
    wget \
    git \
    ca-certificates \
    # File watching tools
    inotify-tools \
    # Clean up immediately
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y \
    && apt-get autoclean

# =====================================
# Stage 2: Python Environment
# =====================================
FROM base-system AS python-env

# Install Python and pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment for better dependency management
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy Python dependencies first for better layer caching
COPY pyproject.toml /tmp/
WORKDIR /tmp

# Install Python dependencies with caching and optimization
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir \
    matplotlib>=3.7.0 \
    seaborn>=0.12.0 \
    numpy>=1.24.0 \
    pandas>=2.0.0 \
    scipy>=1.10.0 \
    Pillow>=9.0.0 \
    pypdf>=3.0.0 \
    PyYAML>=6.0.0

# =====================================
# Stage 3: LaTeX Environment
# =====================================
FROM python-env AS latex-env

# Install LaTeX packages efficiently
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Full LaTeX installation for compatibility
    texlive-full \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y \
    && apt-get autoclean

# =====================================
# Stage 4: Node.js and Mermaid
# =====================================
FROM latex-env AS node-env

# Install Node.js and Mermaid CLI
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g @mermaid-js/mermaid-cli \
    && npm cache clean --force

# =====================================
# Stage 5: Production Image
# =====================================
FROM node-env AS production

# Set working directory
WORKDIR /app

# Copy virtual environment from python stage
COPY --from=python-env /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set environment variables
ENV PYTHONPATH=/app/src/py
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    mkdir -p /app/output && \
    chown -R appuser:appuser /app

# Copy application files (optimized for layer caching)
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Default command
CMD ["make", "pdf"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 --version && pdflatex --version || exit 1

# =====================================
# Stage 6: Development Image
# =====================================
FROM production AS development

# Switch back to root for development tools installation
USER root

# Install development tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    nano \
    htop \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install development Python packages
RUN pip install --no-cache-dir \
    pytest>=7.0 \
    black>=22.0 \
    flake8>=5.0 \
    mypy>=1.0 \
    pytest-cov>=4.0

# Switch back to appuser
USER appuser

# Development command (keep container running)
CMD ["tail", "-f", "/dev/null"]
