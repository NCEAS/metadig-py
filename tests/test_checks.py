"""Test module for the metadig checks module."""

import json
import multiprocessing
import os
import pytest
from metadig import checks
from metadig.object_store import StoreManager


def get_test_data_path(file_name):
    """Get the path to a test file in tests/testdata"""
    test_data_directory = os.path.join(os.path.dirname(__file__), "testdata")
    return os.path.join(test_data_directory, file_name)


def test_run_check_datatable_glimpse(storemanager_props, init_hashstore_with_test_data):
    """Test 'run_check' with 'data.table-text-delimited.glimpse.xml' python check."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    # Confirm no exception is thrown and object and metadata is in place
    _ = manager.get_object("urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1")

    # Now execute 'run_check' by providing it the required args
    sample_check_file_path = get_test_data_path("data.table-text-delimited.glimpse.xml")
    sample_metadata_file_path = get_test_data_path("doi:10.18739_A2QJ78081.xml")
    sample_sysmeta_file_path = get_test_data_path("doi:10.18739_A2QJ78081_sysmeta.xml")

    result = checks.run_check(
        sample_check_file_path,
        sample_metadata_file_path,
        sample_sysmeta_file_path,
        storemanager_props,
    )

    result_data = json.loads(result)
    assert result_data is not None
    assert result_data["identifiers"] is not None
    assert result_data["output"] is not None
    assert result_data["status"] is not None


def test_run_check_datatable_well_formed(storemanager_props, init_hashstore_with_test_data):
    """Test 'run_check' with 'data.table-text-delimited.well-formed.xml' python check."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    # Confirm no exception is thrown and object and metadata is in place
    _ = manager.get_object("urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1")

    # Now execute 'run_check' by providing it the required args
    sample_check_file_path = get_test_data_path("data.table-text-delimited.well-formed.xml")
    sample_metadata_file_path = get_test_data_path("doi:10.18739_A2QJ78081.xml")
    sample_sysmeta_file_path = get_test_data_path("doi:10.18739_A2QJ78081_sysmeta.xml")

    result = checks.run_check(
        sample_check_file_path,
        sample_metadata_file_path,
        sample_sysmeta_file_path,
        storemanager_props,
    )

    result_data = json.loads(result)
    assert result_data is not None
    assert result_data["identifiers"] is not None
    assert result_data["output"] is not None
    assert "is able to be parsed" in result_data["output"][0]
    assert result_data["status"] is not None


def test_run_check_datatable_variables_congruent(storemanager_props, init_hashstore_with_test_data):
    """Test 'run_check' with 'data.table-text-delimited.variables-congruent.xml' python check."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    # Confirm no exception is thrown and object and metadata is in place
    _ = manager.get_object("urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1")

    # Now execute 'run_check' by providing it the required args
    sample_check_file_path = get_test_data_path("data.table-text-delimited.variables-congruent.xml")
    sample_metadata_file_path = get_test_data_path("doi:10.18739_A2QJ78081.xml")
    sample_sysmeta_file_path = get_test_data_path("doi:10.18739_A2QJ78081_sysmeta.xml")

    result = checks.run_check(
        sample_check_file_path,
        sample_metadata_file_path,
        sample_sysmeta_file_path,
        storemanager_props,
    )

    result_data = json.loads(result)
    assert result_data is not None
    assert result_data["identifiers"] is not None
    assert result_data["output"] is not None
    assert "variable names match documentation." in result_data["output"][0]
    assert result_data["status"] is not None


def test_run_check_dataformat_normalized(storemanager_props, init_hashstore_with_test_data):
    """Test 'run_check' with 'data.table-text-delimited.normalized.xml' python check."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    # Confirm no exception is thrown and object and metadata is in place
    _ = manager.get_object("urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1")

    # Now execute 'run_check' by providing it the required args
    sample_check_file_path = get_test_data_path("data.table-text-delimited.normalized.xml")
    sample_metadata_file_path = get_test_data_path("doi:10.18739_A2QJ78081.xml")
    sample_sysmeta_file_path = get_test_data_path("doi:10.18739_A2QJ78081_sysmeta.xml")

    result = checks.run_check(
        sample_check_file_path,
        sample_metadata_file_path,
        sample_sysmeta_file_path,
        storemanager_props,
    )

    result_data = json.loads(result)
    assert result_data is not None
    assert result_data["identifiers"] is not None
    assert result_data["output"] is not None
    assert "is normalized" in result_data["output"][0]
    assert result_data["status"] is not None


