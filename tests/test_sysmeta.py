import pytest

from metadig import StoreManager
from metadig import read_sysmeta_element


def test_sysmeta_fn(store_dir):

    properties = {
        "store_type": "HashStore",
        "store_path": store_dir,
        "store_depth": 3,
        "store_width": 2,
        "store_algorithm": "SHA-256",
        "store_metadata_namespace": "https://ns.dataone.org/service/types/v2.0#SystemMetadata",
    }

    manager = StoreManager(properties)
    obj, sys = manager.get_object("test-pid")

    fid = read_sysmeta_element(sys, "formatId")
    assert fid == "text/csv"
