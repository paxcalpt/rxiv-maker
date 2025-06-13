# =====================================
# Article-Forge Makefile
# =====================================
# Automated LaTeX article generation and building system
# 
# Quick Start:
#   make easy-setup     # First-time Docker setup
#   make easy-build     # Generate PDF with Docker
#   make pdf            # Generate PDF locally (requires LaTeX)
#   make help           # Show all available commands
#
# Author: Article-Forge Project
# Documentation: See README.md
# =====================================

# =====================================
# Configuration Variables
# =====================================
OUTPUT_DIR := output
ARTICLE_DIR := ARTICLE
FIGURES_DIR := $(ARTICLE_DIR)/FIGURES
STYLE_DIR := src/tex/style
PYTHON_SCRIPT := src/py/commands/generate_article.py
FIGURE_SCRIPT := src/py/commands/generate_figures.py
TEMPLATE_FILE := src/tex/template.tex
ARTICLE_MD := $(ARTICLE_DIR)/00_ARTICLE.md
REFERENCES_BIB := $(ARTICLE_DIR)/02_REFERENCES.bib
SUPPLEMENTARY_MD := $(ARTICLE_DIR)/01_SUPPLEMENTARY_INFO.md

# =====================================
# Default and Convenience Targets
# ====================================="

# Default target
.PHONY: all
all: build

# =====================================
# Quick Start Aliases
# =====================================
# Convenience aliases for Docker commands
.PHONY: easy-setup
easy-setup: docker-setup

.PHONY: easy-build
easy-build: docker-build

# =====================================
# Core Build Targets
# =====================================

# Create output directory and generate LaTeX files
.PHONY: setup
setup:
	@echo "Setting up output directory..."
	@mkdir -p $(OUTPUT_DIR)
	@mkdir -p $(OUTPUT_DIR)/Figures
	@echo "Output directory created: $(OUTPUT_DIR)"

# Generate figures from .mmd and .py files (always regenerates)
.PHONY: figures
figures:
	@echo "Generating figures from $(FIGURES_DIR)..."
	@python3 $(FIGURE_SCRIPT) --figures-dir $(FIGURES_DIR) --output-dir $(FIGURES_DIR) --format pdf
	@echo "Figure generation complete"

