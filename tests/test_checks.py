"""Test module for the metadig checks module."""

from metadig import checks
from metadig.object_store import StoreManager
import os
import pytest


def get_test_data_path(file_name):
    """Get the path to a test file in tests/testdata"""
    test_data_directory = os.path.join(os.path.dirname(__file__), "testdata")
    return os.path.join(test_data_directory, file_name)


def test_run_check(storemanager_props, init_hashstore_with_test_data):
    """Test that the 'run_check' method successfully executes the subprocess and check"""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    # Confirm no exception is thrown and object and metadata is in place
    _ = manager.get_object("urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1")

    # Now execute 'run_check' by providing it the required args
    check_vars = {}
    pid = "urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1"
    check_vars["dataPids"] = [pid]
    check_vars["storeConfiguration"] = storemanager_props
    sample_check_file_path = get_test_data_path("data.table-text-delimited.glimpse.xml")
    sample_metadata_file_path = get_test_data_path("doi:10.18739_A2QJ78081.xml")

    result = checks.run_check(
        sample_check_file_path, sample_metadata_file_path, check_vars
    )
    assert result is not None, "Expected a result from the embedded code."
    assert result["Check Status"] == 0
    assert result["Check Result"] is not None


def test_run_check_multiple_pids(storemanager_props, init_hashstore_with_test_data):
    """Test that the 'run_check' method successfully executes the subprocess and check"""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    # Confirm no exception is thrown and object and metadata is in place
    _ = manager.get_object("urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1")

    # Now execute 'run_check' by providing it the required args
    check_vars = {}
    pid = "urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1"
    pid_two = "test-pid"
    check_vars["dataPids"] = [pid, pid_two]
    check_vars["storeConfiguration"] = storemanager_props
    sample_check_file_path = get_test_data_path("data.table-text-delimited.glimpse.xml")
    sample_metadata_file_path = get_test_data_path("doi:10.18739_A2QJ78081.xml")

    result = checks.run_check(
        sample_check_file_path, sample_metadata_file_path, check_vars
    )
    assert result is not None, "Expected a result from the embedded code."
    assert result["Check Status"] == 0
    assert len(result["Check Result"]) == 2


def test_run_check_error_missing_pid(storemanager_props, init_hashstore_with_test_data):
    """Test that the 'run_check' returns failed results successfully"""
    # Initialize hashstore and confirm it is in working order
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    _ = manager.get_object("urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1")

    # Now execute 'run_check' by providing it the required args
    check_vars = {}
    pid = "pid.not.found"
    check_vars["dataPids"] = [pid]
    check_vars["storeConfiguration"] = storemanager_props
    sample_check_file_path = get_test_data_path("data.table-text-delimited.glimpse.xml")
    sample_metadata_file_path = get_test_data_path("doi:10.18739_A2QJ78081.xml")

    result = checks.run_check(
        sample_check_file_path, sample_metadata_file_path, check_vars
    )
    assert result is not None
    assert result["Check Status"] == 1
    assert result["Check Result"] is not None


def test_run_check_error_multiple_pids_one_success_one_failure(
    storemanager_props,
    init_hashstore_with_test_data,
):
    """Test that the 'run_check' returns failed results successfully when a pid fails
    even if another pid succeeds"""
    # Initialize hashstore and confirm it is in working order
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    _ = manager.get_object("urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1")

    # Now execute 'run_check' by providing it the required args
    check_vars = {}
    pid = "urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1"  # Working pid
    pid_two = "pid.not.found"  # Failing pid
    check_vars["dataPids"] = [pid, pid_two]
    check_vars["storeConfiguration"] = storemanager_props
    sample_check_file_path = get_test_data_path("data.table-text-delimited.glimpse.xml")
    sample_metadata_file_path = get_test_data_path("doi:10.18739_A2QJ78081.xml")

    result = checks.run_check(
        sample_check_file_path, sample_metadata_file_path, check_vars
    )
    assert result is not None
    assert result["Check Status"] == 1


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
    checks.get_data_pids(identifier)
    assert True
