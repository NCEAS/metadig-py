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
for their `metadig-checks`. By importing this package, users get access to all available helper
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
$ mkvirtualenv -p python3.9 metadigpy // Create a virtual environment
(metadigpy) $ poetry install // Run poetry command to install dependencies
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
- Tip: you may run `pytest` with the option `-s` (ex. `pytest -s`) to see print statements when running pytests. Not all pytests have print statements, but if you want to extend from what already exists, this may prove to be helpful!

### How to use the MetaDIG-py command line client

The MetaDIG-py command line client was created to help users test python checks without having to spin up the java engine `metadig-engine` and run a check through the dispatcher.

After you've installed `MetaDIG-py`, you will have access to the command `metadigpy`. Please see installation section above if you haven't installed `MetaDIG-py`. Below is what running a check looks like:

```sh
(metadigpy) $ metadigpy -runcheck -store_path=/path/to/hashstore -check_xml=/path/to/check_xml -metadata_doc=/path/to/metadata/doc -sysmeta_doc=/path/to/sysmeta
```

### How does the MetaDIG-py client run a check with the arguments supplied?

The `metadigclient` processes the system metadata document supplied, which should be for the given eml metadata document. It then extracts the identifier (ex. DOI) and the authoritative member node (MN) (e.g. `urn:node:ARCTIC`). Using this DOI, it queries the MN via an HTTP get request to retrieve the associated data objects/PIDs. These values are then combined into a dictionary with the hashstore configuration properties to pass onto the `run_check` function. 

The `run_check` function parses the check xml provided, validates the check definition, executes the check (which involves retrieving the data objects/pids retrieved from the supplied hashstore path), and lastly prints the final result to stdout.

As of writing this documentation, we have only setup the `metadigclient` to work with the following MN:
- urn:node:ARCTIC

To have additional nodes set-up, please contact us at support@dataone.org

### How to set-up and run a data check

To set-up a data check, you must have/prepare the following before you run the respective `metadigpy` client command (above)
1) A HashStore - this step is necessary because `run_check` will look for the data objects in a HashStore after retrieving the data pids.
2) The data objects associated with the DOI to check stored in HashStore, including the data objects' system metadata.
2) A copy of the metadata document and its respective system metadata for the DOI.
4) The check you want to run

#### HashStore

HashStore is a python package developed for DataONE services to efficiently access data objects, metadata and system metadata. In order to simulate the process of retrieving data objects with a `metadig` check, we must mimic the environment in which it happens in production. So the requirement of having a HashStore means that we need to create a HashStore and then store data objects and system metadata inside of it. Please see below for an example:

```sh
# Step 0: Install hashstore via poetry to create an executable script
(metadigpy) ~/Code $ git clone https://github.com/DataONEorg/hashstore.git /Code/hashstore

(metadigpy) ~/Code/hashstore $ poetry install

# Step 1: Create a HashStore at your desired store path (ex. /var/metacat/hashstore)
(metadigpy) ~/Code/hashstore $ /path/to/store/ -chs -dp=3 -wp=2 -ap=SHA-256 -nsp="https://ns.dataone.org/service/types/v2.0#SystemMetadata"

# Store a data object
(metadigpy) ~/Code/hashstore $ /path/to/store/ -storeobject -pid=persistent_identifier -path=/path/to/object

# Store a metadata object
(metadigpy) ~/Code/hashstore $ /path/to/store/ -storemetadata -pid=persistent_identifier -path=/path/to/metadata/object -formatid=https://ns.dataone.org/service/types/v2.0#SystemMetadata
```

Learn more about HashStore [here](https://github.com/DataONEorg/hashstore/). 

#### Data objects, system metadata and metadata.

Every data object stored in HashStore will have an equivalent system metadata that describes the basic attributes of the data object. Every dataset also has metadata about the dataset, which usually comes in the form of an EML metadata document. These "files" must all exist in HashStore for a given identifier in order for a check to retrieve what it needs to execute the check code. 

#### Metadata + System Metadata

TODO

#### The Python Check

TODO

## License

```
Copyright [2022] [Regents of the University of California]

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