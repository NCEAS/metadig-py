"""Metadig suite utilities"""

import os
import multiprocessing
import json
from typing import Dict, Any, Optional
from datetime import datetime
from lxml import etree
import metadig.checks as checks


def does_file_exist(path_to_check: str):
    """Check to see whether the file exists in the system."""
    if os.path.isfile(path_to_check):
        return True
    else:
        return False


def map_and_get_check_ids_to_files_and_env(path_to_checks: str):
    """Given a path to a directory of metadig checks, open each check and map the id
    to the file path.
    
    :param str path_to_checks: Path to the folder containing metadig checks
    :return: Tuple of two dictionaries:
         (1) a dictionary mapping check ids to file paths,
         (2) a dictionary mapping check ids to check environment
    """
    id_to_path_dict = {}
    id_to_env_dict = {}

    for filename in os.listdir(path_to_checks):
        if filename.endswith(".xml"):
            file_path = os.path.join(path_to_checks, filename)

            try:
                # pylint: disable=I1101
                tree = etree.parse(file_path)
                root = tree.getroot()

                # Get the file path that matches the id
                id_elem = root.find("id")
                if id_elem is not None and id_elem.text:
                    check_id = id_elem.text.strip()
                    id_to_path_dict[check_id] = file_path
                else:
                    print(f"Warning: No <id> found in {file_path}")
                # Get the environment of the check
                env_elem = root.find("environment")
                env_elem_txt = env_elem.text
                if env_elem is not None and env_elem_txt:
                    check_id = id_elem.text.strip()
                    id_to_env_dict[check_id] = env_elem_txt
                else:
                    print(f"Warning: No <environment> found in {file_path}") 
            # pylint: disable=W0718
            except Exception as e:
                # If there is an unexpected exception, add it to the dict with an err msg
                check_id = id_elem.text.strip() if id_elem is not None and id_elem.text else None
                id_to_path_dict[check_id] = f"Error parsing {file_path}: {e}"

    return id_to_path_dict, id_to_env_dict


def run_suite(
    suite_path: str,
    checks_path: str,
    metadata_xml_path: str,
    metadata_sysmeta_path: str,
    store_props: Optional[Dict[str, Any]] = None,
):
    """Run a metadig-check suite which can contain multiple checks.
    
    :param str suite_path: Path to the suite xml containing the checks to run.
    :param str checks_path: Path to the checks found in the suite to be executed.
    :param str metadata_xml_path: Path to the XML metadata document.
    :param str metadata_sysmeta_path: Path to the sysmeta for the XML metadata document
    :param Dict store_props: Dictionary containing the store properties: store_type, store_path,
        store_depth, store_width, store_algorithm, store_metadata_namespace
    :return: The result of the suite function.
    """
    # Confirm files exist at the given paths
    if not does_file_exist(suite_path):
        raise FileNotFoundError(f"Suite path not found: {suite_path}")
    if not does_file_exist(metadata_xml_path):
        raise FileNotFoundError(f"Metadata not found: {metadata_xml_path}")
    if not does_file_exist(metadata_sysmeta_path):
        raise FileNotFoundError(f"Metadata sysmeta not found: {metadata_sysmeta_path}")

    # Read the suite_path & get the checks to run
    # pylint: disable=I1101
    suite_doc = etree.parse(suite_path).getroot()

    # Create list of checks to run
    checks_to_run_list = []
    # And a list of messages to include if there are issues
    additional_run_comments = []
    check_file_map, check_env_map = map_and_get_check_ids_to_files_and_env(checks_path)
    for check in suite_doc.findall("check"):
        check_id = check.find("id").text
        check_env = check_env_map.get(check_id)
        check_id_path = check_file_map.get(check_id)
        # 'run_suite' only executes python checks
        if check_env == "python":
            if check_id_path is None:
                additional_run_comments.append(
                    f"Check not found in check map for check: {check_id}"
                )
            elif does_file_exist(check_id_path):
                check_tuple_item = (
                    check_id_path,
                    metadata_xml_path,
                    metadata_sysmeta_path,
                    store_props,
                )
                checks_to_run_list.append(check_tuple_item)
            else:
                additional_run_comments.append(
                    f"Check not found at path: {check_id_path}"
                )
        else:
            additional_run_comments.append(
                f"Check environment ({check_env}) incompatible for check: {check_id}"
            )

    if not checks_to_run_list:
        raise RuntimeError("No checks to run. Details: " + additional_run_comments)

    # Set up multiprocessing pool
    pool = multiprocessing.Pool()
    results = pool.imap(checks.try_run_check, checks_to_run_list)
    pool.close() # Close the pool and wait for all processes to complete
    pool.join()

    # Gather variables to add to suite results
    check_results = []
    for result, check_id, msg in results:
        if result is None:
            check_results.append({
                "check_id": check_id,
                "identifiers": "N/A",
                "output": f"Unexpected exception: {msg}",
                "status": "ERROR",
            })
        else:
            result_data = json.loads(result)
            check_results.append({
                "check_id": check_id,
                "identifiers": result_data.get("identifiers", ["N/A"]),
                "output": result_data.get("output"),
                "status": result_data.get("status"),
            })
    suite_name = suite_path.rsplit("/", 1)[-1]
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    metadata_sysmeta = checks.get_sysmeta_vars(metadata_sysmeta_path)
    sysmeta = {
        "origin_member_node": metadata_sysmeta.get("authoritative_member_node"),
        "rights_holder": metadata_sysmeta.get("rights_holder"),
        "date_uploaded": metadata_sysmeta.get("date_uploaded"),
        "format_id": metadata_sysmeta.get("format_id"),
        "obsoletes": metadata_sysmeta.get("obsoletes"),
    }
    # Format results
    suite_results = {
        "suite": suite_name,
        "timestamp": timestamp,
        "object_identifier": metadata_sysmeta.get("identifier"),
        "run_status": "SUCCESS" if check_results else "FAILURE",
        "run_comments": additional_run_comments,
        "sysmeta": sysmeta,
        "results": check_results
    }
    json_suite_results = json.dumps(suite_results, indent=4)
    # print(json_suite_results)
    return json_suite_results
