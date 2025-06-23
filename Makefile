# ======================================================================
#  _____  __   __  _  __   __         __  __          _
# |  __ \ \ \ / / (_)\ \ / /         |  \/  |        | |
# | |__) | \ V /   _  \ V /   _____  | \  / |  __ _  | | __  ___  _ __
# |  _  /   > <   | |  > <   |_____| | |\/| | / _` | | |/ / / _ \| '__|
# |_| \_\  /_/\_\ |_| /_/\_\         | |  | || (_| | |   < |  __/| |
#                                     |_|  |_| \__,_| |_|\_\ \___||_|
#
# ======================================================================
# Automated Scientific Article Generation and Publishing System
#
# 🚀 QUICK START:
#   make setup        # First-time setup with Docker (easiest)
#   make pdf          # Generate PDF with Docker (no LaTeX needed)
#   make local        # Generate PDF locally (requires LaTeX)
#   make help         # Show all available commands
#
# Author: RXiv-Maker Project
# Documentation: See README.md
# ======================================================================

# ======================================================================
# ⚙️  CONFIGURATION VARIABLES
# ======================================================================

# Load environment variables from .env file if it exists
-include .env
export

# Python command selection (use venv if available, otherwise system python)
PYTHON_CMD := $(shell if [ -f ".venv/bin/python" ]; then echo ".venv/bin/python"; else echo "python3"; fi)
# Determine timeout command (GNU timeout or gtimeout on macOS)
TIMEOUT_CMD := $(shell if command -v timeout >/dev/null 2>&1; then echo timeout; elif command -v gtimeout >/dev/null 2>&1; then echo gtimeout; else echo ""; fi)
# Timeout wrapper (use TIMEOUT from .env if set, otherwise default to 15s)
TIMEOUT_VALUE ?= $(if $(TIMEOUT),$(TIMEOUT),15)
TIMEOUT := $(if $(TIMEOUT_CMD),$(TIMEOUT_CMD) $(TIMEOUT_VALUE)s,)

OUTPUT_DIR := output
MANUSCRIPT_PATH ?= MANUSCRIPT
ARTICLE_DIR := $(MANUSCRIPT_PATH)
FIGURES_DIR := $(ARTICLE_DIR)/FIGURES
STYLE_DIR := src/tex/style
PYTHON_SCRIPT := src/py/commands/generate_preprint.py
FIGURE_SCRIPT := src/py/commands/generate_figures.py

# Testing configuration
TEMPLATE_FILE := src/tex/template.tex
ARTICLE_MD := $(ARTICLE_DIR)/01_MAIN.md
MANUSCRIPT_CONFIG := $(ARTICLE_DIR)/00_CONFIG.yml
SUPPLEMENTARY_MD := $(ARTICLE_DIR)/02_SUPPLEMENTARY_INFO.md
REFERENCES_BIB := $(ARTICLE_DIR)/03_REFERENCES.bib

# ======================================================================
# 📌 DEFAULT AND CONVENIENCE TARGETS
# ======================================================================

# Default target
.PHONY: all
all: pdf

# ======================================================================
# 🚀 QUICK START COMMANDS
# ======================================================================
# Main user-facing commands with simple names

# Setup Docker for first-time use
.PHONY: setup
setup:
	@echo "Setting up Docker environment..."
	@echo "Using pre-built image henriqueslab/rxiv-maker:latest"
	@docker pull henriqueslab/rxiv-maker:latest
	@echo "✅ Setup complete! Now you can run 'make pdf' to create your document."

# Generate PDF with Docker (no LaTeX installation needed)
.PHONY: pdf
pdf:
	@echo "Building PDF using Docker..."
	@docker run --rm \
		-v $(PWD):/app \
		-w /app \
		--env-file .env \
		henriqueslab/rxiv-maker:latest \
		bash -c "make _build_pdf"
	@echo "PDF compilation complete: $(OUTPUT_DIR)/MANUSCRIPT.pdf"
	@echo "Copying PDF to manuscript folder with custom filename..."
	@MANUSCRIPT_PATH=$(MANUSCRIPT_PATH) $(PYTHON_CMD) src/py/commands/copy_pdf.py --output-dir $(OUTPUT_DIR)

# Generate PDF locally (requires LaTeX installation)
.PHONY: local
local: _build_pdf

# ======================================================================
# 🔨 INTERNAL BUILD TARGETS
# ======================================================================

# Internal target for building PDF (used by both pdf and local targets)
.PHONY: _build_pdf
_build_pdf: _generate_files
	@echo "Compiling LaTeX to PDF..."
	cd $(OUTPUT_DIR) && \
	 pdflatex -interaction=nonstopmode MANUSCRIPT.tex || true && \
	 bibtex MANUSCRIPT || true && \
	 pdflatex -interaction=nonstopmode MANUSCRIPT.tex || true && \
	 pdflatex -interaction=nonstopmode MANUSCRIPT.tex || true
	@echo "PDF compilation complete: $(OUTPUT_DIR)/MANUSCRIPT.pdf"
	@$(PYTHON_CMD) src/py/commands/analyze_word_count.py

