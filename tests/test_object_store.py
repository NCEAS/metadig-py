"""Test module for object_store module"""

import xml.etree.ElementTree as ET
import pytest

from metadig import StoreManager
from metadig import ObjectNotFoundError


def test_object_store_returns_correct_data(storemanager_props, init_hashstore_with_test_data):
    """Test that the object store returns data, and that it is the data expected."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    obj = manager.get_object("test-pid")

    content = obj[0].read(10).decode("utf-8")
    assert content == "Year,Site,"

    meta = obj[1].read().decode("utf-8")
    root = ET.fromstring(meta)
    pid = root.find(".//identifier").text
    assert pid == "test-pid"


def test_object_store_handles_no_store(hashstore_props):
    """Confirm that when a store_type is not prvided, an exception is thrown."""
    with pytest.raises(
        ValueError, match="Unknown storeType: None. Expected one of: HashStore"
    ):
        StoreManager(hashstore_props)


def test_object_store_handles_no_metadata(storemanager_props, init_hashstore_with_test_data):
    """Confirm that an exception is thrown when no metadata is found for a pid."""
    assert init_hashstore_with_test_data
    manager = StoreManager(storemanager_props)
    with pytest.raises(
        ValueError,
        match="No metadata found for pid: test-pid-2",
    ):
        _ = manager.get_object("test-pid-2")


def test_object_store_handles_no_object(storemanager_props):
    """Confirm that an exception is thrown when a data object is missing."""
    manager = StoreManager(storemanager_props)
    with pytest.raises(
        ObjectNotFoundError, match="Object with identifier not-a-pid not found"
    ):
        _ = manager.get_object("not-a-pid")
