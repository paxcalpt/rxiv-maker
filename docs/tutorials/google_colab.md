# Google Colab Tutorial for Rxiv-Maker

## 🎯 **Overview**

Google Colab provides the easiest way to use Rxiv-Maker without any local installation. This tutorial walks you through the complete process of generating a professional PDF from your Markdown manuscript using only your web browser.

## 🚀 **Quick Start**

### Step 1: Open the Colab Notebook

Click this badge to open Rxiv-Maker in Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/henriqueslab/rxiv-maker/blob/main/rxiv_forge_colab.ipynb)

### Step 2: Runtime Setup

1. **Connect to runtime**: Click "Connect" in the top-right corner
2. **Enable GPU (optional)**: For faster processing, go to `Runtime > Change runtime type > Hardware accelerator > GPU`

## 📝 **Working with Your Manuscript**

### Option A: Use the Example Manuscript

The notebook comes with a pre-configured example manuscript that demonstrates all features. Simply run all cells to see Rxiv-Maker in action.

### Option B: Upload Your Own Manuscript

1. **Prepare your manuscript folder** with this structure:
   ```
   MY_MANUSCRIPT/
   ├── 00_CONFIG.yml         # Paper metadata
   ├── 01_MAIN.md            # Main content
   ├── 02_SUPPLEMENTARY_INFO.md  # Optional
   ├── 03_REFERENCES.bib     # Bibliography
   └── FIGURES/              # Figure scripts and data
       ├── Figure_1.py
       ├── Figure_2.mmd
       └── DATA/             # Data files
   ```

2. **Upload files to Colab**:
   - Click the folder icon in the left sidebar
   - Drag and drop your manuscript folder
   - Or use the upload button to select files

3. **Update the manuscript path** in the notebook:
   ```python
   MANUSCRIPT_PATH = "MY_MANUSCRIPT"  # Change this to your folder name
   ```

## 🛠️ **Step-by-Step Walkthrough**

### Cell 1: Install Dependencies
```python
# Installs LaTeX, Python packages, and Rxiv-Maker
!apt-get update && apt-get install -y texlive-full
!pip install -r requirements.txt
```
**What it does**: Sets up the complete LaTeX environment and Python dependencies.

### Cell 2: Clone Repository
```python
# Downloads the latest Rxiv-Maker code
!git clone https://github.com/henriqueslab/rxiv-maker.git
%cd rxiv-maker
```
**What it does**: Gets the Rxiv-Maker codebase and navigates to the project directory.

### Cell 3: Generate PDF
```python
# Main command that builds your PDF
!make pdf MANUSCRIPT_PATH=EXAMPLE_MANUSCRIPT
```
**What it does**: Converts your Markdown to LaTeX, generates figures, and compiles the final PDF.

### Cell 4: Download Results
```python
# Downloads the generated PDF to your computer
from google.colab import files
files.download('output/EXAMPLE_MANUSCRIPT.pdf')
```
**What it does**: Saves the finished PDF to your Downloads folder.

## 📊 **Working with Figures**

### Python Figure Scripts

Create Python scripts in your `FIGURES/` folder:

```python
# FIGURES/Figure_1.py
import matplotlib.pyplot as plt
import numpy as np

# Your plotting code here
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('My Figure')

# Save in both formats (required)
plt.savefig('output/Figures/Figure_1.pdf')  # For LaTeX
plt.savefig('output/Figures/Figure_1.png')  # For preview
plt.close()
```

### Mermaid Diagrams

Create `.mmd` files for diagrams:

```mermaid
# FIGURES/Figure_2.mmd
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process]
    B -->|No| D[End]
    C --> D
```

## 📚 **Manuscript Configuration**

### Basic Config (`00_CONFIG.yml`)
```yaml
title: "Your Paper Title"
date: "2024-12-13"
authors:
  - name: "Your Name"
    affiliation: "Your Institution"
    email: "your.email@institution.edu"
    orcid: "0000-0000-0000-0000"
keywords: ["keyword1", "keyword2", "keyword3"]
bibliography: "03_REFERENCES.bib"
```

### Enhanced Markdown Syntax (`01_MAIN.md`)
```markdown
# Introduction

This paper presents...

![My analysis](FIGURES/Figure_1.py){#fig:analysis width="0.8"}

As shown in @fig:analysis, our results demonstrate...

Multiple citations can be included [@ref1;@ref2] or single citations @ref3.
```

## 🔧 **Troubleshooting**

### Common Issues and Solutions

#### ❌ "No module named 'X'"
**Solution**: Add the missing package to the installation cell:
```python
!pip install package_name
```

#### ❌ "Figure generation failed"
**Solutions**:
- Check your Python script syntax
- Ensure data files are in the correct `FIGURES/DATA/` subdirectory
- Verify file paths are relative to the `FIGURES/` directory

#### ❌ "LaTeX compilation error"
**Solutions**:
- Check the LaTeX log in `output/MANUSCRIPT.log`
- Ensure special characters are properly escaped
- Verify bibliography file format

#### ❌ "File not found"
**Solutions**:
- Check file paths and names match exactly
- Ensure files are uploaded to the correct directories
- Use the file browser to verify file locations

### Debug Mode
Add this cell to enable verbose output:
```python
# Enable debug mode for detailed output
!make pdf MANUSCRIPT_PATH=YOUR_MANUSCRIPT VERBOSE=true
```

## 💡 **Pro Tips**

### Efficient Workflow
1. **Start with the example**: Modify the example manuscript rather than starting from scratch
2. **Test incrementally**: Generate PDF after each major change to catch issues early
3. **Use simple figures first**: Start with basic plots before complex visualizations
4. **Check file paths**: Use relative paths within your manuscript structure

### Collaboration
1. **Share notebooks**: Use Colab's sharing features for team collaboration
2. **Version control**: Download and commit your manuscript files to Git
3. **Export options**: Save notebooks to GitHub or Google Drive for backup

### Performance Optimization
1. **Reuse runtime**: Keep the same runtime session for multiple builds
2. **Cache data**: Store large datasets in Colab's temporary storage
3. **Minimize uploads**: Only upload files that have changed

## 📥 **Downloading Your Work**

### Download Individual Files
```python
# Download specific files
files.download('output/MANUSCRIPT.pdf')
files.download('output/MANUSCRIPT.log')  # For debugging
```

### Download Everything
```python
# Create and download a zip file with all outputs
!zip -r output.zip output/
files.download('output.zip')
```

## 🔄 **Next Steps**

Once you're comfortable with Colab:

1. **Consider GitHub Actions**: For automated PDF generation on every change
2. **Local installation**: If you need more control or work offline frequently
3. **Advanced features**: Explore custom LaTeX styling and complex figure generation

## 🆘 **Getting Help**

- **Issues**: Report problems at [GitHub Issues](https://github.com/henriqueslab/rxiv-maker/issues)
- **Discussions**: Ask questions at [GitHub Discussions](https://github.com/henriqueslab/rxiv-maker/discussions)
- **Documentation**: Check the [User Guide](../user_guide.md) for detailed information

---

**Happy writing! 🎉 Your research deserves beautiful presentation.**