# Internal target for generating all necessary files
.PHONY: _generate_files
_generate_files:
	@echo "Setting up output directory..."
	@mkdir -p $(OUTPUT_DIR)
	@mkdir -p $(OUTPUT_DIR)/Figures

	@echo "Checking if figures need to be generated..."
	@NEED_FIGURES=false; \
	for mmd_file in $(FIGURES_DIR)/*.mmd; do \
		if [ -f "$$mmd_file" ]; then \
			base_name=$$(basename "$$mmd_file" .mmd); \
			if [ ! -f "$(FIGURES_DIR)/$$base_name/$$base_name.pdf" ]; then \
				NEED_FIGURES=true; \
				break; \
			fi; \
		fi; \
	done; \
	if [ "$$NEED_FIGURES" = "true" ] || [ "$(FORCE_FIGURES)" = "true" ]; then \
		echo "Generating figures from $(FIGURES_DIR)..."; \
		$(PYTHON_CMD) $(FIGURE_SCRIPT) --figures-dir $(FIGURES_DIR) --output-dir $(FIGURES_DIR) --format pdf; \
	fi

	@echo "Generating MANUSCRIPT.tex from $(ARTICLE_MD)..."
	@$(PYTHON_CMD) $(PYTHON_SCRIPT) --output-dir $(OUTPUT_DIR)

	@echo "Copying necessary files to $(OUTPUT_DIR)..."
	@cp $(STYLE_DIR)/*.cls $(OUTPUT_DIR)/ 2>/dev/null || echo "No .cls files found"
	@cp $(STYLE_DIR)/*.bst $(OUTPUT_DIR)/ 2>/dev/null || echo "No .bst files found"
	@cp $(STYLE_DIR)/*.sty $(OUTPUT_DIR)/ 2>/dev/null || echo "No .sty files found"

	@if [ -f $(REFERENCES_BIB) ]; then \
		cp $(REFERENCES_BIB) $(OUTPUT_DIR)/; \
	fi

	@if [ -d $(FIGURES_DIR) ]; then \
		mkdir -p $(OUTPUT_DIR)/Figures; \
		cp -r $(FIGURES_DIR)/* $(OUTPUT_DIR)/Figures/ 2>/dev/null || true; \
	fi

	@find src/tex -name "*.tex" -not -name "template.tex" -exec cp {} $(OUTPUT_DIR)/ \; 2>/dev/null || true
	@find src/tex -name "*.cls" -exec cp {} $(OUTPUT_DIR)/ \; 2>/dev/null || true
	@find src/tex -name "*.sty" -exec cp {} $(OUTPUT_DIR)/ \; 2>/dev/null || true

# ======================================================================
# 🧹 MAINTENANCE
# ======================================================================

# Clean output directory
.PHONY: clean
clean:
	@echo "Cleaning output directory..."
	@rm -rf $(OUTPUT_DIR)
	@echo "Output directory cleaned"

# Show help
.PHONY: help
help:
	@VERSION=$$($(PYTHON_CMD) -c "import sys; sys.path.insert(0, 'src/py'); from src.py import __version__; print(__version__)" 2>/dev/null || echo "unknown"); \
	echo "====================================="; \
	echo "RXiv-Maker v$$VERSION - Makefile Commands"; \
	echo "====================================="; \
	echo ""; \
	echo "🚀 ESSENTIAL COMMANDS:"; \
	echo "  make setup          - Set up Docker environment (first time)"; \
	echo "  make pdf            - Generate PDF with Docker (no LaTeX needed)"; \
	echo "  make local          - Generate PDF locally (requires LaTeX)"; \
	echo "  make clean          - Remove output directory"; \
	echo "  make help           - Show this help message"; \
	echo ""; \
	echo "📁 DIRECTORIES:"; \
	echo "  - Manuscript files: $(ARTICLE_DIR)/"; \
	echo "  - Figures:          $(FIGURES_DIR)/"; \
	echo "  - Output:           $(OUTPUT_DIR)/"; \
	echo ""; \
	echo "💡 TIP: New to RXiv-Maker?"; \
	echo "   1. Run 'make setup' to set up Docker"; \
	echo "   2. Run 'make pdf' to generate your first PDF"; \
	echo "   3. Edit files in $(ARTICLE_DIR)/ and re-run 'make pdf'"; \
	echo ""; \
	echo "💡 ADVANCED OPTIONS:"; \
	echo "   - Force figure regeneration: make pdf FORCE_FIGURES=true"; \
	echo "   - Use different manuscript folder: make pdf MANUSCRIPT_PATH=path/to/folder"
