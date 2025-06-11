# Project configuration
PROJECT = main
TEX_DIR = src/tex
BIB_DIR = src/bibliography
FIG_DIR = src/figures
BUILD_DIR = build
OUTPUT_DIR = $(BUILD_DIR)/output
AUX_DIR = $(BUILD_DIR)/aux
LOG_DIR = $(BUILD_DIR)/logs

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
.PHONY: all clean docker-build docker-clean help watch

all: $(OUTPUT_DIR)/$(PROJECT).pdf

help:
	@echo "Available targets:"
	@echo "  all           Build the PDF document"
	@echo "  clean         Remove build artifacts"
	@echo "  docker-build  Build using Docker container"
	@echo "  docker-clean  Clean using Docker container"
	@echo "  watch         Watch for changes and rebuild"
	@echo "  help          Show this help message"

# Create necessary directories
$(BUILD_DIR) $(OUTPUT_DIR) $(AUX_DIR) $(LOG_DIR):
	mkdir -p $@

# Main PDF target with proper dependency handling
$(OUTPUT_DIR)/$(PROJECT).pdf: $(TEX_DIR)/$(PROJECT).tex $(wildcard $(TEX_DIR)/sections/*.tex) $(BIB_DIR)/references.bib $(wildcard $(FIG_DIR)/*.png) $(wildcard $(FIG_DIR)/*.pdf) | $(OUTPUT_DIR) $(AUX_DIR) $(LOG_DIR)
	# Copy necessary files to output directory for proper path resolution
	cp $(TEX_DIR)/style/HenriquesLab_style.bst $(OUTPUT_DIR)/ || true
	cp $(BIB_DIR)/references.bib $(OUTPUT_DIR)/ || true
	$(LATEX_BUILD) $(TEX_DIR)/$(PROJECT).tex
	cd $(OUTPUT_DIR) && $(BIBTEX) $(BIBTEX_FLAGS) $(PROJECT)
	$(LATEX_BUILD) $(TEX_DIR)/$(PROJECT).tex
	$(LATEX_BUILD) $(TEX_DIR)/$(PROJECT).tex
	@echo "PDF built successfully: $(OUTPUT_DIR)/$(PROJECT).pdf"

# Docker-based compilation
docker-build: | $(BUILD_DIR)
	$(DOCKER_RUN) make all

docker-clean:
	$(DOCKER_RUN) make clean

# Watch for changes (requires inotify-tools)
watch:
	while inotifywait -r -e modify,create,delete $(TEX_DIR) $(BIB_DIR) $(FIG_DIR); do \
		make all; \
	done

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR)/*
	@echo "Build artifacts cleaned"

# Development target for quick compilation
quick: | $(OUTPUT_DIR) $(AUX_DIR)
	$(LATEX_BUILD) $(TEX_DIR)/$(PROJECT).tex
