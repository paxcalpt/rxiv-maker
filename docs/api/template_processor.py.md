<!-- markdownlint-disable -->

<a href="../../src/py/processors/template_processor.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `template_processor.py`
Template processing utilities for RXiv-Maker. 

This module handles template content generation and replacement operations. 


---

<a href="../../src/py/processors/template_processor.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_template_path`

```python
get_template_path()
```

Get the path to the template file. 


---

<a href="../../src/py/processors/template_processor.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `find_supplementary_md`

```python
find_supplementary_md()
```

Find supplementary information file in the manuscript directory. 


---

<a href="../../src/py/processors/template_processor.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_supplementary_cover_page`

```python
generate_supplementary_cover_page(yaml_metadata)
```

Generate LaTeX code for the supplementary information cover page. 


---

<a href="../../src/py/processors/template_processor.py#L88"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_supplementary_tex`

```python
generate_supplementary_tex(output_dir, yaml_metadata=None)
```

Generate Supplementary.tex file from supplementary markdown. 


---

<a href="../../src/py/processors/template_processor.py#L213"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_keywords`

```python
generate_keywords(yaml_metadata)
```

Generate LaTeX keywords section from YAML metadata. 


---

<a href="../../src/py/processors/template_processor.py#L230"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_bibliography`

```python
generate_bibliography(yaml_metadata)
```

Generate LaTeX bibliography section from YAML metadata. 


---

<a href="../../src/py/processors/template_processor.py#L241"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `count_words_in_text`

```python
count_words_in_text(text)
```

Count words in text, excluding LaTeX commands. 


---

<a href="../../src/py/processors/template_processor.py#L255"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `analyze_section_word_counts`

```python
analyze_section_word_counts(content_sections)
```

Analyze word counts for each section and provide warnings. 


---

<a href="../../src/py/processors/template_processor.py#L319"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `process_template_replacements`

```python
process_template_replacements(template_content, yaml_metadata, article_md)
```

Process all template replacements with metadata and content. 