def test_run_check_dataformat_normalized_data_is_not_normalized(storemanager_props, init_hashstore_with_test_data):
    """Test 'run_check' with 'data.table-text-delimited.normalized.xml' returns expected
    output when data is normalized and issues are found."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    # Confirm no exception is thrown and object and metadata is in place
    _ = manager.get_object("urn:uuid:60101459-96a2-41ea-b9e7-0dd80ecde3ce")

    # Now execute 'run_check' by providing it the required args
    sample_check_file_path = get_test_data_path("data.table-text-delimited.normalized.xml")
    sample_metadata_file_path = get_test_data_path("doi:10.18739_A2RJ48X0F.xml")
    sample_sysmeta_file_path = get_test_data_path("doi:10.18739_A2RJ48X0F_sysmeta.xml")

    result = checks.run_check(
        sample_check_file_path,
        sample_metadata_file_path,
        sample_sysmeta_file_path,
        storemanager_props,
    )

    result_data = json.loads(result)
    print(result_data)
    assert result_data is not None
    assert result_data["identifiers"] is not None
    assert result_data["output"] is not None
    # TODO: Revise how this determines that a failure is found (ex. 4 errors found)
    # assert "duplicate columns found" in result_data["output"][0]
    assert result_data["status"] is not None


def test_run_check_dataformat_congruent(storemanager_props, init_hashstore_with_test_data):
    """Test 'run_check' with 'data.format.congruent.xml' python check."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    # Confirm no exception is thrown and object and metadata is in place
    _ = manager.get_object("urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1")

    # Now execute 'run_check' by providing it the required args
    sample_check_file_path = get_test_data_path("data.format.congruent.xml")
    sample_metadata_file_path = get_test_data_path("doi:10.18739_A2QJ78081.xml")
    sample_sysmeta_file_path = get_test_data_path("doi:10.18739_A2QJ78081_sysmeta.xml")

    result = checks.run_check(
        sample_check_file_path,
        sample_metadata_file_path,
        sample_sysmeta_file_path,
        storemanager_props,
    )

    result_data = json.loads(result)
    assert result_data is not None
    assert result_data["identifiers"] is not None
    assert result_data["output"] is not None
    assert "matches its media type and extension" in result_data["output"][0]
    assert result_data["status"] is not None

# TODO: Continue testing multiprocessing with `run_check`

def try_run_check(obj_tuple):
    """Executes a 'run_check' function in a try block"""
    try:
        result = checks.run_check(*obj_tuple)
        return result
    # pylint: disable=W0718
    except Exception as so_exception:
        print(so_exception)


def test_run_check_with_multiprocessing(storemanager_props, init_hashstore_with_test_data):
    """Test 'run_check' function in a multiprocessing setting"""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    # Confirm no exception is thrown and object and metadata is in place
    _ = manager.get_object("urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1")

    # Now execute 'run_check' by providing it the required args
    sample_check_file_path = get_test_data_path("data.table-text-delimited.glimpse.xml")
    sample_metadata_file_path = get_test_data_path("doi:10.18739_A2QJ78081.xml")
    sample_sysmeta_file_path = get_test_data_path("doi:10.18739_A2QJ78081_sysmeta.xml")

    # Create an array with these values repeated 10 times
    input_array = [
        (
            sample_check_file_path,
            sample_metadata_file_path,
            sample_sysmeta_file_path,
            storemanager_props,
        )
        for _ in range(10)
    ]

    # Set up pool and processes
    pool = multiprocessing.Pool()
    results = pool.imap(try_run_check, input_array)
    pool.close() # Close the pool and wait for all processes to complete
    pool.join()

    for result in results:
        result_data = json.loads(result)
        assert result_data is not None
        assert result_data["identifiers"] is not None
        assert result_data["output"] is not None
        assert result_data["status"] is not None


