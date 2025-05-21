#!/usr/bin/env python
"""Metadig Command Line App"""
import os
from argparse import ArgumentParser
import urllib.parse
import yaml
from lxml import etree
from hashstore import HashStoreFactory
from metadig import checks

class MetaDigPyParser:
    """Class to set up parsing arguments via argparse."""

    def __init__(self):
        """Initialize the argparse 'parser'."""

        program_name = "MetaDIG-Py Command Line Client"
        description = "Command line tool to run python checks."
        epilog = "Created for DataONE (NCEAS)"

        self.parser = ArgumentParser(
            prog=program_name,
            description=description,
            epilog=epilog,
        )

        # MetaDIG-py test method to run
        self.parser.add_argument(
            "-runcheck",
            dest="run_check",
            action="store_true",
            help="Flag to run a check through the MetaDIG-py client",
        )

        # Arguments to retrieve to run a check
        self.parser.add_argument(
            "-sp",
            "-store_path",
            dest="hashstore_path",
            help="Path of the HashStore that contains the objects to retrieve",
        )
        self.parser.add_argument(
            "-cxml",
            "-check_xml",
            dest="checkxml_path",
            help="Path to the check xml for MetaDIG-py to parse.",
        )
        self.parser.add_argument(
            "-mdoc",
            "-metadata_doc",
            dest="metadatadoc_path",
            help="Path to document to check (ex. EML metadata doc)",
        )
        self.parser.add_argument(
            "-sysmeta",
            "-sysmeta_doc",
            dest="sysmeta_path",
            help="Path to document to the sysmeta to retrieve the identifier and member node",
        )

    def get_parser_args(self):
        """Get command line arguments."""
        return self.parser.parse_args()


class MetaDigClientUtilities:
    """Class to assist the metadig client with running checks and/or suites."""

    def __init__(self):
        """Initialize the default properties for the MetaDigClientUtilities (ex. hashstore)"""
        default_hashstore_path = os.getcwd() + "/hashstore"
        storemanager_props = self.get_store_manager_props(default_hashstore_path)
        hashstore_factory = HashStoreFactory()
        module_name = "hashstore.filehashstore"
        class_name = "FileHashStore"
        self.default_store = hashstore_factory.get_hashstore(
            module_name, class_name, storemanager_props
        )

    @staticmethod
    def get_store_manager_props(store_path):
        """Given a path, look for the 'hashstore.yaml' configuration file and return a dictionary
        that contains the properties found in the config file.
        
        :param str path_to_data_folder: Path to the folder containing data objects to store.
        :return: Dictionary containing store manager properties
        """
        hashstore_yaml_path = store_path + "/hashstore.yaml"
        if not os.path.isfile(hashstore_yaml_path):
            err_msg = "'hashstore.yaml' not found in store root path."
            raise FileNotFoundError(err_msg)

        storemanager_props = {}
        try:
            with open(hashstore_yaml_path, "r", encoding="utf-8") as hs_yaml_file:
                storemanager_props = yaml.safe_load(hs_yaml_file)
                storemanager_props["store_type"] = "HashStore"
                storemanager_props["store_path"] = store_path
        except Exception as ge:
            raise RuntimeError(
                f"Unexpected exception while trying to read 'hashstore.yaml' from store_path: {ge}"
            ) from ge

        return storemanager_props

    @staticmethod
    def get_data_object_system_metadata(identifier: str, member_node: str):
        """Retrieve the system metadata for a data object with the given identifier and
        member node endpoint

        :param str identifier: The persistent identifier to retrieve data pids for
        :param str member_node: The member node whose URL to query (ex. 'urn:node:ARCTIC')
        :return: A tuple containing:
            - data_obj_file_name (str): File name of the data object.
            - system_metadata (bytes): Data object's system metadata.
        :rtype: tuple
        """
        member_node_url = checks.get_member_node_url(member_node)
        encoded_identifier = urllib.parse.quote(identifier)
        sysmeta_query = f"/meta/{encoded_identifier}"
        query_url = member_node_url + sysmeta_query

        system_metadata = None
        data_obj_file_name = None
        try:
            # Create a request and parse response for the associated data pids (objects)
            req = urllib.request.Request(query_url)

            # Send the request and read the response
            with urllib.request.urlopen(req) as response:
                # Read and decode the response
                system_metadata = response.read()
                # pylint: disable=I1101
                root = etree.fromstring(system_metadata)

        except Exception as ge:
            raise RuntimeError(f"Unexpected exception encountered: {ge}") from ge

        for elem in root.iter():
            if elem.tag.endswith("fileName"):
                data_obj_file_name = elem.text
                break

        return data_obj_file_name, system_metadata

    def import_data_to_hashstore(self, metadata_sysmeta_path: str, path_to_data_folder: str):
        """Takes a dataset metadata sysmeta document and retrieves the associated data pids, and
        then parses the given path to the data folder to store the data objects into the metadig-py
        hashstore. The system metadata for each data object is also retrieved and stored.

        :param str metadata_sysmeta_path: Path to the sysmeta for the XML metadata document.
        :param str path_to_data_folder: Path to the folder containing data objects to store.
        :return: The result of the suite function.
        """
        # Read the sysmeta
        sysmeta_vars = checks.get_sysmeta_vars(metadata_sysmeta_path)
        identifier = sysmeta_vars.get("identifier")
        auth_mn_node = sysmeta_vars.get("authoritative_member_node")
        data_pids = checks.get_data_pids(identifier, auth_mn_node)

        if len(data_pids) == 0:
            raise ValueError(f"No data pids found for identifier: {identifier}")
        else:
            # Initialize the default hashstore
            mcdu = MetaDigClientUtilities()

            # Store the data object and system metadata
            for pid in data_pids:
                data_obj_name, sysmeta = self.get_data_object_system_metadata(
                    identifier, auth_mn_node
                )
                ## TODO: Find the file name in the given folder
                ## TODO: Store the data object
                ## TODO: Store the data object for the system metadata
                # mcdu.default_store.store_metadata(pid, sysmeta)
            return

def main():
    """Entry point of the Metadig client."""
    # Set-up parser and retrieve arguments
    parser = MetaDigPyParser()
    args = parser.get_parser_args()

    run_check = getattr(args, "run_check")
    store_path = getattr(args, "hashstore_path")
    check_xml_path = getattr(args, "checkxml_path")
    metadata_doc_path = getattr(args, "metadatadoc_path")
    sysmeta_path = getattr(args, "sysmeta_path")
    if run_check:
        if store_path is None:
            raise ValueError("'-store_path' arg is required")
        if check_xml_path is None:
            raise ValueError("'-check_xml' arg is required")
        if metadata_doc_path is None:
            raise ValueError("'-metadata_doc' arg is required")
        if sysmeta_path is None:
            raise ValueError("'-sysmeta_doc' arg is required")

        # Get the store configuration from the given config file at the store_path
        storemanager_props = MetaDigClientUtilities.get_store_manager_props(store_path)

        # Run the check
        result = checks.run_check(
            check_xml_path, metadata_doc_path, sysmeta_path, storemanager_props
        )
        print(result)
        return

if __name__ == "__main__":
    main()
