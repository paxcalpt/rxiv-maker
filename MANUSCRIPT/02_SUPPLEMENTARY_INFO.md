# Supplementary Information

## Supplementary Tables

| Markdown Element | LaTeX Output | Description |
|------------------|--------------|-------------|
| `**bold text**` | `\textbf{bold text}` | Bold formatting |
| `*italic text*` | `\textit{italic text}` | Italic formatting |
| `@citation` | `\cite{citation}` | Single citation |
| `[@cite1;@cite2]` | `\cite{cite1,cite2}` | Multiple citations |
| `@fig:label` | `\ref{fig:label}` | Figure reference |

{#stable:syntax} **RXiv-Maker Syntax Examples.** Basic markdown-to-LaTeX conversion examples showing the essential syntax transformations.

| Deployment Method | Environment | Setup Required | Ease of Use |
|-------------------|-------------|----------------|-------------|
| Docker | Local/Cloud | Docker only | High |
| GitHub Actions | Cloud CI/CD | None | Very High |
| Local Python | Local | Python + LaTeX | Medium |

{#stable:deployment} **Deployment Options.** Comparison of different ways to use RXiv-Maker.

## Supplementary Notes

{#snote:examples} **Usage Examples and Best Practices.**

This supplementary note demonstrates the special syntax for creating structured supplementary content. The `{#snote:id}` syntax creates automatically numbered and labeled supplementary notes that can be cross-referenced from the main text.

Key best practices include:
- Use clear, descriptive labels for all figures and tables
- Include comprehensive captions that explain the content
- Cross-reference supplementary materials from the main text
- Organize supplementary content logically

{#snote:advanced-features} **Advanced RXiv-Maker Features.**

The framework supports several advanced features beyond basic markdown conversion:

**Mathematical notation**: Both inline math $E = mc^2$ and display equations:
$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$

**Code syntax highlighting**: Python, R, and other languages are automatically highlighted when specified:

```python
import pandas as pd
data = pd.read_csv("input.csv")
print(data.head())
```

**Custom LaTeX commands**: Direct LaTeX code can be included when needed for specialized formatting requirements.

## Supplementary Figures

<!-- Supplementary figures would be referenced here with SFigure labels -->