def test_run_check_multiple_pids(storemanager_props, init_hashstore_with_test_data):
    """Test that the 'run_check' method successfully executes with multiple pids"""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    # Confirm no exception is thrown and object and metadata is in place
    _ = manager.get_object("urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1")

    # Now execute 'run_check' by providing it the required args
    sample_check_file_path = get_test_data_path("data.table-text-delimited.glimpse.xml")
    sample_metadata_file_path = get_test_data_path("doi:10.18739_A2QJ78081.xml")
    sample_sysmeta_file_path = get_test_data_path("doi:10.18739_A2QJ78081_sysmeta.xml")

    result = checks.run_check(
        sample_check_file_path,
        sample_metadata_file_path,
        sample_sysmeta_file_path,
        storemanager_props,
    )

    result_data = json.loads(result)
    assert result_data is not None
    assert result_data["identifiers"] is not None
    assert result_data["output"] is not None
    assert result_data["status"] is not None
    assert len(result_data["identifiers"]) == 1
    assert len(result_data["output"]) == 1


def test_run_check_error_missing_pid_objects(storemanager_props, init_hashstore_with_test_data):
    """Test that the 'run_check' returns failed results successfully when missing a pid"""
    # Initialize hashstore and confirm it is in working order
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    _ = manager.get_object("urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1")

    # Now execute 'run_check' by providing it the required args
    sample_check_file_path = get_test_data_path("data.table-text-delimited.glimpse.xml")
    sample_metadata_file_path = get_test_data_path("doi:10.18739_A2QJ78081.xml")
    # The sysmeta below is for another DOI, which will return pids that are not stored
    sample_sysmeta_file_path = get_test_data_path("doi:10.18739_A2DF6K53C_sysmeta.xml")

    result = checks.run_check(
        sample_check_file_path,
        sample_metadata_file_path,
        sample_sysmeta_file_path,
        storemanager_props,
    )

    result_data = json.loads(result)
    assert result_data is not None
    assert result_data["identifiers"] is not None
    assert result_data["output"] is not None
    assert result_data["status"] is not None
    assert len(result_data["identifiers"]) == 6
    assert len(result_data["output"]) == 6


def test_get_sysmeta_run_check_vars():
    """Test that we are able to retrieve the expected identifier and member node
    from a given sysmeta document."""
    path = get_test_data_path("doi:10.18739_A2QJ78081_sysmeta.xml")
    sm_rn_vars = checks.get_sysmeta_run_check_vars(path)
    assert sm_rn_vars.get("identifier") == "doi:10.18739/A2QJ78081"
    assert sm_rn_vars.get("authoritative_member_node") == "urn:node:ARCTIC"


def test_get_sysmeta_run_check_vars_missing_elements():
    """Test that exception is thrown when we are missing expected elements from a sysmeta doc."""
    path = get_test_data_path("sysmeta_missing_elements.xml")
    with pytest.raises(AttributeError):
        _ = checks.get_sysmeta_run_check_vars(path)


def test_get_sysmeta_run_check_vars_empty_elements():
    """Test that exception is thrown when we an expected elements from a sysmeta doc is empty."""
    path = get_test_data_path("sysmeta_empty_elements.xml")
    with pytest.raises(ValueError):
        _ = checks.get_sysmeta_run_check_vars(path)


def test_get_data_pids():
    """Check that we are able to retrieve data pids from a member node"""
    path = get_test_data_path("doi:10.18739_A2QJ78081_sysmeta.xml")
    sm_rn_vars = checks.get_sysmeta_run_check_vars(path)
    identifier = sm_rn_vars.get("identifier")
    member_node = "urn:node:ARCTIC"
    data_pids = checks.get_data_pids(identifier, member_node)
    expected_pids = [
        "urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1"
    ]
    for pid in expected_pids:
        assert pid in data_pids


def test_get_data_pids_member_node_url_unavailable():
    """Check that get_data_pids throws an exception when there is no member node available."""
    identifier = "dou.test.id.eml"
    member_node = "urn:node:DOU"
    with pytest.raises(ValueError):
        _ = checks.get_data_pids(identifier, member_node)


def test_get_member_node_url():
    """Check that get_member_node_url returns the expected Base URL."""
    member_node = "urn:node:ARCTIC"
    base_url = checks.get_member_node_url(member_node)
    assert base_url == "https://arcticdata.io/metacat/d1/mn/v2"


def test_get_member_node_url_not_found():
    """Check that get_member_node_url raises ValueError when Base URL is not found."""
    member_node = "urn:node:DOU"
    with pytest.raises(ValueError):
        checks.get_member_node_url(member_node)
