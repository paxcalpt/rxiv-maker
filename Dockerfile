FROM texlive/texlive:latest

# Install additional system packages and dependencies
RUN apt-get update && apt-get install -y \
    make \
    inotify-tools \
    python3 \
    python3-pip \
    nodejs \
    npm \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Mermaid CLI globally
RUN npm install -g @mermaid-js/mermaid-cli

# Set working directory
WORKDIR /workspace

# Copy project files
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Make scripts executable
RUN chmod +x scripts/*.sh

# Default command
CMD ["make", "all"]
