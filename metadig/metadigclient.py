#!/usr/bin/env python
"""Metadig Command Line App"""
from argparse import ArgumentParser

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

    def get_parser_args(self):
        """Get command line arguments."""
        return self.parser.parse_args()

def main():
    """Entry point of the Metadig client."""
    print("The poetry install worked.")

    parser = MetaDigPyParser()
    args = parser.get_parser_args()

    run_check = getattr(args, "run_check")
    store_path = getattr(args, "hashstore_path")
    check_xml_path = getattr(args, "checkxml_path")
    metadata_doc_path = getattr(args, "metadatadoc_path")
    print(run_check)
    print(store_path)
    print(check_xml_path)
    print(metadata_doc_path)
    return
