import xml.etree.ElementTree as ET


def read_sysmeta_element(stream, element):

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
