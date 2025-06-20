"""RXiv-Maker Python Package.

A comprehensive toolkit for automated scientific article generation and building.
"""

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

__author__ = "RXiv-Maker Contributors"

from . import _version

__version__ = _version.get_versions()["version"]
