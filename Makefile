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

# Colors for output
BOLD := \033[1m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

# Default target
.PHONY: all
all: pdf

# ================================================================
# MAIN TARGETS
# ================================================================

# Build complete PDF (main target)
.PHONY: pdf
pdf: $(OUTPUT_DIR)/ARTICLE.pdf

# Quick development build (LaTeX only, no PDF compilation)
.PHONY: build
build: $(OUTPUT_DIR)/ARTICLE.tex

# Preview in browser (if PDF exists)
.PHONY: preview
preview: $(OUTPUT_DIR)/ARTICLE.pdf
	@open $< || xdg-open $< || echo "$(RED)Cannot open PDF. Please open $(OUTPUT_DIR)/ARTICLE.pdf manually$(RESET)"

# ================================================================
# FILE GENERATION TARGETS
# ================================================================

# Generate the final PDF
$(OUTPUT_DIR)/ARTICLE.pdf: $(OUTPUT_DIR)/ARTICLE.tex $(OUTPUT_DIR)/$(REFERENCES_BIB)
	@printf "$(BOLD)$(GREEN)Compiling LaTeX to PDF...$(RESET)\n"
	@cd $(OUTPUT_DIR) && \
		pdflatex -interaction=nonstopmode ARTICLE.tex > /dev/null && \
		bibtex ARTICLE > /dev/null 2>&1 || true && \
		pdflatex -interaction=nonstopmode ARTICLE.tex > /dev/null && \
		pdflatex -interaction=nonstopmode ARTICLE.tex > /dev/null
	@printf "$(GREEN)✓ PDF ready: $(OUTPUT_DIR)/ARTICLE.pdf$(RESET)\n"

# Generate LaTeX file and copy all dependencies
$(OUTPUT_DIR)/ARTICLE.tex: $(ARTICLE_MD) $(TEMPLATE_FILE) | $(OUTPUT_DIR)
	@printf "$(BOLD)Generating LaTeX from markdown...$(RESET)\n"
	@python3 $(PYTHON_SCRIPT) --output-dir $(OUTPUT_DIR)
	@$(MAKE) --no-print-directory copy-dependencies
	@printf "$(GREEN)✓ LaTeX ready: $(OUTPUT_DIR)/ARTICLE.tex$(RESET)\n"

# Copy bibliography file
$(OUTPUT_DIR)/$(REFERENCES_BIB): $(REFERENCES_BIB) | $(OUTPUT_DIR)
	@cp $< $@

# Create output directory
$(OUTPUT_DIR):
	@mkdir -p $(OUTPUT_DIR)/Figures

# ================================================================
# FIGURE GENERATION
# ================================================================

.PHONY: figures
figures:
	@printf "$(BOLD)Generating figures...$(RESET)\n"
	@python3 $(FIGURE_SCRIPT) --figures-dir $(FIGURES_DIR) --output-dir $(FIGURES_DIR) --format png
	@printf "$(GREEN)✓ Figures generated$(RESET)\n"

# Force figure regeneration before building PDF
.PHONY: pdf-with-figures
pdf-with-figures: figures pdf

# ================================================================
# UTILITY TARGETS
# ================================================================

# Copy all LaTeX dependencies to output directory
.PHONY: copy-dependencies
copy-dependencies:
	@# Copy style files (suppress errors for missing files)
	@find $(STYLE_DIR) -name "*.cls" -o -name "*.bst" -o -name "*.sty" 2>/dev/null | \
		xargs -I {} cp {} $(OUTPUT_DIR)/ 2>/dev/null || true
	@find src/tex -name "*.tex" -not -name "template.tex" -o -name "*.cls" -o -name "*.sty" 2>/dev/null | \
		xargs -I {} cp {} $(OUTPUT_DIR)/ 2>/dev/null || true
	@# Copy figures
	@if [ -d $(FIGURES_DIR) ]; then \
		cp -r $(FIGURES_DIR)/* $(OUTPUT_DIR)/Figures/ 2>/dev/null || true; \
	fi

# ================================================================
# DEVELOPMENT TARGETS
# ================================================================

# Watch for changes and auto-rebuild (requires fswatch: brew install fswatch)
.PHONY: watch
watch:
	@printf "$(BOLD)$(YELLOW)Watching for changes...$(RESET)\n"
	@while true; do \
		$(MAKE) --no-print-directory build; \
		printf "$(YELLOW)Waiting for changes...$(RESET)\n"; \
		fswatch -1 $(ARTICLE_MD) $(REFERENCES_BIB) $(TEMPLATE_FILE) src/ $(FIGURES_DIR) 2>/dev/null || \
		(printf "$(RED)fswatch not found. Install with: brew install fswatch$(RESET)\n" && break); \
		printf "$(YELLOW)Changes detected, rebuilding...$(RESET)\n"; \
	done

# Quick development cycle: figures + build + open PDF
.PHONY: dev
dev: figures build
	@$(MAKE) --no-print-directory preview

# Show current status
.PHONY: status
status:
	@printf "$(BOLD)Article-Forge Status:$(RESET)\n"
	@printf "Source: $(ARTICLE_MD) "
	@[ -f $(ARTICLE_MD) ] && printf "$(GREEN)✓$(RESET)\n" || printf "$(RED)✗$(RESET)\n"
	@printf "Bibliography: $(REFERENCES_BIB) "
	@[ -f $(REFERENCES_BIB) ] && printf "$(GREEN)✓$(RESET)\n" || printf "$(RED)✗$(RESET)\n"
	@printf "Template: $(TEMPLATE_FILE) "
	@[ -f $(TEMPLATE_FILE) ] && printf "$(GREEN)✓$(RESET)\n" || printf "$(RED)✗$(RESET)\n"
	@printf "LaTeX: "
	@pdflatex --version >/dev/null 2>&1 && printf "$(GREEN)✓$(RESET)\n" || printf "$(RED)✗ (run: make install)$(RESET)\n"
	@printf "Python: "
	@python3 --version >/dev/null 2>&1 && printf "$(GREEN)✓$(RESET)\n" || printf "$(RED)✗$(RESET)\n"
	@if [ -f $(OUTPUT_DIR)/ARTICLE.pdf ]; then \
		printf "PDF: $(GREEN)✓ $(OUTPUT_DIR)/ARTICLE.pdf$(RESET)\n"; \
	else \
		printf "PDF: $(YELLOW)Not built$(RESET)\n"; \
	fi

# ================================================================
# INSTALLATION & SETUP
# ================================================================

# Install all dependencies
.PHONY: install
install: install-python install-latex

# Install Python dependencies
.PHONY: install-python
install-python:
	@printf "$(BOLD)Installing Python dependencies...$(RESET)\n"
	@if [ -f pyproject.toml ]; then \
		pip3 install -e . || pip3 install -r requirements.txt 2>/dev/null || \
		printf "$(RED)No requirements.txt found$(RESET)\n"; \
	elif [ -f requirements.txt ]; then \
		pip3 install -r requirements.txt; \
	else \
		printf "$(YELLOW)No Python dependencies file found$(RESET)\n"; \
	fi

# Install LaTeX (macOS with Homebrew)
.PHONY: install-latex
install-latex:
	@printf "$(BOLD)Installing LaTeX...$(RESET)\n"
	@if command -v brew >/dev/null 2>&1; then \
		brew install --cask mactex || brew install --cask basictex; \
		printf "$(GREEN)✓ LaTeX installed$(RESET)\n"; \
	else \
		printf "$(RED)Homebrew not found. Install MacTeX from: https://www.tug.org/mactex/$(RESET)\n"; \
	fi

# ================================================================
# DOCKER TARGETS
# ================================================================

.PHONY: docker-build
docker-build:
	@printf "$(BOLD)Building with Docker...$(RESET)\n"
	@if [ ! -f Dockerfile ]; then $(MAKE) --no-print-directory create-dockerfile; fi
	@docker build -t article-forge .
	@docker run --rm -v "$(PWD)/$(OUTPUT_DIR):/workspace/$(OUTPUT_DIR)" article-forge make pdf
	@printf "$(GREEN)✓ Docker build complete$(RESET)\n"

.PHONY: create-dockerfile
create-dockerfile:
	@printf "$(YELLOW)Creating Dockerfile...$(RESET)\n"
	@echo "FROM texlive/texlive:latest" > Dockerfile
	@echo "WORKDIR /workspace" >> Dockerfile
	@echo "RUN apt-get update && apt-get install -y python3 python3-pip make" >> Dockerfile
	@echo "COPY . ." >> Dockerfile
	@echo "RUN pip3 install -e . 2>/dev/null || true" >> Dockerfile
	@echo 'CMD ["make", "pdf"]' >> Dockerfile
	@printf "$(GREEN)✓ Dockerfile created$(RESET)\n"

# ================================================================
# MAINTENANCE TARGETS
# ================================================================

# Clean output directory
.PHONY: clean
clean:
	@printf "$(BOLD)Cleaning...$(RESET)\n"
	@rm -rf $(OUTPUT_DIR)
	@printf "$(GREEN)✓ Output directory cleaned$(RESET)\n"

# Deep clean (including Docker images)
.PHONY: clean-all
clean-all: clean
	@docker rmi article-forge 2>/dev/null || true
	@printf "$(GREEN)✓ Deep clean complete$(RESET)\n"

# Validate all source files
.PHONY: check
check:
	@printf "$(BOLD)Checking files...$(RESET)\n"
	@errors=0; \
	for file in $(ARTICLE_MD) $(PYTHON_SCRIPT) $(TEMPLATE_FILE); do \
		if [ -f "$$file" ]; then \
			printf "$(GREEN)✓$(RESET) $$file\n"; \
		else \
			printf "$(RED)✗$(RESET) $$file $(RED)(missing)$(RESET)\n"; \
			errors=$$((errors + 1)); \
		fi; \
	done; \
	if [ $$errors -eq 0 ]; then \
		printf "$(GREEN)✓ All files present$(RESET)\n"; \
	else \
		printf "$(RED)✗ $$errors missing files$(RESET)\n"; \
		exit 1; \
	fi

# ================================================================
# HELP & DOCUMENTATION
# ================================================================

.PHONY: help
help:
	@printf "$(BOLD)Article-Forge - Automated LaTeX Article Generation$(RESET)\n\n"
	@printf "$(BOLD)$(GREEN)Main Commands:$(RESET)\n"
	@printf "  $(BOLD)make pdf$(RESET)              Build complete PDF (recommended)\n"
	@printf "  $(BOLD)make build$(RESET)            Generate LaTeX only (faster)\n"
	@printf "  $(BOLD)make preview$(RESET)          Open generated PDF\n"
	@printf "  $(BOLD)make figures$(RESET)          Generate figures from .py/.mmd files\n"
	@printf "  $(BOLD)make pdf-with-figures$(RESET) Regenerate figures and build PDF\n\n"
	@printf "$(BOLD)$(YELLOW)Development:$(RESET)\n"
	@printf "  $(BOLD)make dev$(RESET)              Quick dev cycle (figures + build + preview)\n"
	@printf "  $(BOLD)make watch$(RESET)            Auto-rebuild on file changes\n"
	@printf "  $(BOLD)make status$(RESET)           Show project status\n"
	@printf "  $(BOLD)make check$(RESET)            Validate all source files\n\n"
	@printf "$(BOLD)$(GREEN)Setup:$(RESET)\n"
	@printf "  $(BOLD)make install$(RESET)          Install all dependencies\n"
	@printf "  $(BOLD)make install-python$(RESET)   Install Python dependencies only\n"
	@printf "  $(BOLD)make install-latex$(RESET)    Install LaTeX only\n\n"
	@printf "$(BOLD)$(YELLOW)Docker:$(RESET)\n"
	@printf "  $(BOLD)make docker-build$(RESET)     Build using Docker (no local LaTeX needed)\n\n"
	@printf "$(BOLD)$(RED)Cleanup:$(RESET)\n"
	@printf "  $(BOLD)make clean$(RESET)            Remove output directory\n"
	@printf "  $(BOLD)make clean-all$(RESET)        Deep clean (including Docker images)\n\n"
	@printf "$(BOLD)Examples:$(RESET)\n"
	@printf "  $(YELLOW)make pdf$(RESET)              # Build complete article\n"
	@printf "  $(YELLOW)make dev$(RESET)              # Quick development workflow\n"
	@printf "  $(YELLOW)make watch$(RESET)            # Auto-rebuild during writing\n"
	@printf "  $(YELLOW)make status$(RESET)           # Check what's ready/missing\n\n"
	@printf "Output: $(BOLD)$(OUTPUT_DIR)/ARTICLE.pdf$(RESET)\n"