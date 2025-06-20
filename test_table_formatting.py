#!/usr/bin/env python3

from src.py.converters.md2tex import generate_latex_table

headers = ['Markdown Element', 'LaTeX Equivalent', 'Description']
data_rows = [
    ['`**bold text**`', r'`\textbf{bold text}`', 'Bold formatting for emphasis']
]

result = generate_latex_table(headers, data_rows, 'Test table', 'single', 'test:table')
print(result)