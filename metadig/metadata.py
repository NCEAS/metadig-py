"""Metadig metadata utilities"""

import xml.etree.ElementTree as ET
import io
import hashlib
import pandas


def read_sysmeta_element(stream, element):
    """
    Reads and parses a stream of system metadata to find and return the text value
    of a specified element.

    Args:
        stream (BufferedReader): A stream containing system metadata.
        element (str): The name of the element to retrieve.

    Returns:
        str or None: The text content of the found element, or None if not found.

    Raises:
        ValueError: If there is an error parsing the sysmeta or if the specified
        element is not found.
    """
    try:
        # Parse the XML from the buffered reader
        stream.seek(0)
        tree = ET.parse(stream)
        root = tree.getroot()

        # Find the specified element and return its text value
        for elem in root.findall(element):
            return elem.text

    except ET.ParseError as e:
        raise ValueError(f"Error parsing XML: {e}, could not find element {element}") from e


def find_eml_entity(doc, identifier, file_name):
    """
    Searches through a string EML document to find and return dataTable and otherEntity elements
    that matches the identifier or fileName according to specified priority. The function will
    try to match first from identifier to the id element, then by file_name to entityName, then
    to objectName.

    Args:
        doc (str): XML document as a string.
        identifier (str): Identifier to match against the id element.
        file_name (str): File name to match against the entityName or objectName elements.

    Returns:
        xml.etree.Element: The XML element (dataTable or otherEntity) that matches the
        identifier or file_name, according to the specified priority (id, entityName, objectName).
        Returns None if no match is found.
    """

    root = ET.fromstring(doc)

    # Search through dataTable and otherEntity elements
    for element in root.findall(".//dataTable") + root.findall(".//otherEntity"):
        # Check if identifier matches the id element
        id_elem = element.find(".//id")
        if id_elem is not None and id_elem.text == identifier:
            return element

        # Check if fileName matches the entity name element
        entity_name_elem = element.find(".//entityName")
        if entity_name_elem is not None and entity_name_elem.text == file_name:
            return element

        # Check if fileName matches the object name element
        object_name_elem = element.find(".//objectName")
        if object_name_elem is not None and object_name_elem.text == file_name:
            return element

    # Return None if no match is found
    return None


def get_valid_csv(manager, pid):
    """
    Returns an input stream for a given pid if the file is a csv file, along with its
    filename and a status.

    Args:
        manager: a store manager returned from StoreManager()
        pid (str): Identifier of file to return.

    Returns:
        obj: An input stream object
        fname: The filename of the object
        status: SKIP or VALID. Returns skip if not a csv.
        
    """
    obj, sys = manager.get_object(pid)
    try:
        fname = read_sysmeta_element(sys, "fileName")
        if read_sysmeta_element(sys, "formatId") != "text/csv":
            return None, fname, "SKIP"
    finally:
        sys.close()
    return obj, fname, "VALID"

def find_entity_index(fname, pid, entity_names, ids):
    """
    Finds the index of a documented entity from a list of entities in a metadata document. The
    function will first try to match based on filename, then identifier. Returns none if no match.

    Args:
        fname (str): Filename of the file to match.
        pid (str): Identifier of file to match.
        entity_names: List of entity names to search for filename in
        ids: List of identifiers to search for identifier in

    Returns:
        z: Index of matching entity in documentation.

    """
    # Checks all elements in entity_names to find matches with fname
    z = [i for i, x in enumerate(entity_names) if x == fname]
    # If z is empty, we will try to match by pid instead
    if not z:
        z = [i for i, x in enumerate(ids) if x == pid.replace(":", "-")]

    # If there are multiple matches, we will return the first one
    if len(z) > 1:
        z = z[0]
    # If a single match is found, [0] is the value returned
    return z if z else None

def read_csv_with_metadata(d_read, fd, header_line):
    """
    Uses pandas to read in a csv with given field delimiter and header rows to skip

    Args:
        d_read: Data as read in from the stream 
        fd (str): Field delimiter from metadata
        header_line (int): Number of rows to skip

    Returns:
        df: Pandas data.frame with data
        error: error message on exception
        
    """
    # Ensure fd is an int or str
    if isinstance(fd, list):
        fd = fd[0]  # Extract first element if list
    if not isinstance(fd, (str, int)):
        fd = ","  # Default to comma if invalid type

    pd_header_val = 0
    if isinstance(header_line, list):
        # When a list is provided, the expectation is that this value is coming from the sysmeta
        # We will extract the first element and cast it into an integer, this number is usually 1
        try:
            first_element_from_list = int(header_line[0])
        except (ValueError, TypeError) as vte:
            raise ValueError(
                f"Unable to retrieve a numeric value from skiprows. Details: {vte}"
            ) from vte
        # We subtract 1 to standardize this value to pass onto pandas.read_csv
        pd_header_val = max(0, first_element_from_list - 1) # Ensure it is never negative
    elif isinstance(header_line, int):
        if header_line > 0:
            pd_header_val = header_line - 1
    else:
        error_msg = (
            "Unable to read CSV, cannot determine 'header_line'. It must be an integer."
            + f" Detected type: {type(header_line)}. Value: {header_line}"
        )
        return None, error_msg

    try:
        return pandas.read_csv(io.StringIO(d_read), delimiter=fd, header=pd_header_val), None
    # pylint: disable=W0718
    except Exception as e:
        return None, f"Error reading CSV: {str(e)}"


def find_duplicate_columns(pandas_df):
    """Find duplicate columns in a .CSV file by calculating the hash of the column.
    
    :param df pandas_df: Data frame to check for duplicate columns
    :return: List of duplicate columns
    """

    def hash_series(series):
        """Get the hash based on the column's values, ignoring the index"""
        return hashlib.md5(
            pandas.util.hash_pandas_object(series, index=False).values
        ).hexdigest()

    seen_hashes = {}
    duplicates = []

    for col in pandas_df.columns:
        col_hash = hash_series(pandas_df[col])
        if col_hash in seen_hashes:
            duplicates.append((col, seen_hashes[col]))
        else:
            seen_hashes[col_hash] = col

    return duplicates
