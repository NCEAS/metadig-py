"""
metadig

Python package for metadig
"""

__version__ = "1.3.0"

from .checks import getType
from .checks import isResolvable
from .variable import isBlank
from .variable import toUnicode
from .object_store import StoreManager
from .object_store import MetadataNotFoundError
from .object_store import ObjectNotFoundError
from .sysmeta import read_sysmeta_element

__all__ = ['StoreManager', 'getType', 'isResolvable', 'isBlank', 'toUnicode', 'read_sysmeta_element']