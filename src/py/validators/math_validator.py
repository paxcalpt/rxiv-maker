"""Mathematical expression validator for checking LaTeX math syntax."""

import re
import os
from typing import List, Dict, Optional, Set, Tuple
from .base_validator import BaseValidator, ValidationResult, ValidationLevel


class MathValidator(BaseValidator):
    """Validates mathematical expressions and LaTeX math syntax."""
    
    # Math patterns based on codebase analysis
    MATH_PATTERNS = {
        'inline_math': re.compile(r'\$([^$]+)\$'),                           # $...$
        'display_math': re.compile(r'\$\$([^$]+)\$\$'),                     # $$...$$
        'attributed_math': re.compile(r'\$\$(.*?)\$\$\s*\{([^}]*#[^}]*)\}'), # $$...$${#eq:label}
        'environment_math': re.compile(r'\\begin\{([^}]+)\}.*?\\end\{\1\}', re.DOTALL)
    }
    
    # Valid LaTeX math environments
    VALID_ENVIRONMENTS = {
        'equation', 'align', 'gather', 'multiline', 'split',
        'aligned', 'gathered', 'cases', 'matrix', 'pmatrix',
        'bmatrix', 'vmatrix', 'Vmatrix', 'array', 'eqnarray'
    }
    
    # Common LaTeX math commands and their argument patterns
    MATH_COMMANDS = {
        r'\\frac': 2,           # \frac{numerator}{denominator}
        r'\\sqrt': 1,           # \sqrt{expression} or \sqrt[n]{expression}
        r'\\sum': 0,            # \sum, \sum_{lower}^{upper}
        r'\\int': 0,            # \int, \int_{lower}^{upper}
        r'\\lim': 0,            # \lim, \lim_{x \to a}
        r'\\prod': 0,           # \prod
        r'\\text': 1,           # \text{content}
        r'\\textbf': 1,         # \textbf{content}
        r'\\textit': 1,         # \textit{content}
        r'\\mathrm': 1,         # \mathrm{content}
        r'\\mathbf': 1,         # \mathbf{content}
        r'\\mathcal': 1,        # \mathcal{content}
        r'\\label': 1,          # \label{eq:name}
    }
    
    # Delimiter pairs that should be balanced
    DELIMITER_PAIRS = [
        (r'\{', r'\}'),         # Braces
        (r'\(', r'\)'),         # Parentheses  
        (r'\[', r'\]'),         # Square brackets
        (r'\\left\(', r'\\right\)'),    # \left( \right)
        (r'\\left\[', r'\\right\]'),    # \left[ \right]
        (r'\\left\{', r'\\right\}'),    # \left{ \right}
    ]
    
    def __init__(self, manuscript_path: str):
        """Initialize math validator.
        
        Args:
            manuscript_path: Path to the manuscript directory
        """
        super().__init__(manuscript_path)
        self.found_math: List[Dict] = []
        self.equation_labels: Set[str] = set()
        
    def validate(self) -> ValidationResult:
        """Validate mathematical expressions in manuscript files."""
        errors = []
        metadata = {}
        
        # Process manuscript files
        files_to_check = [
            ("01_MAIN.md", "main"),
            ("02_SUPPLEMENTARY_INFO.md", "supplementary")
        ]
        
        for filename, file_type in files_to_check:
            file_path = os.path.join(self.manuscript_path, filename)
            if os.path.exists(file_path):
                file_errors = self._validate_file_math(file_path, file_type)
                errors.extend(file_errors)
                
        # Add statistics to metadata
        metadata.update(self._generate_math_statistics())
        
        return ValidationResult("MathValidator", errors, metadata)
        
    def _validate_file_math(self, file_path: str, file_type: str) -> List:
        """Validate mathematical expressions in a specific file."""
        errors = []
        content = self._read_file_safely(file_path)
        
        if not content:
            errors.append(self._create_error(
                ValidationLevel.ERROR,
                f"Could not read file: {os.path.basename(file_path)}",
                file_path=file_path
            ))
            return errors
            
        # Find and validate all math expressions
        math_errors = self._find_and_validate_math(content, file_path, file_type)
        errors.extend(math_errors)
        
        return errors
        
    def _find_and_validate_math(self, content: str, file_path: str, file_type: str) -> List:
        """Find and validate all mathematical expressions in content."""
        errors = []
        processed_ranges = []
        
        # Skip content within code blocks to avoid false positives
        protected_content = self._protect_code_blocks(content)

        # First, validate attributed math expressions (with labels) to avoid double-matching
        for match in self.MATH_PATTERNS['attributed_math'].finditer(protected_content):
            if 'XXPROTECTEDCODEXX' in match.group(0):
                continue
                
            line_num = protected_content[:match.start()].count('\n') + 1
            math_content = match.group(1)
            attrs_content = match.group(2)
            
            math_info = {
                'type': 'attributed',
                'content': math_content,
                'attributes': attrs_content,
                'line': line_num,
                'file': os.path.basename(file_path),
                'file_type': file_type,
                'full_match': match.group(0)
            }
            
            self.found_math.append(math_info)
            
            math_errors = self._validate_math_expression(math_info, file_path, line_num)
            errors.extend(math_errors)
            
            # Validate equation label
            label_errors = self._validate_equation_label(math_info, file_path, line_num)
            errors.extend(label_errors)
            
            # Store the range as processed to avoid display_math pattern match
            processed_ranges.append((match.start(), match.end()))
        
        # Validate inline math expressions, but skip overlapping ranges
        for match in self.MATH_PATTERNS['inline_math'].finditer(protected_content):
            if 'XXPROTECTEDCODEXX' in match.group(0):
                continue  # Skip protected code
                
            # Check if this match overlaps with any processed attributed_math ranges
            match_start, match_end = match.start(), match.end()
            is_overlapping = any(
                not (match_end <= proc_start or match_start >= proc_end)
                for proc_start, proc_end in processed_ranges
            )
            
            if is_overlapping:
                continue  # Skip this match as it overlaps with attributed math
                
            line_num = protected_content[:match.start()].count('\n') + 1
            math_content = match.group(1)
            
            math_info = {
                'type': 'inline',
                'content': math_content,
                'line': line_num,
                'file': os.path.basename(file_path),
                'file_type': file_type,
                'full_match': match.group(0)
            }
            
            self.found_math.append(math_info)
            
            math_errors = self._validate_math_expression(math_info, file_path, line_num)
            errors.extend(math_errors)
            
        # Then validate display math expressions, but skip overlapping ranges
        for match in self.MATH_PATTERNS['display_math'].finditer(protected_content):
            if 'XXPROTECTEDCODEXX' in match.group(0):
                continue  # Skip protected code
                
            # Check if this match overlaps with any processed attributed_math ranges
            match_start, match_end = match.start(), match.end()
            is_overlapping = any(
                not (match_end <= proc_start or match_start >= proc_end)
                for proc_start, proc_end in processed_ranges
            )
            
            if is_overlapping:
                continue  # Skip this match as it overlaps with attributed math
                
            line_num = protected_content[:match.start()].count('\n') + 1
            math_content = match.group(1)
            
            math_info = {
                'type': 'display',
                'content': math_content,
                'line': line_num,
                'file': os.path.basename(file_path),
                'file_type': file_type,
                'full_match': match.group(0)
            }
            
            self.found_math.append(math_info)
            
            math_errors = self._validate_math_expression(math_info, file_path, line_num)
            errors.extend(math_errors)
            
        return errors
        
    def _validate_math_expression(self, math_info: Dict, file_path: str, line_num: int) -> List:
        """Validate a single mathematical expression."""
        errors = []
        math_content = math_info['content']
        
        # Check for balanced delimiters
        delimiter_errors = self._check_balanced_delimiters(math_content, file_path, line_num)
        errors.extend(delimiter_errors)
        
        # Check for valid LaTeX environments
        env_errors = self._check_math_environments(math_content, file_path, line_num)
        errors.extend(env_errors)
        
        # Check for common syntax issues
        syntax_errors = self._check_math_syntax(math_content, file_path, line_num)
        errors.extend(syntax_errors)
        
        # Check for empty or whitespace-only math
        if not math_content.strip():
            errors.append(self._create_error(
                ValidationLevel.WARNING,
                "Empty mathematical expression",
                file_path=file_path,
                line_number=line_num,
                suggestion="Remove empty math delimiters or add content",
                error_code="empty_math"
            ))
            
        return errors
        
    def _check_balanced_delimiters(self, math_content: str, file_path: str, line_num: int) -> List:
        """Check for balanced delimiters in math expression."""
        errors = []
        
        for open_delim, close_delim in self.DELIMITER_PAIRS:
            open_count = len(re.findall(open_delim, math_content))
            close_count = len(re.findall(close_delim, math_content))
            
            if open_count != close_count:
                delim_name = open_delim.replace('\\', '')  # Remove escapes for display
                errors.append(self._create_error(
                    ValidationLevel.ERROR,
                    f"Unbalanced {delim_name} delimiters in math expression",
                    file_path=file_path,
                    line_number=line_num,
                    context=math_content[:100] + "..." if len(math_content) > 100 else math_content,
                    suggestion=f"Ensure every {open_delim} has a matching {close_delim}",
                    error_code="unbalanced_delimiters"
                ))
                
        return errors
        
    def _check_math_environments(self, math_content: str, file_path: str, line_num: int) -> List:
        """Check for valid LaTeX math environments."""
        errors = []
        
        # Find all environments in the math content
        for match in self.MATH_PATTERNS['environment_math'].finditer(math_content):
            env_name = match.group(1)
            
            if env_name not in self.VALID_ENVIRONMENTS:
                errors.append(self._create_error(
                    ValidationLevel.WARNING,
                    f"Unknown or non-standard math environment: {env_name}",
                    file_path=file_path,
                    line_number=line_num,
                    context=match.group(0)[:100] + "..." if len(match.group(0)) > 100 else match.group(0),
                    suggestion=f"Use standard environments like: {', '.join(sorted(list(self.VALID_ENVIRONMENTS)[:5]))}",
                    error_code="unknown_environment"
                ))
                
        return errors
        
    def _check_math_syntax(self, math_content: str, file_path: str, line_num: int) -> List:
        """Check for common LaTeX math syntax issues."""
        errors = []
        
        # Check for unescaped special characters
        special_chars = ['&', '%', '#', '$']
        for char in special_chars:
            if char in math_content and f'\\{char}' not in math_content:
                # Check if it's not part of a valid command
                if not re.search(rf'\\[a-zA-Z]*{re.escape(char)}', math_content):
                    errors.append(self._create_error(
                        ValidationLevel.WARNING,
                        f"Unescaped special character '{char}' in math",
                        file_path=file_path,
                        line_number=line_num,
                        suggestion=f"Use \\{char} to display the character literally",
                        error_code="unescaped_special_char"
                    ))
                    
        # Check for common command syntax issues
        command_errors = self._check_command_syntax(math_content, file_path, line_num)
        errors.extend(command_errors)
        
        # Check for double dollar signs in display math (should be outside)
        if '$$' in math_content:
            errors.append(self._create_error(
                ValidationLevel.ERROR,
                "Nested dollar signs in math expression",
                file_path=file_path,
                line_number=line_num,
                context=math_content,
                suggestion="Remove inner $$ - they should only surround the entire expression",
                error_code="nested_math_delimiters"
            ))
            
        return errors
        
    def _check_command_syntax(self, math_content: str, file_path: str, line_num: int) -> List:
        """Check LaTeX command syntax in math expressions."""
        errors = []
        
        # Find all LaTeX commands
        command_pattern = re.compile(r'\\([a-zA-Z]+)')
        
        for match in command_pattern.finditer(math_content):
            command = match.group(0)  # Full command including backslash
            command_name = match.group(1)  # Command name without backslash
            
            # Check if it's a known command that requires arguments
            for cmd_pattern, arg_count in self.MATH_COMMANDS.items():
                # Use the pattern directly since it's already properly escaped
                if re.match(cmd_pattern, command):
                    # Check if the command has the required number of arguments
                    remaining_content = math_content[match.end():]
                    if arg_count > 0:
                        arg_errors = self._check_command_arguments(
                            command, arg_count, remaining_content, file_path, line_num
                        )
                        errors.extend(arg_errors)
                    break
            else:
                # Unknown command - might be valid but flag as info
                if len(command_name) > 1:  # Single letter commands are usually fine
                    errors.append(self._create_error(
                        ValidationLevel.INFO,
                        f"Unknown or custom LaTeX command: {command}",
                        file_path=file_path,
                        line_number=line_num,
                        suggestion="Ensure the command is defined or use standard LaTeX commands",
                        error_code="unknown_command"
                    ))
                    
        return errors
        
    def _check_command_arguments(self, command: str, expected_args: int, 
                                remaining_content: str, file_path: str, line_num: int) -> List:
        """Check if a command has the expected number of arguments."""
        errors = []
        
        # Count braced arguments immediately following the command
        found_args = 0
        content = remaining_content.strip()
        
        while found_args < expected_args and content.startswith('{'):
            # Find matching closing brace, handling nested braces
            brace_count = 0
            pos = 0
            
            for i, char in enumerate(content):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        pos = i
                        break
            
            if brace_count == 0:  # Found matching brace
                found_args += 1
                content = content[pos + 1:].strip()
            else:
                break  # Unmatched braces
                
        if found_args < expected_args:
            errors.append(self._create_error(
                ValidationLevel.ERROR,
                f"Command {command} expects {expected_args} argument(s), found {found_args}",
                file_path=file_path,
                line_number=line_num,
                suggestion=f"Provide all required arguments for {command}",
                error_code="missing_command_arguments"
            ))
            
        return errors
        
    def _validate_equation_label(self, math_info: Dict, file_path: str, line_num: int) -> List:
        """Validate equation labels in attributed math expressions."""
        errors = []
        attrs_content = math_info.get('attributes', '')
        
        # Extract equation label
        label_match = re.search(r'#eq:([a-zA-Z0-9_:-]+)', attrs_content)
        if label_match:
            label_id = label_match.group(1)
            
            # Check for duplicate labels
            if label_id in self.equation_labels:
                errors.append(self._create_error(
                    ValidationLevel.ERROR,
                    f"Duplicate equation label: eq:{label_id}",
                    file_path=file_path,
                    line_number=line_num,
                    suggestion="Use unique labels for each equation",
                    error_code="duplicate_equation_label"
                ))
            else:
                self.equation_labels.add(label_id)
                
            # Check label format
            if not re.match(r'^[a-zA-Z0-9_:-]+$', label_id):
                errors.append(self._create_error(
                    ValidationLevel.WARNING,
                    f"Non-standard equation label format: {label_id}",
                    file_path=file_path,
                    line_number=line_num,
                    suggestion="Use letters, numbers, underscores, and hyphens for labels",
                    error_code="non_standard_label"
                ))
                
        # Check for environment specification
        env_match = re.search(r'\.([a-zA-Z]+)', attrs_content)
        if env_match:
            env_name = env_match.group(1)
            if env_name not in self.VALID_ENVIRONMENTS:
                errors.append(self._create_error(
                    ValidationLevel.WARNING,
                    f"Unknown math environment specified: {env_name}",
                    file_path=file_path,
                    line_number=line_num,
                    suggestion=f"Use standard environments: {', '.join(sorted(list(self.VALID_ENVIRONMENTS)[:5]))}",
                    error_code="unknown_specified_environment"
                ))
                
        return errors
        
    def _protect_code_blocks(self, content: str) -> str:
        """Protect code blocks from math validation."""
        # Protect fenced code blocks
        protected = re.sub(
            r'```.*?```',
            lambda m: f'XXPROTECTEDCODEXX{len(m.group(0))}XXPROTECTEDCODEXX',
            content,
            flags=re.DOTALL
        )
        
        # Protect inline code
        protected = re.sub(
            r'`[^`]+`',
            lambda m: f'XXPROTECTEDCODEXX{len(m.group(0))}XXPROTECTEDCODEXX',
            protected
        )
        
        return protected
        
    def _generate_math_statistics(self) -> Dict[str, any]:
        """Generate statistics about mathematical expressions."""
        stats = {
            'total_math_expressions': len(self.found_math),
            'inline_math': 0,
            'display_math': 0,
            'attributed_math': 0,
            'unique_equation_labels': len(self.equation_labels),
            'math_by_file_type': {'main': 0, 'supplementary': 0},
            'average_math_length': 0
        }
        
        total_length = 0
        for math_expr in self.found_math:
            # Count by type
            if math_expr['type'] == 'inline':
                stats['inline_math'] += 1
            elif math_expr['type'] == 'display':
                stats['display_math'] += 1
            elif math_expr['type'] == 'attributed':
                stats['attributed_math'] += 1
                
            # Count by file type
            stats['math_by_file_type'][math_expr['file_type']] += 1
            
            # Calculate length
            total_length += len(math_expr['content'])
            
        if len(self.found_math) > 0:
            stats['average_math_length'] = total_length / len(self.found_math)
            
        return stats