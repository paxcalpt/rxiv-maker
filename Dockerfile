FROM texlive/texlive:latest

# Install additional system packages if needed
RUN apt-get update && apt-get install -y \
    make \
    inotify-tools \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy project files
COPY . .

# Default command
CMD ["make", "all"]
