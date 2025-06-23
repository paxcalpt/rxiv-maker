#!/usr/bin/env python3

import os
import sys

# Add the parent directory (src/py) to the path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from converters.text_formatters import escape_special_characters, process_code_spans

# Test the conversion flow step by step
original_text = r"`\begin{minted}{python}... \end{minted}`"
print("Original text:")
print(original_text)

# Step 1: process_code_spans
after_code_spans = process_code_spans(original_text)
print("After process_code_spans:")
print(after_code_spans)

# Step 2: escape_special_characters
after_escape = escape_special_characters(after_code_spans)
print("After escape_special_characters:")
print(after_escape)
