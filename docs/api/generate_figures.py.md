<!-- markdownlint-disable -->

<a href="https://github.com/henriqueslab/rxiv-maker/blob/main/src/py/commands/generate_figures.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `generate_figures.py`
Figure Generation Script for Rxiv-Maker. 

This script automatically processes figure files in the FIGURES directory and generates publication-ready output files. It supports: 
- .mmd files: Mermaid diagrams (generates SVG/PNG/PDF) 
- .py files: Python scripts for matplotlib/seaborn figures 

Usage:  python generate_figures.py [--output-dir OUTPUT_DIR] [--format FORMAT] 


---

<a href="https://github.com/henriqueslab/rxiv-maker/blob/main/src/py/commands/generate_figures.py#L334"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `main`

```python
main()
```

Main function with command-line interface. 


---

## <kbd>class</kbd> `FigureGenerator`
Main class for generating figures from various source formats. 

<a href="https://github.com/henriqueslab/rxiv-maker/blob/main/src/py/commands/generate_figures.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(figures_dir='FIGURES', output_dir='FIGURES', output_format='png')
```

Initialize the figure generator. 



**Args:**
 
 - <b>`figures_dir`</b>:  Directory containing source figure files 
 - <b>`output_dir`</b>:  Directory for generated output files 
 - <b>`output_format`</b>:  Default output format for figures 




---

<a href="https://github.com/henriqueslab/rxiv-maker/blob/main/src/py/commands/generate_figures.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `generate_all_figures`

```python
generate_all_figures()
```

Generate all figures found in the figures directory. 

---

<a href="https://github.com/henriqueslab/rxiv-maker/blob/main/src/py/commands/generate_figures.py#L84"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `generate_mermaid_figure`

```python
generate_mermaid_figure(mmd_file)
```

Generate figure from Mermaid diagram file. 

---

<a href="https://github.com/henriqueslab/rxiv-maker/blob/main/src/py/commands/generate_figures.py#L154"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `generate_python_figure`

```python
generate_python_figure(py_file)
```

Generate figure from Python script. 


