"""Test module for the MetaDIG-py client."""
import os
import sys
import json
import pytest
from metadig import metadigclient


def get_test_data_path(file_name):
    """Get the path to a test file in tests/testdata"""
    test_data_directory = os.path.join(os.path.dirname(__file__), "testdata")
    return os.path.join(test_data_directory, file_name)


def test_metadig_client_run_check(capsys, store, init_hashstore_with_test_data):
    """Confirm metadig runs a check successfully"""
    assert init_hashstore_with_test_data
    client_directory = os.getcwd() + "/metadig"
    client_module_path = f"{client_directory}/metadigclient.py"
    test_dir = "tests/testdata/"
    test_store_path = str(store.root)
    run_check_opt = "-runcheck"
    hashstore_path_opt = f"-store_path={test_store_path}"
    check_xml_path_opt = f"-check_xml={test_dir}/checks/data.table-text-delimited.variables-congruent.xml"
    metadata_doc_path_opt = f"-metadata_doc={test_dir}/doi:10.18739_A2QJ78081.xml"
    sysmeta_doc_path_opt = f"-sysmeta_doc={test_dir}/doi:10.18739_A2QJ78081_sysmeta.xml"

    chs_args = [
        client_module_path,
        run_check_opt,
        hashstore_path_opt,
        check_xml_path_opt,
        metadata_doc_path_opt,
        sysmeta_doc_path_opt
    ]

    sys.path.append(client_directory)
    sys.argv = chs_args
    metadigclient.main()

    result_data = json.loads(capsys.readouterr().out)
    assert result_data is not None
    assert result_data["identifiers"] is not None
    assert result_data["output"] is not None
    assert result_data["status"] is not None
    assert len(result_data["identifiers"]) is 1
    assert len(result_data["output"]) is 1

@pytest.mark.parametrize(
    "missing_opt", ["store_path", "check_xml", "metadata_doc", "sysmeta_doc"]
)
def test_metadig_client_run_check_missing_args(missing_opt, store):
    """Use pytest 'parametrize' decorator to efficiently test missing arguments"""
    client_directory = os.getcwd() + "/metadig"
    client_module_path = f"{client_directory}/metadigclient.py"
    test_dir = "tests/testdata/"
    test_store_path = str(store.root)
    run_check_opt = "-runcheck"

    # Map options
    options = {
        "store_path": f"-store_path={test_store_path}",
        "check_xml": f"-check_xml={test_dir}/data.table-text-delimited.glimpse.xml",
        "metadata_doc": f"-metadata_doc={test_dir}/doi:10.18739_A2QJ78081.xml",
        "sysmeta_doc": f"-sysmeta_doc={test_dir}/doi:10.18739_A2QJ78081_sysmeta.xml",
    }

    # Remove the missing option dynamically by creating a new list that excludes the missing opt
    required_opts = [opt for key, opt in options.items() if key != missing_opt]

    chs_args = [
        client_module_path,
        run_check_opt,
        *required_opts,  # Include only required options
    ]

    sys.path.append(client_directory)
    sys.argv = chs_args

    with pytest.raises(ValueError):
        metadigclient.main()


# MetaDigClientUtilities Tests


def test_get_data_object_system_metadata(mcdu):
    """Check that we can retrieve a data object's sysmeta and parse it for the file name."""
    identifier = "doi:10.18739/A24F1MM18"
    auth_mn_node = "urn:node:ARCTIC"

    data_obj_name, sysmeta = mcdu.get_data_object_system_metadata(
        identifier, auth_mn_node
    )

    assert data_obj_name == "Ground_Temperature_Monitoring_of_a_Cover_Crop_Vari.xml"
    assert sysmeta is not None


def test_find_file(mcdu):
    """Check that 'find_file' can find a data file that's in a subfolder in a given folder."""
    # Current directory
    folder_to_check = os.path.join(os.path.dirname(__file__))
    file_to_find = "resource.license.present-2.0.0.xml"

    data_object_path = mcdu.find_file(folder_to_check, file_to_find)
    assert data_object_path is not None


def test_import_data_to_hashstore(mcdu):
    """Test that 'import_data_to_hashstore' imports data to the default hashstore."""
    sample_sysmeta_file_path = get_test_data_path("doi:10.18739_A2QJ78081_sysmeta.xml")
    test_data_directory = os.path.join(os.path.dirname(__file__), "testdata")

    data_pids_stored = mcdu.import_data_to_hashstore(sample_sysmeta_file_path, test_data_directory)
    for pid in data_pids_stored:
        # No exceptions should be thrown if the data objects and system metadata were stored
        obj_stream = mcdu.default_store.retrieve_object(pid)
        sysmeta_stream = mcdu.default_store.retrieve_metadata(pid)
        obj_stream.close()
        sysmeta_stream.close()
