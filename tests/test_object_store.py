import pytest
import xml.etree.ElementTree as ET

from metadig import StoreManager
from metadig import MetadataNotFoundError
from metadig import ObjectNotFoundError



def test_object_store_returns_correct_data(store_dir):
    """
    Test that the object store returns data, and that it is the data expected
    """

    properties = {
        "store_type": "HashStore",
        "store_path": store_dir,
        "store_depth": 3,
        "store_width": 2,
        "store_algorithm": "SHA-256",
        "store_metadata_namespace": "https://ns.dataone.org/service/types/v2.0#SystemMetadata",
    }

    manager = StoreManager(properties)
    obj = manager.get_object("test-pid")

    content = obj[0].read(10).decode("utf-8")
    assert content == "Year,Site,"

    meta = obj[1].read().decode("utf-8")
    root = ET.fromstring(meta)
    pid = root.find(".//identifier").text
    assert pid == "test-pid"

def test_object_store_handles_no_store(store_dir):

    properties = {
        "store_path": store_dir,
        "store_depth": 3,
        "store_width": 2,
        "store_algorithm": "SHA-256",
        "store_metadata_namespace": "https://ns.dataone.org/service/types/v2.0#SystemMetadata",
    }

    with pytest.raises(ValueError, match = "Unknown storeType: None. Expected one of: HashStore"):
        StoreManager(properties)

def test_object_store_handles_no_metadata(store_dir):

    properties = {
        "store_type": "HashStore",
        "store_path": store_dir,
        "store_depth": 3,
        "store_width": 2,
        "store_algorithm": "SHA-256",
        "store_metadata_namespace": "https://ns.dataone.org/service/types/v2.0#SystemMetadata",
    }

    manager = StoreManager(properties)
    with pytest.raises(MetadataNotFoundError, match = 'Metadata for object with identifier test-pid-2 not found'):
        obj = manager.get_object("test-pid-2")

def test_object_store_handles_no_object(store_dir):

    properties = {
        "store_type": "HashStore",
        "store_path": store_dir,
        "store_depth": 3,
        "store_width": 2,
        "store_algorithm": "SHA-256",
        "store_metadata_namespace": "https://ns.dataone.org/service/types/v2.0#SystemMetadata",
    }

    manager = StoreManager(properties)
    with pytest.raises(ObjectNotFoundError, match = 'Object with identifier not-a-pid not found'):
        obj = manager.get_object("not-a-pid")