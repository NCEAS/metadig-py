"""Metadig metadata utilities"""

import xml.etree.ElementTree as ET
import io
import pandas as pd


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
        fileName (str): File name to match against the entityName or objectName elements.

    Returns:
        xml.etree.Element: The XML element (dataTable or otherEntity) that matches the
        identifier or fileName, according to the specified priority (id, entityName, objectName).
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
    Returns an input stream for a given pid if the file is a csv file, along with it's
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
    fname = read_sysmeta_element(sys, "fileName")
    if read_sysmeta_element(sys, "formatId") != "text/csv":
        return None, fname, "SKIP"
    return obj, fname, "VALID"

def find_entity_index(fname, pid, entity_names, ids):
    """
    Finds the index of a documented entity from a list of entities in a metadata document. The
    function will first try to match based on filename, then identifier. Returns none if no match.

    Args:
        fname (str): Filename of the file to match.
        pid (str): Identifier of file to match.
        entity_names: List of entity names to search for filename in
        ids: List of idenfitiers to search for identifier in

    Returns:
        z: Index of matching entity in documentation.
        
    """
    z = [i for i, x in enumerate(entity_names) if x == fname]
    if not z:
        z = [i for i, x in enumerate(ids) if x == pid.replace(":", "-")]

    if len(z) > 1:
        z = z[0]
    return z if z else None

def read_csv_with_metadata(d_read, fd, skiprows):
    """
    Uses pandas to read in a csv with given field delimiter and header rows to skip

    Args:
        d_read: Data as read in from the stream 
        fd (str): Field delimiter from metadata
        skiprows (int): Number of rows to skip

    Returns:
        df: Pandas data.frame with data
        error: error message on exception
        
    """
    delimiter = "," if fd is None else fd[0]
    header = 0 if skiprows is None else int(skiprows[0]) - 1
    try:
        return pd.read_csv(io.StringIO(d_read), delimiter=delimiter, header=header), None
    # pylint: disable=W0718
    except Exception as e:
        return None, f"Error reading CSV: {str(e)}"
