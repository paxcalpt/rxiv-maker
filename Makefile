# Project configuration
PROJECT = main
TEX_DIR = src/tex
BIB_DIR = src/bibliography
FIG_DIR = build/figures
BUILD_DIR = build
OUTPUT_DIR = $(BUILD_DIR)/output
AUX_DIR = $(BUILD_DIR)/aux
LOG_DIR = $(BUILD_DIR)/logs
SCRIPTS_DIR = scripts

# Python and figure generation settings
PYTHON = python3
FIGURE_SCRIPTS_DIR = $(SCRIPTS_DIR)/figures
FIGURE_GENERATOR = $(FIGURE_SCRIPTS_DIR)/generators/generate_all.py

# LaTeX compilation settings
LATEX = pdflatex
LATEX_FLAGS = -shell-escape -interaction=nonstopmode -file-line-error
# Remove aux-directory for macOS compatibility, use output-directory only
LATEX_BUILD = $(LATEX) $(LATEX_FLAGS) -output-directory=$(OUTPUT_DIR)
BIBTEX = bibtex
BIBTEX_FLAGS = -terse

# Docker settings
DOCKER_IMAGE = texlive/texlive:latest
DOCKER_RUN = docker run --rm -v "$(PWD):/workspace" -w /workspace $(DOCKER_IMAGE)

# Targets
.PHONY: all clean docker-build docker-clean help watch figures install-deps check-deps

all: figures $(OUTPUT_DIR)/$(PROJECT).pdf

help:
	@echo "Available targets:"
	@echo "  all           Build the PDF document (includes figure generation)"
	@echo "  figures       Generate all figures"
	@echo "  clean         Remove build artifacts"
	@echo "  docker-build  Build using Docker container"
	@echo "  docker-clean  Clean using Docker container"
	@echo "  watch         Watch for changes and rebuild"
	@echo "  install-deps  Install Python dependencies for figure generation"
	@echo "  check-deps    Check figure generation dependencies"
	@echo "  help          Show this help message"

# Create necessary directories
$(BUILD_DIR) $(OUTPUT_DIR) $(AUX_DIR) $(LOG_DIR):
	mkdir -p $@

# Figure generation dependencies
FIGURE_SCRIPTS = $(wildcard $(FIGURE_SCRIPTS_DIR)/*.py)
GENERATED_FIGURES = $(wildcard $(FIG_DIR)/*.pdf) $(wildcard $(FIG_DIR)/*.svg)

# Main PDF target with proper dependency handling
$(OUTPUT_DIR)/$(PROJECT).pdf: $(TEX_DIR)/$(PROJECT).tex $(wildcard $(TEX_DIR)/sections/*.tex) $(BIB_DIR)/references.bib $(GENERATED_FIGURES) | $(OUTPUT_DIR) $(AUX_DIR) $(LOG_DIR)
	# Copy necessary files to output directory for proper path resolution
	cp $(TEX_DIR)/style/HenriquesLab_style.bst $(OUTPUT_DIR)/ || true
	cp $(BIB_DIR)/references.bib $(OUTPUT_DIR)/ || true
	# Copy generated figures to output directory
	cp -r $(FIG_DIR)/* $(OUTPUT_DIR)/ || true
	$(LATEX_BUILD) $(TEX_DIR)/$(PROJECT).tex
	cd $(OUTPUT_DIR) && $(BIBTEX) $(BIBTEX_FLAGS) $(PROJECT)
	$(LATEX_BUILD) $(TEX_DIR)/$(PROJECT).tex
	$(LATEX_BUILD) $(TEX_DIR)/$(PROJECT).tex
	@echo "PDF built successfully: $(OUTPUT_DIR)/$(PROJECT).pdf"

# Figure generation targets
figures: $(FIGURE_GENERATOR)
	@echo "Generating figures..."
	cd $(FIGURE_SCRIPTS_DIR) && $(PYTHON) generators/generate_all.py
	@echo "Figures generated successfully"

# Install Python dependencies for figure generation
install-deps:
	@echo "Installing Python dependencies..."
	$(PYTHON) -m pip install -r requirements.txt
	@echo "Python dependencies installed"
	@echo "Note: For Mermaid diagrams, also install: npm install -g @mermaid-js/mermaid-cli"

# Check figure generation dependencies
check-deps:
	@echo "Checking figure generation dependencies..."
	cd $(FIGURE_SCRIPTS_DIR) && $(PYTHON) generators/generate_all.py --check-deps

# Docker-based compilation
docker-build: | $(BUILD_DIR)
	$(DOCKER_RUN) make all

docker-clean:
	$(DOCKER_RUN) make clean

# Watch for changes (requires inotify-tools on Linux, fswatch on macOS)
watch:
	@echo "Watching for changes... (Press Ctrl+C to stop)"
	@if command -v fswatch >/dev/null 2>&1; then \
		fswatch -o $(TEX_DIR) $(BIB_DIR) $(FIG_DIR) $(FIGURE_SCRIPTS_DIR) | while read num; do \
			echo "Changes detected, rebuilding..."; \
			make all; \
		done; \
	elif command -v inotifywait >/dev/null 2>&1; then \
		while inotifywait -r -e modify,create,delete $(TEX_DIR) $(BIB_DIR) $(FIG_DIR) $(FIGURE_SCRIPTS_DIR); do \
			make all; \
		done; \
	else \
		echo "Error: Neither fswatch (macOS) nor inotify-tools (Linux) found"; \
		echo "Install with: brew install fswatch (macOS) or apt-get install inotify-tools (Linux)"; \
		exit 1; \
	fi

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR)/*
	@echo "Build artifacts and generated figures cleaned"

# Development target for quick compilation
quick: | $(OUTPUT_DIR) $(AUX_DIR)
	$(LATEX_BUILD) $(TEX_DIR)/$(PROJECT).tex
