# =====================================
# RXiv-Maker Makefile
# =====================================
# Automated LaTeX article generation and building system
#
# Quick Start:
#   make easy-setup     # First-time Docker setup
#   make easy-build     # Generate PDF with Docker
#   make pdf            # Generate PDF locally (requires LaTeX)
#   make help           # Show all available commands
#
# Author: RXiv-Maker Project
# Documentation: See README.md
# =====================================

# =====================================
# Configuration Variables
# =====================================

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
PYTEST_ARGS ?= -v --tb=short
COVERAGE_ARGS ?= --cov=src/py --cov-report=html --cov-report=term
TEMPLATE_FILE := src/tex/template.tex
ARTICLE_MD := $(ARTICLE_DIR)/01_MAIN.md
MANUSCRIPT_CONFIG := $(ARTICLE_DIR)/00_CONFIG.yml
SUPPLEMENTARY_MD := $(ARTICLE_DIR)/02_SUPPLEMENTARY_INFO.md
REFERENCES_BIB := $(ARTICLE_DIR)/03_REFERENCES.bib

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
	@$(PYTHON_CMD) $(FIGURE_SCRIPT) --figures-dir $(FIGURES_DIR) --output-dir $(FIGURES_DIR) --format pdf
	@echo "Figure generation complete"

# Generate figures conditionally (only if they don't exist or FORCE_FIGURES=true)
.PHONY: figures-conditional
figures-conditional:
	@if [ "$(FORCE_FIGURES)" = "true" ]; then \
		echo "Forcing figure regeneration from $(FIGURES_DIR)..."; \
		$(PYTHON_CMD) $(FIGURE_SCRIPT) --figures-dir $(FIGURES_DIR) --output-dir $(FIGURES_DIR) --format pdf; \
		echo "Figure generation complete"; \
	else \
		echo "Checking if figures need to be generated..."; \
		NEED_FIGURES=false; \
		for mmd_file in $(FIGURES_DIR)/*.mmd; do \
			if [ -f "$$mmd_file" ]; then \
				base_name=$$(basename "$$mmd_file" .mmd); \
				if [ ! -f "$(FIGURES_DIR)/$$base_name/$$base_name.pdf" ] || [ ! -f "$(FIGURES_DIR)/$$base_name/$$base_name.svg" ] || [ ! -f "$(FIGURES_DIR)/$$base_name/$$base_name.png" ]; then \
					NEED_FIGURES=true; \
					break; \
				fi; \
			fi; \
		done; \
		for py_file in $(FIGURES_DIR)/*.py; do \
			if [ -f "$$py_file" ]; then \
				base_name=$$(basename "$$py_file" .py); \
				if [ ! -d "$(FIGURES_DIR)/$$base_name" ] || [ ! -f "$(FIGURES_DIR)/$$base_name/$$base_name.pdf" ] || [ ! -f "$(FIGURES_DIR)/$$base_name/$$base_name.png" ]; then \
					NEED_FIGURES=true; \
					break; \
				fi; \
			fi; \
		done; \
		if [ "$$NEED_FIGURES" = "true" ]; then \
			echo "Missing figures detected, generating figures from $(FIGURES_DIR)..."; \
			$(PYTHON_CMD) $(FIGURE_SCRIPT) --figures-dir $(FIGURES_DIR) --output-dir $(FIGURES_DIR) --format pdf; \
			echo "Figure generation complete"; \
		else \
			echo "All figures exist, skipping generation (use FORCE_FIGURES=true to regenerate)"; \
		fi; \
	fi


# Generate the MANUSCRIPT.tex file
.PHONY: generate
generate: setup figures-conditional
	@echo "Generating MANUSCRIPT.tex from $(ARTICLE_MD)..."
	@$(PYTHON_CMD) $(PYTHON_SCRIPT) --output-dir $(OUTPUT_DIR)

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

	# Copy figures directory and subdirectories
	@if [ -d $(FIGURES_DIR) ]; then \
		mkdir -p $(OUTPUT_DIR)/Figures; \
		cp $(FIGURES_DIR)/*.pdf $(OUTPUT_DIR)/Figures/ 2>/dev/null || true; \
		cp $(FIGURES_DIR)/*.png $(OUTPUT_DIR)/Figures/ 2>/dev/null || true; \
		cp $(FIGURES_DIR)/*.svg $(OUTPUT_DIR)/Figures/ 2>/dev/null || true; \
		for fig_dir in $(FIGURES_DIR)/*/; do \
			if [ -d "$$fig_dir" ]; then \
				fig_name=$$(basename "$$fig_dir"); \
				mkdir -p "$(OUTPUT_DIR)/Figures/$$fig_name"; \
				cp "$$fig_dir"*.pdf "$(OUTPUT_DIR)/Figures/$$fig_name/" 2>/dev/null || true; \
				cp "$$fig_dir"*.png "$(OUTPUT_DIR)/Figures/$$fig_name/" 2>/dev/null || true; \
				cp "$$fig_dir"*.svg "$(OUTPUT_DIR)/Figures/$$fig_name/" 2>/dev/null || true; \
			fi; \
		done; \
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
	@echo ""
	@if [ -f "$(OUTPUT_DIR)/MANUSCRIPT.pdf" ]; then \
		echo "✅ PDF already exists: $(OUTPUT_DIR)/MANUSCRIPT.pdf"; \
		echo "   To regenerate PDF, run: make pdf"; \
	else \
		echo "ℹ️  No PDF found. To generate PDF, run: make pdf"; \
	fi
	@echo ""
	# Run word count analysis as the final step
	@$(PYTHON_CMD) src/py/commands/analyze_word_count.py

