# Troubleshooting: Missing Figure Files

## Problem: PDF Generation Fails Due to Missing PNG Files

### Symptoms
- `make pdf` fails with validation errors
- Error messages like: "Figure file not found: FIGURES/example_figure/example_figure.png"
- The validation shows missing PNG files in MANUSCRIPT/FIGURES/ subdirectories

### Root Cause
The repository tracks generated PNG files alongside their Python generation scripts. If these PNG files are accidentally deleted (e.g., by `make clean`, manual deletion, or git operations), the build process will fail because the LaTeX compilation expects these files to exist.

### Solution
Regenerate the missing PNG files by running the corresponding Python scripts:

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

### Prevention
- The `make clean` command removes generated figures, so always run `make pdf` (not just `make validate`) after cleaning
- When cloning the repository, ensure all tracked PNG files are properly downloaded
- If using figure generation scripts, understand that their outputs are tracked in git

### Automated Figure Generation
For a more robust solution, you can use the built-in figure generation command:

```bash
# Generate all figures automatically
source .venv/bin/activate
python src/py/commands/generate_figures.py --figures-dir MANUSCRIPT/FIGURES --verbose
```

### Why PNG Files Are Tracked
Unlike typical development practices where generated files are ignored, Rxiv-Maker tracks the generated PNG files because:
- They ensure reproducible builds across different environments
- Not all users have the Python dependencies needed for figure generation
- LaTeX compilation requires these files to exist
- They serve as fallbacks when figure generation scripts fail