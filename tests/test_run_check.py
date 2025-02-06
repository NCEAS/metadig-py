"""Test module for the metadig module."""

from metadig import run_check

def test_run_check(sample_check_file_path, sample_metadata_file_path):
    check_vars = {}

    # todo: replace all this hardcoded proof of concept stuff with something that makes sense
    check_vars['dataPids'] = ["urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1"]
    check_vars['storeConfiguration'] = {
         "store_type": "HashStore",
        "store_path": "/Users/clark/Documents/metacat-hashstore",
        "store_depth": "3",
        "store_width": 2,
        "store_algorithm": "SHA-256",
        "store_metadata_namespace": "https://ns.dataone.org/service/types/v2.0#SystemMetadata",
    }

    result = run_check(sample_check_file_path, sample_metadata_file_path, check_vars)
    print("Dou ~ Result:")
    print(result)

    assert result is not None, "Expected a result from the embedded code."