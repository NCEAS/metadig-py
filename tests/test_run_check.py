"""Test module for the metadig checks module."""

from metadig import run_check
from metadig.object_store import StoreManager


def test_run_check(
    sample_check_file_path,
    sample_metadata_file_path,
    storemanager_props,
    init_hashstore_with_test_data,
):
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

    result = run_check(sample_check_file_path, sample_metadata_file_path, check_vars)
    assert result is not None, "Expected a result from the embedded code."
    assert result["Check Status"] == 0
    assert result["Check Result"] != ""
