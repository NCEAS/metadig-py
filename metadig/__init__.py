"""
metadig

Python package for metadig
"""

__version__ = "1.0"

from .checks import getType
from .checks import isResolvable
from .variable import isBlank
from .variable import toUnicode
from .object_store import StoreManager
from .object_store import MetadataNotFoundError
from .object_store import ObjectNotFoundError

__all__ = ['StoreManager', 'getType', 'isResolvable', 'isBlank', 'toUnicode']