# Compile the LaTeX document to PDF (requires LaTeX installation)
.PHONY: pdf
pdf: build
	@echo "Compiling LaTeX to PDF..."
	# Use nonstopmode and ignore errors to still produce PDF even with minor LaTeX issues
	cd $(OUTPUT_DIR) && \
	 pdflatex -interaction=nonstopmode MANUSCRIPT.tex || true && \
	 bibtex MANUSCRIPT || true && \
	 pdflatex -interaction=nonstopmode MANUSCRIPT.tex || true && \
	 pdflatex -interaction=nonstopmode MANUSCRIPT.tex || true
	@echo "PDF compilation complete: $(OUTPUT_DIR)/MANUSCRIPT.pdf"
	@echo "Copying PDF to manuscript folder with custom filename..."
	@MANUSCRIPT_PATH=$(MANUSCRIPT_PATH) $(PYTHON_CMD) src/py/commands/copy_pdf.py --output-dir $(OUTPUT_DIR)
	@echo ""
	# Run word count analysis as the final step
	@$(PYTHON_CMD) src/py/commands/analyze_word_count.py

# =====================================
# Installation and Dependencies
# =====================================

# Setup virtual environment
.PHONY: venv
venv:
	@echo "Setting up Python virtual environment..."
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
		echo "✓ Virtual environment created at .venv"; \
	else \
		echo "✓ Virtual environment already exists at .venv"; \
	fi
	@echo "To activate: source .venv/bin/activate"

# Install Python dependencies in virtual environment
.PHONY: install-deps
install-deps: venv
	@echo "Installing Python dependencies in virtual environment..."
	@if [ -f ".venv/bin/activate" ]; then \
		. .venv/bin/activate && pip install -r requirements.txt; \
		echo "✓ Dependencies installed in .venv"; \
	else \
		echo "✗ Virtual environment not found. Run 'make venv' first"; \
		exit 1; \
	fi

# Alias for install-deps
.PHONY: install
install: install-deps

# Install Python dependencies without virtual environment
.PHONY: install-deps-global
install-deps-global:
	@echo "Installing Python dependencies globally..."
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
	@echo "Using pre-built image henriqueslab/rxiv-maker:latest"
	@docker pull henriqueslab/rxiv-maker:latest

.PHONY: docker-build
docker-build:
	@echo "Building PDF using Docker..."
	@docker run --rm \
		-v $(PWD):/app \
		-w /app \
		--env-file .env \
		henriqueslab/rxiv-maker:latest \
		bash -c "make pdf"

.PHONY: docker-dev
docker-dev:
	@echo "Starting Docker development mode..."
	@docker run -it --rm \
		-v $(PWD):/app \
		-w /app \
		--env-file .env \
		henriqueslab/rxiv-maker:dev \
		bash

.PHONY: docker-shell
docker-shell:
	@echo "Opening Docker interactive shell..."
	@docker run -it --rm \
		-v $(PWD):/app \
		-w /app \
		--env-file .env \
		henriqueslab/rxiv-maker:latest \
		bash

.PHONY: docker-watch
docker-watch:
	@echo "Starting Docker watch mode..."
	@echo "Watch mode not supported with pre-built images. Use 'make watch' for local development."

