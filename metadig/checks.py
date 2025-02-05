"""Metadig check utilities
"""

import json
import subprocess
import sys
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
from types import SimpleNamespace
from urllib.parse import urlparse
from lxml import etree


def getType(object):
    print("type: {}".format(type(object)))


def isResolvable(url):
    # First parse the url for a protocol, host port and path
    """Function that checks if a url is resolvable

    The function first checks if the url uses HTTP protocols, which is
    currently the only protocol supported.

    Args:
        url - the url to check for resolvability

    Returns:
        list: the first element is either True or False (i.e. is/is not resolvable)
              the second element is a status message, describing success or an error message.

    """
    # url = 'https://cn.dataone.org/cn/v2/resolve/urn:uuid:7098ba54-ca6f-4e35-beb3-718bd0fe58a8'
    urlComps = urlparse(url)
    location = urlComps.netloc
    if urlComps.netloc == "":
        return (False, '"{}" does not appear to be a URL'.format(url))

    # Check the 'schema' to see if it is an open one. Currently we
    # are just check for http and https.
    knownProtocols = ["http", "https"]
    if urlComps.scheme not in set(knownProtocols):
        return (
            False,
            'Unknown or proprietary communications protocol: "{}", known protocols: {}'.format(
                urlComps.scheme, ", ".join(knownProtocols)
            ),
        )

    # Perform an HTTP 'Head' request - we just want to know if the file exists and do not need to
    # download it.
    request = urllib.request.Request(url)
    request.get_method = lambda: "HEAD"
    # Python urllib2 strangly throws an error for an http status, and the response object is returned
    # by the exception code.
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as he:
        # An error was encountered resolving the url, check which one so that we can print
        # a more meaningful error message than provided by HTTPError
        # FYI, HTTP status codes (from FAIR FM_A1.1 https://github.com/FAIRMetrics/Metrics/blob/master/Distributions/FM_A1.1.pdf)
        if he.code == 400:
            return (False, "Unable to resolved URL {}: Bad request".format(url))
        elif he.code == 401:
            return (False, "Unable to resolved URL {}: Unauthorized".format(url))
        elif he.code == 404:
            return (False, "Unable to resolved URL {}: Not Found".format(url))
        elif he.code == 500:
            return (False, "Unable to resolved URL {}: Server Error".format(url))
        else:
            return (
                False,
                'Error resolving URL "{}": {} {}'.format(url, he.code, he.headers),
            )
    except urllib.error.URLError as ue:
        return (False, ue.reason[1])
    except Exception as e:
        return (False, repr(e))
    except OSError as oe:
        return (False, repr(oe))
    except:
        return (False, "Unexpected error:", sys.exc_info()[0])

    response.close()
    if response.code in set([200, 202, 203, 206, 301, 302, 303, 307, 308]):
        return (
            True,
            "Successfully resolved the URL {}: status {}".format(url, response.code),
        )
    else:
        return (False, "Did not resolved the URL {}".format(url))


