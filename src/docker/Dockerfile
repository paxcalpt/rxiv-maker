# syntax=docker/dockerfile:1
# RXiv-Maker Docker Container - Optimized Multi-stage Build with TeXLive base
# This Dockerfile provides an efficient build process with multiple optimization layers

# =====================================
# Stage 1: TeXLive Base with System Dependencies
# =====================================
FROM --platform=$TARGETPLATFORM texlive/texlive:latest AS base-system

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
    # Clean up
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# =====================================
# Stage 2: Node.js Environment (moved before Python for better caching)
# =====================================
FROM base-system AS node-env

# Install Node.js and npm with specific version for consistency
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Install Mermaid CLI and dependencies
RUN npm install -g @mermaid-js/mermaid-cli@10.6.1 && \
    apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/* \
    && npm cache clean --force \
    && apt-get clean

# =====================================
# Stage 3: Python Environment
# =====================================
FROM node-env AS python-env

# Install Python and pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create virtual environment for better dependency management
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy Python dependencies first for better layer caching
COPY pyproject.toml /tmp/
WORKDIR /tmp

# Install uv in the virtual environment for faster package installation
RUN pip install --no-cache-dir uv

# Install Python dependencies from pyproject.toml with uv for speed
RUN uv pip install --no-cache -e . && \
    # Remove build dependencies to reduce image size
    apt-get update && apt-get purge -y build-essential python3-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# =====================================
# Stage 4: Production Image
# =====================================
FROM python-env AS production

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app/src/py \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# Create non-root user for security with proper permissions
RUN groupadd -r appuser && useradd -r -g appuser -s /bin/bash appuser && \
    mkdir -p /app/output /app/tmp && \
    chown -R appuser:appuser /app

# Copy application files (optimized for layer caching)
# Copy only necessary files to reduce image size
COPY --chown=appuser:appuser src/ /app/src/
COPY --chown=appuser:appuser Makefile /app/

# Switch to non-root user
USER appuser

# Default command
CMD ["make", "pdf"]

# Health check (optimized)
HEALTHCHECK --interval=60s --timeout=30s --start-period=10s --retries=2 \
    CMD python3 -c "import sys; print(sys.version)" && \
        pdflatex --version > /dev/null 2>&1 || exit 1

# =====================================
# Stage 5: Development Image
# =====================================
FROM production AS development

# Switch back to root for development tools installation
USER root

# Install development tools efficiently
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    nano \
    htop \
    procps \
    tree \
    less \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install development Python packages from pyproject.toml with uv
RUN uv pip install --no-cache -e ".[dev]"

# Copy full project for development (including tests, docs, etc.)
COPY --chown=appuser:appuser . /app/

# Switch back to appuser
USER appuser

# Development command (keep container running)
CMD ["tail", "-f", "/dev/null"]
