import os
import pytest
from hashstore import HashStoreFactory

@pytest.fixture(name="store_path")
def init_store_path(tmp_path):
    """Create and return the path to a hashstore"""
    directory = tmp_path / "metacat" / "hashstore"
    directory.mkdir(parents=True)
    hashstore_path = directory.as_posix()
    return hashstore_path

@pytest.fixture(name="props")
def init_props(store_path):
    """Properties to initialize HashStore."""
    properties = {
        "store_path": store_path,
        "store_depth": 3,
        "store_width": 2,
        "store_algorithm": "SHA-256",
        "store_metadata_namespace": "https://ns.dataone.org/service/types/v2.0#SystemMetadata",
    }
    return properties

# Create store and put an object in it
@pytest.fixture
def store_dir(store_path, props):
    current_dir = os.path.dirname(__file__)
    obj_path = os.path.join(current_dir, "testdata", "test-data.csv")
    obj2_path = os.path.join(current_dir, "testdata", "test-data-2.csv")
    meta_path = os.path.join(current_dir, "testdata", "test-pid.xml")

    # Get HashStore from factory
    hashstore_factory = HashStoreFactory()
    module_name = "hashstore.filehashstore"
    class_name = "FileHashStore"
    store = hashstore_factory.get_hashstore(module_name, class_name, props)

    store.store_object("test-pid", str(obj_path))
    store.store_object("test-pid-2", str(obj2_path))
    store.store_metadata("test-pid", str(meta_path))
    return str(store_path)

@pytest.fixture(name="sample_check_file_path")
def init_sample_check_file():
    """Return a sample check file from testdata."""
    test_data_directory = os.path.join(os.path.dirname(__file__), 'testdata')
    return os.path.join(test_data_directory, 'data.table-text-delimited.glimpse.xml')

@pytest.fixture(name="sample_metadata_file_path")
def init_sample_metadata_file():
    """Return a sample metadata file from testdata."""
    test_data_directory = os.path.join(os.path.dirname(__file__), 'testdata')
    return os.path.join(test_data_directory, 'doi:10.18739_A2QJ78081.xml')