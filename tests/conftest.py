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
    """Store data objects and system metadata for tests to run as expected.'"""
    # Store data and metadata objects for 'object_store' and 'metadata' pytest
    current_dir = os.path.dirname(__file__)
    testdata_dir = os.path.join(current_dir, "testdata")

    # Store text delimited objects for metadata module checks
    test_objects = [
        ("test-pid", "test-data.csv"),
        ("test-pid-2", "test-data-2.csv"),
        ("test-pid-3skip", "test-data-2_3rowstoskip.csv"),
        ("test-pid-4dupcols", "test-data_duplicate_columns.csv"),
        ("test-pid-dupcols-names", "test-data_duplicate_columns_dif_names.csv"),
        ("test-pid-duprows", "test-data_duplicate_rows.csv"),
        ("test-pid-decode-errors", "test-data_illegalcharacter.csv"),
    ]

    # For ease of adding test data, we are using the same sysmeta which is not tested against
    meta_path = os.path.join(testdata_dir, "test-pid.xml")
    for pid, filename in test_objects:
        store.store_object(pid, os.path.join(testdata_dir, filename))
        # We are skipping this specific sysmeta to trigger an exception for a pytest
        if pid != "test-pid-2":
            store.store_metadata(pid, meta_path)

    # Store data and metadata object for 'checks' pytest for DOI: doi:10.18739/A2QJ78081
    doi = "doi:10.18739/A2QJ78081"
    store.store_object(doi, os.path.join(testdata_dir, "doi:10.18739_A2QJ78081.xml"))
    store.store_metadata(doi, os.path.join(testdata_dir, "doi:10.18739_A2QJ78081_sysmeta.xml"))
    # Store associated data objects and sysmeta
    store.store_object(
        "urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1",
        os.path.join(testdata_dir, "the_arctic_plant_aboveground_biomass_synthesis_dataset.csv")
    )
    store.store_metadata(
        "urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1",
        os.path.join(testdata_dir, "urn_uuid_6a7a874a-39b5-4855-85d4-0fdfac795cd1.xml")
    )

    # Store data and metadata object for 'checks' pytest for DOI: doi:10.18739/A2RJ48X0F
    # We have physically altered the data to have normalization issues
    nmi_doi = "doi:10.18739/A2RJ48X0F"
    store.store_object(nmi_doi, os.path.join(testdata_dir, "doi:10.18739_A2RJ48X0F.xml"))
    store.store_metadata(nmi_doi, os.path.join(testdata_dir, "doi:10.18739_A2QJ78081_sysmeta.xml"))
    # Store associated data objects and sysmeta
    store.store_object(
        "urn:uuid:a4aadc85-9fa4-46c9-9642-46066cf7a691",
        os.path.join(testdata_dir, "SKQ2020309T_Chla_modified.csv")
    )
    store.store_metadata(
        "urn:uuid:a4aadc85-9fa4-46c9-9642-46066cf7a691",
        os.path.join(testdata_dir, "urn_uuid_a4aadc85-9fa4-46c9-9642-46066cf7a691.xml")
    )
    store.store_object(
        "urn:uuid:60101459-96a2-41ea-b9e7-0dd80ecde3ce",
        os.path.join(testdata_dir, "SKQ2020309T_Chlorophyll_Pigments_README.pdf")
    )
    store.store_metadata(
        "urn:uuid:60101459-96a2-41ea-b9e7-0dd80ecde3ce",
        os.path.join(testdata_dir, "urn_uuid_60101459-96a2-41ea-b9e7-0dd80ecde3ce.xml")
    )

    return True
