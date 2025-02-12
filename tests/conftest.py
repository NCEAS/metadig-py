"""This pytest conf file provides fixtures (variables, methods) for metadig pytests."""

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

@pytest.fixture(name="hashstore_props")
def init_hashstore_props(store_path):
    """Properties to initialize HashStore."""
    properties = {
        "store_path": store_path,
        "store_depth": 3,
        "store_width": 2,
        "store_algorithm": "SHA-256",
        "store_metadata_namespace": "https://ns.dataone.org/service/types/v2.0#SystemMetadata",
    }
    return properties

@pytest.fixture(name="storemanager_props")
def init_storemanager_props(hashstore_props):
    """Properties to initialize StoreManager."""
    # Add 'store_type' to hashstore properties
    storemanager_props = hashstore_props
    storemanager_props["store_type"] = "HashStore"
    return storemanager_props

@pytest.fixture(name="store")
def init_hashstore(hashstore_props):
    """Properties to initialize HashStore."""
    # Get HashStore from factory
    hashstore_factory = HashStoreFactory()
    module_name = "hashstore.filehashstore"
    class_name = "FileHashStore"
    store = hashstore_factory.get_hashstore(module_name, class_name, hashstore_props)
    return store

# Create store and put an object in it
@pytest.fixture
def init_hashstore_with_test_data(store):
    """Store two data objects with pids 'test-pid' and 'test-pid-2' and one metadata
    document with pid 'test-pid'"""
    current_dir = os.path.dirname(__file__)
    obj_path = os.path.join(current_dir, "testdata", "test-data.csv")
    obj2_path = os.path.join(current_dir, "testdata", "test-data-2.csv")
    meta_path = os.path.join(current_dir, "testdata", "test-pid.xml")

    # Store data and metadata objects for 'object_store' pytest
    store.store_object("test-pid", str(obj_path))
    store.store_object("test-pid-2", str(obj2_path))
    store.store_metadata("test-pid", str(meta_path))
    # Store data and metadata object for 'checks' pytest
    # TODO: The data object here may not be suitable tor the actual check that is run
    # TODO: Determine if specific data object and metadata should be used
    pid_associated_file_name = "the_arctic_plant_aboveground_biomass_synthesis_dataset.csv"
    pid_sysmeta_name = "urn_uuid_6a7a874a-39b5-4855-85d4-0fdfac795cd1.xml"
    obj_path_to_pid_obj = os.path.join(current_dir, "testdata", pid_associated_file_name)
    obj_path_to_pid_sysmeta = os.path.join(current_dir, "testdata", pid_sysmeta_name)
    store.store_object("urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1", str(obj_path_to_pid_obj))
    store.store_metadata(
        "urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1", str(obj_path_to_pid_sysmeta)
    )
    return True
