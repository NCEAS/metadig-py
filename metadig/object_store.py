"""
Module: object_store.py

This module provides classes for managing different types of object stores
 and their retrieval operations.

Classes:
- ObjectStore: Abstract base class defining the interface for object stores.
- StoreManager: Concrete class managing different store instances based on
configuration.
- HashStore: Implementation of ObjectStore interface for a hash-based store.

Example Usage:
    configuration = {
        'store_type': 'HashStore',
    }
    manager = StoreManager(configuration)
    obj = manager.get_object('pid')
    print(obj)
"""

from abc import ABC, abstractmethod
from hashstore import HashStoreFactory

class ObjectStore(ABC):
    """
    Abstract base class for defining an object storage interface.

    Methods:
        get_object(identifier):
            Abstract method to retrieve an object from the store based on its
              identifier.
            This method must be implemented by concrete subclasses.
    """

    @abstractmethod
    def get_object(self, identifier):
        """
        Retrieve an object from the store based on its identifier.

        Args:
            identifier (str): The identifier of the object to retrieve.

        Returns:
            object: The retrieved object as a stream
        """


class HashStore(ObjectStore):
    """
    A class representing a hashstore that implements the ObjectStore interface.

    This class creates an instance of a hashstore (`FileHashStore`) based on
     the provided configuration. It inherits functionality from the abstract
     base class ObjectStore.

    Attributes:
        store: An instance of a hash store created by the factory.

    Methods:
        __init__(configuration):
            Initializes the HashStore instance using the provided
             configuration

        get_object(identifier):
            Retrieves an object from the hash store based on the given
             identifier.
    """

    def __init__(self, configuration):

        # if the config is not a dictionary, convert it
        if not isinstance(configuration, dict):
            if hasattr(configuration, 'keySet'):
                configuration = {str(key): configuration.get(key) for key in configuration.keySet()}
            else:
                raise TypeError("Configuration must be a dictionary or have a keySet method.")
            
        #configuration.pop('store_type', None)
        # check required keys are present
        required_keys = ['store_path', 'store_depth', 'store_width', 'store_algorithm', 'store_metadata_namespace']
        for key in required_keys:
            if key not in configuration:
                raise ValueError(f"Missing required configuration key: {key}")
        # initialize hashstore
        factory = HashStoreFactory()
        module_name = "hashstore.filehashstore"
        class_name = "FileHashStore"
        self.store = factory.get_hashstore(module_name, class_name, configuration)

    def get_object(self, identifier):
        obj = self.store.retrieve_object(identifier)
        return obj


class StoreManager:
    """
    Manage different types of stores based on the configuration.

    Initializes and manage instances of various store classes
    based on the 'store_type' value provided in the configuration dictionary.

    Attributes:
        store: An instance of the selected store class.

    Methods:
        __init__(configuration):
            Initializes the StoreManager instance.

        _create_store(configuration):
            Private method that creates and returns an instance of the appropriate
            store class based on the 'store_type' value in the configuration.

        get_object(identifier):
            Retrieves an object from the managed store instance based on the given identifier.
    """

    def __init__(self, configuration):
        """
        Initializes the StoreManager instance.

        Args:
            configuration (dict): A dictionary containing configuration options
                including the 'store_type' that determines the type of store to manage.
        """
        self.store = self._create_store(configuration)

    def _create_store(self, configuration):
        """
        Creates and returns an instance of the appropriate store class
        based on the 'store_type' value in the configuration.

        Args:
            configuration (dict): A dictionary containing configuration options
                including the 'store_type' that determines the type of store to manage.

        Returns:
            object: An instance of the selected store class.

        Raises:
            ValueError: If the 'store_type' in the configuration is unknown or unsupported.
        """
        store_type = configuration.get("store_type")

        if store_type == "HashStore":  # Default path if not provided
            return HashStore(configuration)

        # Add more conditions for other store types if needed

        raise ValueError(f"Unknown storeType: {store_type}. Expected one of: HashStore")

    def get_object(self, identifier):
        """
        Retrieves an object from the managed store instance based on the given identifier.

        Args:
            identifier (str): The identifier of the object to retrieve.

        Returns:
            object: The retrieved object from the managed store instance.
        """
        return self.store.get_object(identifier)
