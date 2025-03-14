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
    # Store data and metadata objects for 'object_store' pytest
    current_dir = os.path.dirname(__file__)
    obj_path = os.path.join(current_dir, "testdata", "test-data.csv")
    obj2_path = os.path.join(current_dir, "testdata", "test-data-2.csv")
    obj3_path = os.path.join(current_dir, "testdata", "test-data-2_3rowstoskip.csv")
    meta_path = os.path.join(current_dir, "testdata", "test-pid.xml")
    store.store_object("test-pid", str(obj_path))
    store.store_object("test-pid-2", str(obj2_path))
    store.store_object("test-pid-3skip", str(obj3_path))
    store.store_metadata("test-pid", str(meta_path))
    store.store_metadata("test-pid-3skip", str(meta_path))

    # Store data and metadata object for 'checks' pytest for DOI: doi:10.18739/A2QJ78081
    doi = "doi:10.18739/A2QJ78081"

    # Store the data object for the eml metadata doc
    doi_eml_metadata_doc = "doi:10.18739_A2QJ78081.xml"
    obj_path_to_pid_eml_meta_doc = os.path.join(current_dir, "testdata", doi_eml_metadata_doc)
    store.store_object(doi, str(obj_path_to_pid_eml_meta_doc))

    # Store the sysmeta for the eml metadata doc
    doi_eml_metadata_doc = "doi:10.18739_A2QJ78081_sysmeta.xml"
    obj_path_to_pid_eml_meta_doc_sysmeta = os.path.join(
        current_dir, "testdata", doi_eml_metadata_doc
    )
    store.store_metadata(doi, str(obj_path_to_pid_eml_meta_doc_sysmeta))

    # Store the associated .CSV
    pid_associated_file_name = "the_arctic_plant_aboveground_biomass_synthesis_dataset.csv"
    obj_path_to_pid_obj = os.path.join(current_dir, "testdata", pid_associated_file_name)
    store.store_object("urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1", str(obj_path_to_pid_obj))

    # Store the sysmeta document for the .CSV
    pid_sysmeta_name = "urn_uuid_6a7a874a-39b5-4855-85d4-0fdfac795cd1.xml"
    obj_path_to_pid_sysmeta = os.path.join(current_dir, "testdata", pid_sysmeta_name)
    store.store_metadata(
        "urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1", str(obj_path_to_pid_sysmeta)
    )

    # Store data and metadata object for 'checks' pytest for DOI: doi:10.18739/A2RJ48X0F
    # We will physically alter the data to have normalization issues
    nmi_doi = "doi:10.18739/A2RJ48X0F"

    # Store the data object for the eml metadata doc
    nmi_doi_eml_metadata_doc = "doi:10.18739_A2RJ48X0F.xml"
    nmi_obj_path_to_pid_eml_meta_doc = os.path.join(
        current_dir, "testdata", nmi_doi_eml_metadata_doc
    )
    store.store_object(nmi_doi, str(nmi_obj_path_to_pid_eml_meta_doc))

    # Store the sysmeta for the eml metadata doc
    nmi_doi_eml_metadata_doc = "doi:10.18739_A2QJ78081_sysmeta.xml"
    nmi_obj_path_to_pid_eml_meta_doc_sysmeta = os.path.join(
        current_dir, "testdata", nmi_doi_eml_metadata_doc
    )
    store.store_metadata(nmi_doi, str(nmi_obj_path_to_pid_eml_meta_doc_sysmeta))

    # Store the associated .CSV
    nmi_pid_associated_file_name = "SKQ2020309T_Chla_modified.csv"
    nmi_obj_path_to_pid_obj = os.path.join(
        current_dir, "testdata", nmi_pid_associated_file_name
    )
    store.store_object(
        "urn:uuid:a4aadc85-9fa4-46c9-9642-46066cf7a691", str(nmi_obj_path_to_pid_obj)
    )

    # Store the sysmeta document for the .CSV
    nmi_pid_sysmeta_name = "urn_uuid_a4aadc85-9fa4-46c9-9642-46066cf7a691.xml"
    nmi_obj_path_to_pid_sysmeta = os.path.join(current_dir, "testdata", nmi_pid_sysmeta_name)
    store.store_metadata(
        "urn:uuid:a4aadc85-9fa4-46c9-9642-46066cf7a691", str(nmi_obj_path_to_pid_sysmeta)
    )

    # Store other related files to the dataset (must be present in hashstore)
    other_pid_associated_file_name = "SKQ2020309T_Chlorophyll_Pigments_README.pdf"
    other_obj_path_to_pid_obj = os.path.join(
        current_dir, "testdata", other_pid_associated_file_name
    )
    store.store_object(
        "urn:uuid:60101459-96a2-41ea-b9e7-0dd80ecde3ce", str(other_obj_path_to_pid_obj)
    )

    other_pid_sysmeta_name = "urn_uuid_60101459-96a2-41ea-b9e7-0dd80ecde3ce.xml"
    other_obj_path_to_pid_sysmeta = os.path.join(current_dir, "testdata", other_pid_sysmeta_name)
    store.store_metadata(
        "urn:uuid:60101459-96a2-41ea-b9e7-0dd80ecde3ce", str(other_obj_path_to_pid_sysmeta)
    )

    return True
