#!/usr/bin/env python
"""Metadig Command Line App"""
import os
from argparse import ArgumentParser
import yaml
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

        # Run the check
        result = checks.run_check(
            check_xml_path, metadata_doc_path, sysmeta_path, storemanager_props
        )
        print(result)
        return

if __name__ == "__main__":
    main()
