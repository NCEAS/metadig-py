"""Test module for the metadig suites module."""

import json
import os
from metadig import suites


def get_test_data_path(file_name):
    """Get the path to a test file in tests/testdata"""
    test_data_directory = os.path.join(os.path.dirname(__file__), "testdata")
    return os.path.join(test_data_directory, file_name)


def test_run_suite(storemanager_props, init_hashstore_with_test_data):
    """Check that run_suite can execute a suite of checks successfully."""
    assert init_hashstore_with_test_data

    sample_metadata_file_path = get_test_data_path("doi:10.18739_A2QJ78081.xml")
    sample_sysmeta_file_path = get_test_data_path("doi:10.18739_A2QJ78081_sysmeta.xml")
    suite_path = get_test_data_path("FAIR-suite-0.4.0.xml")
    checks_path = get_test_data_path("checks")

    suite_results = suites.run_suite(
        suite_path,
        checks_path,
        sample_metadata_file_path,
        sample_sysmeta_file_path,
        storemanager_props,
    )

    suite_data = json.loads(suite_results)
    assert suite_data["suite"] is not None
    assert suite_data["run_status"] == "SUCCESS"
    assert suite_data["sysmeta"] is not None
    assert suite_data["results"] is not None


def test_map_and_get_check_ids_to_files():
    """Check that 'map_and_get_check_ids_to_files' can read .xml files and map the ids"""
    path_to_checks = get_test_data_path("checks")
    id_to_checks_dict = suites.map_and_get_check_ids_to_files(path_to_checks)

    path_to_resolvable_2 = get_test_data_path(
        "checks/metadata.identifier.resolvable-2.0.0.xml"
    )
    path_to_congruent = get_test_data_path(
        "checks/data.table-text-delimited.variables-congruent.xml"
    )
    path_to_attrib_differs = get_test_data_path(
        "checks/entity.attributeName.differs-2.0.0.xml"
    )
    path_to_process_stepcode = get_test_data_path(
        "checks/provenance.processStepCode.present-2.0.0.xml"
    )
    path_to_license_present = get_test_data_path(
        "checks/resource.license.present-2.0.0.xml"
    )
    path_to_pubdate_timeframe = get_test_data_path(
        "checks/resource.publicationDate.timeframe.xml"
    )

    assert (
        id_to_checks_dict["metadata.identifier.resolvable-2.0.0"]
        == path_to_resolvable_2
    )
    assert (
        id_to_checks_dict["data.table-text-delimited.variables-congruent"]
        == path_to_congruent
    )
    assert (
        id_to_checks_dict["entity.attributeName.differs-2.0.0"]
        == path_to_attrib_differs
    )
    assert (
        id_to_checks_dict["provenance.ProcessStepCode.present-2.0.0"]
        == path_to_process_stepcode
    )
    assert (
        id_to_checks_dict["resource.license.present-2.0.0"] == path_to_license_present
    )
    # Note: The id found in this check is not the same as the file name, this is the purpose
    # of the mapping function (to bridge this gap)
    assert (
        id_to_checks_dict["resource.publicationDate.timeframe.1"]
        == path_to_pubdate_timeframe
    )


def test_does_file_exist():
    """Test that exceptions are raised when a file cannot be found at the given path."""
    path_that_does_not_exist = "/this/path/does/not/exist"
    file_exists = suites.does_file_exist(path_that_does_not_exist)
    assert not file_exists