.PHONY: docker-force-figures
docker-force-figures:
	@echo "Building PDF with forced figure regeneration..."
	@docker run --rm \
		-v $(PWD):/app \
		-w /app \
		--env-file .env \
		-e FORCE_FIGURES=true \
		henriqueslab/rxiv-maker:latest \
		bash -c "make pdf"

.PHONY: docker-status
docker-status:
	@echo "Checking Docker status..."
	@docker images henriqueslab/rxiv-maker:*
	@echo "Available containers:"
	@docker ps -a --filter ancestor=henriqueslab/rxiv-maker

.PHONY: docker-clean
docker-clean:
	@echo "Cleaning Docker resources..."
	@docker system prune -f
	@docker rmi henriqueslab/rxiv-maker:* 2>/dev/null || true

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
		echo "Waiting for changes to $(MANUSCRIPT_MD), $(REFERENCES_BIB), $(TEMPLATE_FILE), or source files..."; \
		fswatch -1 $(MANUSCRIPT_PATH)/ $(TEMPLATE_FILE) src/; \
		echo "Changes detected, rebuilding..."; \
	done

# Show help
.PHONY: help
help:
	@VERSION=$$($(PYTHON_CMD) -c "import sys; sys.path.insert(0, 'src/py'); from src.py import __version__; print(__version__)" 2>/dev/null || echo "unknown"); \
	echo "====================================="; \
	echo "RXiv-Maker v$$VERSION - Makefile Commands"; \
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
	echo "🧪 TESTING COMMANDS:"; \
	echo "  make test            - Run all tests"; \
	echo "  make test-unit       - Run unit tests only"; \
	echo "  make test-integration - Run integration tests only"; \
	echo "  make test-notebooks  - Run notebook tests only"; \
	echo "  make test-coverage   - Run tests with coverage report"; \
	echo "  make test-docker     - Run tests in Docker environment"; \
	echo "  make lint            - Run code linting and formatting"; \
	echo "  make typecheck       - Run type checking with mypy"; \
	echo ""; \
	echo "🔧 SETUP & MAINTENANCE:"; \
	echo "  make setup-dev       - Complete development setup (venv + deps)"; \
	echo "  make venv            - Create Python virtual environment (.venv)"; \
	echo "  make install-deps    - Install Python dependencies in .venv"; \
	echo "  make install-deps-global - Install Python dependencies globally"; \
	echo "  make install-system-deps - Install LaTeX (macOS with Homebrew)"; \
	echo "  make clean           - Remove output directory"; \
	echo "  make check           - Check if required files exist"; \
	echo "  make help            - Show this help message"; \
	echo ""; \
	echo "📚 DOCUMENTATION:"; \
	echo "  make docs            - Generate API documentation with lazydocs"; \
	echo "  make docs-serve      - Serve documentation locally (http://localhost:8080)"; \
	echo "  make docs-clean      - Clean generated documentation files"; \
	echo ""; \
	echo "📊 FIGURE GENERATION:"; \
	echo "  - 'make figures':    Always regenerates all figures"; \
	echo "  - 'make pdf':        Only generates missing figures"; \
	echo "  - 'make pdf FORCE_FIGURES=true': Forces regeneration of all figures"; \
	echo "  - Supports .mmd (Mermaid) and .py (Python) figure sources"; \
	echo ""; \
	echo "📁 DIRECTORIES:"; \
	echo "  - Manuscript files: $(ARTICLE_DIR)/"; \
	echo "  - Figures:          $(FIGURES_DIR)/"; \
	echo "  - Output:           $(OUTPUT_DIR)/"; \
	echo "  - Source:           src/"; \
	echo ""; \
	echo "� TIP: New to RXiv-Maker?"; \
	echo "   1. Run 'make easy-setup' to set up Docker"; \
	echo "   2. Run 'make easy-build' to generate your first PDF"; \
	echo "   3. Edit files in $(ARTICLE_DIR)/ and re-run 'make easy-build'"

