<!-- markdownlint-disable -->

<a href="../../src/py/utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.py`
Utility functions for RXiv-Maker. 

This module contains general utility functions used across the RXiv-Maker system. 


---

<a href="../../src/py/utils.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create_output_dir`

```python
create_output_dir(output_dir)
```

Create output directory if it doesn't exist. 


---

<a href="../../src/py/utils.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `find_manuscript_md`

```python
find_manuscript_md()
```

Look for manuscript main file in the manuscript directory. 


---

<a href="../../src/py/utils.py#L46"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `write_manuscript_output`

```python
write_manuscript_output(output_dir, template_content)
```

Write the generated manuscript to the output directory. 


---

<a href="../../src/py/utils.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_custom_pdf_filename`

```python
get_custom_pdf_filename(yaml_metadata)
```

Generate custom PDF filename from metadata. 


---

<a href="../../src/py/utils.py#L90"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `copy_pdf_to_manuscript_folder`

```python
copy_pdf_to_manuscript_folder(output_dir, yaml_metadata)
```

Copy generated PDF to manuscript folder with custom filename. 


---

<a href="../../src/py/utils.py#L114"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `copy_pdf_to_base`

```python
copy_pdf_to_base(output_dir, yaml_metadata)
```

Backward compatibility function - delegates to copy_pdf_to_manuscript_folder. 


