"""Test module for the MetaDIG-py client."""
import os
import sys
import pytest
from metadig import metadigclient

def test_metadig_client_run_check(store, init_hashstore_with_test_data):
    """Confirm metadig runs a check successfully"""
    assert init_hashstore_with_test_data
    client_directory = os.getcwd() + "/metadig"
    client_module_path = f"{client_directory}/metadigclient.py"
    test_dir = "tests/testdata/"
    test_store_path = str(store.root)
    run_check_opt = "-runcheck"
    hashstore_path_opt = f"-store_path={test_store_path}"
    check_xml_path_opt = f"-check_xml={test_dir}/data.table-text-delimited.glimpse.xml"
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
