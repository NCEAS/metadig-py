# MetaDIG-py - A python client package for assisting with running MetaDIG checks

MetaDIG-Py is a library that contains helper functions and classes to assist users with writing 
python checks for suites in [metadig-checks](https://github.com/NCEAS/metadig-checks).

## Contributors

- **Author**: Jeanette Clark, Dou Mok, Peter Slaughter
- **License**: [Apache 2](http://opensource.org/licenses/Apache-2.0)
- [Package source code on GitHub](https://github.com/NCEAS/metadig-py)
- [**Submit Bugs and feature requests**](https://github.com/NCEAS/metadig-py/issues)
- Contact us: support@dataone.org
- [DataONE discussions](https://github.com/DataONEorg/dataone/discussions)

## Introduction

The MetaDIG-py client package contains python modules that users can call when writing checks
for their [`metadig-checks`](https://github.com/NCEAS/metadig-checks). By importing this
package, users get access to all available helper functions and classes, such as `object_store.py`
which enables users to write checks that efficiently retrieves data objects to work with.

## Installation

To install MetaDIG-py, run the following commands

```sh
mkvirtualenv -p python3.9 metadigpy # Create a virtual environment
poetry install # Run poetry command to install dependencies
```
- Note: If you run into an issue with installing jep, it is likely due to a backwards
compatibility issue with `setuptools`. Try downgrading to the version 58.0.0:

  ```sh
 pip install setuptools==58.0.0
  ```

To confirm that you have installed `MetaDIG-py` successfully, run `pytest`.
```sh
pytest
```
- Tip: You may run `pytest` with the option `-s` (ex. `pytest -s`) to see print statements. Not all pytests have print statements, but if you want to extend from what already exists, this may prove to be helpful!

## How do I import the `MetaDIG-py` library?

In your python code, you can import a specific module or function like such:

```py
from metadig import read_sysmeta_element
from metadig import MetaDigClientUtilities as mcdu
```

Currently, we have the following modules and functions available:

```py
"StoreManager", # Class to work with a HashStore
"getType", # fn
"isResolvable", # fn
"isBlank", # fn
"toUnicode", # fn
"read_sysmeta_element", # fn
"find_eml_entity", # fn
"find_entity_index", # fn
"read_csv_with_metadata", # fn
"get_valid_csv", # fn
"detect_text_encoding", # fn
"run_check", # fn
"checks", # Module
"metadata", # Module
"suites", # Module
"MetaDigClientUtilities", = # Module
```

## How do I run an entire check suite (ex. FAIR-suite-0.4.0.xml)?

To run a suite, you must have the path to the suite to run, a path to the folder containing all the checks, the metadata file path and the path to the metadata's system metadata.

```py
from metadig import suites

suite_file_path = "/path/to/FAIR-suite-0.4.0.xml"
checks_path = "path/to/folder/containing/checks"
metadata_file_path = "path/to/metadata:data_file.xml"
sysmeta_file_path = "path/to/metadata:data_sysmeta_file.xml"
# Note: storemanager_props are only relevant if you are executing data checks and has a default value of 'None'. In the example below, we intentionally do not supply an argument for storemanager_props because the 'fair-suite' does not require data objects.

suite_results = suites.run_suite(
    suite_path,
    checks_path,
    sample_metadata_file_path,
    sample_sysmeta_file_path,
)

print(suite_results)

{
    "suite": "FAIR-suite-0.4.0.xml",
    "timestamp": "2025-04-23 12:12:31",
    "object_identifier": "doi:10.18739/A2QJ78081",
    "run_status": "SUCCESS",
    "run_comments": [
        "Check not found: /Users/doumok/Code/metadig-py/tests/testdata/checks/resource.abstractLength.sufficient.1.xml",
        ...
        "Check not found: /Users/doumok/Code/metadig-py/tests/testdata/checks/resource.type.valid.1.xml",
    ],
    "sysmeta": {
        "origin_member_node": "urn:node:ARCTIC",
        "rights_holder": "http://orcid.org/0000-0001-2345-6789",
        "date_uploaded": "2024-07-03T19:46:44.414+00:00",
        "format_id": "https://eml.ecoinformatics.org/eml-2.2.0",
        "obsoletes": "urn:uuid:dou-test-obsoleted"
    },
    "results": [
        {
            "check_id": "metadata.identifier.resolvable-2.0.0.xml",
            "identifiers": [
                "N/A"
            ],
            "output": "The metadata identifier 'urn:uuid:dou-test-obsoleted' was found and is resolvable using the DataONE resolve service.",
            "status": "SUCCESS"
        },
        {
            "check_id": "entity.attributeName.differs-2.0.0.xml",
            "identifiers": [
                "N/A"
            ],
            "output": "All 33 attributes have definitions that differ from the name",
            "status": "SUCCESS"
        },
        {
            "check_id": "provenance.ProcessStepCode.present-2.0.0.xml",
            "identifiers": [
                [
                    "urn:uuid:6a7a874a-39b5-4855-85d4-0fdfac795cd1"
                ]
            ],
            "output": [
                "Unexpected exception while running check: list index out of range"
            ],
            "status": "Unable to execute check."
        },
        {
            "check_id": "resource.license.present-2.0.0.xml",
            "identifiers": [
                "N/A"
            ],
            "output": "The resource license 'This work is dedicated to the public dom...' was found.",
            "status": "SUCCESS"
        }
    ]
}

```


## How do I run a single metadata check?

To run a metadata check, pass the check.xml, metadata file path and metadata's system metadata's file path to the `run_check` function.

```py
from metadig import checks

check_file_path = "/path/to/resource.license.present-2.0.0.xml"
metadata_file_path = "path/to/metadata:data_file.xml"
sysmeta_file_path = "path/to/metadata:data_sysmeta_file.xml"

result = checks.run_check(
    check_file_path,
    metadata_file_path,
    sysmeta_file_path
)
print(result)

{
    "output": "The resource license 'This work is dedicated to the public dom...' was found.",
    "status": "SUCCESS"
}
```

## How to use the MetaDIG-py command line client

The `MetaDIG-py` command line client was created to help users test python checks without having to spin up the java engine `metadig-engine` and run a check through the dispatcher.

After you've installed `MetaDIG-py`, you will have access to the command `metadigpy`. Please see installation section above if you haven't installed `MetaDIG-py`. Below is what running a check looks like:

```sh
metadigpy -runcheck -store_path=/path/to/hashstore -check_xml=/path/to/check_xml -metadata_doc=/path/to/metadata/doc -sysmeta_doc=/path/to/sysmeta
```

To get help and see all the options available, you can run metadigpy with the `-h` flag

```sh
metadigpy -h
```

### How to set up and run a data check through the MetaDig-py command line client

To set up a data check, you must have/prepare the following before you run the `metadigpy` client command (above)
1) A HashStore - note, `MetaDig-py` ships with a default hashstore that is ready to use.

    Please see the section below to learn more.

2) The data objects and their associated system metadata stored into the hashstore

    During the `run_check` process, after retrieving the data pids for the provided identifier, we then retrieve their associated data objects and system metadata from the provided HashStore. If these 'files' are not found, it could cause errors with the check that you're trying to run or test. Note, every data object stored in HashStore must have an equivalent system metadata, and this system metadata describes the basic attributes of the data object.

3) A copy of the metadata document and its respective system metadata for the DOI.

    Every dataset not only has metadata about the dataset (which usually comes in the form of an EML metadata document) but also system metadata for the metadata. For us to run a `metadig` check at this time, we need both the metadata document and its respective system metadata. The system metadata is parsed for the identifier, which is then used to retrieve the appropriate data pids, which is then used in the check.

4) The suite and/or checks you want to run

    Suites and checks can be found in the `metadig-checks` repository. You may check this repo out and then provide the necessary paths for running a suite or check through the `metadigclient`.

#### HashStore 101

  * **Friendly Reminder**: A HashStore is only required if you are running data quality checks

HashStore is a python package developed for DataONE services to efficiently access data objects, metadata and system metadata. In order to simulate the process of retrieving data objects with a `metadig` check, we must mimic the environment in which it happens in production. So the requirement of having a HashStore means that we need to create a HashStore and then store data objects and system metadata inside of it. Please see below for an example:

```sh
# Step 0: Install hashstore via poetry to create an executable script
git clone https://github.com/DataONEorg/hashstore.git /Code/hashstore

poetry install

# Step 1: Create a HashStore at your desired store path (ex. /var/metacat/hashstore)
hashstore /path/to/store/ -chs -dp=3 -wp=2 -ap=SHA-256 -nsp="https://ns.dataone.org/service/types/v2.0#SystemMetadata"

# Store a data object
hashstore /path/to/store/ -storeobject -pid=persistent_identifier -path=/path/to/object

# Store a metadata object
hashstore /path/to/store/ -storemetadata -pid=persistent_identifier -path=/path/to/metadata/object -formatid=https://ns.dataone.org/service/types/v2.0#SystemMetadata
```

On your file system, HashStore looks like a folder with data objects and system metadata stored with hashes based on either a content identifier, or a combination of values that create a unique identifier. To interact with a HashStore and learn more, please see the documentation [here](https://github.com/DataONEorg/hashstore/).

#### How do I use the default HashStore?

`MetaDig-py` ships with a hashstore that can be worked with directly through the command line, or through the `metadigclient`. If you do not provide a path to a hashstore to the `metadigclient`, its associated functions will attempt to search for data objects and sysmeta in the default hashstore found in `/hashstore`. You could also use the default hashstore path in the manual process should you desire to.

##### How do I import my data objects to the default hashstore?

To import data to the default hashstore, you will need the system metadata document for the dataset metadata, and a folder that contains the data objects to import. This folder should contain data objects with the exact name of the data objects that are documented. 

This can be done by viewing your dataset on the member node url (ex. `https://arcticdata.io/catalog/view/doi:...`), downloading the dataset and then extracting its contents. You then copy this path and provide it to the `-data_folder` flag (an example can be found below).

The `-importhashstoredata` process will parse the provided metadata system metadata document for the necessary details to validate, and then store the data objects and its associated system metadata to the default hashstore. 

```sh
metadigpy -importhashstoredata -sysmeta_doc=/path/to/sysmeta -data_folder=/path/to/datset/folder/with/data/objects
```

Now you may run your desired check or suite against the dataset you just imported to the default hashstore.

## Example of the full `MetaDIG-py` command line client process to run a data suite (default hashstore)

```sh
mkvirtualenv -p python3.9 metadigpy // Create a virtual environment
git clone https://github.com/NCEAS/metadig-py.git ~/Code/metadigpy

cd /metadigpy

poetry install // Run poetry command to install dependencies

metadigpy -importhashstoredata -sysmeta_doc=/path/to/sysmeta -data_folder=/path/to/datset/folder/with/data/objects

metadigpy -runsuite -suite_path=/path/to/the/data-suite.xml -check_folder=path/to/the/folder/containing/checks/ -metadata_doc=/path/to/metadata/doc -sysmeta_doc=/path/to/sysmeta

{
  "suite": "data-suite.xml",
  "timestamp": "2025-06-04 12:04:52",
  "object_identifier": "doi:10.18739/A2QJ70000",
  "run_status": "SUCCESS",
  "run_comments": [],
  "sysmeta": {
    "origin_member_node": "urn:node:ARCTIC",
    "rights_holder": "http://orcid.org/0000-0000-0000-0000",
    "date_uploaded": "2024-07-03T19:46:44.414+00:00",
    "format_id": "https://eml.ecoinformatics.org/eml-2.2.0",
    "obsoletes": "urn:uuid:..."
  },
  "results": [
    {
      ...
    },
    ...
  ]
}
```

## Example of the full `MetaDIG-py` command line client process to run a data check (manual hashstore)

```sh
mkvirtualenv -p python3.9 metadigpy // Create a virtual environment
git clone https://github.com/NCEAS/metadig-py.git ~/Code/metadigpy

cd /metadigpy

poetry install // Run poetry command to install dependencies

git clone https://github.com/DataONEorg/hashstore.git ~/Code/hashstore

cd ../hashstore

poetry install

# Step 1: Create a HashStore at your desired store path (ex. /var/metacat/hashstore)
hashstore /path/to/store/ -chs -dp=3 -wp=2 -ap=SHA-256 -nsp="https://ns.dataone.org/service/types/v2.0#SystemMetadata"

# Store a data object
hashstore /path/to/store/ -storeobject -pid=persistent_identifier -path=/path/to/object

# Store a metadata object
hashstore /path/to/store/ -storemetadata -pid=persistent_identifier -path=/path/to/metadata/object -formatid=https://ns.dataone.org/service/types/v2.0#SystemMetadata

metadigpy -runcheck -store_path=/path/to/hashstore -check_xml=/path/to/check_xml -metadata_doc=/path/to/metadata/doc -sysmeta_doc=/path/to/sysmeta

{'identifiers': ['...', '...'], 'output': ["the_dataset_checked.csv is a valid 'utf-8' document and does not contain encoding errors."], 'status': 'SUCCESS'}
```

## License

```
Copyright 2020-2025 [Regents of the University of California]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Acknowledgements

Work on this package was supported by:

- DataONE Network
- Arctic Data Center: NSF-PLR grant #2042102 to M. B. Jones, A. Budden, M. Schildhauer, and J.
  Dozier

Additional support was provided for collaboration by the National Center for Ecological Analysis and
Synthesis, a Center funded by the University of California, Santa Barbara, and the State of
California.

[![DataONE_footer](https://user-images.githubusercontent.com/6643222/162324180-b5cf0f5f-ae7a-4ca6-87c3-9733a2590634.png)](https://dataone.org)

[![nceas_footer](https://www.nceas.ucsb.edu/sites/default/files/2020-03/NCEAS-full%20logo-4C.png)](https://www.nceas.ucsb.edu)