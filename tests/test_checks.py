"""Test module for the metadig checks module."""

from metadig import checks
from metadig.object_store import StoreManager
import os
import pytest
import json


def get_test_data_path(file_name):
    """Get the path to a test file in tests/testdata"""
    test_data_directory = os.path.join(os.path.dirname(__file__), "testdata")
    return os.path.join(test_data_directory, file_name)


def test_run_check(storemanager_props, init_hashstore_with_test_data):
    """Test that the 'run_check' method successfully executes"""
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
    assert len(result_data["identifiers"]) is 2
    assert len(result_data["output"]) is 2


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
    print(result_data)
    assert result_data is not None
    assert result_data["identifiers"] is not None
    assert result_data["output"] is not None
    assert result_data["status"] is not None
    assert len(result_data["identifiers"]) is 7
    assert len(result_data["output"]) is 7


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
        "urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1",
        "doi:10.18739/A2QJ78081",
    ]
    for pid in expected_pids:
        assert pid in data_pids


def test_get_data_pids_member_node_url_unavailable():
    """Check that get_data_pids throws an exception when there is no member node available."""
    identifier = "dou.test.id.eml"
    member_node = "urn:node:KNB"
    with pytest.raises(ValueError):
        _ = checks.get_data_pids(identifier, member_node)
