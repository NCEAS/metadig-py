"""
metadig

Python package for metadig
"""

__version__ = "1.3.0"

from metadig import checks
from metadig import metadata
from metadig import suites
from .checks import getType
from .checks import isResolvable
from .checks import run_check
from .variable import isBlank
from .variable import toUnicode
from .object_store import StoreManager
from .object_store import MetadataNotFoundError
from .object_store import ObjectNotFoundError
from .metadata import read_sysmeta_element
from .metadata import find_eml_entity
from .metadata import find_entity_index
from .metadata import read_csv_with_metadata
from .metadata import get_valid_csv

__all__ = [
    "StoreManager",
    "getType",
    "isResolvable",
    "isBlank",
    "toUnicode",
    "read_sysmeta_element",
    "find_eml_entity",
    "find_entity_index",
    "read_csv_with_metadata",
    "get_valid_csv",
    "run_check",
    "checks",
    "metadata",
    "suites",
]
