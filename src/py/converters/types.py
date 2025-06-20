"""Type definitions for markdown to LaTeX conversion."""

from typing import Dict, List, Union

# Type aliases for better readability
MarkdownContent = str
LatexContent = str
SectionKey = str
SectionTitle = str
CitationKey = str
FigureId = str
TableId = str
Placeholder = str

# Dictionary types
SectionDict = Dict[SectionKey, LatexContent]
ProtectedContent = Dict[Placeholder, str]
FigureAttributes = Dict[str, str]
TableAttributes = Dict[str, str]

# Content processing types
ContentProcessor = Union[str, List[str]]
ProcessingContext = Dict[str, Union[bool, str, int, ProtectedContent]]

# Table-specific types
TableRow = List[str]
TableData = List[TableRow]
TableHeaders = List[str]

# Figure-specific types
FigurePath = str
FigureCaption = str
FigurePosition = str
FigureWidth = str

# Citation-specific types
CitationList = List[CitationKey]
CitationFormat = str
