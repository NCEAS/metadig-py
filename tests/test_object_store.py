from hashstore import HashStoreFactory
import pytest
from metadig import StoreManager

# Create store and put an object in it
@pytest.fixture
def store_dir(tmp_path_factory):
    store_path = tmp_path_factory.mktemp("store")
    obj_path = tmp_path_factory.mktemp("temp") / "numbers.txt"

    object_content = ''.join(str(i) for i in range(10))
    with open(obj_path, "w") as f:
        f.write(object_content)
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
    return str(store_path)


def test_object_store(store_dir):

    properties = {
        "store_type": 'HashStore',
        "store_path": store_dir,
        "store_depth": 3,
        "store_width": 2,
        "store_algorithm": "SHA-256",
        "store_metadata_namespace": "https://ns.dataone.org/service/types/v2.0#SystemMetadata",
    }
        
    manager = StoreManager(properties)
    obj = manager.get_object("test-pid")
    #content = obj.read()
    assert obj is not None
    #assert content == '0123456789'