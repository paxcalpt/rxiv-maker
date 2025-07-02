# Troubleshooting: Missing Figure Files

## Problem: PDF Generation Fails Due to Missing PNG Files

### Symptoms
- `make pdf` fails with validation errors
- Error messages like: "Figure file not found: FIGURES/example_figure/example_figure.png"
- The validation shows missing PNG files in MANUSCRIPT/FIGURES/ subdirectories

### Root Cause
The repository tracks generated PNG files alongside their Python generation scripts. If these PNG files are accidentally deleted (e.g., by `make clean`, manual deletion, or git operations), the build process will fail because the LaTeX compilation expects these files to exist.

## ✅ Automatic Solution (Recommended)

**As of the latest version, `make pdf` automatically detects and runs Python figure generation scripts!**

Simply run:
```bash
make pdf
```

The build system will:
1. **Auto-detect missing figures** - Check if PNG/PDF files exist for each Python script
2. **Execute Python scripts** - Automatically run `example_figure.py`, `supplementary_figure.py`, etc.
3. **Generate missing files** - Create both PNG and PDF versions
4. **Continue with PDF build** - Proceed with LaTeX compilation

### Manual Solution (If Needed)
If you need to regenerate figures manually:

```bash
# Navigate to the FIGURES directory
cd MANUSCRIPT/FIGURES

# Activate the virtual environment
source ../../.venv/bin/activate

# Run the figure generation scripts
python example_figure.py
python supplementary_figure.py

# Return to project root and test the build
cd ../..
make pdf
```

### Advanced Figure Generation
For more control, you can use the dedicated figure generation command:

```bash
# Generate all figures automatically (Mermaid + Python)
source .venv/bin/activate
python src/py/commands/generate_figures.py --figures-dir MANUSCRIPT/FIGURES --verbose

# Force regenerate all figures even if they exist
make pdf FORCE_FIGURES=true
```

### How It Works
The enhanced build system automatically:
- **Detects Python scripts** (`.py` files) in the FIGURES directory
- **Checks for corresponding outputs** (PNG and PDF files in subdirectories)
- **Runs missing scripts** using the project's Python environment
- **Handles both Mermaid diagrams** (`.mmd` files) and Python scripts

### Prevention
- The `make clean` command removes generated figures, but `make pdf` will automatically regenerate them
- When cloning the repository, missing figures will be auto-generated on first build
- The build process is now robust against missing figure files

### Why PNG Files Are Still Tracked
Even with automatic generation, PNG files remain tracked in git because:
- They ensure reproducible builds across different environments
- Not all users have Python dependencies needed for figure generation
- They provide immediate availability without requiring script execution
- They serve as fallbacks when figure generation environments differ