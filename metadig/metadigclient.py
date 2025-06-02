#!/usr/bin/env python
"""Metadig Command Line App"""
import os
import io
from typing import Optional
from pathlib import Path
from argparse import ArgumentParser
import urllib.parse
import yaml
from lxml import etree
from hashstore import HashStoreFactory
from hashstore.filehashstore import HashStoreRefsAlreadyExists
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
        self.parser.add_argument(
            "-runsuite",
            dest="run_suite",
            action="store_true",
            help="Flag to run a suite through the MetaDIG-py client",
        )
        self.parser.add_argument(
            "-importhashstoredata",
            dest="import_hashstore_data",
            action="store_true",
            help="Flag to run import data to a hashstore using the MetaDIG-py client",
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
            help="Path to document to the sysmeta to retrieve the identifier and member node.",
        )
        self.parser.add_argument(
            "-datafolder",
            "-data_folder",
            dest="data_folder_path",
            help="Path to folder containining the desired data objects to upload to hashstore.",
        )

    def get_parser_args(self):
        """Get command line arguments."""
        return self.parser.parse_args()


class MetaDigClientUtilities:
    """Class to assist the metadig client with running checks and/or suites."""

    def __init__(self):
        """Initialize the default properties for the MetaDigClientUtilities (ex. hashstore)"""
        default_hashstore_path = os.getcwd() + "/hashstore"
        self.default_store_props = self.get_store_manager_props(default_hashstore_path)
        hashstore_factory = HashStoreFactory()
        module_name = "hashstore.filehashstore"
        class_name = "FileHashStore"
        self.default_store = hashstore_factory.get_hashstore(
            module_name, class_name, self.default_store_props
        )

    def get_hashstore_from_factory(self, hashstore_path):
        """Get a hashstore that is ready to store objects and metadata at the given store path."""
        self.get_store_manager_props(hashstore_path)
        hashstore_factory = HashStoreFactory()
        module_name = "hashstore.filehashstore"
        class_name = "FileHashStore"
        hashstore = hashstore_factory.get_hashstore(
            module_name, class_name, self.default_store_props
        )
        return hashstore

    @staticmethod
    def get_store_manager_props(store_path) -> dict:
        """Given a path, look for the 'hashstore.yaml' configuration file and return a dictionary
        that contains the properties found in the config file.
        
        :param str path_to_data_folder: Path to the folder containing data objects to store.
        :return: Dictionary containing store manager properties
        :rtype: Dict
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

    def get_data_object_system_metadata(
        self, identifier: str, member_node: str, data_folder: str = None
    ) -> tuple:
        """Retrieve the system metadata for a data object with the given identifier and
        member node endpoint

        :param str identifier: The persistent identifier to retrieve data pids for
        :param str member_node: The member node whose URL to query (ex. 'urn:node:ARCTIC')
        :param str data_folder: The folder to attempt to try and find the sysmeta file in
        :return: A tuple containing:
            - data_obj_file_name (str): File name of the data object.
            - system_metadata (bytes): Data object's system metadata.
        :rtype: tuple
        """
        data_obj_file_name = None
        system_metadata = None
        sysmeta_etree = None
        # First, try to find the file in the given data folder
        path_to_sysmeta_file = None
        if data_folder is not None:
            sysmeta_to_find = f"sysmeta-{identifier.replace(':','_')}.xml"
            path_to_sysmeta_file = self.find_file(data_folder, sysmeta_to_find)

        # If a path was found to the system metadata document, read it and set variables
        if path_to_sysmeta_file is not None:
            with open(path_to_sysmeta_file, "rb") as f:
                system_metadata = f.read()
                # pylint: disable=I1101
                sysmeta_etree = etree.fromstring(system_metadata)
        else:
            # If not, retrieve the system metadata from the DataONE API
            member_node_url = checks.get_member_node_url(member_node)
            encoded_identifier = urllib.parse.quote(identifier)
            sysmeta_query = f"/meta/{encoded_identifier}"
            query_url = member_node_url + sysmeta_query
            try:
                # Create a request and parse response for the associated data pids (objects)
                req = urllib.request.Request(query_url)

                # Send the request and read the response
                with urllib.request.urlopen(req) as response:
                    # Read and decode the response
                    system_metadata = response.read()
                    # pylint: disable=I1101
                    sysmeta_etree = etree.fromstring(system_metadata)

            except Exception as ge:
                raise RuntimeError(f"Unexpected exception encountered: {ge}") from ge

        for elem in sysmeta_etree.iter():
            if elem.tag.endswith("fileName"):
                data_obj_file_name = elem.text
                break

        return data_obj_file_name, system_metadata

    @staticmethod
    def find_file(folder_to_check: str, file_to_find: str) -> Path:
        """Check the supplied folder for the given file and return its full path. This function
        will also search subfolders.

        :param str folder_to_check: Folder that contains data files
        :param str file_to_find: The data file to look for
        :return: Path to the data object
        :rtype: Path
        """
        folder_path = Path(folder_to_check)
        for path in folder_path.rglob(file_to_find):
            return path
        # If nothing is found
        return None

    def import_data_to_hashstore(
        self,
        metadata_sysmeta_path: str,
        path_to_data_folder: str,
        hashstore_path: Optional[str] = None,
    ) -> list:
        """Takes a dataset metadata sysmeta document and retrieves the associated data pids, and
        then parses the given path to the data folder to store the data objects into the metadig-py
        hashstore. The system metadata for each data object is also retrieved and stored.

        :param str metadata_sysmeta_path: Path to the sysmeta for the XML metadata document.
        :param str path_to_data_folder: Path to the folder containing data objects to store.
        :param str hashstore_path: Path to a hashstore to store into.
        :return: The data pids that were stored
        :rtype: list
        """
        # Read the sysmeta
        sysmeta_vars = checks.get_sysmeta_vars(metadata_sysmeta_path)
        identifier = sysmeta_vars.get("identifier")
        auth_mn_node = sysmeta_vars.get("authoritative_member_node")
        data_pids = checks.get_data_pids(identifier, auth_mn_node)

        if len(data_pids) == 0:
            raise ValueError(f"No data pids found for identifier: {identifier}")
        else:
            # Store the data object and system metadata
            for pid in data_pids:
                # Retrieve the system metadata (to be stored) and parse it for the file name
                data_obj_name, sysmeta = self.get_data_object_system_metadata(
                    pid, auth_mn_node, path_to_data_folder
                )
                data_object_path = self.find_file(path_to_data_folder, data_obj_name)
                if data_object_path is not None:
                    # Determine hashstore to use
                    if hashstore_path is not None:
                        target_hashstore = self.get_hashstore_from_factory(hashstore_path)
                    else:
                        target_hashstore = self.default_store
                    # Import data to hashstore
                    try:
                        target_hashstore.store_object(pid, data_object_path)
                    except HashStoreRefsAlreadyExists as hsrae:
                        print(
                            f"Data object already found in hashstore for pid: {pid}. {hsrae}"
                        )
                    # pylint: disable=W0718
                    except Exception as e:
                        raise RuntimeError(
                            f"Unexpected exception while attempting to store data object: {e}"
                        ) from e

                    try:
                        sysmeta_file_like_object = io.BytesIO(sysmeta)
                        sysmeta_file_like_object.name = pid + ".xml"
                        target_hashstore.store_metadata(
                            pid, sysmeta_file_like_object
                        )
                    # pylint: disable=W0718
                    except Exception as e:
                        raise RuntimeError(
                            f"Unexpected exception while attempting to store data metadata: {e}"
                        ) from e
                else:
                    print(
                        f"Data object not found: {data_obj_name} in folder: {path_to_data_folder}"
                    )
            return data_pids


def main():
    """Entry point of the Metadig client."""
    # Set-up parser and retrieve arguments
    mcdu = MetaDigClientUtilities()
    parser = MetaDigPyParser()
    args = parser.get_parser_args()

    run_check = getattr(args, "run_check")
    store_path = getattr(args, "hashstore_path")
    check_xml_path = getattr(args, "checkxml_path")
    metadata_doc_path = getattr(args, "metadatadoc_path")
    sysmeta_path = getattr(args, "sysmeta_path")
    import_hashstore_data = getattr(args, "import_hashstore_data")
    data_folder_path = getattr(args, "data_folder_path")
    if run_check:
        if store_path is None:
            raise ValueError("'-store_path' arg is required to run a check")
        if check_xml_path is None:
            raise ValueError("'-check_xml' arg is required to run a check")
        if metadata_doc_path is None:
            raise ValueError("'-metadata_doc' arg is required to run a check")
        if sysmeta_path is None:
            raise ValueError("'-sysmeta_doc' arg is required to run a check")

        # Get the store configuration from the given config file at the store_path
        storemanager_props = mcdu.get_store_manager_props(store_path)

        # Run the check
        result = checks.run_check(
            check_xml_path, metadata_doc_path, sysmeta_path, storemanager_props
        )
        print(result)
        return
    if import_hashstore_data:
        if data_folder_path is None:
            raise ValueError("'-data_folder' arg is required to import hashstore data")
        if sysmeta_path is None:
            raise ValueError("'-sysmeta_doc' arg is required to import hashstore data")
        # If 'store_path' is None, we will use the default hashstore that ships with metadig-py

        # Parse the sysmeta for the data pids, retrieve the system metadata and store
        # both the data objects and their respective sysmeta to hashstore
        data_pids_stored = mcdu.import_data_to_hashstore(
            sysmeta_path, data_folder_path, store_path
        )
        print(f"Data objects have been stored for pids: {data_pids_stored}")
        return

if __name__ == "__main__":
    main()