# Generate figures conditionally (only if they don't exist or FORCE_FIGURES=true)
.PHONY: figures-conditional
figures-conditional:
	@if [ "$(FORCE_FIGURES)" = "true" ]; then \
		echo "Forcing figure regeneration from $(FIGURES_DIR)..."; \
		python3 $(FIGURE_SCRIPT) --figures-dir $(FIGURES_DIR) --output-dir $(FIGURES_DIR) --format pdf; \
		echo "Figure generation complete"; \
	else \
		echo "Checking if figures need to be generated..."; \
		NEED_FIGURES=false; \
		for mmd_file in $(FIGURES_DIR)/*.mmd; do \
			if [ -f "$$mmd_file" ]; then \
				base_name=$$(basename "$$mmd_file" .mmd); \
				if [ ! -f "$(FIGURES_DIR)/$$base_name.pdf" ] || [ ! -f "$(FIGURES_DIR)/$$base_name.svg" ]; then \
					NEED_FIGURES=true; \
					break; \
				fi; \
			fi; \
		done; \
		for py_file in $(FIGURES_DIR)/*.py; do \
			if [ -f "$$py_file" ]; then \
				base_name=$$(basename "$$py_file" .py); \
				if [ ! -f "$(FIGURES_DIR)/$$base_name.pdf" ]; then \
					NEED_FIGURES=true; \
					break; \
				fi; \
			fi; \
		done; \
		if [ "$$NEED_FIGURES" = "true" ]; then \
			echo "Missing figures detected, generating figures from $(FIGURES_DIR)..."; \
			python3 $(FIGURE_SCRIPT) --figures-dir $(FIGURES_DIR) --output-dir $(FIGURES_DIR) --format pdf; \
			echo "Figure generation complete"; \
		else \
			echo "All figures exist, skipping generation (use FORCE_FIGURES=true to regenerate)"; \
		fi; \
	fi


# Generate the ARTICLE.tex file
.PHONY: generate
generate: setup figures-conditional
	@echo "Generating ARTICLE.tex from $(ARTICLE_MD)..."
	@python3 $(PYTHON_SCRIPT) --output-dir $(OUTPUT_DIR)

# Copy all necessary files for LaTeX compilation
.PHONY: copy-files
copy-files: generate
	@echo "Copying necessary files to $(OUTPUT_DIR)..."
	# Copy LaTeX style files
	@cp $(STYLE_DIR)/*.cls $(OUTPUT_DIR)/ 2>/dev/null || echo "No .cls files found in $(STYLE_DIR)"
	@cp $(STYLE_DIR)/*.bst $(OUTPUT_DIR)/ 2>/dev/null || echo "No .bst files found in $(STYLE_DIR)"
	@cp $(STYLE_DIR)/*.sty $(OUTPUT_DIR)/ 2>/dev/null || echo "No .sty files found in $(STYLE_DIR)"
	
	# Copy bibliography file
	@if [ -f $(REFERENCES_BIB) ]; then \
		cp $(REFERENCES_BIB) $(OUTPUT_DIR)/; \
		echo "Copied $(REFERENCES_BIB)"; \
	else \
		echo "Warning: $(REFERENCES_BIB) not found"; \
	fi
	
	# Copy figures directory
	@if [ -d $(FIGURES_DIR) ]; then \
		cp -r $(FIGURES_DIR)/* $(OUTPUT_DIR)/Figures/ 2>/dev/null || echo "No figures to copy"; \
		echo "Copied figures from $(FIGURES_DIR)"; \
	else \
		echo "Warning: $(FIGURES_DIR) directory not found"; \
	fi
	
	# Copy any additional LaTeX files from src/tex
	@find src/tex -name "*.tex" -not -name "template.tex" -exec cp {} $(OUTPUT_DIR)/ \; 2>/dev/null || true
	@find src/tex -name "*.cls" -exec cp {} $(OUTPUT_DIR)/ \; 2>/dev/null || true
	@find src/tex -name "*.sty" -exec cp {} $(OUTPUT_DIR)/ \; 2>/dev/null || true
	
	@echo "All necessary files copied to $(OUTPUT_DIR)"

# Build the complete output directory
.PHONY: build
build: copy-files
	@echo "Build complete! Output directory: $(OUTPUT_DIR)"
	@echo "Contents of $(OUTPUT_DIR):"
	@ls -la $(OUTPUT_DIR)/

# Compile the LaTeX document to PDF (requires LaTeX installation)
.PHONY: pdf
pdf: build
	@echo "Compiling LaTeX to PDF..."
	@cd $(OUTPUT_DIR) && \
	pdflatex ARTICLE.tex && \
	bibtex ARTICLE && \
	pdflatex ARTICLE.tex && \
	pdflatex ARTICLE.tex
	@echo "PDF compilation complete: $(OUTPUT_DIR)/ARTICLE.pdf"
	@echo "Copying PDF to base directory with custom filename..."
	@python3 src/py/commands/copy_pdf.py --output-dir $(OUTPUT_DIR)

# =====================================
# Installation and Dependencies
# =====================================

# Install Python dependencies
.PHONY: install-deps
install-deps:
	@echo "Installing Python dependencies..."
	@pip3 install -r requirements.txt

# Install system dependencies (macOS with Homebrew)
.PHONY: install-system-deps
install-system-deps:
	@echo "Installing system dependencies..."
	@if command -v brew >/dev/null 2>&1; then \
		brew install --cask mactex || brew install --cask basictex; \
		echo "LaTeX installed via Homebrew"; \
	else \
		echo "Homebrew not found. Please install MacTeX manually from https://www.tug.org/mactex/"; \
	fi

# =====================================
# Docker Commands (Optimized)
# =====================================
# Note: Using new optimized Docker setup in src/docker/

.PHONY: docker-setup
docker-setup:
	@echo "Setting up Docker environment..."
	@./docker.sh build

.PHONY: docker-build
docker-build:
	@echo "Building PDF using Docker..."
	@./docker.sh pdf

.PHONY: docker-dev
docker-dev:
	@echo "Starting Docker development mode..."
	@./docker.sh dev

.PHONY: docker-shell
docker-shell:
	@echo "Opening Docker interactive shell..."
	@./docker.sh shell

.PHONY: docker-watch
docker-watch:
	@echo "Starting Docker watch mode..."
	@./docker.sh watch

.PHONY: docker-force-figures
docker-force-figures:
	@echo "Building PDF with forced figure regeneration..."
	@./docker.sh pdf --force-figures

.PHONY: docker-status
docker-status:
	@echo "Checking Docker status..."
	@./docker.sh status

.PHONY: docker-clean
docker-clean:
	@echo "Cleaning Docker resources..."
	@./docker.sh clean

# =====================================
# Maintenance and Utilities
# ====================================="

# Clean output directory
.PHONY: clean
clean:
	@echo "Cleaning output directory..."
	@rm -rf $(OUTPUT_DIR)
	@echo "Output directory cleaned"

# Development target - watch for changes and rebuild
.PHONY: watch
watch:
	@echo "Watching for changes..."
	@while true; do \
		$(MAKE) build; \
		echo "Waiting for changes to $(ARTICLE_MD), $(REFERENCES_BIB), $(TEMPLATE_FILE), or source files..."; \
		fswatch -1 $(ARTICLE_DIR)/ $(TEMPLATE_FILE) src/; \
		echo "Changes detected, rebuilding..."; \
	done

# Show help
.PHONY: help
help:
	@echo "====================================="; \
	echo "Article-Forge Makefile Commands"; \
	echo "====================================="; \
	echo ""; \
	echo "🚀 QUICK START:"; \
	echo "  make easy-setup      - Set up Docker environment (first time)"; \
	echo "  make easy-build      - Generate PDF with Docker (no LaTeX needed)"; \
	echo ""; \
	echo "📝 LOCAL COMMANDS (require LaTeX installation):"; \
	echo "  make build           - Generate ARTICLE.tex and copy all files"; \
	echo "  make figures         - Always regenerate figures from .mmd and .py files"; \
	echo "  make pdf             - Build LaTeX document (generates missing figures only)"; \
	echo "  make pdf FORCE_FIGURES=true - Build PDF and force all figure regeneration"; \
	echo "  make watch           - Watch for changes and rebuild automatically"; \
	echo ""; \
	echo "🐳 DOCKER COMMANDS (no local LaTeX needed):"; \
	echo "  make docker-setup    - Build Docker image"; \
	echo "  make docker-build    - Build PDF using Docker"; \
	echo "  make docker-dev      - Start development container"; \
	echo "  make docker-shell    - Open interactive Docker shell"; \
	echo "  make docker-watch    - Watch mode with auto-rebuild"; \
	echo "  make docker-force-figures - Build PDF with forced figure regeneration"; \
	echo "  make docker-status   - Check Docker container/image status"; \
	echo "  make docker-clean    - Clean up Docker resources"; \
	echo ""; \
	echo "🔧 MAINTENANCE:"; \
	echo "  make clean           - Remove output directory"; \
	echo "  make check           - Check if required files exist"; \
	echo "  make install-deps    - Install Python dependencies"; \
	echo "  make install-system-deps - Install LaTeX (macOS with Homebrew)"; \
	echo "  make help            - Show this help message"; \
	echo ""; \
	echo "📊 FIGURE GENERATION:"; \
	echo "  - 'make figures':    Always regenerates all figures"; \
	echo "  - 'make pdf':        Only generates missing figures"; \
	echo "  - 'make pdf FORCE_FIGURES=true': Forces regeneration of all figures"; \
	echo "  - Supports .mmd (Mermaid) and .py (Python) figure sources"; \
	echo ""; \
	echo "📁 DIRECTORIES:"; \
	echo "  - Article files: $(ARTICLE_DIR)/"; \
	echo "  - Figures:       $(FIGURES_DIR)/"; \
	echo "  - Output:        $(OUTPUT_DIR)/"; \
	echo "  - Source:        src/"; \
	echo ""; \
	echo "� TIP: New to Article-Forge?"; \
	echo "   1. Run 'make easy-setup' to set up Docker"; \
	echo "   2. Run 'make easy-build' to generate your first PDF"; \
	echo "   3. Edit files in $(ARTICLE_DIR)/ and re-run 'make easy-build'"

# Check if required files exist
.PHONY: check
check:
	@echo "Checking required files..."
	@[ -f $(ARTICLE_MD) ] && echo "✓ $(ARTICLE_MD)" || echo "✗ $(ARTICLE_MD) missing"
	@[ -f $(PYTHON_SCRIPT) ] && echo "✓ $(PYTHON_SCRIPT)" || echo "✗ $(PYTHON_SCRIPT) missing"
	@[ -f $(TEMPLATE_FILE) ] && echo "✓ $(TEMPLATE_FILE)" || echo "✗ $(TEMPLATE_FILE) missing"
	@[ -f $(REFERENCES_BIB) ] && echo "✓ $(REFERENCES_BIB)" || echo "✗ $(REFERENCES_BIB) missing"
	@[ -d $(STYLE_DIR) ] && echo "✓ $(STYLE_DIR)" || echo "✗ $(STYLE_DIR) missing"
	@python3 --version >/dev/null 2>&1 && echo "✓ Python 3" || echo "✗ Python 3 missing"
	@pdflatex --version >/dev/null 2>&1 && echo "✓ pdflatex" || echo "✗ pdflatex missing (install LaTeX)"