def run_check(check_xml_path: str, metadata_xml_path: str):
    """
    Run a validation check against an XML metadata document.

    :param check_xml_path: Path to the XML file containing the check configuration.
    :param metadata_xml_path: Path to the XML metadata document.
    :return: The result of the check function.
    """
    # Load the metadata and check XML files
    metadata_doc = etree.parse(metadata_xml_path).getroot()
    metadata_doc_no_ns = etree.parse(metadata_xml_path).getroot()

    # Remove namespaces
    for elem in metadata_doc_no_ns.iter():
        if elem.tag.startswith("{") and not elem.tag.startswith("{http://www.w3.org/2001/XMLSchema-instance}"):
            elem.tag = elem.tag.split('}', 1)[1]  # Remove namespace

    # Load the check XML
    check_doc = etree.parse(check_xml_path).getroot()

    # Ensure the check is valid
    check_id_elem = check_doc.xpath(".//id")
    check_id = check_id_elem[0].text if check_id_elem else "Unknown"

    if not is_check_valid(check_doc, metadata_doc):
        print(f"Check {check_id} is not valid for metadata document {metadata_xml_path}")
        return

    # Extract selectors and apply them
    selectors = check_doc.xpath(".//selector")
    check_vars = {}

    # todo: replace all this hardcoded proof of concept stuff with something that makes sense
    check_vars['dataPids'] = ["urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1"]
    check_vars['storeConfiguration'] = {
         "store_type": "HashStore",
        "store_path": "/Users/clark/Documents/metacat-hashstore",
        "store_depth": "3",
        "store_width": 2,
        "store_algorithm": "SHA-256",
        "store_metadata_namespace": "https://ns.dataone.org/service/types/v2.0#SystemMetadata",
    }

    if not selectors:
        raise ValueError("No selectors are defined for this check.")

    # Extract the information from selectors
    for selector in selectors:
        selector_xpath = selector.xpath("xpath")[0].text
        selector_name = selector.xpath("name")[0].text


        ns_aware_elem = selector.get("namespaceAware")
        ns_aware = ns_aware_elem and ns_aware_elem[0].text.lower() == "true"
        metadata_doc_to_use = metadata_doc if ns_aware else metadata_doc_no_ns

        variable_list = select_nodes(metadata_doc_to_use, selector)

        check_vars[selector_name] = variable_list

    # Execute check function
    result = None
    code_elem = check_doc.xpath("code")
    if code_elem:
        code_str =f"""
import json
locals().update({json.dumps(check_vars)})
""" + code_elem[0].text + "\ncall()"


    result = subprocess.run(
        [sys.executable, "-c", code_str],
        capture_output=True,
        text=True,
        check=True
    )

    # with the subprocess, the only way to get the output out is to print to stdout and then parse it
    # there must be a better way to do this - maybe with a sub environment instead? I'm not sure how this
    # works in python


def is_check_valid(check_doc, metadata_doc):
    """
    Check if the given check document is valid for the metadata document.

    :param check_doc: XML representing the check document.
    :param metadata_doc: XML representing the metadata document.
    :return: True if valid, False otherwise.
    """
    dialect_nodes = check_doc.xpath("dialect")
    if dialect_nodes:
        for dialect_node in dialect_nodes:
            dialect_name_elem = dialect_node.xpath("name")
            dialect_xpath_elem = dialect_node.xpath("xpath")

            if dialect_name_elem and dialect_xpath_elem:
                dialect_xpath = dialect_xpath_elem[0].text
                dialect_match_node = metadata_doc.xpath(dialect_xpath)

                if dialect_match_node:
                    return True
        return False
    # If no dialect specified, assume check is valid for all metadata
    return True


def ns_strip(xml_doc, ns_prefix):
    """
    Strip the specified namespace from a document.

    :param xml_doc: The document to strip.
    :param ns_prefix: The namespace prefix to strip.
    :return: XML document without the specified namespace.
    """
    xpath_str = f".//namespace::*[name()='{ns_prefix}']/parent::*"
    for element in xml_doc.xpath(xpath_str):
        ns_decl = f"xmlns:{ns_prefix}"
        if ns_decl in element.attrib:
            del element.attrib[ns_decl]
    return xml_doc


def select_nodes(context_node, selector_context):
    """
    Select data values from a metadata document as specified in a check's selectors.

    :param context_node: Metadata document node.
    :param selector_context: Selector node defining the extraction criteria.
    :return: List of selected node values.
    """
    if selector_context is None:
        return []
    values = []
    selector_xpath = selector_context.xpath("xpath")[0].text
    sub_selector = selector_context.xpath("subSelector")

    selected_nodes = context_node.xpath(selector_xpath)
    if not selected_nodes:
        return values

    for node in selected_nodes:
        if sub_selector:
            value = select_nodes(node, sub_selector[0])
        else:
            if hasattr(node, 'text') and node.text is not None:
                text_val = node.text
            else:
                text_val = node
            try:
                value = float(text_val)
            except (ValueError, TypeError):
                if text_val == "True":
                    value = True
                elif text_val == "False":
                    value = False
                else:
                    value = text_val
        values.append(value)

    return values
