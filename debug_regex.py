#!/usr/bin/env python3

import re

# Test the regex pattern
pattern = r"\\texttt\{((?:[^{}]*(?:\{[^}]*\})*[^{}]*)*)\}"
test_text = r"\texttt{\begin{minted}{python}... \end{minted}}"

print("Test text:")
print(test_text)
print()

matches = re.findall(pattern, test_text, flags=re.DOTALL)
print("Regex matches:")
for i, match in enumerate(matches):
    print(f'Match {i}: "{match}"')
print()


# Test with re.sub
def process_texttt_block(match):
    full_content = match.group(1)
    print(f'Processing texttt block with content: "{full_content}"')

    # If this texttt block contains minted, replace with verb
    if "\\begin{minted}" in full_content:
        print("Contains minted - replacing with verb")
        return f"\\verb|{full_content}|"
    else:
        print("Does not contain minted - keeping as texttt")
        return f"\\texttt{{{full_content}}}"


result = re.sub(pattern, process_texttt_block, test_text, flags=re.DOTALL)
print("Final result:")
print(result)
