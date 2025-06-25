<!-- markdownlint-disable -->

<a href="https://github.com/henriqueslab/rxiv-maker/blob/main/src/py/scripts/custom_doc_generator.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `custom_doc_generator.py`
Custom documentation generator. 

This script generates markdown documentation for Python modules by inspecting classes, methods, functions and their docstrings. It uses Python's introspection capabilities to extract information and create well-formatted markdown files. 


---

<a href="https://github.com/henriqueslab/rxiv-maker/blob/main/src/py/scripts/custom_doc_generator.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_markdown_doc`

```python
generate_markdown_doc(module_name, module, output_dir)
```

Generate markdown documentation for a module. 



**Args:**
 
 - <b>`module_name`</b>:  The name of the module 
 - <b>`module`</b>:  The module object to document 
 - <b>`output_dir`</b>:  Directory where documentation files will be written 


---

<a href="https://github.com/henriqueslab/rxiv-maker/blob/main/src/py/scripts/custom_doc_generator.py#L88"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `process_directory`

```python
process_directory(dir_path, output_dir, base_package='')
```

Process a directory and its subdirectories for Python modules. 



**Args:**
 
 - <b>`dir_path`</b>:  Path to the directory containing Python modules 
 - <b>`output_dir`</b>:  Directory where documentation files will be written 
 - <b>`base_package`</b>:  Base package name for imports (used for recursion) 


---

<a href="https://github.com/henriqueslab/rxiv-maker/blob/main/src/py/scripts/custom_doc_generator.py#L127"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `main`

```python
main()
```

Main entry point for the documentation generator. 


