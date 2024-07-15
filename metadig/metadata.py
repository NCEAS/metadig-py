import xml.etree.ElementTree as ET


def read_sysmeta_element(stream, element):
    """
    Reads and parses a stream of system metadata to find and return the text value of a specified element.

    Args:
        stream (BufferedReader): A stream containing system metadata.
        element (str): The name of the element to retrieve.

    Returns:
        str or None: The text content of the found element, or None if not found.

    Raises:
        ValueError: If there is an error parsing the sysmeta or if the specified element is not found.
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
        raise ValueError(f"Error parsing XML: {e}, could not find element {element}")


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
        xml.etree.Element: The XML element (dataTable or otherEntity) that matches the identifier or fileName,
        according to the specified priority (id, entityName, objectName). Returns None if no match is found.
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
