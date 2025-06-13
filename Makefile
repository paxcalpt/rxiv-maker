# Article-Forge Makefile
# Automated LaTeX article generation and building

# Configuration
OUTPUT_DIR := output
FIGURES_DIR := FIGURES
STYLE_DIR := src/tex/style
PYTHON_SCRIPT := src/py/commands/generate_article.py
FIGURE_SCRIPT := src/py/commands/generate_figures.py
TEMPLATE_FILE := src/tex/template.tex
ARTICLE_MD := 00_ARTICLE.md
REFERENCES_BIB := 02_REFERENCES.bib
SUPPLEMENTARY_MD := 01_SUPPLEMENTARY_INFO.md

# Default target
.PHONY: all
all: build

# Convenience aliases for Docker commands
.PHONY: easy-setup
easy-setup: docker-setup

.PHONY: easy-build
easy-build: docker-build

# Create output directory and generate LaTeX files
.PHONY: setup
setup:
	@echo "Setting up output directory..."
	@mkdir -p $(OUTPUT_DIR)
	@mkdir -p $(OUTPUT_DIR)/Figures
	@echo "Output directory created: $(OUTPUT_DIR)"

# Generate figures from .mmd and .py files (conditional)
.PHONY: figures
figures:
	@if [ "$(FORCE_FIGURES)" = "true" ]; then \
		echo "Generating figures from $(FIGURES_DIR)..."; \
		python3 $(FIGURE_SCRIPT) --figures-dir $(FIGURES_DIR) --output-dir $(FIGURES_DIR) --format png; \
		echo "Figure generation complete"; \
	else \
		echo "Skipping figure generation (use 'make pdf FORCE_FIGURES=true' or 'make figures' to regenerate)"; \
	fi

# Force figure generation
.PHONY: force-figures
force-figures:
	@echo "Forcing figure generation from $(FIGURES_DIR)..."
	@python3 $(FIGURE_SCRIPT) --figures-dir $(FIGURES_DIR) --output-dir $(FIGURES_DIR) --format png
	@echo "Figure generation complete"

# Generate the ARTICLE.tex file
.PHONY: generate
generate: setup figures
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

# Docker commands (using new src/docker structure)
.PHONY: docker-setup
docker-setup:
	@echo "Setting up Docker environment..."
	@./src/docker/setup.sh

.PHONY: docker-build
docker-build:
	@echo "Building PDF using Docker..."
	@./src/docker/run.sh

.PHONY: docker-dev
docker-dev:
	@echo "Starting Docker development mode..."
	@./src/docker/dev.sh

.PHONY: docker-shell
docker-shell:
	@echo "Opening Docker interactive shell..."
	@./src/docker/shell.sh

.PHONY: docker-force-figures
docker-force-figures:
	@echo "Building PDF with forced figure regeneration..."
	@./src/docker/run.sh --force-figures

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
		echo "Waiting for changes to $(ARTICLE_MD), $(REFERENCES_BIB), or $(TEMPLATE_FILE)..."; \
		fswatch -1 $(ARTICLE_MD) $(REFERENCES_BIB) $(TEMPLATE_FILE) src/; \
		echo "Changes detected, rebuilding..."; \
	done

# Show help
.PHONY: help
help:
	@echo "Article-Forge Makefile Commands:"
	@echo ""
	@echo "Local Commands (require LaTeX installation):"
	@echo "  make build           - Generate ARTICLE.tex and copy all necessary files"
	@echo "  make figures         - Generate figures only if FORCE_FIGURES=true"
	@echo "  make force-figures   - Always regenerate figures from .mmd and .py files"
	@echo "  make pdf             - Build complete LaTeX document and compile to PDF"
	@echo "  make pdf FORCE_FIGURES=true - Build PDF and force figure regeneration"
	@echo "  make clean           - Remove output directory"
	@echo "  make install-deps    - Install Python dependencies"
	@echo "  make install-system-deps - Install LaTeX (macOS with Homebrew)"
	@echo "  make watch           - Watch for changes and rebuild automatically"
	@echo ""
	@echo "Docker Commands (no local LaTeX needed):"
	@echo "  make docker-setup    - Set up Docker environment (first time only)"
	@echo "  make docker-build    - Build PDF using Docker"
	@echo "  make docker-force-figures - Build PDF with forced figure regeneration"
	@echo "  make docker-dev      - Start development mode with auto-rebuild"
	@echo "  make docker-shell    - Open interactive Docker shell"
	@echo ""
	@echo "Easy Commands (aliases for non-programmers):"
	@echo "  make easy-setup      - Same as docker-setup"
	@echo "  make easy-build      - Same as docker-build"
	@echo ""
	@echo "  make help            - Show this help message"
	@echo "  make check           - Check if required files exist"
	@echo ""
	@echo "Figure generation options:"
	@echo "  - Default: Figures are NOT regenerated during 'make pdf'"
	@echo "  - Force:   Use 'make pdf FORCE_FIGURES=true' to regenerate figures"
	@echo "  - Manual:  Use 'make force-figures' to only regenerate figures"
	@echo ""
	@echo "Output directory: $(OUTPUT_DIR)"
	@echo ""
	@echo "🚀 New to Article-Forge? Run 'make easy-setup' to get started!"
	@echo "   Then use 'make easy-build' to generate your PDF."

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