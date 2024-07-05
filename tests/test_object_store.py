import pytest
import os
import xml.etree.ElementTree as ET
from hashstore import HashStoreFactory
from metadig import StoreManager
from metadig import MetadataNotFoundError
from metadig import ObjectNotFoundError


# Create store and put an object in it
@pytest.fixture
def store_dir(tmp_path_factory):
    store_path = tmp_path_factory.mktemp("store")
    current_dir = os.path.dirname(__file__)
    obj_path = os.path.join(current_dir, "testdata", "test-data.csv")
    obj2_path = os.path.join(current_dir, "testdata", "test-data-2.csv")
    meta_path = os.path.join(current_dir, "testdata", "test-pid.xml")

    hashstore_factory = HashStoreFactory()

    # Create a properties dictionary with the required fields
    properties = {
        "store_path": str(store_path),
        "store_depth": 3,
        "store_width": 2,
        "store_algorithm": "SHA-256",
        "store_metadata_namespace": "https://ns.dataone.org/service/types/v2.0#SystemMetadata",
    }

    # Get HashStore from factory
    module_name = "hashstore.filehashstore"
    class_name = "FileHashStore"
    store = hashstore_factory.get_hashstore(module_name, class_name, properties)

    store.store_object("test-pid", str(obj_path))
    store.store_object("test-pid-2", str(obj2_path))
    store.store_metadata("test-pid", str(meta_path))
    return str(store_path)


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