# Check if required files exist
.PHONY: check
check:
	@echo "Checking required files..."
	@[ -f $(ARTICLE_MD) ] && echo "✓ $(ARTICLE_MD)" || echo "✗ $(ARTICLE_MD) missing"
	@[ -f $(MANUSCRIPT_CONFIG) ] && echo "✓ $(MANUSCRIPT_CONFIG)" || echo "ℹ $(MANUSCRIPT_CONFIG) optional (fallback to inline YAML)"
	@[ -f $(PYTHON_SCRIPT) ] && echo "✓ $(PYTHON_SCRIPT)" || echo "✗ $(PYTHON_SCRIPT) missing"
	@[ -f $(TEMPLATE_FILE) ] && echo "✓ $(TEMPLATE_FILE)" || echo "✗ $(TEMPLATE_FILE) missing"
	@[ -f $(REFERENCES_BIB) ] && echo "✓ $(REFERENCES_BIB)" || echo "✗ $(REFERENCES_BIB) missing"
	@[ -d $(STYLE_DIR) ] && echo "✓ $(STYLE_DIR)" || echo "✗ $(STYLE_DIR) missing"
	@echo "Environment:"
	@[ -d ".venv" ] && echo "✓ Virtual environment (.venv)" || echo "ℹ No virtual environment (run 'make venv')"
	@echo "Python: $(PYTHON_CMD)"
	@$(PYTHON_CMD) --version >/dev/null 2>&1 && echo "✓ Python available" || echo "✗ Python missing"
	@pdflatex --version >/dev/null 2>&1 && echo "✓ pdflatex" || echo "✗ pdflatex missing (install LaTeX)"

# =====================================
# Testing Targets
# =====================================

# Run all tests
.PHONY: test
test:
	@echo "Running all tests..."
	python -m pytest $(PYTEST_ARGS)

# Run unit tests only
.PHONY: test-unit
test-unit:
	@echo "Running unit tests..."
	python -m pytest tests/unit/ $(PYTEST_ARGS)

# Run integration tests only
.PHONY: test-integration
test-integration:
	@echo "Running integration tests..."
	python -m pytest tests/integration/ $(PYTEST_ARGS)

# Run notebook tests only
.PHONY: test-notebooks
test-notebooks:
	@echo "Running notebook tests..."
	python -m pytest tests/notebooks/ $(PYTEST_ARGS) -m notebook

# Run tests with coverage report
.PHONY: test-coverage
test-coverage:
	@echo "Running tests with coverage..."
	python -m pytest $(COVERAGE_ARGS) $(PYTEST_ARGS)

# Run tests in Docker environment
.PHONY: test-docker
test-docker:
	@echo "Running tests in Docker..."
	docker run --rm -v $(PWD):/app -w /app henriqueslab/rxiv-maker:dev \
		python -m pytest $(PYTEST_ARGS)

# Run code linting and formatting
.PHONY: lint
lint:
	@echo "Running code formatting and linting..."
	@command -v black >/dev/null 2>&1 && black src/ tests/ || echo "⚠️  black not installed, skipping formatting"
	@command -v flake8 >/dev/null 2>&1 && flake8 src/ tests/ || echo "⚠️  flake8 not installed, skipping linting"
	@command -v isort >/dev/null 2>&1 && isort src/ tests/ || echo "⚠️  isort not installed, skipping import sorting"

# Run type checking
.PHONY: typecheck
typecheck:
	@echo "Running type checking..."
	@command -v mypy >/dev/null 2>&1 && mypy src/ || echo "⚠️  mypy not installed, skipping type checking"

# Complete development setup
.PHONY: setup-dev
setup-dev: venv install-deps
	@echo "✓ Development environment setup complete!"
	@echo "To activate virtual environment: source .venv/bin/activate"
	@echo "To build PDF: make build"

# Install development dependencies
.PHONY: install-dev
install-dev: venv
	@echo "Installing development dependencies..."
	@if [ -f ".venv/bin/activate" ]; then \
		. .venv/bin/activate && pip install -e ".[dev]"; \
		echo "✓ Development dependencies installed in .venv"; \
	else \
		pip install -e ".[dev]"; \
		echo "✓ Development dependencies installed globally"; \
	fi

# =====================================
# Documentation Targets
# =====================================

# Generate API documentation using lazydocs
.PHONY: docs
docs:
	@echo "Generating API documentation..."
	@$(PYTHON_CMD) src/py/commands/generate_docs.py
	@echo "✓ Documentation generated in docs/api/"

# Serve documentation locally for preview
.PHONY: docs-serve
docs-serve:
	@echo "Starting local documentation server..."
	@command -v python3 >/dev/null 2>&1 && \
		(cd docs && python3 -m http.server 8080) || \
		echo "Python 3 not found. Please install Python 3 to serve docs locally."
	@echo "Documentation served at http://localhost:8080/api/"

# Clean generated documentation
.PHONY: docs-clean
docs-clean:
	@echo "Cleaning generated documentation..."
	@find docs/api -name "*.md" -not -name "README.md" -delete 2>/dev/null || true
	@find docs/api -type d -not -name "api" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Generated documentation cleaned"
