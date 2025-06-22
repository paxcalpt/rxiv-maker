#!/usr/bin/env python3
"""Feature comparison visualization for RXiv-Maker vs other authoring tools.

Creates a comprehensive comparison chart showing capabilities across platforms.
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Set style for publication-quality plots
plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("husl")

# Define the comparison data
tools = ["RXiv-Maker", "Overleaf", "Quarto", "Pandoc", "LaTeX Direct", "Word + Zotero"]
features = [
    "Markdown Support",
    "LaTeX Output Quality",
    "Version Control Integration",
    "Collaborative Editing",
    "Reproducible Figures",
    "Cloud Compilation",
    "Learning Curve (Ease)",
    "Template Customisation",
    "Citation Management",
    "Cross-referencing",
    "Docker Support",
    "GitHub Integration",
    "Preprint Focus",
    "Open Source",
]

# Scoring matrix (0-5 scale: 0=Not supported, 5=Excellent)
scores = np.array(
    [
        [5, 4, 5, 3, 5, 3, 4, 4, 4, 4, 5, 5, 5, 5],  # RXiv-Maker
        [3, 5, 2, 5, 2, 5, 3, 5, 4, 5, 2, 3, 3, 3],  # Overleaf
        [5, 4, 4, 3, 4, 3, 3, 4, 4, 4, 3, 4, 3, 5],  # Quarto
        [5, 3, 4, 2, 3, 2, 2, 3, 3, 3, 3, 3, 2, 5],  # Pandoc
        [1, 5, 3, 2, 3, 2, 1, 5, 3, 5, 2, 2, 3, 5],  # LaTeX Direct
        [1, 2, 2, 4, 1, 2, 4, 2, 5, 3, 1, 2, 2, 3],  # Word + Zotero
    ]
)

# Create the visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))

# Main heatmap
im = ax1.imshow(scores.T, cmap="RdYlGn", aspect="auto", vmin=0, vmax=5)

# Set ticks and labels
ax1.set_xticks(np.arange(len(tools)))
ax1.set_yticks(np.arange(len(features)))
ax1.set_xticklabels(tools, rotation=45, ha="right")
ax1.set_yticklabels(features)

# Add text annotations
for i in range(len(tools)):
    for j in range(len(features)):
        score = scores[i, j]
        color = "white" if score < 2.5 else "black"
        ax1.text(
            i,
            j,
            f"{score}",
            ha="center",
            va="center",
            color=color,
            fontweight="bold",
            fontsize=9,
        )

ax1.set_title(
    "Feature Comparison Matrix\nScientific Authoring Tools",
    fontsize=14,
    fontweight="bold",
    pad=20,
)

# Add colorbar
cbar = plt.colorbar(im, ax=ax1, shrink=0.8)
cbar.set_label("Capability Score (0-5)", rotation=270, labelpad=20)

# Radar chart for top 3 tools
categories = [
    "Ease of Use",
    "LaTeX Quality",
    "Reproducibility",
    "Collaboration",
    "Version Control",
    "Automation",
]

# Aggregate scores for radar chart
rxiv_radar = [4.2, 4.5, 4.8, 3.5, 5.0, 4.5]
overleaf_radar = [4.0, 5.0, 2.5, 5.0, 2.0, 3.5]
quarto_radar = [3.2, 4.0, 4.2, 3.0, 4.0, 3.8]

# Radar chart setup
angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
angles = np.concatenate((angles, [angles[0]]))

# Close the radar chart
for data in [rxiv_radar, overleaf_radar, quarto_radar]:
    data.append(data[0])

ax2 = plt.subplot(1, 2, 2, projection="polar")
ax2.plot(angles, rxiv_radar, "o-", linewidth=2, label="RXiv-Maker", color="#2E8B57")
ax2.fill(angles, rxiv_radar, alpha=0.25, color="#2E8B57")
ax2.plot(angles, overleaf_radar, "s-", linewidth=2, label="Overleaf", color="#FF6B35")
ax2.fill(angles, overleaf_radar, alpha=0.25, color="#FF6B35")
ax2.plot(angles, quarto_radar, "^-", linewidth=2, label="Quarto", color="#4682B4")
ax2.fill(angles, quarto_radar, alpha=0.25, color="#4682B4")

ax2.set_xticks(angles[:-1])
ax2.set_xticklabels(categories)
ax2.set_ylim(0, 5)
ax2.set_title(
    "Capability Radar Comparison\nTop 3 Modern Tools",
    fontsize=14,
    fontweight="bold",
    pad=30,
)
ax2.legend(loc="upper right", bbox_to_anchor=(1.3, 1.0))
ax2.grid(True)

# Add grid labels
ax2.set_yticks([1, 2, 3, 4, 5])
ax2.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=8)

plt.tight_layout()

# Add a subtitle with key insights
fig.suptitle(
    "Scientific Authoring Tools: Comprehensive Feature Analysis\n"
    + "RXiv-Maker optimises for simplicity, reproducibility, and preprint workflows",
    fontsize=16,
    fontweight="bold",
    y=0.95,
)

# Save the figure
plt.savefig("SFigure_3.svg", dpi=300, bbox_inches="tight", format="svg")
plt.savefig("SFigure_3.png", dpi=300, bbox_inches="tight", format="png")
plt.savefig("SFigure_3.pdf", dpi=300, bbox_inches="tight", format="pdf")

print("Feature comparison visualization saved as SFigure_3.svg/png/pdf")
