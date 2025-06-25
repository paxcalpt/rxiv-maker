# GitHub Actions Tutorial for Rxiv-Maker

## 🎯 **Overview**

GitHub Actions provides automated PDF generation for Rxiv-Maker manuscripts. Every time you push changes to your repository, GitHub automatically builds your PDF and makes it available for download. This tutorial covers everything from basic setup to advanced workflows.

## 🚀 **Quick Setup (5 Minutes)**

### Step 1: Fork the Repository

1. Go to [https://github.com/henriqueslab/rxiv-maker](https://github.com/henriqueslab/rxiv-maker)
2. Click the **"Fork"** button in the top-right corner
3. Choose your GitHub account as the destination

### Step 2: Enable Actions (If Needed)

- **Public repositories**: Actions are enabled by default
- **Private repositories**: Go to `Settings > Actions > General` and enable Actions

### Step 3: Add Your Manuscript

1. **Navigate** to your forked repository
2. **Edit files** directly in GitHub's web interface, or clone locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/rxiv-maker.git
   cd rxiv-maker
   ```
3. **Modify the manuscript** in the `MANUSCRIPT/` folder:
   - Edit `MANUSCRIPT/00_CONFIG.yml` with your paper details
   - Write your content in `MANUSCRIPT/01_MAIN.md`
   - Add references to `MANUSCRIPT/03_REFERENCES.bib`
   - Add figures to `MANUSCRIPT/FIGURES/`

### Step 4: Trigger PDF Generation

**Option A: Direct editing on GitHub**
1. Click on any file in `MANUSCRIPT/`
2. Click the pencil icon to edit
3. Make your changes
4. Scroll down and click "Commit changes"
5. PDF generation starts automatically!

**Option B: Local editing and push**
```bash
# Make your changes locally
git add .
git commit -m "Update manuscript content"
git push origin main
```

### Step 5: Download Your PDF

1. Go to the **"Actions"** tab in your repository
2. Click on the latest workflow run
3. Scroll down to **"Artifacts"** section
4. Download `manuscript-pdf` 

## 📋 **Detailed Workflow Guide**

### Understanding the Build Process

When you push changes, GitHub Actions automatically:

1. **🔧 Sets up environment** (Ubuntu + LaTeX + Python)
2. **📦 Installs dependencies** (cached for speed)
3. **🖼️ Generates figures** (Python scripts + Mermaid diagrams)
4. **📄 Converts Markdown** to LaTeX
5. **🏗️ Compiles PDF** using pdflatex
6. **📤 Creates artifacts** (downloadable PDF)
7. **🚀 Makes releases** (on tags)

### Build Status and Monitoring

#### Check Build Status
- **Green checkmark** ✅: Build successful, PDF ready
- **Red X** ❌: Build failed, check logs
- **Yellow circle** 🟡: Build in progress
- **Gray dash** ⚪: Build queued or skipped

#### View Build Logs
1. Go to **"Actions"** tab
2. Click on the workflow run
3. Click on **"Build PDF"** job
4. Expand sections to see detailed logs

## 🛠️ **Advanced Configuration**

### Custom Manuscript Paths

Use different manuscript folders for multiple projects:

#### Method 1: Manual Trigger
1. Go to **"Actions"** tab
2. Click **"Build PDF"** workflow
3. Click **"Run workflow"**
4. Enter custom path (e.g., `MY_PROJECT_A`)
5. Click **"Run workflow"**

#### Method 2: Environment Variables
Add to your repository settings (`Settings > Secrets and variables > Actions`):
```
MANUSCRIPT_PATH = MY_PROJECT_A
```

### Multiple Manuscripts in One Repository

Create separate folders for different projects:
```
├── PROJECT_A/
│   ├── 00_CONFIG.yml
│   ├── 01_MAIN.md
│   └── FIGURES/
├── PROJECT_B/
│   ├── 00_CONFIG.yml
│   ├── 01_MAIN.md
│   └── FIGURES/
└── MANUSCRIPT/  # Default folder
```

Build specific projects using manual triggers with custom paths.

### Automated Releases

The workflow automatically creates releases when you:

1. **Create a tag**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **GitHub creates a release** with:
   - Timestamped PDF file
   - Release notes
   - Downloadable assets

### Branch-Based Workflows

#### Development Workflow
```bash
# Create feature branch
git checkout -b draft/my-paper-v2
# Make changes
git add . && git commit -m "Add methodology section"
git push origin draft/my-paper-v2
# Create pull request → automatic PDF generation for review
```

#### Review Process
1. **Pull requests** trigger PDF generation
2. **Reviewers** can download PDFs from PR Actions
3. **Merge** to main when ready

## 📊 **Working with Figures in Actions**

### Python Figure Scripts

Your Python scripts run automatically during the build:

```python
# FIGURES/Figure_1.py
import matplotlib.pyplot as plt
import pandas as pd

# Read data (use relative paths)
data = pd.read_csv('FIGURES/DATA/my_data.csv')

# Create plot
plt.figure(figsize=(8, 6))
plt.plot(data['x'], data['y'])
plt.xlabel('X Label')
plt.ylabel('Y Label')
plt.title('My Analysis')

# Save both formats (required)
plt.savefig('output/Figures/Figure_1.pdf')  # For LaTeX
plt.savefig('output/Figures/Figure_1.png')  # For preview
plt.close()
```

### Data Files

Store data in `FIGURES/DATA/` subdirectories:
```
FIGURES/
├── Figure_1.py
├── Figure_2.mmd
└── DATA/
    ├── figure1_data/
    │   └── results.csv
    └── figure2_data/
        └── measurements.json
```

### External Dependencies

Add Python packages to `requirements.txt`:
```txt
matplotlib>=3.5.0
seaborn>=0.11.0
pandas>=1.3.0
numpy>=1.21.0
your_custom_package>=1.0.0
```

## 🔒 **Private Repository Features**

### Security and Privacy

- **Code stays private**: Your manuscript never leaves GitHub
- **Secure builds**: Actions run in isolated environments
- **Access control**: Team members need repository access
- **Audit logs**: Full history of builds and changes

### Team Collaboration

#### Team Member Workflow
```bash
# Clone the shared repository
git clone https://github.com/TEAM_REPO/manuscript-project.git
cd manuscript-project

# Create your branch
git checkout -b feature/my-section

# Make changes and push
git add . && git commit -m "Add my contributions"
git push origin feature/my-section

# Create pull request for review
```

#### Review and Merge Process
1. **Authors** push changes to feature branches
2. **Pull requests** trigger automatic PDF generation
3. **Reviewers** download PDFs from PR Actions
4. **Team lead** merges approved changes
5. **Final PDF** generated on main branch

### Access Management

#### Repository Permissions
- **Read**: Download PDFs, view source
- **Write**: Edit manuscript, trigger builds
- **Admin**: Manage settings, add collaborators

#### Secrets Management
Store sensitive data in repository secrets:
- API keys for data sources
- Custom configuration values
- Authentication tokens

## 🐛 **Troubleshooting**

### Common Issues and Solutions

#### ❌ **Build Failed: LaTeX Error**
**Symptoms**: Red X in Actions, PDF not generated

**Solutions**:
1. **Check the logs**:
   - Go to Actions → Failed build → Build PDF
   - Look for LaTeX error messages
2. **Common fixes**:
   - Escape special characters: `\&`, `\%`, `\#`, `\$`
   - Check bibliography syntax
   - Verify figure file paths

#### ❌ **Build Failed: Python Error**
**Symptoms**: Figure generation fails

**Solutions**:
1. **Check Python script syntax** locally first
2. **Verify data file paths** are relative to `FIGURES/`
3. **Add missing packages** to `requirements.txt`
4. **Check data file formats** and encoding

#### ❌ **Build Timeout**
**Symptoms**: Build stops after 6 hours

**Solutions**:
1. **Optimize figure generation** (reduce data size, simplify plots)
2. **Split large manuscripts** into smaller documents
3. **Use image files** instead of generating complex figures

#### ❌ **No Artifacts Available**
**Symptoms**: Build succeeds but no PDF to download

**Solutions**:
1. **Check build logs** for artifact upload errors
2. **Verify PDF was generated** in the logs
3. **Re-run the workflow** (temporary GitHub issue)

### Debug Mode

Enable verbose logging by adding to your commit message:
```
Update manuscript [debug]
```

Or manually trigger with debug enabled in the workflow interface.

### Getting Detailed Logs

1. **Download logs**: Actions → Workflow run → Download logs
2. **Search logs**: Use browser search for error keywords
3. **LaTeX log**: Check the uploaded `manuscript.log` artifact

## 📈 **Performance Optimization**

### Build Speed Tips

1. **Use caching**: Dependencies are cached automatically
2. **Optimize figures**: 
   - Use vector formats when possible
   - Avoid unnecessary data processing
   - Cache intermediate results
3. **Incremental builds**: Only changed figures are regenerated

### Resource Management

#### GitHub Actions Limits
- **Free tier**: 2,000 minutes/month
- **Typical build time**: 5-15 minutes
- **Concurrent jobs**: 20 for free accounts
- **Storage**: 500MB for free accounts

#### Best Practices
- **Use draft mode** for quick previews
- **Batch changes** instead of frequent small commits
- **Clean up old artifacts** to save storage space

## 🔄 **Integration with Other Tools**

### Git Hooks

Set up pre-commit hooks for local validation:

```bash
# .git/hooks/pre-commit
#!/bin/bash
# Validate manuscript before commit
python scripts/validate_manuscript.py
```

### External Tools

#### Overleaf Integration
1. Export LaTeX from Rxiv-Maker
2. Import to Overleaf for collaborative editing
3. Export back to Markdown for final processing

#### Reference Managers
- **Zotero**: Export to BibTeX format
- **Mendeley**: Sync bibliography files
- **EndNote**: Convert to BibTeX

### Notifications

#### Email Notifications
1. Go to **"Watch"** → **"Custom"**
2. Select **"Actions"** notifications
3. Choose email frequency

#### Slack/Discord Integration
Use GitHub Apps to send notifications to team channels when builds complete.

## 📊 **Analytics and Monitoring**

### Build Analytics

Track your manuscript development:
- **Build frequency**: How often you're iterating
- **Build duration**: Performance trends
- **Success rate**: Quality metrics
- **File sizes**: Growth over time

### Usage Monitoring

Monitor GitHub Actions usage:
1. Go to **"Settings"** → **"Billing"**
2. Check **"Actions"** usage
3. Set up **"Spending limits"** if needed

## 🎯 **Best Practices**

### Manuscript Organization

```
MANUSCRIPT/
├── 00_CONFIG.yml           # Paper metadata
├── 01_MAIN.md             # Main content
├── 02_SUPPLEMENTARY_INFO.md # Supplementary material
├── 03_REFERENCES.bib      # Bibliography
├── FIGURES/               # All figures
│   ├── Figure_1.py        # Python plots
│   ├── Figure_2.mmd       # Mermaid diagrams
│   ├── Figure_3.png       # Static images
│   └── DATA/              # Data files
│       ├── figure1/       # Organized by figure
│       └── figure2/
└── TABLES/                # Table data (optional)
```

### Commit Message Conventions

Use clear, descriptive commit messages:
```bash
git commit -m "Add methodology section and Figure 2"
git commit -m "Fix citation formatting in results"
git commit -m "Update author affiliations"
git commit -m "Final revision for submission"
```

### Version Control Strategy

1. **Main branch**: Production-ready manuscript
2. **Feature branches**: Individual sections or major changes
3. **Tags**: Mark important milestones (submissions, revisions)
4. **Releases**: Final versions for distribution

## 🆘 **Getting Help**

### Documentation Resources
- **[User Guide](../user_guide.md)**: Comprehensive Rxiv-Maker documentation
- **[Architecture](../architecture.md)**: Technical details
- **[Local Development](../platforms/LOCAL_DEVELOPMENT.md)**: Local setup instructions

### Community Support
- **[GitHub Issues](https://github.com/henriqueslab/rxiv-maker/issues)**: Bug reports and feature requests
- **[GitHub Discussions](https://github.com/henriqueslab/rxiv-maker/discussions)**: Questions and community help
- **[GitHub Actions Documentation](https://docs.github.com/en/actions)**: Official GitHub Actions docs

### Professional Support
For institutional or commercial use:
- **Consulting**: Custom workflow development
- **Training**: Team workshops and tutorials
- **Support**: Priority issue resolution

---

**🎉 Congratulations! You now have automated PDF generation for your scientific manuscripts. Focus on your research while GitHub takes care of the typesetting!**