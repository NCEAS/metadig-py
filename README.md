# MetaDIG-py - A python client package for assisting with running MetaDIG checks

MetaDIG-Py is a library that contains helper functions and classes to assist users with writing 
python checks for suites in [metadig-checks](https://github.com/NCEAS/metadig-checks).

## Contributors

- **Author**: Jeanette Clark, Dou Mok
- **License**: [Apache 2](http://opensource.org/licenses/Apache-2.0)
- [Package source code on GitHub](https://github.com/NCEAS/metadig-py)
- [**Submit Bugs and feature requests**](https://github.com/NCEAS/metadig-py/issues)
- Contact us: support@dataone.org
- [DataONE discussions](https://github.com/DataONEorg/dataone/discussions)

## Introduction

The MetaDIG-py client package contains python modules that users can call when writing checks
for their [`metadig-checks`](https://github.com/NCEAS/metadig-checks). By importing this package, users get access to all available helper
functions and classes, such as `object_store.py` which enables users to write checks that
efficiently retrieves data objects to work with.

## How do I import the `MetaDIG-py` library to my check?

In your python code, you can import a specific module or function like such:

```py
from metadig import read_sysmeta_element
```

Currently, we have the following modules and functions available:

```py
"StoreManager", # fn
"getType", # fn
"isResolvable", # fn
"isBlank", # fn
"toUnicode", # fn
"read_sysmeta_element", # fn
"find_eml_entity", # fn
"find_entity_index", # fn
"read_csv_with_metadata", # fn
"get_valid_csv", # fn
"run_check", # fn
"checks" # Module
```

## Installation

To install MetaDIG-py, run the following commands

```sh
$ mkvirtualenv -p python3.9 metadigpy # Create a virtual environment
(metadigpy) $ poetry install # Run poetry command to install dependencies
```
- Note: If you run into an issue with installing jep, it is likely due to a backwards
compatibility issue with `setuptools`. Try downgrading to the version 58.0.0:
  ```sh
  (metadigpy) $ pip install setuptools==58.0.0
  ```

To confirm that you have installed `MetaDIG-py` successfully, run `pytest`.
```sh
(metadigpy) $ pytest
```
- Tip: You may run `pytest` with the option `-s` (ex. `pytest -s`) to see print statements. Not all pytests have print statements, but if you want to extend from what already exists, this may prove to be helpful!

### How to use the MetaDIG-py command line client

The MetaDIG-py command line client was created to help users test python checks without having to spin up the java engine `metadig-engine` and run a check through the dispatcher.

After you've installed `MetaDIG-py`, you will have access to the command `metadigpy`. Please see installation section above if you haven't installed `MetaDIG-py`. Below is what running a check looks like:

```sh
(metadigpy) $ metadigpy -runcheck -store_path=/path/to/hashstore -check_xml=/path/to/check_xml -metadata_doc=/path/to/metadata/doc -sysmeta_doc=/path/to/sysmeta
```

### How does the MetaDIG-py command line client run a check with the arguments supplied?

The `metadigclient` extracts the identifier (ex. DOI) & the authoritative member node (MN) (e.g. `urn:node:ARCTIC`) from the system metadata document supplied for the given eml metadata document. It then passes these values to the `run_check` function, which retrieves the associated data pids and their respective system metadata from the given hashstore.

The `run_check` function then parses the check xml provided, validates the check definition, executes the check, and lastly prints the final result to stdout.

As of writing this documentation, we have only set up the `metadigclient` to work with the following MN:
- urn:node:ARCTIC

To have additional nodes set up, please contact us at support@dataone.org

### How to set up and run a data check through the MetaDig-py command line client

To set-up a data check, you must have/prepare the following before you run the `metadigpy` client command (above)
1) A HashStore - this step is necessary because `run_check` will look for the data objects in a HashStore after retrieving the data pids.
2) The data objects associated with the DOI to check stored in HashStore, including the data objects' system metadata.
2) A copy of the metadata document and its respective system metadata for the DOI.
4) The check you want to run

#### What is HashStore?

HashStore is a python package developed for DataONE services to efficiently access data objects, metadata and system metadata. In order to simulate the process of retrieving data objects with a `metadig` check, we must mimic the environment in which it happens in production. So the requirement of having a HashStore means that we need to create a HashStore and then store data objects and system metadata inside of it. Please see below for an example:

```sh
# Step 0: Install hashstore via poetry to create an executable script
(metadigpy) ~/Code $ git clone https://github.com/DataONEorg/hashstore.git /Code/hashstore

(metadigpy) ~/Code/hashstore $ poetry install

# Step 1: Create a HashStore at your desired store path (ex. /var/metacat/hashstore)
(metadigpy) ~/Code/hashstore $ hashstore /path/to/store/ -chs -dp=3 -wp=2 -ap=SHA-256 -nsp="https://ns.dataone.org/service/types/v2.0#SystemMetadata"

# Store a data object
(metadigpy) ~/Code/hashstore $ hashstore /path/to/store/ -storeobject -pid=persistent_identifier -path=/path/to/object

# Store a metadata object
(metadigpy) ~/Code/hashstore $ hashstore /path/to/store/ -storemetadata -pid=persistent_identifier -path=/path/to/metadata/object -formatid=https://ns.dataone.org/service/types/v2.0#SystemMetadata
```

On your file system, HashStore looks like a folder with data objects and system metadata stored with hashes based on either a content identifier, or a combination of values that create a unique identifier. To interact with a HashStore and learn more, please see the documentation [here](https://github.com/DataONEorg/hashstore/).

#### Why data objects and its associated system metadata must be stored

During the `run_check` process, after retrieving the data pids for the provided identifier, we then retrieve their associated data objects and system metadata from the provided HashStore. If these 'files' are not found, it could cause errors with the check that you're trying to run or test. Note, every data object stored in HashStore must have an equivalent system metadata, and this system metadata describes the basic attributes of the data object.

#### Dataset Metadata + System Metadata

Every dataset not only has metadata about the dataset (which usually comes in the form of an EML metadata document) but also system metadata for the metadata. For us to run a `metadig` check at this time, we need both the metadata document and its respective system metadata. The system metadata is parsed for the identifier, which is then used to retrieve the appropriate data pids, which is then used in the check.

#### The Python Check

TODO: Discuss how a python check is created, and link to `metadig-checks` for more info.

#### Example of the Entire Process via the `MetaDIG-py` command line client

```sh
$ mkvirtualenv -p python3.9 metadigpy // Create a virtual environment
(metadigpy) ~/Code $ git clone https://github.com/NCEAS/metadig-py.git ~/Code/metadigpy

(metadigpy) ~/Code $ cd /metadigpy

(metadigpy) ~/Code/metadigpy $ poetry install // Run poetry command to install dependencies

(metadigpy) ~/Code/metadigpy $ git clone https://github.com/DataONEorg/hashstore.git ~/Code/hashstore

(metadigpy) ~/Code $ cd ../hashstore

(metadigpy) ~/Code/hashstore $ poetry install

# Step 1: Create a HashStore at your desired store path (ex. /var/metacat/hashstore)
(metadigpy) ~/Code/hashstore $ hashstore /path/to/store/ -chs -dp=3 -wp=2 -ap=SHA-256 -nsp="https://ns.dataone.org/service/types/v2.0#SystemMetadata"

# Store a data object
(metadigpy) ~/Code/hashstore $ hashstore /path/to/store/ -storeobject -pid=persistent_identifier -path=/path/to/object

# Store a metadata object
(metadigpy) ~/Code/hashstore $ hashstore /path/to/store/ -storemetadata -pid=persistent_identifier -path=/path/to/metadata/object -formatid=https://ns.dataone.org/service/types/v2.0#SystemMetadata

(metadigpy) ~/Code/hashstore $ metadigpy -runcheck -store_path=/path/to/hashstore -check_xml=/path/to/check_xml -metadata_doc=/path/to/metadata/doc -sysmeta_doc=/path/to/sysmeta

(metadigpy) ~/Code/hashstore $ {'Check Status': 0, 'Check Result': ['...RESULT...']}
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